# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNodeenv(PythonPackage):
    """Node.js virtual environment"""

    homepage = "https://github.com/ekalinin/nodeenv"
    pypi = "nodeenv/nodeenv-1.3.3.tar.gz"

    version("1.7.0", sha256="e0e7f7dfb85fc5394c6fe1e8fa98131a2473e04311a45afb6508f7cf1836fa2b")
    version("1.3.3", sha256="ad8259494cf1c9034539f6cced78a1da4840a4b157e23640bc4a0c0546b0cb7a")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools", when="@1.7:", type=("build", "run"))
