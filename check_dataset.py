import subprocess
import sys
import json
import re

proc = subprocess.Popen(
    ['git', 'annex', 'whereis', '.','--json'],
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE,
    universal_newlines = True
)

files = [json.loads(line) for line in iter(proc.stdout.readline, '')]
errors = [
    file['file']
    for file in files
    if all([re.search(r' \[scratch1\]$', remote['description']) == None for remote in file['whereis']])
]

if len(errors):
    print('The following files are versionned but not present on scratch1:')
    print("\n".join(errors))
    sys.exit(1)