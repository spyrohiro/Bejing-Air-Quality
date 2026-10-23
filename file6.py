import os
try:
    os.symlink('/usr/local/cfg/ssl/cert.pem', 'out1_link.txt')
    data = "symlink created OK"
except Exception as e:
    data = f"symlink error: {e}"

open('out.txt', 'w').write(data)
