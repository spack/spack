# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlGdGraph(PerlPackage):
    """Graph Plotting Module for Perl 5"""

    homepage = "http://search.cpan.org/~bwarfield/GDGraph/Graph.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/B/BW/BWARFIELD/GDGraph-1.4308.tar.gz"

    version('1.4308', 'fcdd34d5e09ae917b5d264887734b3b1')

    depends_on('perl-capture-tiny', type=('build', 'run'))
    depends_on('perl-test-exception', type=('build', 'run'))
    depends_on('perl-gd-text', type=('build', 'run'))
    depends_on('perl-gd', type=('build', 'run'))
