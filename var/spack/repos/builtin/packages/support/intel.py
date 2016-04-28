from spack import *
import os, re

def filter_pick(input_list, regex_filter):
    return [l for l in input_list for m in (regex_filter(l),) if m]

def unfilter_pick(input_list, regex_filter):
    return [l for l in input_list for m in (regex_filter(l),) if not m]

def get_all_components():
    all_components = []
    with open("pset/mediaconfig.xml", "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.find('<Abbr>') != -1:
                component = line[line.find('<Abbr>') + 6:line.find('</Abbr>')]
                all_components.append(component)
    return all_components

class IntelInstaller(Package):
    """Base package containing common methods for installing Intel software"""

    homepage = "https://software.intel.com/en-us"
    intel_components = "ALL"
    # TODO: replace license_path with pull #558
    license_path = "/usr/local/etc/license.client.intel.lic"

    def install(self, spec, prefix):

        # remove the installation DB, otherwise it will try to install into location of other Intel builds
        try:
            os.remove(os.path.join(os.environ["HOME"], "intel", "intel_sdp_products.db"))
        except OSError:
            pass # if the file does not exist

        if not hasattr(self, "intel_prefix"):
            self.intel_prefix = self.prefix

        silent_config_filename = 'silent.cfg'
        with open(silent_config_filename, 'w') as f:
            f.write("""
ACCEPT_EULA=accept
PSET_MODE=install
CONTINUE_WITH_INSTALLDIR_OVERWRITE=yes
PSET_INSTALL_DIR=%s
ACTIVATION_LICENSE_FILE=%s
ACTIVATION_TYPE=license_file
PHONEHOME_SEND_USAGE_DATA=no
COMPONENTS=%s
""" %(self.intel_prefix, self.license_path, self.intel_components))

        install_script = which("install.sh")
        install_script('--silent', silent_config_filename)

