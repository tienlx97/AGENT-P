"""Disposable Git worktrees for worker tests; no product checkout or login required."""
import pathlib, subprocess, tempfile

def workspace():
    temp = tempfile.TemporaryDirectory(prefix='office-worker-tests-')
    root = pathlib.Path(temp.name)
    for name in ('FE', 'BE'):
        repo = root / (name + '-P')
        subprocess.run(['git', 'init', '-q', str(repo)], check=True)
        (repo / 'global.json').write_text('{}')
        subprocess.run(['git', '-C', str(repo), 'add', 'global.json'], check=True)
        subprocess.run(['git', '-C', str(repo), '-c', 'user.name=Fixture',
                        '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'fixture'], check=True)
        tree = root / 'worktrees' / (name.lower() + '-smoke')
        tree.parent.mkdir(exist_ok=True)
        subprocess.run(['git', '-C', str(repo), 'worktree', 'add', '--detach', str(tree)],
                       check=True, capture_output=True)
    return temp, root
