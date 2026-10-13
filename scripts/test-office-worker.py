#!/usr/bin/env python3
import importlib.util, pathlib, tempfile, subprocess, unittest
ROOT=pathlib.Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('worker', ROOT/'scripts/office-worker.py')
worker=importlib.util.module_from_spec(spec);spec.loader.exec_module(worker)

class IsolationTests(unittest.TestCase):
    def test_opposite_repo_and_host_secrets_are_absent(self):
        with tempfile.TemporaryDirectory() as scratch:
            args=worker.sandbox(ROOT/'worktrees/fe-smoke','codex',pathlib.Path(scratch),[])
            result=subprocess.run(args[:-1]+['/bin/sh','-c',f'test ! -e {ROOT}/BE-P && test ! -e /home/capybara/.config/gh/hosts.yml && test ! -e /home/capybara/.ssh'],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
    def test_git_common_directory_is_read_only(self):
        with tempfile.TemporaryDirectory() as scratch:
            args=worker.sandbox(ROOT/'worktrees/fe-smoke','codex',pathlib.Path(scratch),[])
            result=subprocess.run(args[:-1]+['/bin/sh','-c',f'touch {ROOT}/FE-P/.git/office-forbidden'],capture_output=True,text=True)
            self.assertNotEqual(result.returncode,0)
            self.assertIn('Read-only',result.stderr)
            self.assertFalse((ROOT/'FE-P/.git/office-forbidden').exists())
    def test_worker_cannot_access_opposite_checkout(self):
        with tempfile.TemporaryDirectory() as scratch:
            args=worker.sandbox(ROOT/'worktrees/be-smoke','claude',pathlib.Path(scratch),[])
            result=subprocess.run(args[:-1]+['/bin/sh','-c',f'test ! -e {ROOT}/FE-P && test -f global.json && test "$HOME" = /home/worker'],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
    def test_host_sensitive_environment_is_not_inherited(self):
        with tempfile.TemporaryDirectory() as scratch:
            args=worker.sandbox(ROOT/'worktrees/fe-smoke','codex',pathlib.Path(scratch),[])
            result=subprocess.run(args[:-1]+['/usr/bin/env'],capture_output=True,text=True,env={'TEST_PRIVATE_TOKEN':'do-not-inherit','PATH':'/usr/bin:/bin'})
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertNotIn('TEST_PRIVATE_TOKEN',result.stdout)
    def test_reviewer_worktree_is_read_only(self):
        with tempfile.TemporaryDirectory() as scratch:
            args=worker.sandbox(ROOT/'worktrees/fe-smoke','codex',pathlib.Path(scratch),[],True)
            result=subprocess.run(args[:-1]+['/bin/sh','-c','touch office-review-forbidden'],capture_output=True,text=True)
            self.assertNotEqual(result.returncode,0)
            self.assertFalse((ROOT/'worktrees/fe-smoke/office-review-forbidden').exists())
    def test_secrets_in_worktree_are_masked(self):
        tree=ROOT/'worktrees/fe-smoke';secret=tree/'.env.office-isolation-test'
        self.assertFalse(secret.exists());secret.write_text('TEST_SECRET=sentinel')
        try:
            with tempfile.TemporaryDirectory() as scratch:
                args=worker.sandbox(tree,'codex',pathlib.Path(scratch),[])
                result=subprocess.run(args[:-1]+['/bin/cat',str(secret)],capture_output=True,text=True)
                self.assertEqual(result.stdout,'');self.assertNotIn('sentinel',result.stdout+result.stderr)
                self.assertEqual(secret.read_text(),'TEST_SECRET=sentinel')
        finally: secret.unlink()

if __name__=='__main__':unittest.main(verbosity=2)
