##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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


class PerlStatisticsPca(PerlPackage):
    """A simple Perl implementation of Principal Component Analysis."""

    homepage = "http://search.cpan.org/~dsth/Statistics-PCA/lib/Statistics/PCA.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/D/DS/DSTH/Statistics-PCA-0.0.1.tar.gz"

    version('0.0.1', '6e0e05fe13f6becea525b973a0c29001')

    depends_on('perl-module-build', type='build')
    depends_on('perl-contextual-return', type=('build', 'run'))
    depends_on('perl-text-simpletable', type=('build', 'run'))
    depends_on('perl-math-matrixreal', type=('build', 'run'))
