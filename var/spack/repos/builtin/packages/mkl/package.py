from spack import *
import os, re

class Mkl(Package):
    """Intel Math Kernel Library.

    Note: You will have to add the download file to a
    mirror so that Spack can find it. For instructions on how to set up a
    mirror, see http://software.llnl.gov/spack/mirrors.html"""

    homepage = "https://software.intel.com/en-us/intel-mkl"

    # TODO: can also try the online installer (will download files on demand)
    version('11.3.2.181', '536dbd82896d6facc16de8f961d17d65',
            url="file://%s/l_mkl_11.3.2.181.tgz" % os.getcwd())

    #provides('mkl')

    def install(self, spec, prefix):

        # remove the installation DB, otherwise it will try to install into location of other Intel builds
        try:
            os.remove(os.path.join(os.environ["HOME"], "intel", "intel_sdp_products.db"))
        except OSError:
            pass # if the file does not exist

        # TODO: Update to use pull request 558
        license_path = "/usr/local/etc/license.client.intel.lic"

#        with open("pset/mediaconfig.xml", "r") as f:
#            lines = f.readlines()
#            all_components = []
#            for line in lines:
#                if line.find('<Abbr>') != -1:
#                    component = line[line.find('<Abbr>') + 6:line.find('</Abbr>')]
#                    all_components.append(component)
#            mkl_components = filter_pick(all_components, re.compile('(mkl)').search)
#
#        components = base_components
#        if not spec.satisfies('+all'):
#            if spec.satisfies('+mkl'):
#                components += mkl_components
#
#        components_string = ';'.join(components)

        silent_config_filename = 'silent.cfg'
        subdir = "pkg"
        with open(silent_config_filename, 'w') as f:
            f.write("""
ACCEPT_EULA=accept
PSET_MODE=install
CONTINUE_WITH_INSTALLDIR_OVERWRITE=yes
PSET_INSTALL_DIR=%s
ACTIVATION_LICENSE_FILE=%s
ACTIVATION_TYPE=license_file
PHONEHOME_SEND_USAGE_DATA=no
COMPONENTS=ALL
""" %(os.path.join(prefix, subdir), license_path))

        install_script = which("install.sh")

        install_script('--silent', silent_config_filename)

        mkl_dir = os.path.join(self.prefix, subdir, "mkl")
        for f in os.listdir(mkl_dir):
            os.symlink(os.path.join(mkl_dir, f), os.path.join(self.prefix, f))
