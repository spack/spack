# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlTestWarnings(PerlPackage):
    """Test for warnings and the lack of them"""

    homepage = "http://deps.cpantesters.org/?module=Test%3A%3ACleanNamespaces;perl=latest"
    url      = "http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/Test-Warnings-0.026.tar.gz"

    version('0.026', '1a379f7eac4c89155d98e652459593a7')
