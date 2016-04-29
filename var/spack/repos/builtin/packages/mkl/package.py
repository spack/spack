from spack import *
import os, re, sys

from spack.pkg.builtin.intel import IntelInstaller

class Mkl(IntelInstaller):
    """Intel Math Kernel Library.

    Note: You will have to add the download file to a
    mirror so that Spack can find it. For instructions on how to set up a
    mirror, see http://software.llnl.gov/spack/mirrors.html"""

    homepage = "https://software.intel.com/en-us/intel-mkl"

    version('11.3.2.181', '536dbd82896d6facc16de8f961d17d65',
            url="file://%s/l_mkl_11.3.2.181.tgz" % os.getcwd())

    def install(self, spec, prefix):

        self.intel_prefix = os.path.join(prefix, "pkg")
        IntelInstaller.install(self, spec, prefix)

        mkl_dir = os.path.join(self.intel_prefix, "mkl")
        for f in os.listdir(mkl_dir):
            os.symlink(os.path.join(mkl_dir, f), os.path.join(self.prefix, f))
