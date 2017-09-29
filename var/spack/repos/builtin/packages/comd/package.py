##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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


class Comd(MakefilePackage):
    """CoMD is a reference implementation of classical molecular dynamics
    algorithms and workloads as used in materials science. It is created and
    maintained by The Exascale Co-Design Center for Materials in Extreme
    Environments (ExMatEx). The code is intended to serve as a vehicle for
    co-design by allowing others to extend and/or reimplement it as needed to
    test performance of new architectures, programming models, etc. New
    versions of CoMD will be released to incorporate the lessons learned from
    the co-design process."""

    homepage = "http://exmatex.github.io/CoMD/"

    version('master', git='https://github.com/exmatex/CoMD.git',
            branch='master')

    depends_on('mpi')

    build_directory = 'src-mpi'

    def edit(self, spec, prefix):
        with working_dir('src-mpi'):
            filter_file(r'^CC\s*=.*', 'CC = %s' % self.spec['mpi'].mpicc,
                        'Makefile.vanilla')
            install('Makefile.vanilla', 'Makefile')

    def install(self, spec, prefix):
        install_tree('bin', prefix.bin)
