# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
