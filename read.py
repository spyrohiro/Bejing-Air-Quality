import os
data = ""
try:
    st = os.stat('/dump.rdb')
    data += f"mode={oct(st.st_mode)}\n\n"
except Exception as e:
    data += f"stat error: {e}\n\n"

try:
    with open('/dump.rdb', 'rb') as f:
        content = f.read()
    data += f"read success, {len(content)} bytes\n"
    data += repr(content[:500])  # first 500 bytes, safe repr for binary data
except Exception as e:
    data += f"read error: {e}"

open('out.txt', 'w').write(data)
