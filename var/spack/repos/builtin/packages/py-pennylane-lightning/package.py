# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPennylaneLightning(PythonPackage):
    """PennyLane-Lightning plugin"""

    homepage = "https://github.com/PennyLaneAI/pennylane-lightning"
    url = "https://github.com/PennyLaneAI/pennylane-lightning/archive/refs/tags/v0.28.0.tar.gz"
    # using github for now, because pypi tarball is missing the CMakeLists.txt file
    # pypi = "PennyLane-Lightning/PennyLane-Lightning-0.28.0.tar.gz"

    version("0.28.0", sha256="f5849c2affb5fb57aca20feb40ca829d171b07db2304fde0a37c2332c5b09e18")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("cmake@3.16:", type="build")

    depends_on("py-ninja", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    # depends_on("py-pennylane@0.19:", type=("build", "run"))  # circular dependency
