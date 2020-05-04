from spack import *
from spack.hooks.sbang import filter_shebang

class PyShroud(Package):
    """Create Fortran wrappers for a C++ library."""

    homepage = "https://github.com/LLNL/shroud"
    git      = "https://github.com/LLNL/shroud.git"

    version('develop', branch='develop')
    version('master',  branch='master')
    version('0.11.0', tag='v0.11.0')
    version('0.10.1', tag='v0.10.1')
    version('0.9.0', tag='v0.9.0')
    version('0.8.0', tag='v0.8.0')

    extends('python')

    depends_on("py-alabaster")
    depends_on("py-pytz")
    depends_on("py-docutils")
    depends_on("py-setuptools")
    depends_on("py-pyyaml")

    def install(self, spec, prefix):
        # simply install to the spack python
        python('setup.py', 'install') 

        # shroud lives in python's bin dir
        shroud_scripts = ["shroud"]
        for script in shroud_scripts:
            script_path = join_path(spec["python"].prefix,"bin",script)
            # use spack sbang to fix issues with shebang that is too long
            filter_shebang(script_path)
