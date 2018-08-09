##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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


class Openmc(MakefilePackage):
    """The OpenMC project aims to provide a fully-featured Monte Carlo particle
       transport code based on modern methods. It is a constructive solid
       geometry, continuous-energy transport code that uses ACE format cross
       sections. The project started under the Computational Reactor Physics
       Group at MIT."""

    homepage = "https://github.com/ANL-CESAR/"
    git      = "https://github.com/ANL-CESAR/openmc.git"

    tags = ['ecp', 'ecp-apps']

    version('develop')

    build_directory = 'src'

    parallel = False

    @property
    def build_targets(self):

        targets = []

        if self.compiler.name == 'gcc':
            targets.append('COMPILER=gnu')
            targets.append('MACHINE=UNKNOWN')
        if self.compiler.name == 'intel':
            targets.append('COMPILER=intel')
        if self.compiler.name == 'pgi':
            targets.append('COMPILER=pgi')
        if self.compiler.name == 'xl':
            targets.append('COMPILER=ibm')
        if self.compiler.name == 'cce':
            targets.append('COMPILER=cray')

        return targets

    def install(self, spec, prefix):
        with working_dir('src'):
            pth_st_cmp = join_path(prefix.bin, 'statepoint_cmp')
            pth_st_histogram = join_path(prefix.bin, 'statepoint_histogram')
            pth_st_meshpoint = join_path(prefix.bin, 'statepoint_meshpoint')
            pth_openmc = join_path(prefix, 'share/man/man1/openmc.1')
            pth_copyright = join_path(prefix, 'share/doc/openmc/copyright')
            mkdir(prefix.bin)
            mkdirp(pth_st_cmp)
            mkdirp(pth_st_histogram)
            mkdirp(pth_st_meshpoint)
            mkdirp(pth_openmc)
            mkdirp(pth_copyright)

            install('openmc', prefix.bin)
            install('utils/statepoint_cmp.py', pth_st_cmp)
            install('utils/statepoint_histogram.py',
                    pth_st_histogram)
            install('utils/statepoint_meshplot.py',
                    pth_st_meshpoint)
        install('man/man1/openmc.1', pth_openmc)
        install('LICENSE', pth_copyright)
        install_tree('docs/', prefix.docs)
        install_tree('examples/', prefix.examples)
        install_tree('data/', prefix.data)
        install_tree('tests/', prefix.tests)
