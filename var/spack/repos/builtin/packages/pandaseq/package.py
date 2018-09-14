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


class Pandaseq(AutotoolsPackage):
    """PANDASEQ is a program to align Illumina reads, optionally with PCR
    primers embedded in the sequence, and reconstruct an overlapping
    sequence."""

    homepage = "https://github.com/neufeld/pandaseq"
    url      = "https://github.com/neufeld/pandaseq/archive/v2.11.tar.gz"

    version('2.11', 'a8ae0e938bac592fc07dfa668147d80b')
    version('2.10', '5b5b04c9b693a999f10a9c9bd643f068')

    depends_on('autoconf',    type='build')
    depends_on('automake',    type='build')
    depends_on('libtool',     type=('build', 'link'))
    depends_on('m4',          type='build')
    depends_on('zlib',        type='build')
    depends_on('pkgconfig',   type='build')
    depends_on('bzip2',       type='link')

    def autoreconf(self, spec, prefix):
        bash = which('bash')
        bash('./autogen.sh')
