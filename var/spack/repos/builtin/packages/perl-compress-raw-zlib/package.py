# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlCompressRawZlib(PerlPackage):
    """A low-Level Interface to zlib compression library."""

    homepage = "https://metacpan.org/pod/Compress::Raw::Zlib"
    url = "https://cpan.metacpan.org/authors/id/P/PM/PMQS/Compress-Raw-Zlib-2.081.tar.gz"

    version("2.204", sha256="f161f4297efadbed79c8b096a75951784fc5ccd3170bd32866a19e5c6876d13f")
    version("2.081", sha256="e156de345bd224bbdabfcab0eeb3f678a3099a4e86c9d1b6771d880b55aa3a1b")

    depends_on("zlib-api")
    depends_on("perl-extutils-makemaker", type="build")
