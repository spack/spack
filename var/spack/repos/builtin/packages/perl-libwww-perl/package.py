# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlLibwwwPerl(PerlPackage):
    """The libwww-perl collection is a set of Perl modules which provides
    a simple and consistent application programming interface to the
    World-Wide Web. The main focus of the library is to provide classes and
    functions that allow you to write WWW clients."""

    homepage = "https://github.com/libwww-perl/libwww-perl"
    url = "https://cpan.metacpan.org/authors/id/O/OA/OALDERS/libwww-perl-6.33.tar.gz"

    version("6.67", sha256="96eec40a3fd0aa1bd834117be5eb21c438f73094d861a1a7e5774f0b1226b723")
    version("6.33", sha256="97417386f11f007ae129fe155b82fd8969473ce396a971a664c8ae6850c69b99")
    version("6.29", sha256="4c6f2697999d2d0e6436b584116b12b30dc39990ec0622751c1a6cec2c0e6662")

    provides("perl-lwp")  # AUTO-CPAN2Spack
    provides("perl-lwp-authen-basic")  # AUTO-CPAN2Spack
    provides("perl-lwp-authen-digest")  # AUTO-CPAN2Spack
    provides("perl-lwp-authen-ntlm")  # AUTO-CPAN2Spack
    provides("perl-lwp-conncache")  # AUTO-CPAN2Spack
    provides("perl-lwp-debug")  # AUTO-CPAN2Spack
    provides("perl-lwp-debug-tracehttp")  # AUTO-CPAN2Spack
    provides("perl-lwp-debugfile")  # AUTO-CPAN2Spack
    provides("perl-lwp-membermixin")  # AUTO-CPAN2Spack
    provides("perl-lwp-protocol")  # AUTO-CPAN2Spack
    provides("perl-lwp-protocol-cpan")  # AUTO-CPAN2Spack
    provides("perl-lwp-protocol-data")  # AUTO-CPAN2Spack
    provides("perl-lwp-protocol-file")  # AUTO-CPAN2Spack
    provides("perl-lwp-protocol-ftp")  # AUTO-CPAN2Spack
    provides("perl-lwp-protocol-gopher")  # AUTO-CPAN2Spack
    provides("perl-lwp-protocol-http")  # AUTO-CPAN2Spack
    provides("perl-lwp-protocol-loopback")  # AUTO-CPAN2Spack
    provides("perl-lwp-protocol-mailto")  # AUTO-CPAN2Spack
    provides("perl-lwp-protocol-nntp")  # AUTO-CPAN2Spack
    provides("perl-lwp-protocol-nogo")  # AUTO-CPAN2Spack
    provides("perl-lwp-robotua")  # AUTO-CPAN2Spack
    provides("perl-lwp-simple")  # AUTO-CPAN2Spack
    provides("perl-lwp-useragent")  # AUTO-CPAN2Spack
    depends_on("perl-encode-locale", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-http-cookies@6:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-http-response@6:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-uri-escape", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-digest-md5", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-scalar-util", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-www-robotrules@6:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-test-requiresinternet", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-file-listing@6:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-html-entities", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-http-negotiate@6:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-http-daemon@6.12:", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-http-status@6.7:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-test-needs", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-net-http@6.18:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl@5.8.1:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-test-fatal", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-uri@1.10:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-http-request-common@6:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-test-leaktrace", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-http-date@6:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-http-request@6:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-html-headparser", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-lwp-mediatypes@6:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-try-tiny", type="run")  # AUTO-CPAN2Spack
