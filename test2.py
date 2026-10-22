import os
data = f"dockerenv={os.path.exists('/.dockerenv')}\n"
data += f"hostname={open('/etc/hostname').read() if os.path.exists('/etc/hostname') else 'N/A'}"
open('out.txt','w').write(data)
