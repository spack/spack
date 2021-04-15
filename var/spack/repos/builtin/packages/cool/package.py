# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cool(CMakePackage):
    """COOL provides specific software components and tools for the handling of the time
       variation and versioning of the experiment conditions data."""

    homepage = "https://coral-cool.docs.cern.ch/"
    git      = "https://gitlab.cern.ch/lcgcool/cool.git"

    tags = ['hep']

    version('3.3.5', tag='COOL_3_3_5')
    version('3.3.4', tag='COOL_3_3_4')
    version('3.3.3', tag='COOL_3_3_3')

    patch('cool.patch', level=0)

    variant('binary_tag', default='auto')

    depends_on('coral')
    depends_on('root')
    depends_on('vdt')
    depends_on('xz')
    depends_on('qt@5:', when='platform=linux')

    def determine_binary_tag(self):
        # As far as I can tell from reading the source code, `binary_tag`
        # can be almost arbitraryThe only real difference it makes is
        # disabling oracle dependency for non-x86 platforms
        if self.spec.variants['binary_tag'].value != 'auto':
            return self.spec.variants['binary_tag'].value

        binary_tag = str(self.spec.target.family) + \
            '-' + self.spec.os + \
            '-' + self.spec.compiler.name + str(self.spec.compiler.version.joined) + \
            ('-opt' if 'Rel' in self.spec.variants['build_type'].value else '-dbg')

        return binary_tag

    def cmake_args(self):
        binary_tag = self.determine_binary_tag()
        args = ['-DBINARY_TAG=' + binary_tag]
        if self.spec['python'].version >= Version("3.0.0"):
            args.append('-DLCG_python3=on')

        return args
