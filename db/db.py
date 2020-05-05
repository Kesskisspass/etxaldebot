import os
def sh(script):
    os.system(f"bash -c {script}")

sh("ls -a")
