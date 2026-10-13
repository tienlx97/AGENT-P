#!/usr/bin/env python3
"""Bounded Linux worker, launched inside Munder's existing PTY. No orchestrator."""
import argparse, json, re, os, pathlib, shutil, subprocess, tempfile, time, threading, sys, contextlib, fcntl

BASE = pathlib.Path(__file__).resolve().parent.parent
RUNTIMES = {'claude': pathlib.Path.home()/'.local/bin/claude', 'codex': pathlib.Path.home()/'.local/bin/codex'}

def sandbox(worktree, runtime, scratch, argv, read_only=False):
    worktree = pathlib.Path(worktree).resolve()
    binary = RUNTIMES[runtime].resolve(strict=True)
    args = ['bwrap', '--die-with-parent', '--new-session', '--unshare-pid', '--unshare-ipc', '--unshare-uts', '--unshare-user', '--clearenv']
    for p in ['/usr', '/bin', '/lib', '/lib64']:
        if pathlib.Path(p).exists(): args += ['--ro-bind', p, p]
    args += ['--proc', '/proc', '--dev', '/dev', '--tmpfs', '/tmp']
    for p in ['/etc/ssl/certs','/etc/ssl/openssl.cnf', '/etc/resolv.conf', '/etc/hosts', '/etc/nsswitch.conf']:
        if pathlib.Path(p).exists(): args += ['--ro-bind', p, p]
    args += ['--ro-bind', str(binary.parent), str(binary.parent)]
    node_root = pathlib.Path(shutil.which('node')).resolve().parent.parent
    args += ['--ro-bind', str(node_root), str(node_root)]
    pnpm=shutil.which('pnpm')
    if pnpm:
        pnpm_root=pathlib.Path(pnpm).resolve().parent.parent
        if not str(pnpm_root).startswith(str(node_root)): args += ['--ro-bind',str(pnpm_root),str(pnpm_root)]
    dotnet = pathlib.Path.home()/'.dotnet'
    if dotnet.exists(): args += ['--ro-bind', str(dotnet), str(dotnet)]
    args += ['--bind', str(scratch), '/home/worker', '--ro-bind' if read_only else '--bind', str(worktree), str(worktree)]
    packages=pathlib.Path.home()/'.nuget/packages'
    if packages.exists(): args += ['--ro-bind',str(packages),'/home/worker/.nuget/packages']
    git_file = worktree/'.git'
    if git_file.is_file():
        git_dir = pathlib.Path(git_file.read_text().strip().removeprefix('gitdir: ')).resolve()
        common = (git_dir/(git_dir/'commondir').read_text().strip()).resolve()
        args += ['--ro-bind', str(common), str(common)]
    # Follow dependency links without exposing the source checkout.
    modules = worktree/'node_modules'
    if modules.is_symlink():
        actual = modules.resolve()
        args += ['--ro-bind', str(actual), str(actual)]
    # Never expose local application secrets to workers, including worktree copies.
    for directory, folders, files in os.walk(worktree):
        folders[:] = [x for x in folders if x not in ('node_modules', '.git', '.next', 'bin', 'obj')]
        for name in files:
            if name.startswith('.env') and not name.endswith(('example', 'sample')):
                args += ['--ro-bind', '/dev/null', str(pathlib.Path(directory)/name)]
    for name in ['.ai-login.local.md']:
        if (worktree/name).exists(): args += ['--ro-bind', '/dev/null', str(worktree/name)]
    args += ['--setenv', 'HOME', '/home/worker', '--setenv', 'PATH', f'{node_root}/bin:{dotnet}:{dotnet}/tools:/usr/bin:/bin', '--setenv', 'TERM', 'xterm-256color', '--setenv', 'LANG', 'C.UTF-8', '--setenv', 'DO_NOT_TRACK', '1', '--setenv', 'pnpm_config_verify_deps_before_run', 'false', '--setenv', 'DOTNET_ROOT', str(dotnet), '--chdir', str(worktree)]
    return args + ['--', str(binary)] + argv

