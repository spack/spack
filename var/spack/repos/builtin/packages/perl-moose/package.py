# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlMoose(PerlPackage):
    """A postmodern object system for Perl 5"""

    homepage = "https://metacpan.org/pod/Moose"
    url = "https://cpan.metacpan.org/authors/id/E/ET/ETHER/Moose-2.2006.tar.gz"

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
