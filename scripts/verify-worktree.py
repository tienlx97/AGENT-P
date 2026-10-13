#!/usr/bin/env python3
"""Run repository gate inside worker isolation, without credentials or a model."""
import importlib.util,pathlib,subprocess,sys,tempfile
spec=importlib.util.spec_from_file_location('worker',pathlib.Path(__file__).with_name('office-worker.py'))
w=importlib.util.module_from_spec(spec);spec.loader.exec_module(w)
root=pathlib.Path(sys.argv[1]).resolve()
if not (root/'harness/verify.sh').is_file(): raise SystemExit('Repository harness/verify.sh missing')
w.RUNTIMES['gate']=pathlib.Path('/bin/bash')
with tempfile.TemporaryDirectory(prefix='office-gate-') as temp:
 command=w.sandbox(root,'gate',pathlib.Path(temp),['harness/verify.sh'])
 raise SystemExit(subprocess.call(command))
