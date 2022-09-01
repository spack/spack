# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPodParser(PerlPackage):
    """Modules for parsing/translating POD format documents."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/M/MA/MAREKR"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/M/MA/MAREKR/Pod-Parser-1.65.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("1.65", sha256="3ba7bdec659416a51fe2a7e59f0883e9c6a3b21bc9d001042c1d6a32d401b28a")
    version("1.64", sha256="02f6649faa46ef8967743b0f5e50b8330bb3f0244da7a0bb40c96a1a44d6661d")

    provides("perl-pod-cache")  # AUTO-CPAN2Spack
    provides("perl-pod-cache-item")  # AUTO-CPAN2Spack
    provides("perl-pod-find")  # AUTO-CPAN2Spack
    provides("perl-pod-hyperlink")  # AUTO-CPAN2Spack
    provides("perl-pod-inputobjects")  # AUTO-CPAN2Spack
    provides("perl-pod-inputsource")  # AUTO-CPAN2Spack
    provides("perl-pod-interiorsequence")  # AUTO-CPAN2Spack
    provides("perl-pod-list")  # AUTO-CPAN2Spack
    provides("perl-pod-paragraph")  # AUTO-CPAN2Spack
    provides("perl-pod-parsetree")  # AUTO-CPAN2Spack
    provides("perl-pod-parseutils")  # AUTO-CPAN2Spack
    provides("perl-pod-plaintext@2.07")  # AUTO-CPAN2Spack
    provides("perl-pod-select")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack

