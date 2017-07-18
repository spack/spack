##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

from spack import *
import platform
import numbers


def is_integral(x):
    """Any integer value"""
    try:
        return isinstance(int(x), numbers.Integral) and not isinstance(x, bool)
    except ValueError:
        return False


class Lcals(MakefilePackage):
    """LCALS ("Livermore Compiler Analysis Loop Suite") is a collection of loop
       kernels based, in part, on historical "Livermore Loops" benchmarks
       (See the 1986 technical report: "The Livermore Fortran Kernels:
        A Computer Test of the Numerical Performance Range",
        by Frank H. McMahon, UCRL-53745.). The suite contains facilities to
        generate timing statistics and reports."""

    homepage = "https://codesign.llnl.gov/LCALS-downloads/"
    url = "https://codesign.llnl.gov/LCALS-downloads/lcals-v1.0.2.tgz"

    tags = ['proxy-app']

    version('1.0.2', '40c65a88f1df1436a2f72b7d3c986a21')

    variant(
        'xlcn',
        default=9,
        description='Version number for XLC compiler 9 or 12.',
        values=is_integral
    )

    variant(
        'microarch',
        description='Micro arch: SSE, AVX, MIC.',
        default='sse',
        values=('sse', 'avx', 'MIC'),
    )

    @property
    def build_targets(self):

        targets = []

        compiler = ''

        xlcn = self.spec.variants['xlcn'].value
        microarch = self.spec.variants['microarch'].value

        arch = platform.machine()

        if microarch == 'MIC':
            arch = 'MIC'
        elif arch == 'x86_64' or arch == 'x86_32':
            arch = 'x86'
        elif arch != 'bgq':
            raise InstallError('unknown architecture.')

        if self.compiler.name == 'gcc':
            compiler = 'gnu'
        elif self.compiler.name == 'intel':
            compiler = 'icc'
        elif self.compiler.name == 'xl':
            compiler = 'xlc' + xlcn
        elif self.compiler.name == 'clang' and arch == 'bgq':
            compiler = self.compiler.name
        else:
            raise InstallError('unknown compiler.')

        if arch == 'x86':
            arch = arch + '_' + microarch + '_' + compiler
        elif arch == 'bgq':
            arch = arch + '_' + compiler
        else:
            raise InstallError('Fatal Error: unknown construct.')

        targets.append('LCALS_ARCH={0}'.format(arch))
        targets.append('CXX={0}'.format(spack_cxx))

        return targets

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('lcals.exe', prefix.bin)
        install('lcalsversioninfo.txt', prefix)
