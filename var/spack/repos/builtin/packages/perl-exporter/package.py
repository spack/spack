# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlExporter(PerlPackage):
    """Exporter - Implements default import method for modules."""

    homepage = "https://metacpan.org/pod/Exporter"
    url = "https://cpan.metacpan.org/authors/id/T/TO/TODDR/Exporter-5.77.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("5.77", sha256="3892ee5c6ae6e482068d53b61e25cae4fc71ddc79cc47446e385df0a669bb8ed")

    depends_on("perl-extutils-makemaker", type="build")
    depends_on("perl-carp")
