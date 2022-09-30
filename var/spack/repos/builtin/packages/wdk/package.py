

import os
import re

from spack import *


class WDK(Package):

    executables = ['mt']


    def determine_version(self, exe):
        """
        WDK is a set of drivers that we would like to
        be discoverable externally by Spack.
        The executable does not provide the WDK
        version so we derive from the exe path
        """
        version_match_pat = re.compile(r'[1-9][1-9].[1-9]+.[1-9][1-9][1-9][1-9][1-9]')
        ver_str = re.search(version_match_pat, exe)
        return ver_str if not ver_str else Version(ver_str)