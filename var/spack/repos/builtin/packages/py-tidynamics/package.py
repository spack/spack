# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTidynamics(PythonPackage):
    """A tiny package to compute the dynamics of stochastic and molecular simulations."""

    homepage = "https://lab.pdebuyl.be/tidynamics/"
    pypi = "tidynamics/tidynamics-1.0.0.tar.gz"

    maintainers("RMeli")

    version("1.0.0", sha256="b7bd669d380b0f469f3a8aedfbc0e5fa967fe8dc44e196f54baf0edb59846976")

    depends_on("py-setuptools", type="build")

    depends_on("py-numpy", type=("build", "run"))
