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


class PerlInlineC(PerlPackage):
    """C Language Support for Inline"""

    homepage = "http://search.cpan.org/~tinita/Inline-C-0.78/lib/Inline/C.pod"
    url      = "http://search.cpan.org/CPAN/authors/id/T/TI/TINITA/Inline-C-0.78.tar.gz"

    version('0.78', '710a454b5337b1cbf3f2ae5c8c45b413')

    depends_on('perl-yaml-libyaml', type=('build', 'run'))
    depends_on('perl-parse-recdescent', type=('build', 'run'))
    depends_on('perl-inline', type=('build', 'run'))
    depends_on('perl-pegex', type=('build', 'run'))
    depends_on('perl-file-copy-recursive', type=('build', 'run'))
