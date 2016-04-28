from spack import *
import sys, os, re

#TODO we may want to fix this path hack if something is implemented for #832
sys.path.append(os.path.split(os.path.dirname(os.path.realpath(__file__)))[0])
from support.intel import *
sys.path.pop()

class Ipp(IntelInstaller):
    """Intel Integrated Performance Primitives.

    Note: You will have to add the download file to a
    mirror so that Spack can find it. For instructions on how to set up a
    mirror, see http://software.llnl.gov/spack/mirrors.html"""

    homepage = "https://software.intel.com/en-us/intel-ipp"

    version('9.0.2.181', 'd66e8761488fc35d58919f97499e0551',
            url="file://%s/l_ipp_9.0.2.181.tgz" % os.getcwd())

    def install(self, spec, prefix):

        self.intel_prefix = os.path.join(prefix, "pkg")
        IntelInstaller.install(self, spec, prefix)

        ipp_dir = os.path.join(self.intel_prefix, "ipp")
        for f in os.listdir(ipp_dir):
            os.symlink(os.path.join(ipp_dir, f), os.path.join(self.prefix, f))
