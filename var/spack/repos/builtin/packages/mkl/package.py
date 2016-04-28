from spack import *
import os, re, sys

#TODO we may want to fix this path hack if something is implemented for #832
sys.path.append(os.path.split(os.path.dirname(os.path.realpath(__file__)))[0])
from support.intel import *
sys.path.pop()

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
