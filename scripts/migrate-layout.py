#!/usr/bin/env python3
"""Idempotent layout migration. Legacy symlinks preserve historical paths."""
import argparse,json,pathlib,shutil,subprocess,datetime
root=pathlib.Path(__file__).resolve().parents[2]
target=root/'agent-office'
mapping={'munder-difflin':'app','office-state':'.local/state','office-tools':'.local/toolchain','scripts':'scripts','policies':'policies','docs':'docs','evidence':'.local/evidence','worktrees':'.local/smoke-worktrees'}
p=argparse.ArgumentParser();p.add_argument('--apply',action='store_true');a=p.parse_args()
for old,new in mapping.items(): print(f'{old} -> agent-office/{new} (legacy symlink retained)')
if not a.apply: raise SystemExit()
processes=subprocess.check_output(['ps','-eo','pid,args'],text=True).splitlines()
if any(('out/main/index.js' in s and 'electron' in s or 'python3 ' in s and '/office-worker.py ' in s) for s in processes): raise SystemExit('Close the office and stop workers before migration')
backup=target/'.local/backups'/datetime.datetime.now().strftime('%Y%m%d-%H%M%S');backup.mkdir(parents=True)
config=root/'office-state/config/Electron/config.json'
if config.exists(): shutil.copy2(config,backup/'config.json')
for old,new in mapping.items():
 src=root/old;dst=target/new
 if src.is_symlink(): continue
 if not src.exists(): continue
 dst.parent.mkdir(parents=True,exist_ok=True)
 if dst.exists():
  for child in src.iterdir():
   if (dst/child.name).exists(): raise SystemExit(f'Collision: {dst/child.name}')
   shutil.move(str(child),dst/child.name)
  src.rmdir()
 else: shutil.move(str(src),dst)
 src.symlink_to(pathlib.Path('agent-office')/new,target_is_directory=True)
config=target/'.local/state/config/Electron/config.json'
if config.exists():
 c=json.loads(config.read_text());c['harnessHome']=str(target/'.local/state/home');c['codingOffice']['worker']=str(target/'scripts/office-worker.py')
 config.write_text(json.dumps(c,indent=2)+'\n')
for repo in ['FE-P','BE-P']: subprocess.run(['git','-C',str(root/repo),'worktree','repair'],check=True)
print('Migrated; old paths remain valid through compatibility symlinks. Backup:',backup)
