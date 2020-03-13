import time
import subprocess
import os

stamppi = os.path.getmtime(r"T:\Project Data\Projects\1CVX999999 Fincantieri NCL 1 TEST\IDremotelog.txt")

while time.time()-stamppi < 300:
    stamppi = os.path.getmtime(r"T:\Project Data\Projects\1CVX999999 Fincantieri NCL 1 TEST\IDremotelog.txt")
    print(time.time()-stamppi)

subprocess.call(r"C:\Users\FIMAHEI2\Git\ID remote EngTool\Warning.bat")