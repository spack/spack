# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
# Copyright 2023 EMBL-European Bioinformatics Institute
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Kyotocabinet(AutotoolsPackage):
    """Kyoto Cabinet is a library of routines for managing a database."""

    homepage = "https://dbmx.net/kyotocabinet/"
    url = "https://dbmx.net/kyotocabinet/pkg/kyotocabinet-1.2.80.tar.gz"

    maintainers("EbiArnie")

    version("1.2.80", sha256="4c85d736668d82920bfdbdb92ac3d66b7db1108f09581a769dd9160a02def349")

    depends_on("zlib@1.2.3:", type=("build", "link"))