def execute(worktree, runtime, prompt, seconds=180, token_cap=None, max_steps=80, read_only=False, model=None, effort=None):
    if model is not None and (not isinstance(model,str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._:/-]{0,119}',model)): raise ValueError('Invalid model id')
    if effort is not None and effort not in (['low','medium','high','xhigh','max'] if runtime=='claude' else ['low','medium','high','xhigh']): raise ValueError('Invalid effort for selected runtime')
    summary = {'requestedEffort':effort,'requestedModel':model,'runtime':runtime,'model':'unknown','tokens':'unknown','cost':'unknown','status':'running','completionObserved':False}
    started=time.monotonic()
    # Auth is copied into a private, disposable home. No global hooks, MCP servers,
    # GitHub tokens, SSH keys or user provider configuration are inherited.
    with tempfile.TemporaryDirectory(prefix='munder-worker-') as temp:
        scratch = pathlib.Path(temp)
        config_dir = scratch/('.claude' if runtime == 'claude' else '.codex')
        config_dir.mkdir(mode=0o700)
        auth_name = '.credentials.json' if runtime == 'claude' else 'auth.json'
        source = pathlib.Path.home()/config_dir.name/auth_name
        if not source.exists(): raise RuntimeError(f'{runtime} authentication unavailable')
        original_auth=source.read_bytes()
        shutil.copyfile(source, config_dir/auth_name)
        (config_dir/auth_name).chmod(0o600)
        def preserve_refresh():
            # OAuth refresh tokens can rotate. Preserve a CLI-written refresh only
            # if the host profile is still the revision copied for this attempt.
            # Never print credentials or overwrite a concurrent login.
            refreshed=(config_dir/auth_name).read_bytes()
            if refreshed!=original_auth and source.read_bytes()==original_auth:
                json.loads(refreshed)
                descriptor,name=tempfile.mkstemp(prefix='.munder-auth-',dir=source.parent)
                try:
                    with os.fdopen(descriptor,'wb') as updated: updated.write(refreshed)
                    os.replace(name,source)
                finally:
                    if os.path.exists(name): os.unlink(name)
        if runtime == 'claude':
            argv = ['-p', prompt, '--output-format', 'json', '--permission-mode', 'bypassPermissions', '--strict-mcp-config', '--mcp-config', '{"mcpServers":{}}', '--setting-sources', '', '--tools', 'Read,Edit,Write,Bash,Glob,Grep']
        else:
            argv = ['exec', '--json', '--disable', 'multi_agent', '--disable', 'multi_agent_v2', '--dangerously-bypass-approvals-and-sandbox', prompt]
        if effort: argv += ['--effort',effort] if runtime=='claude' else ['-c',f'model_reasoning_effort={json.dumps(effort)}']
        if model: argv += ['--model',model]
        child = subprocess.Popen(sandbox(worktree, runtime, scratch, argv,read_only), stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, start_new_session=True)
        steps=0
        output_bytes=0
        def collect():
            nonlocal steps, output_bytes
            def halt(reason):
                import signal
                summary.update(status='blocked',reason=reason)
                try: os.killpg(child.pid,signal.SIGTERM)
                except ProcessLookupError: pass
            for line in child.stdout:
                output_bytes+=len(line.encode('utf-8'))
                if output_bytes>8*1024*1024:
                    halt('output limit exceeded')
                    break
                print(line, end='', flush=True)
                try: event=json.loads(line)
                except (ValueError, TypeError): continue
                if not isinstance(event,dict): continue
                def token_value(value): return value if type(value) is int and value>=0 else 'unknown'
                if event.get('type')=='item.started':
                    steps+=1
                    if steps>max_steps: halt('iteration limit exceeded')
                if event.get('type')=='thread.started':summary['sessionId']=event.get('thread_id','unknown')
                if event.get('type') == 'result':
                    summary['completionObserved']=True
                    summary['sessionId']=event.get('session_id','unknown')
                    if event.get('is_error'):
                        summary.update(status='blocked', reason=event.get('api_error',event.get('result','provider error')))
                        halt(str(summary['reason']))
                    models=event.get('modelUsage',{})
                    if isinstance(models,dict) and models and all(isinstance(k,str) for k in models): summary['model']=','.join(models)
                    usage=event.get('usage',{})
                    if not isinstance(usage,dict):usage={}
                    fields=[token_value(usage.get(k)) for k in ('input_tokens','output_tokens','cache_creation_input_tokens','cache_read_input_tokens')]
                    summary.update(inputTokens=fields[0],freshInputTokens=fields[0],outputTokens=fields[1],cachedInputTokens=fields[3],cacheWriteTokens=fields[2])
                    summary['tokens']=sum(fields) if all(type(v) is int for v in fields) else 'unknown'
                    # Subscription spend is not an invoice; preserve provider estimate separately.
                    summary['providerCostEstimate']=event.get('total_cost_usd','unknown')
                elif event.get('type') == 'turn.completed':
                    summary['completionObserved']=True
                    usage=event.get('usage',{})
                    if not isinstance(usage,dict):usage={}
                    input_tokens=token_value(usage.get('input_tokens'));output_tokens=token_value(usage.get('output_tokens'))
                    cached=token_value(usage.get('cached_input_tokens'))
                    for key,value in [('inputTokens',input_tokens),('outputTokens',output_tokens),('cachedInputTokens',cached)]:
                        previous=summary.get(key,0)
                        summary[key]=previous+value if type(previous) is int and type(value) is int else 'unknown'
                    inp,out,cache=summary['inputTokens'],summary['outputTokens'],summary['cachedInputTokens']
                    summary['tokens']=inp+out if type(inp) is int and type(out) is int else 'unknown'
                    summary['freshInputTokens']=inp-cache if type(inp) is int and type(cache) is int and cache<=inp else 'unknown'
                elif event.get('type') in ('turn.failed','error'):
                    error=event.get('error','provider error')
                    summary.update(status='blocked',reason=event.get('message',error.get('message','provider error') if isinstance(error,dict) else error))
                    halt(str(summary['reason']))
                if token_cap and isinstance(summary['tokens'],int) and summary['tokens']>token_cap:
                    halt('observed token budget exceeded')
        reader=threading.Thread(target=collect,daemon=True); reader.start()
        try:
            code=child.wait(timeout=seconds)
            reader.join(timeout=5)
            child.stdout.close()
            if summary['status']=='running':
                summary['status']='done' if code==0 and summary['completionObserved'] else 'blocked'
                if not summary['completionObserved']:summary['reason']='missing or malformed provider completion'
            summary['exitCode']=code
            summary['seconds']=round(time.monotonic()-started,3)
            print('OFFICE_RESULT '+json.dumps(summary),flush=True)
            preserve_refresh()
            return code if summary['status']=='done' else (code or 1)
        except subprocess.TimeoutExpired:
            import signal
            os.killpg(child.pid, signal.SIGTERM)
            try: child.wait(timeout=3)
            except subprocess.TimeoutExpired:
                os.killpg(child.pid, signal.SIGKILL); child.wait()
            reader.join(timeout=5)
            child.stdout.close()
            summary.update(status='blocked',reason='wall-clock limit exceeded',seconds=round(time.monotonic()-started,3))
            print('OFFICE_RESULT '+json.dumps(summary), flush=True)
            preserve_refresh()
            return 124

if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--worktree', required=True)
    p.add_argument('--runtime', choices=RUNTIMES, required=True)
    p.add_argument('--prompt', required=True)
    p.add_argument('--model')
    p.add_argument('--effort')
    p.add_argument('--seconds', type=int, default=180)
    p.add_argument('--read-only', action='store_true')
    p.add_argument('--token-cap', type=int)
    p.add_argument('--max-steps', type=int, default=80)
    p.add_argument('--log', help='Trusted host path for durable CLI output; not exposed to worker')
    a=p.parse_args()
    if not 1 <= a.seconds <= 3600: p.error('seconds must be 1..3600')
    if not 1 <= a.max_steps <= 200: p.error('max-steps must be 1..200')
    lock_dir=pathlib.Path.home()/'.cache/munder-office'
    lock_dir.mkdir(parents=True,exist_ok=True,mode=0o700)
    lock=open(lock_dir/f'auth-{a.runtime}.lock','a')
    os.chmod(lock.name,0o600)
    deadline=time.monotonic()+a.seconds
    while True:
        try:
            if a.runtime=='claude': fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
            break
        except BlockingIOError:
            if time.monotonic()>=deadline:
                print('OFFICE_RESULT '+json.dumps({'runtime':a.runtime,'status':'blocked','reason':'authentication profile busy; wall-clock limit exceeded','tokens':'unknown','cost':'unknown'}),flush=True)
                raise SystemExit(124)
            time.sleep(0.1)
    a.seconds=max(1,int(deadline-time.monotonic()))
    if a.log:
        descriptor=os.open(a.log,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
        with os.fdopen(descriptor,'w') as log:
            class Tee:
                def write(self,data): log.write(data);return sys.__stdout__.write(data)
                def flush(self): log.flush();sys.__stdout__.flush()
            with contextlib.redirect_stdout(Tee()):
                code=execute(a.worktree,a.runtime,a.prompt,a.seconds,a.token_cap,a.max_steps,a.read_only,a.model,a.effort)
        raise SystemExit(code)
    raise SystemExit(execute(a.worktree, a.runtime, a.prompt, a.seconds,a.token_cap,a.max_steps,a.read_only,a.model,a.effort))
