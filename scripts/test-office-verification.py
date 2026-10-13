#!/usr/bin/env python3
"""Exercise the real verification sandbox without a provider session."""
import os,pathlib,subprocess,tempfile,unittest
class GateIsolation(unittest.TestCase):
 def test_repository_gate_without_credentials(self):
  with tempfile.TemporaryDirectory(prefix='office-gate-test-') as temp:
   repo=pathlib.Path(temp)/'repo';worktree=pathlib.Path(temp)/'worktree'
   subprocess.run(['git','init','-q',str(repo)],check=True)
   subprocess.run(['git','-C',str(repo),'-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','--allow-empty','-qm','fixture'],check=True)
   subprocess.run(['git','-C',str(repo),'worktree','add','--detach',str(worktree)],check=True,capture_output=True)
   (worktree/'harness').mkdir()
   (worktree/'harness/verify.sh').write_text('set -eu\ntest -z "${OFFICE_TEST_SECRET:-}"\ntest ! -e "$HOME/.codex/auth.json"\ntest ! -e "$HOME/.claude/.credentials.json"\nprintf "verified without credentials\\n"\n')
   helper=pathlib.Path(__file__).with_name('verify-worktree.py')
   result=subprocess.run(['python3',str(helper),str(worktree)],env={**os.environ,'OFFICE_TEST_SECRET':'fixture'},capture_output=True,text=True,timeout=20)
   self.assertEqual(result.returncode,0,result.stderr);self.assertIn('verified without credentials',result.stdout)
   (worktree/'harness/verify.sh').write_text('exit 7\n')
   failed=subprocess.run(['python3',str(helper),str(worktree)],capture_output=True,text=True,timeout=20)
   self.assertEqual(failed.returncode,7)
if __name__=='__main__':unittest.main(verbosity=2)
