# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class RBiocmanager(RPackage):
    """Access the Bioconductor Project Package Repository.

    A convenient tool to install and update Bioconductor packages."""

    cran = "BiocManager"

    version('1.30.16', sha256='75a754a55192ef6aa6ac9b054fd5381ff03fe6bb8b2e033eb8143da930ef3855')
    version('1.30.10', sha256='f3b7a412b42be0ab8df5fcd9bf981876ba9e5c55bc5faaca7af7ede3b6d0c90e')
