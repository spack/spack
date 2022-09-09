# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlClassXsaccessor(PerlPackage):
    """Generate fast XS accessors without runtime compilation."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/S/SM/SMUELLER"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/S/SM/SMUELLER/Class-XSAccessor-1.19.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("1.19", sha256="99c56b395f1239af19901f2feeb125d9ecb4e351a0d80daa9529211a4700a6f2")
    version("1.18", sha256="0a3d25f5261f449e2e1711e53a659244cb314322d2d70abf37c81cd6d853c995")

    provides("perl-class-xsaccessor-array")  # AUTO-CPAN2Spack
    depends_on("perl@5.8:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-time-hires", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
