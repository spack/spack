from spack import *
import os

from spack.pkg.builtin.intel import IntelInstaller


class Ipp(IntelInstaller):
    """Intel Integrated Performance Primitives.

    Note: You will have to add the download file to a
    mirror so that Spack can find it. For instructions on how to set up a
    mirror, see http://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "https://software.intel.com/en-us/intel-ipp"

    version('9.0.3.210', '0e1520dd3de7f811a6ef6ebc7aa429a3',
            url="file://%s/l_ipp_9.0.3.210.tgz" % os.getcwd())

    def install(self, spec, prefix):

        self.intel_prefix = os.path.join(prefix, "pkg")
        IntelInstaller.install(self, spec, prefix)

        ipp_dir = os.path.join(self.intel_prefix, "ipp")
        for f in os.listdir(ipp_dir):
            os.symlink(os.path.join(ipp_dir, f), os.path.join(self.prefix, f))
