# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTimeHires(PerlPackage):
    """High resolution alarm, sleep, gettimeofday, interval timers"""

    homepage = "https://metacpan.org/pod/Time::HiRes"
    url = "https://cpan.metacpan.org/authors/id/A/AT/ATOOMIC/Time-HiRes-1.9764.tar.gz"

    version("1.97.64_02", sha256="35ac3997940503459863a0e3007c3345c5e7b5fda822814e0c42e6b3f4661ef3",
            url="https://cpan.metacpan.org/authors/id/A/AT/ATOOMIC/Time-HiRes-1.9764_02.tar.gz")
    version("1.97.64_01", sha256="1d0a95b23fa216e38594aa08cb5d8408ecc6be0cbc46a5bef07e5667a59eaf8c",
            url="https://cpan.metacpan.org/authors/id/A/AT/ATOOMIC/Time-HiRes-1.9764_01.tar.gz")
    version("1.97.64", sha256="9841be5587bfb7cd1f2fe267b5e5ac04ce25e79d5cc77e5ef9a9c5abd101d7b1",
            url="https://cpan.metacpan.org/authors/id/A/AT/ATOOMIC/Time-HiRes-1.9764.tar.gz")
    version("1.97.60", sha256="2cb898bff42bc10024e0a3252c79e13a2eb7a8a5fb3367bb60583b576a11702b",
            url="https://cpan.metacpan.org/authors/id/A/AT/ATOOMIC/Time-HiRes-1.9760.tar.gz")
    version("1.97.58", sha256="5bfa145bc11e70a8e337543b1084a293743a690691b568493455dedf58f34b1e",
            url="https://cpan.metacpan.org/authors/id/J/JH/JHI/Time-HiRes-1.9758.tar.gz")
    version("1.97.57", sha256="3cda1cf9c0eadc15bdd6d38592164891f6d44c3e264efdba790b11695adf42a4",
            url="https://cpan.metacpan.org/authors/id/J/JH/JHI/Time-HiRes-1.9757.tar.gz")
    version("1.97.56", sha256="aeeebe9898b394dda0e34424993a06034d22d2717bad7033959fa32901063c22",
            url="https://cpan.metacpan.org/authors/id/J/JH/JHI/Time-HiRes-1.9756.tar.gz")
    version("1.97.55", sha256="0c534d62f08bb8543d1b77a7346d786c45da92e8b783cf19d73f683bfab7855f",
            url="https://cpan.metacpan.org/authors/id/J/JH/JHI/Time-HiRes-1.9755.tar.gz")
    version("1.97.54", sha256="6654c007b2d597f863a0bb2ed69c639f0d552f598e35cf474fc6e89b9225b063",
            url="https://cpan.metacpan.org/authors/id/J/JH/JHI/Time-HiRes-1.9754.tar.gz")
    version("1.97.53", sha256="0fbfd5f99cdd26011d5c0bc3a8e369dacc4a9e1d1658f4663ac6018f2cec4915",
            url="https://cpan.metacpan.org/authors/id/J/JH/JHI/Time-HiRes-1.9753.tar.gz")
    version("1.97.52", sha256="a72744abd686cdbd4717ccd7dae68467a0c1548202a8d35096e7394cb24e515d",
            url="https://cpan.metacpan.org/authors/id/J/JH/JHI/Time-HiRes-1.9752.tar.gz")
    version("1.97.51", sha256="004f247c4952b09ce92800c9ab6974aa202f779c1b2ed5791dd64216afd98b7c",
            url="https://cpan.metacpan.org/authors/id/J/JH/JHI/Time-HiRes-1.9751.tar.gz")
    version("1.97.50", sha256="15e734495bdca9ead6ded4ad28d289392476dc0c5da050816c2aafb06b9df82f",
            url="https://cpan.metacpan.org/authors/id/J/JH/JHI/Time-HiRes-1.9750.tar.gz")
    version("1.97.49", sha256="9550211980fb592bbbebe188190d888686661497c940a077e31acc4a580c4514",
            url="https://cpan.metacpan.org/authors/id/J/JH/JHI/Time-HiRes-1.9749.tar.gz")
    version("1.97.46", sha256="89408c81bb827bc908c98eec50071e6e1158f38fa462865ecc3dc03aebf5f596",
            url="https://cpan.metacpan.org/authors/id/J/JH/JHI/Time-HiRes-1.9746.tar.gz")
    depends_on("perl@5.6:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type=("build", "run"))  # AUTO-CPAN2Spack
