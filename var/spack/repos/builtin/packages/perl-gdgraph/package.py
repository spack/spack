# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlGdgraph(PerlPackage):
    """Graph Plotting Module for Perl 5"""

    homepage = "https://metacpan.org/pod/GD::Graph"
    url = "https://cpan.metacpan.org/authors/id/B/BW/BWARFIELD/GDGraph-1.44_01.tar.gz"

    version("1.44_01", sha256="52ca97d03bdcf4b3639fd465a1df51a5e22f72673d27a9ab4e53106320966ef4")
    version("1.44", sha256="1a6aa4023771d5a19f5d0943ccdc37d8b3b7f5883cad1f804d35633fbba5056e")
    version(
        "1.43.08",
        sha256="75b3c7e280431404ed096c6e120d552cc39052a8610787149515e94b9ba237cb",
        url="https://cpan.metacpan.org/authors/id/B/BW/BWARFIELD/GDGraph-1.4308.tar.gz",
    )

    depends_on("perl-capture-tiny", type=("build", "run"))
    depends_on("perl-test-exception", type=("build", "run"))
    depends_on("perl-gdtextutil", type=("build", "run"))
    depends_on("perl-gd", type=("build", "run"))
