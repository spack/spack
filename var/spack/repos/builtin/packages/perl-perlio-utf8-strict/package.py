# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPerlioUtf8Strict(PerlPackage):
    """This module provides a fast and correct UTF-8 PerlIO layer."""

    homepage = "https://metacpan.org/pod/PerlIO::utf8_strict"
    url = "http://search.cpan.org/CPAN/authors/id/L/LE/LEONT/PerlIO-utf8_strict-0.002.tar.gz"

    version("0.009", sha256="ba82cf144820655d6d4836d12dde65f8895a3d905aeb4aa0b421249f43284c14")
    version("0.002", sha256="6e3163f8a2f1d276c975f21789d7a07843586d69e3e6156ffb67ef6680ceb75f")

    depends_on("perl-module-build", type="build")
