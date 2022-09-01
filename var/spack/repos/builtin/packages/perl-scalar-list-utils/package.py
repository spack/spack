# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlScalarListUtils(PerlPackage):
    """Scalar::Util - A selection of general-utility scalar subroutines"""

    homepage = "https://metacpan.org/pod/Scalar::Util"
    url = "https://cpan.metacpan.org/authors/id/P/PE/PEVANS/Scalar-List-Utils-1.50.tar.gz"

    version("1.63", sha256="cafbdf212f6827dc9a0dd3b57b6ee50e860586d7198228a33262d55c559eb2a9")
    version("1.62", sha256="7279c4ec7df0cf2c0acb874abdfe86956f5028d2414974db56edfbed8a4d339f")
    version("1.61", sha256="96e0c3cd9529b7a297c3a4eed97d1c88edf2a0a3b3a19fa2ae9fac729906044f")
    version("1.60", sha256="c685bad8021f008f321288b7c3182ec724ab198a77610e877c86f3fad4b85f07")
    version("1.59", sha256="7a5a66d14e3790e4532347bfdd7c46ec6db3363b15c4bcc5c2f9d83c81ef1b0f")
    version("1.58", sha256="7cdfbfc03c65c0c75f298272e273973e589ef45c4f151d553bd57712393ab2bf")
    version("1.57", sha256="c895ce17d9ba5198abf8f6bf7622cd20505b12002e73512c442f5295007a5b3c")
    version("1.56", sha256="15b8537d40fb3e6dae64b2e7e983c47a99b2c20816a180bb9c868b787a12ab5b")
    version("1.55", sha256="4d2bdc1c72a7bc4d69d6a5cc85bc7566497c3b183c6175b832784329d58feb4b")
    version("1.54", sha256="a6eda0eb8fd69890c2369ad12c1fd1b8aab5b38793cac3688d7fc402c630bf79")
    version("1.53", sha256="bd4086b066fb3b18a0be2e7d9bc100a99aa0f233ad659492340415c7b2bdae99")
    version("1.52_001", sha256="2cdcbd0d3fb7ba98a0c59fb4dca77bc74370a072a0857776ba2396cc4f765123")
    version("1.52", sha256="279d78cef84acae280da4dfb95eff0c9865d1611b1a3b026baddf42d1ba01de4")
    version("1.51", sha256="d9c8eab1ac5a6fc75a7e836304626e2cb7b13cf8c9b10d491a144e1ef6760a76")
    version("1.50", sha256="06aab9c693380190e53be09be7daed20c5d6278f71956989c24cca7782013675")
    provides("perl-list-util")  # AUTO-CPAN2Spack
    provides("perl-list-util-xs")  # AUTO-CPAN2Spack
    provides("perl-scalar-util")  # AUTO-CPAN2Spack
    provides("perl-sub-util")  # AUTO-CPAN2Spack
    depends_on("perl@5.6:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
