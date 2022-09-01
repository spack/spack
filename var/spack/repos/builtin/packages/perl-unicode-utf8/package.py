# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlUnicodeUtf8(PerlPackage):
    """Encoding and decoding of UTF-8 encoding form."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/C/CH/CHANSEN"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/C/CH/CHANSEN/Unicode-UTF8-0.62.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("0.62", sha256="fa8722d0b74696e332fddd442994436ea93d3bfc7982d4babdcedfddd657d0f6")
    version("0.61", sha256="5ee155a8af856ac9b24819cf153592a13338651440478cb1dbf0e7f8e566676f")

    depends_on("perl-test-fatal@0.6:", type="build")  # AUTO-CPAN2Spack
    depends_on("perl@5.8.1:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker@6.59:", type="build")  # AUTO-CPAN2Spack

