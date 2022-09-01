# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestObject(PerlPackage):
    """Thoroughly testing objects via registered handlers."""  # AUTO-CPAN2Spack

    homepage = "https://github.com/karenetheridge/Test-Object"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/E/ET/ETHER/Test-Object-0.08.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("0.08", sha256="65278964147837313f4108e55b59676e8a364d6edf01b3dc198aee894ab1d0bb")

    provides("perl-test-object-test")  # AUTO-CPAN2Spack
    depends_on("perl@5.6:", type=("build", "run", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-scalar-util@1.16:", type="run")  # AUTO-CPAN2Spack

