# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRncl(RPackage):
    """An Interface to the Nexus Class Library.

    An interface to the Nexus Class Library which allows parsing of NEXUS,
    Newick and other phylogenetic tree file formats. It provides elements of
    the file that can be used to build phylogenetic objects such as ape's
    'phylo' or phylobase's 'phylo4(d)'. This functionality is demonstrated with
    'read_newick_phylo()' and 'read_nexus_phylo()'."""

    cran = "rncl"

    version("0.8.6", sha256="fcc972c04fb43ace0876eb640a6433caddf6ec8304f7ceee37107d812ce68ffb")
    version("0.8.4", sha256="6b19d0dd9bb08ecf99766be5ad684bcd1894d1cd9291230bdd709dbd3396496b")

    depends_on("r@3.1.1:", type=("build", "run"))
    depends_on("r-rcpp@0.11.0:", type=("build", "run"))
    depends_on("r-progress@1.1.2:", type=("build", "run"))
