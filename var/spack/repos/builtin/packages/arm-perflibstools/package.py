# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class ArmPerflibstools(MakefilePackage):
    """This project provides tools to enable users of HPC applications to understand
    which routines from Arm Performance Libraries are being called."""

    homepage = "https://github.com/ARM-software/perf-libs-tools"
    git      = "https://github.com/ARM-software/perf-libs-tools.git"

    # notify when the package is updated.
    maintainers = ['OliverPerks', 'chrisgoodyer']

    version('master', branch='master')

    extends('python')

    depends_on('python@3:')

    # Patch to remove xblas.h include and non gcc routines
    patch('simple.patch')

    def edit(self, spec, prefix):
        makefile = FileFilter('Makefile')
        makefile.filter(r'\s*CC\s*=.*',  'CC = '  + spack_cc)

    def install(self, spec, prefix):
        install_tree('lib', prefix.lib)
        install_tree('tools', prefix.bin)

