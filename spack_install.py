import subprocess
import os

def install(spec):
    # Install the spec package if absent
    if "No package" in subprocess.check_output("spack find {}".format(spec), shell=True).decode("utf-8"):
        print("{} not found. Build it.".format(spec))
        os.system("spack install --restage {}".format(spec))

def check_pass(pkg, compiler, spec, mpi="", platform="sandybridge"):
    if ('cuda' not in pkg) and ('+cuda' not in mpi): return True
    if ('+cuda' not in pkg) and ('+cuda' in mpi): return False
    if ('+cuda' in pkg) and ('~cuda' in mpi): return False
    if ('+cuda' in pkg) and ('knightlanding' in platform): return False
    if ('cuda' in spec) and ('knightlanding' in platform): return False
    if ('~cuda' in pkg) and ('+cuda' in mpi): return False
    if ('intel-parallel' in mpi) and ('gcc' in compiler): return False
    return True
