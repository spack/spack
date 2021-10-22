# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import subprocess
import sys
from typing import List  # novm

from spack.compiler import Compiler


class Msvc(Compiler):
    # Subclasses use possible names of C compiler
    cc_names = ['cl.exe']

    # Subclasses use possible names of C++ compiler
    cxx_names = ['cl.exe']

    # Subclasses use possible names of Fortran 77 compiler
    f77_names = []  # type: List[str]

    # Subclasses use possible names of Fortran 90 compiler
    fc_names = []  # type: List[str]

    # Named wrapper links within build_env_path
    link_paths = {'cc': 'msvc/cl.exe',
                  'cxx': 'msvc/cl.exe',
                  'f77': '',
                  'fc': ''}

    #: Compiler argument that produces version information
    version_argument = ''

    #: Regex used to extract version from compiler's output
    version_regex = r'([1-9][0-9]*\.[0-9]*\.[0-9]*)'

    # Initialize, deferring to base class but then adding the vcvarsallfile
    # file based on compiler executable path.

    def __init__(self, *args, **kwargs):
        super(Msvc, self).__init__(*args, **kwargs)
        self.vcvarsallfile = os.path.abspath(
            os.path.join(self.cc, '../../../../../../..'))
        self.vcvarsallfile = os.path.join(
            self.vcvarsallfile, 'Auxiliary', 'Build', 'vcvarsall.bat')

    @property
    def verbose_flag(self):
        return ""

    @property
    def pic_flag(self):
        return ""

    def setup_custom_environment(self, pkg, env):
        """Set environment variables for MSVC using the Microsoft-provided
        script."""
        if sys.version_info[:2] > (2, 6):
            # Capture output from batch script and DOS environment dump
            out = subprocess.check_output(  # novermin
                'cmd /u /c "{0}" {1} && set'.format(self.vcvarsallfile, 'amd64'),
                stderr=subprocess.STDOUT)
            if sys.version_info[0] >= 3:
                out = out.decode('utf-16le', errors='replace')
        else:
            print("Cannot pull msvc compiler information in Python 2.6 or below")

        # Process in to nice Python dictionary
        vc_env = {  # novermin
            key.lower(): value
            for key, _, value in
            (line.partition('=') for line in out.splitlines())
            if key and value
        }

        # Request setting environment variables
        if 'path' in vc_env:
            env.set_path('PATH', vc_env['path'].split(';'))
        env.set_path('INCLUDE', vc_env.get('include', '').split(';'))
        env.set_path('LIB', vc_env.get('lib', '').split(';'))
