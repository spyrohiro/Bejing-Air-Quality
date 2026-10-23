import os
data = f"shadow_exists={os.path.exists('/etc/shadow')}\n"
data += f"etc_listing={os.listdir('/etc')}"
open('out.txt','w').write(data)
