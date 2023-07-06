# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlSubExporter(PerlPackage):
    """A sophisticated exporter for custom-built routines"""

    homepage = "https://metacpan.org/pod/Sub::Exporter"
    url = "http://search.cpan.org/CPAN/authors/id/R/RJ/RJBS/Sub-Exporter-0.987.tar.gz"

    version("0.989", sha256="334896e0af5e0643fc3799cbbcf01f933d4ca6324cd644c0b6660e71cdbd01c9")
    version("0.987", sha256="543cb2e803ab913d44272c7da6a70bb62c19e467f3b12aaac4c9523259b083d6")

    depends_on("perl-params-util", type=("build", "run"))
    depends_on("perl-data-optlist", type=("build", "run"))
