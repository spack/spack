# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlSubExporterProgressive(PerlPackage):
    """Progressive Sub::Exporter"""

    homepage = "https://metacpan.org/pod/Sub::Exporter::Progressive"
    url = "http://cpan.metacpan.org/authors/id/F/FR/FREW/Sub-Exporter-Progressive-0.001013.tar.gz"

    version("0.001.013", sha256="d535b7954d64da1ac1305b1fadf98202769e3599376854b2ced90c382beac056",
            url="http://cpan.metacpan.org/authors/id/F/FR/FREW/Sub-Exporter-Progressive-0.001013.tar.gz")
    version("0.001.012", sha256="b9e579b857d9bfd3b8391e4de6ee6529b4c6208c581c2a7cbf46a86618297cb8",
            url="http://cpan.metacpan.org/authors/id/F/FR/FREW/Sub-Exporter-Progressive-0.001012.tar.gz")

    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
