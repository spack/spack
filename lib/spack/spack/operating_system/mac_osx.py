""" This class represents the MAC_OSX operating system. This will be auto
    detected using the python platform.mac_ver. The MAC_OSX platform
    will be represented using the major version operating system name, i.e
    el capitan, yosemite...etc.
"""

import spack
import os
import platform as py_platform
from spack.architecture import Platform, OperatingSystem

class MacOSX(OperatingSystem):
    def __init__(self):
        """ Autodetects the mac version from a dictionary. Goes back as
            far as 10.6 snowleopard. If the user has an older mac then
            the version will just be a generic mac_os.
        """
        
        def get_mac_release():
            mac_releases = {'10.6': "snowleopard", 
                            "10.7": "lion",
                            "10.8": "mountainlion",
                            "10.9": "mavericks",
                            "10.10": "yosemite",
                            "10.11": "elcapitan"}     

            mac_ver = py_platform.mac_ver()[0][:-2]
            try:
                name = mac_releases[mac_ver]
                return name, mac_ver
            except KeyError:
                name = "mac_os"
                return name, mac_ver

        name, version = get_mac_release()

        super(MacOSX, self).__init__(name, version)

    @property
    def compiler_strategy(self):
        return "PATH"




