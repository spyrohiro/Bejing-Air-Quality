import os, stat
data = ""
try:
    files = os.listdir('ssl')
    data += f"files: {files}\n\n"
    for fn in files:
        full = os.path.join('ssl', fn)
        try:
            st = os.stat(full)
            data += f"{fn}: mode={oct(st.st_mode)} uid={st.st_uid} gid={st.st_gid} size={st.st_size}\n"
        except Exception as e:
            data += f"{fn}: stat error: {e}\n"
except Exception as e:
    data += f"listdir error: {e}\n"

open('out.txt','w').write(data)
