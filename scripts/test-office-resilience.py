#!/usr/bin/env python3
"""Real OS/process tests with synthetic CLI protocol fixtures; zero provider calls."""
import contextlib, importlib.util, io, json, pathlib, tempfile, time, unittest
from unittest.mock import patch
from worker_test_fixture import workspace
_FIXTURE_HOME,ROOT=workspace()
spec=importlib.util.spec_from_file_location('worker',pathlib.Path(__file__).with_name('office-worker.py'))
worker=importlib.util.module_from_spec(spec);spec.loader.exec_module(worker)
FIXTURE='''#!/usr/bin/python3
import json,os,pathlib,sys,time
mode=next((x for x in sys.argv if x in ('good','quota','malformed','runaway','slow','crash','rotate','large','missing-usage','bad-usage','retrying-quota','two-turns')),'good')
if mode=='two-turns':print(json.dumps({'type':'turn.completed','usage':{'input_tokens':10,'output_tokens':2,'cached_input_tokens':8}}))
if mode=='slow':time.sleep(20)
if mode=='large':print('x'*(9*1024*1024),flush=True);sys.exit(0)
if mode=='crash':sys.exit(7)
if mode=='missing-usage':print(json.dumps({'type':'turn.completed'}));sys.exit(0)
if mode=='bad-usage':print(json.dumps({'type':'turn.completed','usage':{'input_tokens':'invalid','output_tokens':None}}));sys.exit(0)
if mode=='malformed':print('not a provider event');sys.exit(0)
if mode=='runaway':
 for n in range(30):print(json.dumps({'type':'item.started'}),flush=True);time.sleep(.05)
if mode=='retrying-quota':
 print(json.dumps({'type':'turn.failed','error':{'message':'fixture quota reached'}}),flush=True);time.sleep(20)
if mode=='quota':print(json.dumps({'type':'turn.failed','error':{'message':'fixture quota reached'}}));sys.exit(0)
if mode=='rotate':
 (pathlib.Path.home()/'.codex/auth.json').write_text(json.dumps({'fixture':True,'revision':2}))
print(json.dumps({'type':'thread.started','thread_id':'fixture-session'}))
print(json.dumps({'type':'turn.completed','usage':{'input_tokens':11,'output_tokens':1,'cached_input_tokens':0}}))
'''
class ResilienceTests(unittest.TestCase):
 def run_fixture(self,mode,seconds=3,token_cap=None,steps=5,model=None,runtime='codex',effort=None):
  with tempfile.TemporaryDirectory(prefix='office-fixture-') as directory:
   home=pathlib.Path(directory);config=home/('.codex' if runtime=='codex' else '.claude');config.mkdir();auth=config/('auth.json' if runtime=='codex' else '.credentials.json');auth.write_text('{"fixture":true,"revision":1}')
   cli=home/'cli';cli.write_text(FIXTURE);cli.chmod(0o700)
   output=io.StringIO();started=time.monotonic()
   with patch.object(pathlib.Path,'home',return_value=home),patch.dict(worker.RUNTIMES,{runtime:cli}),patch.object(worker,'sandbox',wraps=worker.sandbox) as launch,contextlib.redirect_stdout(output):
    code=worker.execute(ROOT/'worktrees/fe-smoke',runtime,mode,seconds,token_cap,steps,model=model,effort=effort)
    argv=launch.call_args.args[3]
    if model:self.assertEqual(argv[-2:],['--model',model])
    else:self.assertNotIn('--model',argv)
    if effort:
     if runtime=='claude':self.assertEqual(argv[argv.index('--effort')+1],effort)
     else:self.assertIn('model_reasoning_effort='+json.dumps(effort),argv)
    else:
     self.assertNotIn('--effort',argv);self.assertFalse(any(x.startswith('model_reasoning_effort=') for x in argv))
   summaries=[json.loads(line[14:]) for line in output.getvalue().splitlines() if line.startswith('OFFICE_RESULT ')]
   return code,summaries[-1],time.monotonic()-started,json.loads(auth.read_text())
 def test_explicit_model_forwarded_to_each_cli(self):
  for runtime in ['codex','claude']:
   with self.subTest(runtime=runtime):
    code,result,_,_=self.run_fixture('good',model='fixture-model-v1',runtime=runtime);self.assertEqual(code,0);self.assertEqual(result['requestedModel'],'fixture-model-v1');self.assertEqual(result['model'],'unknown')
 def test_invalid_model_refused(self):
  with self.assertRaises(ValueError):worker.execute(ROOT/'worktrees/fe-smoke','codex','good',model='bad;command')
 def test_effort_forwarded_for_each_runtime(self):
  for runtime in ['codex','claude']:
   for effort in (['low','medium','high','xhigh','max'] if runtime=='claude' else ['low','medium','high','xhigh']):
    with self.subTest(runtime=runtime,effort=effort):
     code,result,_,_=self.run_fixture('good',model='fixture-model',runtime=runtime,effort=effort);self.assertEqual(code,0);self.assertEqual(result['requestedEffort'],effort)
 def test_invalid_effort_refused(self):
  for runtime,effort in [('codex','max'),('claude','bad;command')]:
   with self.assertRaises(ValueError):worker.execute(ROOT/'worktrees/fe-smoke',runtime,'good',effort=effort)
 def test_good_fixture_completion(self):
  code,result,_,_=self.run_fixture('good');self.assertEqual(code,0);self.assertEqual(result['status'],'done');self.assertEqual(result['tokens'],12);self.assertEqual(result['cost'],'unknown');self.assertEqual(result['sessionId'],'fixture-session')
 def test_multiple_turns_accumulate_usage(self):
  code,result,_,_=self.run_fixture('two-turns');self.assertEqual(code,0);self.assertEqual(result['tokens'],24);self.assertEqual(result['freshInputTokens'],13);self.assertEqual(result['cachedInputTokens'],8)
 def test_quota_never_becomes_success_on_exit_zero(self):
  code,result,_,_=self.run_fixture('quota');self.assertNotEqual(code,0);self.assertEqual(result['status'],'blocked');self.assertEqual(result['reason'],'fixture quota reached');self.assertEqual(result['tokens'],'unknown')
 def test_malformed_completion_fails_closed(self):
  code,result,_,_=self.run_fixture('malformed');self.assertEqual(code,1);self.assertEqual(result['status'],'blocked');self.assertEqual(result['tokens'],'unknown')
 def test_crash_preserves_worktree(self):
  code,result,_,_=self.run_fixture('crash');self.assertEqual(code,7);self.assertEqual(result['status'],'blocked');self.assertTrue((ROOT/'worktrees/fe-smoke/.git').exists())
 def test_step_loop_stops(self):
  code,result,elapsed,_=self.run_fixture('runaway',steps=2);self.assertNotEqual(code,0);self.assertEqual(result['reason'],'iteration limit exceeded');self.assertLess(elapsed,3)
 def test_timeout_stops(self):
  code,result,elapsed,_=self.run_fixture('slow',seconds=1);self.assertEqual(code,124);self.assertEqual(result['reason'],'wall-clock limit exceeded');self.assertLess(elapsed,5)
 def test_observed_token_cap_stops(self):
  code,result,_,_=self.run_fixture('good',token_cap=10);self.assertNotEqual(code,0);self.assertEqual(result['reason'],'observed token budget exceeded')
 def test_output_storm_is_bounded(self):
  code,result,_,_=self.run_fixture('large');self.assertNotEqual(code,0);self.assertEqual(result['reason'],'output limit exceeded')
 def test_missing_usage_stays_unknown(self):
  code,result,_,_=self.run_fixture('missing-usage');self.assertEqual(code,0);self.assertEqual(result['tokens'],'unknown');self.assertEqual(result['cost'],'unknown')
 def test_invalid_usage_stays_unknown(self):
  code,result,_,_=self.run_fixture('bad-usage');self.assertEqual(code,0);self.assertEqual(result['tokens'],'unknown');self.assertEqual(result['inputTokens'],'unknown')
 def test_provider_retry_is_stopped_after_error(self):
  code,result,elapsed,_=self.run_fixture('retrying-quota');self.assertNotEqual(code,0);self.assertEqual(result['reason'],'fixture quota reached');self.assertLess(elapsed,2)
 def test_credential_refresh_is_preserved_without_real_credentials(self):
  code,result,_,auth=self.run_fixture('rotate');self.assertEqual(code,0);self.assertEqual(auth['revision'],2)
if __name__=='__main__':unittest.main(verbosity=2)
