from spack import *
import sys, os, re

#TODO we may want to fix this path hack if something is implemented for #832
sys.path.append(os.path.split(os.path.dirname(os.path.realpath(__file__)))[0])
from support.intel import *
sys.path.pop()

class Intel(IntelInstaller):
    """Intel Compilers.

    Note: You will have to add the download file to a
    mirror so that Spack can find it. For instructions on how to set up a
    mirror, see http://software.llnl.gov/spack/mirrors.html"""

    homepage = "https://software.intel.com/en-us/intel-parallel-studio-xe"

    # TODO: can also try the online installer (will download files on demand)
    version('16.0.2', '1133fb831312eb519f7da897fec223fa',
            url="file://%s/parallel_studio_xe_2016_composer_edition_update2.tgz" % os.getcwd())

    variant('rpath', default=True, description="Add rpath to .cfg files")

    def install(self, spec, prefix):

        # remove the installation DB, otherwise it will try to install into location of other Intel builds
        try:
            os.remove(os.path.join(os.environ["HOME"], "intel", "intel_sdp_products.db"))
        except OSError:
            pass # if the file does not exist

        components = []
        with open("pset/mediaconfig.xml", "r") as f:
            lines = f.readlines()
            all_components = []
            for line in lines:
                if line.find('<Abbr>') != -1:
                    component = line[line.find('<Abbr>') + 6:line.find('</Abbr>')]
                    all_components.append(component)
            components = filter_pick(all_components, re.compile('(comp|openmp|intel-tbb|icc|ifort|psxe|icsxe-pset)').search)

        self.intel_components = ';'.join(components)
        IntelInstaller.install(self, spec, prefix)

        absbindir = os.path.split(os.path.realpath(os.path.join(self.prefix.bin, "icc")))[0]
        abslibdir = os.path.split(os.path.realpath(os.path.join(self.prefix.lib, "intel64", "libimf.a")))[0]

        # symlink or copy?
        os.symlink(self.license_path, os.path.join(absbindir, "license.lic"))

        if spec.satisfies('+rpath'):
            for compiler_command in ["icc", "icpc", "ifort"]:
                cfgfilename = os.path.join(absbindir, "%s.cfg" %(compiler_command))
                with open(cfgfilename, "w") as f:
                    f.write('-Xlinker -rpath -Xlinker %s\n' %(abslibdir))

        os.symlink(os.path.join(self.prefix.man, "common", "man1"), os.path.join(self.prefix.man, "man1"))
