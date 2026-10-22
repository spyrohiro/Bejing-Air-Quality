import subprocess
with open('out.txt', 'w') as f:
    f.write(subprocess.check_output(['id']).decode())
