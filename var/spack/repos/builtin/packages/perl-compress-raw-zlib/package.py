# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlCompressRawZlib(PerlPackage):
    """A low-Level Interface to zlib compression library."""

    homepage = "https://metacpan.org/pod/Compress::Raw::Zlib"
    url = "https://cpan.metacpan.org/authors/id/P/PM/PMQS/Compress-Raw-Zlib-2.081.tar.gz"

    version("2.202", sha256="96e20946eb457a32d2d7a0050b922e37b5ada41246bcdc824196d3f7c4da91b7")
    version("2.081", sha256="e156de345bd224bbdabfcab0eeb3f678a3099a4e86c9d1b6771d880b55aa3a1b")

    depends_on("zlib")
    depends_on("perl-extutils-makemaker", type="build")
