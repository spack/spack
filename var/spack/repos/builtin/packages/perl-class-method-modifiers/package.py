# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PerlClassMethodModifiers(PerlPackage):
    """Provides Moose-like method modifiers."""  # AUTO-CPAN2Spack

    homepage = "https://github.com/moose/Class-Method-Modifiers"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/E/ET/ETHER/Class-Method-Modifiers-2.13.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("2.15", sha256="65cd85bfe475d066e9186f7a8cc636070985b30b0ebb1cde8681cf062c2e15fc")
    version("2.13", sha256="ab5807f71018a842de6b7a4826d6c1f24b8d5b09fcce5005a3309cf6ea40fd63")
    version("2.12", sha256="e44c1073020bf55b8c97975ed77235fd7e2a6a56f29b5c702301721184e27ac8")

    depends_on("perl-exporter-tiny", type=("build", "run"))
    depends_on("perl-test-fatal", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-test-needs", type=("build", "test"))  # AUTO-CPAN2Spack
