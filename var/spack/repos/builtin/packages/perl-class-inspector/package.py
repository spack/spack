# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlClassInspector(PerlPackage):
    """Get information about a class and its structure"""

    homepage = "https://metacpan.org/pod/Class::Inspector"
    url = "https://cpan.metacpan.org/authors/id/P/PL/PLICEASE/Class-Inspector-1.32.tar.gz"

    version("1.36", sha256="cc295d23a472687c24489d58226ead23b9fdc2588e522f0b5f0747741700694e")
    version("1.35_01", sha256="6b3442d5eac6853539c106f05987a7cf4c2fe64be16d71c25e301b8bb53bfbce")
    version("1.34", sha256="fe9a86dcb3ccc7a99d6865e6b674a14d20164f76bd84f2eb43aafcc6bf1cf0d8")
    version("1.33_01", sha256="0ed625d71c3ab9b90a4280678402296143740d9f0db93a7c285f1d2ed26594bc")
    version("1.32", sha256="cefadc8b5338e43e570bc43f583e7c98d535c17b196bcf9084bb41d561cc0535")
    provides("perl-class-inspector-functions")  # AUTO-CPAN2Spack
    depends_on("perl@5.8:", type=("build", "run", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
