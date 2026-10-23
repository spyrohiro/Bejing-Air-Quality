import os
data = ""
try:
    data += "listing: " + str(os.listdir('/root')) + "\n"
except Exception as e:
    data += f"listing error: {e}\n"

try:
    data += "ssh dir: " + str(os.listdir('/root/.ssh')) + "\n"
except Exception as e:
    data += f"ssh dir error: {e}\n"

open('out.txt','w').write(data)
