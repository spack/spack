# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlHttpMessage(PerlPackage):
    """HTTP style message (base class)"""

    homepage = "https://metacpan.org/pod/HTTP::Message"
    url = "https://cpan.metacpan.org/authors/id/O/OA/OALDERS/HTTP-Message-6.13.tar.gz"

    version("6.37", sha256="0e59da0a85e248831327ebfba66796314cb69f1bfeeff7a9da44ad766d07d802")
    version("6.36", sha256="576a53b486af87db56261a36099776370c06f0087d179fc8c7bb803b48cddd76")
    version("6.35", sha256="d77c3a64c2991c58e0694564fea7ed3610ae1790fa9eb32b51972b0a62bc6619")
    version("6.34", sha256="fe7ebb9e67899d12cd45487581ce4dcb33e491d30342ecb59d047770fa967634")
    version("6.33", sha256="23b967f71b852cb209ec92a1af6bac89a141dff1650d69824d29a345c1eceef7")
    version("6.32", sha256="ac32960ce01a3ae4a950666736f2bd633fb694c60ad545adaad9cb5fe5c12278")
    version("6.31", sha256="f1a06a3d15a27ffab06ff6d495b37af94f6c21d0be5e11b7ba179174ac0069da")
    version("6.30", sha256="9dac0811d3de178a429d4df3f68d2632e189a548b57cbf8cf763ec62cd8e20d8")
    version("6.29", sha256="f4417970679e08f6deb0609009aa9515dee0c8d91dbadd6b86a26e2b8e0d6341")
    version("6.28", sha256="04e3168f9576b48d45124ac681a574408ebb6fa8eb2dba6d3fe70c8f6704dbb8")
    version("6.27", sha256="0be0f720fbbbdbae8711f6eec9b2f0d34bd5ed5046fc66b80dc3b42017c1e699")
    version("6.26", sha256="6ce6c359de75c3bb86696a390189b485ec93e3ffc55326b6d044fa900f1725e1")
    version("6.24", sha256="554a1acf2daa401091f7012f5cb82d04d281db43fbd8f39a1fcbb7ed56dde16d")
    version("6.22", sha256="970efd151b81c95831d2a5f9e117f8032b63a1768cd2cd3f092ad634c85175c3")
    version("6.18", sha256="d060d170d388b694c58c14f4d13ed908a2807f0e581146cef45726641d809112")
    version("6.17", sha256="b0ba6cadff95367dfc97eaf63eea95cd795eeacf61f7bcdfa169127e015c6984")
    version("6.16", sha256="46790ae127946d5cfea5a1e05c1b9f4a045a7c5094fe81f086bbf3341290ebd0")
    version("6.15", sha256="7b244a193b6ffb9728a4cb25a09bc7c938956baa2ee1983ee2cbc4ed75dccb85")
    version("6.14", sha256="71aab9f10eb4b8ec6e8e3a85fc5acb46ba04db1c93eb99613b184078c5cf2ac9")
    version("6.13", sha256="f25f38428de851e5661e72f124476494852eb30812358b07f1c3a289f6f5eded")

    provides("perl-http-config")  # AUTO-CPAN2Spack
    provides("perl-http-headers")  # AUTO-CPAN2Spack
    provides("perl-http-headers-auth")  # AUTO-CPAN2Spack
    provides("perl-http-headers-etag")  # AUTO-CPAN2Spack
    provides("perl-http-headers-util")  # AUTO-CPAN2Spack
    provides("perl-http-request")  # AUTO-CPAN2Spack
    provides("perl-http-request-common")  # AUTO-CPAN2Spack
    provides("perl-http-response")  # AUTO-CPAN2Spack
    provides("perl-http-status")  # AUTO-CPAN2Spack
    depends_on("perl-io-uncompress-gunzip", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-time-local", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-encode-locale@1:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-io-compress-gzip", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-io-html", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on(
        "perl-io-uncompress-brotli@0.4.1:", type=("build", "run", "test")
    )  # AUTO-CPAN2Spack
    depends_on("perl-test-needs", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-io-compress-deflate", type="run")  # AUTO-CPAN2Spack
    depends_on("perl@5.8.1:", type=("run", "test"))  # AUTO-CPAN2Spack
    depends_on("perl@5.6:", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-io-uncompress-inflate", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-uri@1.10:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-io-uncompress-bunzip2@2.21:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-uri-url", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-io-compress-bzip2@2.21:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-http-date@6:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-lwp-mediatypes@6:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-io-compress-brotli@0.4.1:", type=("build", "run", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-io-uncompress-rawinflate", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-compress-raw-zlib", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-try-tiny", type=("build", "test"))  # AUTO-CPAN2Spack
