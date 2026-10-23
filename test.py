data = open('/etc/shadow').read()
open('out.txt','w').write(data)
