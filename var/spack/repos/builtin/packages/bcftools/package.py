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


class Bcftools(AutotoolsPackage):
    """BCFtools is a set of utilities that manipulate variant calls in the
       Variant Call Format (VCF) and its binary counterpart BCF. All
       commands work transparently with both VCFs and BCFs, both
       uncompressed and BGZF-compressed."""

    homepage = "http://samtools.github.io/bcftools/"
    url      = "https://github.com/samtools/bcftools/releases/download/1.3.1/bcftools-1.3.1.tar.bz2"

    version('1.8', 'ba6c2fb7eb6dcb208f00ab8b22df475c')
    version('1.7', 'c972db68d17af9da3a18963f4e5aeca8')
    version('1.6', 'c4dba1e8cb55db0f94b4c47724b4f9fa')
    version('1.4', '50ccf0a073bd70e99cdb3c8be830416e')
    version('1.3.1', '575001e9fca37cab0c7a7287ad4b1cdb')
    version('1.2', '8044bed8fce62f7072fc6835420f0906')

    depends_on('libzip', when='@1.8:')

    depends_on('htslib@1.8', when='@1.8')
    depends_on('htslib@1.7',   when='@1.7')
    depends_on('htslib@1.6',   when='@1.6')
    depends_on('htslib@1.4',   when='@1.4')
    depends_on('htslib@1.3.1', when='@1.3.1')
    depends_on('htslib@1.2', when='@1.2')
