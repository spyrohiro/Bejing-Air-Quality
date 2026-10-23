import base64
with open('/dump.rdb', 'rb') as f:
    content = f.read()
open('out.txt', 'w').write(base64.b64encode(content).decode())
