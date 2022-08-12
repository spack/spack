# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlHttpDaemon(PerlPackage):
    """A simple http server class"""

    homepage = "https://metacpan.org/pod/HTTP::Daemon"
    url = "http://search.cpan.org/CPAN/authors/id/O/OA/OALDERS/HTTP-Daemon-6.14.tar.gz"

    version("6.14", sha256="f0767e7f3cbb80b21313c761f07ad8ed253bce9fa2d0ba806b3fb72d309b2e1d")
    version("6.13", sha256="d184d1f3e51e690d60e4b00195aa69f679169c858f2aab419997c70892014516")
    version("6.12", sha256="df47bed10c38670c780fd0116867d5fd4693604acde31ba63380dce04c4e1fa6")

    depends_on("perl-lwp-mediatypes", type=("build", "run"))
    depends_on("perl-http-message", type=("build", "run"))
    depends_on("perl-http-date", type=("build", "run"))
    depends_on("perl-module-build-tiny", type="build")
