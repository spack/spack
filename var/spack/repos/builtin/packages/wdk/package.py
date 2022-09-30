

import os
import re

from spack import *


class Wdk(Package):

    executables = ['mt']

    version("10.0.26639", sha256="")
    version("10.0.10586", sha256="")
    version("10.0.14393", sha256="")
    version("10.0.15063", sha256="")
    version("10.0.16299", sha256="")
    version("10.0.14393", sha256="")


    @classmethod
    def determine_version(cls, exe):
        """
        WDK is a set of drivers that we would like to
        be discoverable externally by Spack.
        The executable does not provide the WDK
        version so we derive from the exe path
        """
        version_match_pat = re.compile(r'[0-9][0-9].[0-9]+.[0-9][0-9][0-9][0-9][0-9]')
        ver_str = re.search(version_match_pat, exe)
        return ver_str if not ver_str else Version(ver_str.group())

    def determine_spec_details(self, prefix, exes_in_prefix):
        # exes_in_prefix = a set of paths, each path is an executable
        # prefix = a prefix that is common to each path in exes_in_prefix

        # return None or [] if none of the exes represent an instance of
        # the package. Return one or more Specs for each instance of the
        # package which is thought to be installed in the provided prefix
        pass
