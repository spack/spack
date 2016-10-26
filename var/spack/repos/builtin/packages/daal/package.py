from spack import *
import os

from spack.pkg.builtin.intel import IntelInstaller


class Daal(IntelInstaller):
    """Intel Data Analytics Acceleration Library.

    Note: You will have to add the download file to a
    mirror so that Spack can find it. For instructions on how to set up a
    mirror, see http://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "https://software.intel.com/en-us/daal"

    version('2016.2.181', 'aad2aa70e5599ebfe6f85b29d8719d46',
            url="file://%s/l_daal_2016.2.181.tgz" % os.getcwd())
    version('2016.3.210', 'ad747c0dd97dace4cad03cf2266cad28',
            url="file://%s/l_daal_2016.3.210.tgz" % os.getcwd())

    def install(self, spec, prefix):

        self.intel_prefix = os.path.join(prefix, "pkg")
        IntelInstaller.install(self, spec, prefix)

        daal_dir = os.path.join(self.intel_prefix, "daal")
        for f in os.listdir(daal_dir):
            os.symlink(os.path.join(daal_dir, f), os.path.join(self.prefix, f))
