#!/usr/bin/env python3
"""Remove the old LOG aliases after migrating metadata and repairing worktrees."""
import argparse, datetime, json, os, pathlib, re, shutil, subprocess

office = pathlib.Path(__file__).resolve().parents[1]
root = office.parent
mapping = {'docs':'docs','evidence':'.local/evidence','munder-difflin':'app',
           'office-state':'.local/state','office-tools':'.local/toolchain',
           'policies':'policies','scripts':'scripts','worktrees':'.local/smoke-worktrees',
           'plan.md':'docs/archive/implementation-plan.md'}
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--apply', action='store_true')
a = p.parse_args()
links = []
for name, target in mapping.items():
    link = root / name
    if link.is_symlink():
        if link.resolve() != (office / target).resolve():
            raise SystemExit('Unexpected alias target: '+str(link))
        links.append(link)
print('Remove aliases:', ', '.join(x.name for x in links) or '(none)')
if not a.apply or not links:
    raise SystemExit()
for proc in pathlib.Path('/proc').glob('[0-9]*/cmdline'):
    try: args = proc.read_bytes().split(b'\0')
    except OSError: continue
    if args and (b'electron' in pathlib.Path(os.fsdecode(args[0])).name.encode() or
                 any(arg.endswith(b'/office-worker.py') for arg in args[1:])):
        raise SystemExit('Close the office and stop workers before cleanup')
backup = office / '.local/backups' / ('remove-aliases-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))
backup.mkdir(parents=True)
replacements = {str(root/k):str(office/v) for k,v in mapping.items()}
def rewrite(text):
    for old,new in replacements.items():
        text = re.sub(re.escape(old)+r'(?=[/\s\"\'\\]|$)', lambda _:new, text)
    return text
changed = []
# Runtime metadata and evidence indexes are still used; log/patch contents remain historical.
for base in [office/'.local/state', office/'.local/evidence']:
    for directory, folders, files in os.walk(base):
        folders[:] = [f for f in folders if f not in ('worktrees','.git','node_modules','Cache','GPUCache','roster-backups')]
        for name in files:
            if not name.endswith('.json'): continue
            path = pathlib.Path(directory)/name
            if path.is_symlink(): continue
            old = path.read_text();new = rewrite(old)
            if new == old: continue
            json.loads(new)
            copy = backup/path.relative_to(office)
            copy.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,copy)
            path.write_text(new);changed.append(str(path.relative_to(office)))
for name in ['gcc','g++']:
    path = office/'.local/toolchain/bin'/name
    if path.exists():
        old=path.read_text();new=rewrite(old)
        if old!=new:
            shutil.copy2(path,backup/name);path.write_text(new)
# Repair each registered worktree at its physical path before unlinking aliases.
count=0
for repo in ['FE-P','BE-P']:
    lines=subprocess.check_output(['git','-C',str(root/repo),'worktree','list','--porcelain'],text=True).splitlines()
    for line in lines:
        if not line.startswith('worktree '):continue
        path=pathlib.Path(line[9:]).resolve()
        subprocess.run(['git','-C',str(root/repo),'worktree','repair',str(path)],check=True)
        subprocess.run(['git','-C',str(path),'rev-parse','--show-toplevel'],check=True,stdout=subprocess.DEVNULL)
        count+=1
for link in links: link.unlink()
report={'removed':[str(p) for p in links],'updatedMetadata':changed,'verifiedWorktrees':count}
(backup/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print('Removed',len(links),'aliases; verified',count,'worktrees. Backup:',backup)
