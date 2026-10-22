with open('out.txt', 'w') as f:
    try:
        import subprocess
        result = subprocess.check_output(['id']).decode()
        f.write(result)
    except Exception as e:
        f.write(str(e))
