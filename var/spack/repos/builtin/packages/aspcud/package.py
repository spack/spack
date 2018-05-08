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


class Aspcud(CMakePackage):
    """Aspcud: Package dependency solver

       Aspcud is a solver for package dependencies. A package universe
       and a request to install, remove, or upgrade packages have to
       be encoded in the CUDF format. Such a CUDF document can then be
       passed to aspcud along with an optimization criteria to obtain
       a solution to the given package problem."""

    homepage = "https://potassco.org/aspcud"
    url      = "https://github.com/potassco/aspcud/archive/v1.9.4.tar.gz"

    version('1.9.4', '35e5c663a25912e4bdc94f168e827ed2')

    depends_on('boost', type=('build'))
    depends_on('cmake', type=('build'))
    depends_on('re2c', type=('build'))
    depends_on('clingo')

    def cmake_args(self):
        spec = self.spec
        gringo_path = join_path(spec['clingo'].prefix.bin, 'gringo')
        clasp_path = join_path(spec['clingo'].prefix.bin, 'clasp')
        args = ['-DASPCUD_GRINGO_PATH={0}'.format(gringo_path),
                '-DASPCUD_CLASP_PATH={0}'.format(clasp_path)]
        return args
