# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTextTabsPluswrap(PerlPackage):
    """Expand tabs and do simple line wrapping."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/A/AR/ARISTOTLE"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/A/AR/ARISTOTLE/Text-Tabs+Wrap-2021.0814.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("2021.0814", sha256="30bbea13a5f5ef446b676b4493644df0ea19fc6a70ff649a8beb64571dbf6dfa")

    provides("perl-text-tabs")  # AUTO-CPAN2Spack
    provides("perl-text-wrap")  # AUTO-CPAN2Spack
    depends_on("perl@5.6:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack

