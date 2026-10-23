import os

def safe_listdir(path):
    try:
        return os.listdir(path)
    except Exception as e:
        return f"ERROR: {e}"

def safe_stat(path):
    try:
        st = os.stat(path)
        return f"size={st.st_size} mode={oct(st.st_mode)} uid={st.st_uid}"
    except Exception as e:
        return f"ERROR: {e}"

data = ""

for d in ['/config', '/exos', '/data', '/data3', '/tmp']:
    data += f"=== {d} ===\n"
    listing = safe_listdir(d)
    data += str(listing) + "\n"
    if isinstance(listing, list):
        for item in listing:
            full = os.path.join(d, item)
            data += f"  {item}: {safe_stat(full)}\n"
    data += "\n"

data += "=== /dump.rdb ===\n"
data += safe_stat('/dump.rdb') + "\n"

open('out.txt', 'w').write(data)
