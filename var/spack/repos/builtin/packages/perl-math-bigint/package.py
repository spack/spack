# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlMathBigint(PerlPackage):
    """Math::BigInt - arbitrary size integer math package"""

    homepage = "https://metacpan.org/pod/Math::BigInt"
    url = "https://cpan.metacpan.org/authors/id/P/PJ/PJACKLAM/Math-BigInt-1.999837.tar.gz"

    version("1.999837", sha256="038f9aad6318f20a84a7b1afe3087a1b02406c9988ce5919311a797f85a32962")
