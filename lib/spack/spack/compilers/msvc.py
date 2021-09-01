# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import subprocess
import sys
from typing import List  # novm

from spack.error import SpackError
import spack.operating_systems.windows_os
import spack.util.executable
from spack.compiler import Compiler


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
    link_paths = {'cc': '',
                  'cxx': '',
                  'f77': '',
                  'fc': ''}

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
            self.setvarsfile = os.path.join(
                os.getenv("ONEAPI_ROOT"), "setvars.bat")
        else:
            self.setvarsfile = os.path.abspath(
                os.path.join(self.cc, '../../../../../../..'))
            self.setvarsfile = os.path.join(
                self.setvarsfile, 'Auxiliary', 'Build', 'vcvars64.bat')

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
            # Set the build environment variables for spack. Just using
            # subprocess.call() doesn't work since that operates in its own
            # environment which is destroyed (along with the adjusted variables)
            # once the process terminates. So go the long way around: examine
            # output, sort into dictionary, use that to make the build
            # environment.
            out = subprocess.check_output(  # novermin
                'cmd /u /c "{}" {} && set'.format(self.setvarsfile, 'amd64'),
                stderr=subprocess.STDOUT)
            if sys.version_info[0] >= 3:
                out = out.decode('utf-16le', errors='replace')  # novermin

            int_env = {  # novermin
                key.lower(): value
                for key, _, value in
                (line.partition('=') for line in out.splitlines())
                if key and value
            }

            if 'path' in int_env:
                env.set_path('PATH', int_env['path'].split(';'))
            env.set_path('INCLUDE', int_env.get('include', '').split(';'))
            env.set_path('LIB', int_env.get('lib', '').split(';'))
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
            except AttributeError:
                raise SpackError("Windows compiler search paths not established")
            clp = spack.util.executable.which_string("cl", path=sps)
            ver = cls.default_version(clp)
            return ver
        else:
            return cls.default_version(fc)

    @classmethod
    def f77_version(cls, f77):
        return cls.fc_version(f77)
