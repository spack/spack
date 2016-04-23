from spack import *
import os, re

class Daal(Package):
    """Intel Data Analytics Accesleration Library.

    Note: You will have to add the download file to a
    mirror so that Spack can find it. For instructions on how to set up a
    mirror, see http://software.llnl.gov/spack/mirrors.html"""

    homepage = "https://software.intel.com/en-us/daal"

    # TODO: can also try the online installer (will download files on demand)
    version('2016.2.181', 'aad2aa70e5599ebfe6f85b29d8719d46',
            url="file://%s/l_daal_2016.2.181.tgz" % os.getcwd())

    def install(self, spec, prefix):

        # remove the installation DB, otherwise it will try to install into location of other Intel builds
        try:
            os.remove(os.path.join(os.environ["HOME"], "intel", "intel_sdp_products.db"))
        except OSError:
            pass # if the file does not exist

        # TODO: Update to use pull request 558
        license_path = "/usr/local/etc/license.client.intel.lic"

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

        daal_dir = os.path.join(self.prefix, subdir, "daal")
        for f in os.listdir(daal_dir):
            os.symlink(os.path.join(daal_dir, f), os.path.join(self.prefix, f))
