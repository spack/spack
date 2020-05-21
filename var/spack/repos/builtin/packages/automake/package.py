# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

import os
import re


class Automake(AutotoolsPackage, GNUMirrorPackage):
    """Automake -- make file builder part of autotools"""

    homepage = 'http://www.gnu.org/software/automake/'
    gnu_mirror_path = 'automake/automake-1.15.tar.gz'

    version('1.16.2', sha256='b2f361094b410b4acbf4efba7337bdb786335ca09eb2518635a09fb7319ca5c1')
    version('1.16.1', sha256='608a97523f97db32f1f5d5615c98ca69326ced2054c9f82e65bade7fc4c9dea8')
    version('1.15.1', sha256='988e32527abe052307d21c8ca000aa238b914df363a617e38f4fb89f5abf6260')
    version('1.15',   sha256='7946e945a96e28152ba5a6beb0625ca715c6e32ac55f2e353ef54def0c8ed924')
    version('1.14.1', sha256='814c2333f350ce00034a1fe718e0e4239998ceea7b0aff67e9fd273ed6dfc23b')
    version('1.13.4', sha256='4c93abc0bff54b296f41f92dd3aa1e73e554265a6f719df465574983ef6f878c')
    version('1.11.6', sha256='53dbf1945401c43f4ce19c1971baecdbf8bc32e0f37fa3f49fe7b6992d0d2030')

    depends_on('autoconf', type='build')
    depends_on('perl', type=('build', 'run'))

    build_directory = 'spack-build'

    executables = ['automake']

    @classmethod
    def determine_spec_details(cls, prefix, exes_in_prefix):
        exe_to_path = dict(
            (os.path.basename(p), p) for p in exes_in_prefix
        )
        if 'automake' not in exe_to_path:
            return None

        exe = spack.util.executable.Executable(exe_to_path['automake'])
        output = exe('--version', output=str)
        if output:
            match = re.search(r'GNU automake\)\s+(\S+)', output)
            if match:
                version_str = match.group(1)
                return Spec('automake@{0}'.format(version_str))

    def patch(self):
        # The full perl shebang might be too long
        files_to_be_patched_fmt = 'bin/{0}.in'
        if '@:1.15.1' in self.spec:
            files_to_be_patched_fmt = 't/wrap/{0}.in'

        for file in ('aclocal', 'automake'):
            filter_file('^#!@PERL@ -w',
                        '#!/usr/bin/env perl',
                        files_to_be_patched_fmt.format(file))

    def _make_executable(self, name):
        return Executable(join_path(self.prefix.bin, name))

    def setup_dependent_package(self, module, dependent_spec):
        # Automake is very likely to be a build dependency,
        # so we add the tools it provides to the dependent module
        executables = ['aclocal', 'automake']
        for name in executables:
            setattr(module, name, self._make_executable(name))
