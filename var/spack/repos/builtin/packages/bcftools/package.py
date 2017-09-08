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


class Bcftools(Package):
    """BCFtools is a set of utilities that manipulate variant calls in the
       Variant Call Format (VCF) and its binary counterpart BCF. All
       commands work transparently with both VCFs and BCFs, both
       uncompressed and BGZF-compressed."""

    homepage = "http://samtools.github.io/bcftools/"
    url      = "https://github.com/samtools/bcftools/releases/download/1.3.1/bcftools-1.3.1.tar.bz2"

    version('1.4', '50ccf0a073bd70e99cdb3c8be830416e')
    version('1.3.1', '575001e9fca37cab0c7a7287ad4b1cdb')

    depends_on('zlib')
    depends_on('bzip2', when="@1.4:")
    # build fails without xz
    depends_on('xz', when="@1.4")

    def install(self, spec, prefix):
        make("prefix=%s" % prefix, "all")
        make("prefix=%s" % prefix, "install")
