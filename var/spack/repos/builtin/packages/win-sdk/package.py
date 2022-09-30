

import os
import re

from spack import *


class WinSdk(Package):
    """
    Windows Desktop C++ development SDK
    Spack packaged used to define search heuristics
    to locate the SDK on a filesystem
    """

    def install(self, prefix, spec):
        raise RuntimeError('This package is not installable from Spack\
            and should be installed on the system prior to Spack use.\
                If not installed this package should be installed via\
                    the Visual Studio installer in order to use the \
                        MSVC compiler on Windows.')


