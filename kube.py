import os

with open('out.txt', 'w') as f:
    f.write(f"uid={os.getuid()} gid={os.getgid()}\n")
    f.write(str(os.path.exists('/var/run/secrets/kubernetes.io/serviceaccount/token')))
