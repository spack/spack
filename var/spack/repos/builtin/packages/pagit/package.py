##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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


class Pagit(Package):
    """PAGIT addresses the need for software to generate high quality draft
       genomes."""

    homepage = "http://www.sanger.ac.uk/science/tools/pagit"
    url      = "ftp://ftp.sanger.ac.uk/pub/resources/software/pagit/PAGIT.V1.01.64bit.tgz"

    version('1.01', '2c4e8512c8c02073146b50b328962e9d')

    depends_on('java', type=('build', 'run'))
    depends_on('perl', type=('build', 'run'))

    def url_for_version(self, version):
        url = 'ftp://ftp.sanger.ac.uk/pub/resources/software/pagit/PAGIT.V{0}.64bit.tgz'
        return url.format(version)

    def install(self, spec, prefix):
        with working_dir('PAGIT'):
            install_tree('ABACAS', prefix.ABACAS)
            install_tree('bin', prefix.bin)
            install_tree('ICORN', prefix.ICORN)
            install_tree('IMAGE', prefix.IMAGE)
            install_tree('lib', prefix.lib)
            install_tree('RATT', prefix.RATT)

    def setup_environment(self, spack_env, run_env):
        run_env.set('PAGIT_HOME', self.prefix)
        run_env.set('PILEUP_HOME', join_path(self.prefix.bin, 'pileup_v0.5'))
        run_env.set('ICORN_HOME', self.prefix.icorn)
        run_env.set('SNPOMATIC_HOME', self.prefix.bin)
        run_env.set('RATT_HOME', self.prefix.RATT)
        run_env.set('RATT_CONFIG', join_path(self.prefix.RATT, 'RATT_config'))
        run_env.prepend_path('PATH', join_path(self.prefix.bin, 'pileup_v0.5',
                             'ssaha2'))
        run_env.prepend_path('PATH', join_path(self.prefix.bin,
                             'pileup_v0.5'))
        run_env.prepend_path('PATH', self.prefix.IMAGE)
        run_env.prepend_path('PATH', self.prefix.ABACAS)
        run_env.prepend_path('PATH', self.prefix.ICORN)
        run_env.prepend_path('PATH', self.prefix.RATT)
        run_env.prepend_path('PERL5LIB', self.prefix.lib)
