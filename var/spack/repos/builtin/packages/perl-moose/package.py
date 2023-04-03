# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlMoose(PerlPackage):
    """A postmodern object system for Perl 5"""

    homepage = "https://metacpan.org/pod/Moose"
    url = "https://cpan.metacpan.org/authors/id/E/ET/ETHER/Moose-2.2006.tar.gz"

    version(
        "2.22.03",
        sha256="fa7814acf4073fa434c148d403cbbf8a7b62f73ad396fa8869f3036d6e3241a7",
        url="https://cpan.metacpan.org/authors/id/E/ET/ETHER/Moose-2.2203.tar.gz",
    )
    version(
        "2.22.01",
        sha256="cd5ff9b4751f73ecb6874ba9761343d35737d4ddf5ff6b19c00d01af5ffc3eb2",
        url="https://cpan.metacpan.org/authors/id/E/ET/ETHER/Moose-2.2201.tar.gz",
    )
    version(
        "2.22.00",
        sha256="1727c4fbc50045f0a7893ed71661d5f09a11b4e3a3c9c5690faf4bd36d7d7cea",
        url="https://cpan.metacpan.org/authors/id/E/ET/ETHER/Moose-2.2200.tar.gz",
    )
    version(
        "2.20.10",
        sha256="af0905b69f18c27de1177c9bc7778ee495d4ec91be1f223e8ca8333af4de08c5",
        url="https://cpan.metacpan.org/authors/id/E/ET/ETHER/Moose-2.2010.tar.gz",
    )
    version(
        "2.20.09",
        sha256="63ba8a5e27dbcbdbac2cd8f4162fff50a31e9829d8955a196a5898240c02d194",
        url="https://cpan.metacpan.org/authors/id/E/ET/ETHER/Moose-2.2009.tar.gz",
    )
    version(
        "2.20.07",
        sha256="bc75a320b55ba26ac9e60e11a77b3471066cb615bf7097537ed22e20df88afe8",
        url="https://cpan.metacpan.org/authors/id/E/ET/ETHER/Moose-2.2007.tar.gz",
    )
    version(
        "2.20.06",
        sha256="a4e00ab25cc41bebc5e7a11d71375fb5e64b56d5f91159afee225d698e06392b",
        url="https://cpan.metacpan.org/authors/id/E/ET/ETHER/Moose-2.2006.tar.gz",
    )

    depends_on("perl-cpan-meta-check", type=("build", "run"))
    depends_on("perl-test-cleannamespaces", type=("build", "run"))
    depends_on("perl-devel-overloadinfo", type=("build", "run"))
    depends_on("perl-class-load-xs", type=("build", "run"))
    depends_on("perl-devel-stacktrace", type=("build", "run"))
    depends_on("perl-eval-closure", type=("build", "run"))
    depends_on("perl-sub-name", type=("build", "run"))
    depends_on("perl-module-runtime-conflicts", type=("build", "run"))
    depends_on("perl-devel-globaldestruction", type=("build", "run"))
    depends_on("perl-package-deprecationmanager", type=("build", "run"))
    depends_on("perl-package-stash-xs", type=("build", "run"))
