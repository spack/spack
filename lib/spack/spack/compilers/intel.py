#
# This is a stub module.  It should be expanded when we implement full
# compiler support.
#

import subprocess
from spack.version import Version

cc = 'icc'
cxx = 'icc'
fortran = 'ifort'

def get_version():
    v = subprocess.check_output([cc, '-dumpversion'])
    return Version(v)
