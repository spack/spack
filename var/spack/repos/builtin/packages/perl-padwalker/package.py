# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPadwalker(PerlPackage):
    """play with other peoples' lexical variables"""

    homepage = "https://metacpan.org/pod/PadWalker"
    url = "https://cpan.metacpan.org/authors/id/R/RO/ROBIN/PadWalker-2.2.tar.gz"

    version("2.5", sha256="07b26abb841146af32072a8d68cb90176ffb176fd9268e6f2f7d106f817a0cd0")
    version("2.4", sha256="ff7e285aecffa3c52ed5c996d070207b649aba38aae8615e5ffaa3b97fd787ec")
    version("2.3", sha256="2a6c44fb600861e54568e74081a8d1f121f0060076069ceab34b1ae89d6588cf")
    version("2.2", sha256="fc1df2084522e29e892da393f3719d2c1be0da022fdd89cff4b814167aecfea3")
    depends_on("perl@5.8.1:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
