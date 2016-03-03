import platform as py_platform
from spack.architecture import OperatingSystem

class MacOsx(OperatingSystem):
    """ This class represents the MAC_OSX operating system. This will be auto
    detected using the python platform.mac_ver. The MAC_OSX platform
    will be represented using the major version operating system name, i.e
    el capitan, yosemite...etc.
    """
    
    def __init__(self):
        """ Autodetects the mac version from a dictionary. Goes back as
            far as 10.6 snowleopard. If the user has an older mac then
            the version will just be a generic mac_os.
        """
        mac_releases = {'10.6': "snowleopard", 
                        "10.7": "lion",
                        "10.8": "mountainlion",
                        "10.9": "mavericks",
                        "10.10": "yosemite",
                        "10.11": "elcapitan"}     

        mac_ver = py_platform.mac_ver()[0][:-2]
        try:
            name = mac_releases[mac_ver]
        except KeyError:
            name = "mac_os"

        super(MacOsx, self).__init__(name, mac_ver)
