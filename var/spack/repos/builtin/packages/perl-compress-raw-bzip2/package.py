# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlCompressRawBzip2(PerlPackage):
    """A low-Level Interface to bzip2 compression library."""

    homepage = "https://metacpan.org/pod/Compress::Raw::Bzip2"
    url = "https://cpan.metacpan.org/authors/id/P/PM/PMQS/Compress-Raw-Bzip2-2.081.tar.gz"

    version("2.201", sha256="6204b270806d924e124e406faf6bbc715f7bb461dfdbea722042325633be300a")
    version("2.103", sha256="6172d16b0797b10a14e7e1e8dfddcd3d98910adcf5681285e716659f1197164d")
    version("2.101", sha256="0c9b134fd388290e30e90fc9f63900966127f98e76b054ecd481eb3b5500b8d8")
    version("2.100", sha256="2f1fe7ef2bf7cf87c8dbc82a605fd4a1411997858d802d0b1ead4745955cda04")
    version("2.096", sha256="a564e7634eca7740c5487d01effe1461e9e51b8909e69b3d8f5be98997958cbe")
    version("2.095", sha256="e57d582419029eb556d5ac99a536b22e6873ca325a27d73b8489755546a6e2d8")
    version("2.094", sha256="be38ba67001e914c5bf66d28be6c7cd85cf3ec0aadf171ec28eaa7ea3ac24cba")
    version("2.093", sha256="295683131efc16024033b4b0d37da8b39e92ed9a8b32458db04a75cfbfd266e9")
    version("2.092", sha256="0b6afc6d723edcee1ce4bf292c163a5cdc56fb737845121dcbba60b132acd1c2")
    version("2.091", sha256="27d7ef3d3b978ab19e20531256111bd847cb5015888d864293f9b269bde2b430")
    version("2.090", sha256="e6a28104f4b5689384e94f539af5e262e951eb310764858b511e4443a338297a")
    version("2.089", sha256="f208783323c21ea998a95c46e649ffda37db8435f524d29f84dc3459ba2880e7")
    version("2.088", sha256="83a787a491513233986faa66fe4e8b11ee9c65cdb6e9b29136dd6b781741bc7f")
    version("2.087", sha256="77bb0dfdda0475b9a2f5d463e4536a6f0ee480917b6743e72bfe31da8cf00cfb")
    version("2.086", sha256="46d3954a676d21cb10557dd3cc8140703b87bd8f14e49160120165586aa9f399")
    version("2.084", sha256="7d16debb73eb862c6a3c2ab4bcc31f165023ad4a0a257316227ba550a8ce924f")
    version("2.083", sha256="8def391d67f974a8ff53151972c34615febbcf873a9a5fb1a5b2969cd407bddf")
    version("2.081", sha256="8692b5c9db91954408e24e805fbfda222879da80d89d9410791421e3e5bc3520")

    depends_on("bzip2")
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
