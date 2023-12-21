# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlSpecio(PerlPackage):
    """Type constraints and coercions for Perl ."""

    homepage = "https://metacpan.org/dist/Specio"
    url = "http://search.cpan.org/CPAN/authors/id/D/DR/DROLSKY/Specio-0.48.tar.gz"

    version("0.48", sha256="0c85793580f1274ef08173079131d101f77b22accea7afa8255202f0811682b2")
