import os
try:
    data = f"uid={os.getuid()} gid={os.getgid()}\n" + open('/proc/self/cgroup').read()
except Exception as e:
    data = str(e)
open('out.txt','w').write(data)
