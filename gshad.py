import os
def read_or_reason(p):
    if not os.path.exists(p):
        return 'ABSENT'
    try:
        with open(p) as f:
            return f.read()
    except PermissionError:
        return 'DENIED'
    except OSError as e:
        return f'ERR:{e.errno}'

data = ""
data += f"gshad={read_or_reason('/etc/gshadow')}"

with open('out.txt', 'w') as f:
    f.write(data)
