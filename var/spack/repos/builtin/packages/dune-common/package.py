# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class DuneCommon(PythonPackage):
    """DUNE, the Distributed and Unified Numerics Environment is a modular toolbox for solving partial differential equations (PDEs) with grid-based methods. 
    It supports the easy implementation of methods like Finite Elements (FE), Finite Volumes (FV), and also Finite Differences (FD)."""

    homepage = "https://www.dune-project.org/doc/gettingstarted/"
    git="https://gitlab.dune-project.org/core/dune-common"
    pypi = "dune-common/dune-common-2.9.0.tar.gz"

    version("2.9.0", sha256="785415bbd27ff9de5d22c63e9ea87773ec6cddaa")

    depends_on("cmake@3.13.0:", type="build")
    depends_on("mpi@2:")
    depends_on("pkgconf", type="build")