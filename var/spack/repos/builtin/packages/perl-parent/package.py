# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlParent(PerlPackage):
    """Establish an ISA relationship with base classes at compile time."""

    homepage = "https://metacpan.org/pod/parent"
    url = "https://cpan.metacpan.org/authors/id/C/CO/CORION/parent-0.241.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.241", sha256="b10b3960ab3997dab7571ffe975ba462d979d086450740a1e08b3959e75128fe")

    depends_on("perl-extutils-makemaker", type="build")
