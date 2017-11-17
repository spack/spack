import subprocess
import os

def install(spec):
    # Install the spec package if absent
    if "No package" in subprocess.check_output("spack find {}".format(spec), shell=True).decode("utf-8"):
        print("{} not found. Build it.".format(spec))
        os.system("spack install --restage {}".format(spec))

