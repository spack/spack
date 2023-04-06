# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlIoCompressBrotli(PerlPackage):
    """Read/write Brotli buffers/streams."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/M/MG/MGV"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/M/MG/MGV/IO-Compress-Brotli-0.004001.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("0.004_002", sha256="2a85869eb41045dbd5318f56f470d0931235efa19d5b7c253c7d145a70381ec0")
    version(
        "0.004.001",
        sha256="8ba5c0167e966f487bde159c18bc1b3486528013b3235d39f2fcb375ca4bf410",
        url="https://cpan.metacpan.org/authors/id/M/MG/MGV/IO-Compress-Brotli-0.004001.tar.gz",
    )

    provides("perl-io-uncompress-brotli")  # AUTO-CPAN2Spack
    depends_on("perl@5.14.0:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-time-hires", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-file-slurper", type="run")  # AUTO-CPAN2Spack
