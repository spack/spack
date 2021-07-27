# Copyright 2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlExporterLite(PerlPackage):
    homepage = "https://metacpan.org/pod/Exporter::Lite"
    url      = "https://cpan.metacpan.org/authors/id/N/NE/NEILB/Exporter-Lite-0.08.tar.gz"

    version('0.08', sha256='c05b3909af4cb86f36495e94a599d23ebab42be7a18efd0d141fc1586309dac2')
