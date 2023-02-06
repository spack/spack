# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PerlClassMethodModifiers(PerlPackage):
    """Class::Method::Modifiers - Provides Moose-like method modifiers"""

    homepage = "https://metacpan.org/pod/Class::Method::Modifiers"
    url = "https://cpan.metacpan.org/authors/id/E/ET/ETHER/Class-Method-Modifiers-2.13.tar.gz"

    version("2.13", sha256="ab5807f71018a842de6b7a4826d6c1f24b8d5b09fcce5005a3309cf6ea40fd63")

    depends_on("perl-carp", type=("build", "run"))
    depends_on("perl-exporter-tiny", type=("build", "run"))
