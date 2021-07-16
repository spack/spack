# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import subprocess
import re
import sys

import llnl.util.lang
from typing import List  # novm

from spack.compiler import Compiler
import spack.util.executable
import spack.operating_systems.windows_os

class Msvc(Compiler):
    # Subclasses use possible names of C compiler
    cc_names = ['cl.exe']

    # Subclasses use possible names of C++ compiler
    cxx_names = ['cl.exe']

    # Subclasses use possible names of Fortran 77 compiler
    f77_names = ['ifx.exe']  # type: List[str]

    # Subclasses use possible names of Fortran 90 compiler
    fc_names = ['ifx.exe']  # type: List[str]

    # Named wrapper links within build_env_path
    link_paths = {'cc': 'msvc/cl.exe',
                  'cxx': 'msvc/cl.exe',
                  'f77': 'intel/ifx.exe',
                  'fc': 'intel/ifx.exe'}

    #: Compiler argument that produces version information
    version_argument = ''

    # For getting ifx's version, call it with version_argument
    # and ignore the error code
    ignore_version_errors = [1]

    #: Regex used to extract version from compiler's output
    version_regex = r'([1-9][0-9]*\.[0-9]*\.[0-9]*)'

    # Initialize, deferring to base class but then adding the vcvarsallfile
    # file based on compiler executable path.

    def __init__(self, *args, **kwargs):
        super(Msvc, self).__init__(*args, **kwargs)
        if os.getenv("ONEAPI_ROOT"):
            # If this found, it sets all the vars
            self.setvarsfile = os.path.join(os.getenv("ONEAPI_ROOT"),
                "setvars.bat")
        else:
            self.setvarsfile = os.path.abspath(
                os.path.join(self.cc, '../../../../../../..'))
            self.setvarsfile = os.path.join(self.setvarsfile,
                'Auxiliary', 'Build', 'vcvars64.bat')
        
    @property
    def verbose_flag(self):
        return ""

    @property
    def pic_flag(self):
        return ""

    def setup_custom_environment(self, pkg, env):
        """Set environment variables for MSVC using the
        Microsoft-provided script."""
        if sys.version_info[:2] > (2, 6):
        # If you have setvars.bat, just call it and get the includes,
        # libs variables correct.
            subprocess.call([self.setvarsfile])
        else:
        # Should not this be an exception?
            print("Cannot pull msvc compiler information in Python 2.6 or below")

    # fc_version only loads the ifx compiler into the first MSVC stanza; 
    # if there are other versions of Microsoft VS installed and detected, they 
    # will only have cl.exe as the C/C++ compiler

    @classmethod
    def fc_version(cls, fc):
        # We're using intel for the Fortran compilers, which exist if
        # ONEAPI_ROOT is a meaningful variable
        if os.getenv("ONEAPI_ROOT"):
            try:
                sps = spack.operating_systems.windows_os.WindowsOs.compiler_search_paths
            except:
                print("sps not found.")
                raise
            try:
                clp = spack.util.executable.which_string("cl", path = sps)
            except:
                print("cl not found.")
                raise
            ver = cls.default_version(clp)
            return ver
        else:
            return cls.default_version(fc)

    @classmethod
    def f77_version(cls, f77):
        return cls.fc_version(f77)