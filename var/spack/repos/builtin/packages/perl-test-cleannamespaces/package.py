# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlTestCleannamespaces(PerlPackage):
    """This module lets you check your module's namespaces for imported
       functions you might have forgotten to remove"""

    homepage = "http://search.cpan.org/~ether/Test-CleanNamespaces-0.22/lib/Test/CleanNamespaces.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/Test-CleanNamespaces-0.22.tar.gz"

    version('0.031', sha256='c087dcf3f6bedf22f6a5e7caa1a0ee88ab15c5a91b7658ae60c5d0be2ccf0e94')
    version('0.24',  sha256='338d5569e8e89a654935f843ec0bc84aaa486fe8dd1898fb9cab3eccecd5327a')
    version('0.23',  sha256='c7bf97f3c786b75f84341135904b492a1a36646aa65db3e0fd15a3cbe0864872')
    version('0.22', sha256='862a221994dd413b2f350450f22c96f57cac78784b1aca1a8fc763fc5449aaca')

    depends_on('perl-sub-exporter', type=('build', 'run'))
    depends_on('perl-module-runtime', type=('build', 'run'))
    depends_on('perl-test-needs', type=('build', 'run'))
    depends_on('perl-test-deep', type=('build', 'run'))
    depends_on('perl-test-warnings', type=('build', 'run'))
    depends_on('perl-file-pushd', type=('build', 'run'))
    depends_on('perl-package-stash', type=('build', 'run'))
    depends_on('perl-sub-identify', type=('build', 'run'))
    depends_on('perl-namespace-clean', type=('build', 'run'))
