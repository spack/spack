# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDevelSymdump(PerlPackage):
    """Devel::Symdump - dump symbol names or the symbol table"""

    homepage = "https://metacpan.org/pod/Devel::Symdump"
    url = "https://cpan.metacpan.org/authors/id/A/AN/ANDK/Devel-Symdump-2.0604.tar.gz"

    version("2.18", sha256="826f81a107f5592a2516766ed43beb47e10cc83edc9ea48090b02a36040776c0")
    version("2.17", sha256="2c50fc7935e6e6200b74fbb9149c8078ee8f92788d2a9c5ab25c9ebace946e62")
    version("2.16", sha256="77426d523f38f93bcbf4d8ce9dd6f43fda879219a981722bacb22fb77b7f4073")
    version("2.15", sha256="76c2a90d31318204ecf1977f0217ce57b142e6681fe2b99fb8789efc5dd86f41")
    version("2.14", sha256="9b14fb22760e8f1292fdc52932b8dcc6abbd95a29f88d2e4faaf7add5ff71ede")
    version("2.12", sha256="9949c44f7646d380e71744f6d12291de29b0f468fe96e8e1614feb913054073d")
    version("2.11", sha256="11950100bcad29a833545da407d3bf2d5e349259c6171f22a6e5569d1117b544")
    version("2.10", sha256="6b362910e8e8f6cd4d0c45550c21842875a6addaec642b7cb172fd0340859b0d")
    version("2.08_53", sha256="32fbed9ae43af99d5f998cbe279b0ed5707e04fd50cd1184f548b062185dc502")
    version("2.08_51", sha256="5f496f952548402c9c90aa69d2ce79b6593f6f6b2544a253af53c924cca90376")
    version("2.08", sha256="a50353a31259b6e61d83cfbdca3ab999b5db74e1009ec3259ad7fbc03f32f263")
    version("2.07", sha256="f96f3137c36af1ea6b55f698a4850c0c9793ea4d4ab85bd04aa850153a5750e9")
    version("2.06.04", sha256="1f9eaa557733f775ccaa852e846566274c017e6fee380aeb8d08e425cfa86d3e",
            url="https://cpan.metacpan.org/authors/id/A/AN/ANDK/Devel-Symdump-2.0604.tar.gz")
    provides("perl-devel-symdump-export")  # AUTO-CPAN2Spack
    depends_on("perl@5.4:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-compress-zlib", type="run")  # AUTO-CPAN2Spack
