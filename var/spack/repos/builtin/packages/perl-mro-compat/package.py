# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlMroCompat(PerlPackage):
    """Provides several utilities for dealing with method resolution order."""

    homepage = "https://metacpan.org/pod/MRO::Compat"
    url = "https://cpan.metacpan.org/authors/id/H/HA/HAARG/MRO-Compat-0.14_01.tar.gz"

    version("0.15", sha256="0d4535f88e43babd84ab604866215fc4d04398bd4db7b21852d4a31b1c15ef61")
    version("0.14_01", sha256="bc214d7964bc72f5a4015cc6b0d27376071cb64bd955280fea40c046b64d911a")
    version("0.13", sha256="8a2c3b6ccc19328d5579d02a7d91285e2afd85d801f49d423a8eb16f323da4f8")
    depends_on("perl@5.6:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
