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
from spack.operating_systems.mac_os import macos_version
import sys


class Bison(AutotoolsPackage):
    """Bison is a general-purpose parser generator that converts
    an annotated context-free grammar into a deterministic LR or
    generalized LR (GLR) parser employing LALR(1) parser tables."""

    homepage = "http://www.gnu.org/software/bison/"
    url      = "https://ftpmirror.gnu.org/bison/bison-3.0.4.tar.gz"

    version('3.0.5', '41ad57813157b61bfa47e33067a9d6f0')
    version('3.0.4', 'a586e11cd4aff49c3ff6d3b6a4c9ccf8')
    version('2.7',   'ded660799e76fb1667d594de1f7a0da9')

    depends_on('m4', type=('build', 'run'))

    patch('pgi.patch', when='@3.0.4')

    if sys.platform == 'darwin' and macos_version() >= Version('10.13'):
        patch('secure_snprintf.patch', level=0, when='@3.0.4')

    build_directory = 'spack-build'
