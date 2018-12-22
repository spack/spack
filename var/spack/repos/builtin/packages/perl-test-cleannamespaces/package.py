# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlTestCleannamespaces(PerlPackage):
    """This module lets you check your module's namespaces for imported
       functions you might have forgotten to remove"""

    homepage = "http://search.cpan.org/~ether/Test-CleanNamespaces-0.22/lib/Test/CleanNamespaces.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/Test-CleanNamespaces-0.22.tar.gz"

    version('0.22', '8c48bb0427f2077edce57c50491468ec')

    depends_on('perl-sub-exporter', type=('build', 'run'))
    depends_on('perl-module-runtime', type=('build', 'run'))
    depends_on('perl-test-needs', type=('build', 'run'))
    depends_on('perl-test-deep', type=('build', 'run'))
    depends_on('perl-test-warnings', type=('build', 'run'))
    depends_on('perl-file-pushd', type=('build', 'run'))
    depends_on('perl-package-stash', type=('build', 'run'))
    depends_on('perl-sub-identify', type=('build', 'run'))
    depends_on('perl-namespace-clean', type=('build', 'run'))
