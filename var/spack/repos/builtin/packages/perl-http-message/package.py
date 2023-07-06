# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlHttpMessage(PerlPackage):
    """HTTP style message (base class)"""

    homepage = "https://metacpan.org/pod/HTTP::Message"
    url = "http://search.cpan.org/CPAN/authors/id/O/OA/OALDERS/HTTP-Message-6.13.tar.gz"

    version("6.44", sha256="398b647bf45aa972f432ec0111f6617742ba32fc773c6612d21f64ab4eacbca1")
    version("6.13", sha256="f25f38428de851e5661e72f124476494852eb30812358b07f1c3a289f6f5eded")

    depends_on("perl-lwp-mediatypes", type=("build", "run"))
    depends_on("perl-encode-locale", type=("build", "run"))
    depends_on("perl-io-html", type=("build", "run"))
    depends_on("perl-try-tiny", type=("build", "run"))
    depends_on("perl-uri", type=("build", "run"))
    depends_on("perl-http-date", type=("build", "run"))
