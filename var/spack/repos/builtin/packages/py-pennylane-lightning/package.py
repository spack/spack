# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPennylaneLightning(PythonPackage):
    """PennyLane-Lightning plugin"""

    homepage = "https://github.com/PennyLaneAI/pennylane-lightning"
    pypi = "PennyLane-Lightning/PennyLane-Lightning-0.28.0.tar.gz"

    version("0.28.0", sha256="30661c16f4bf008e2b817dc793731d5bfe8648e4e1d44f7d76435c60162857af")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("cmake", type="build")

    depends_on("py-ninja", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    # depends_on("py-pennylane@0.19:", type=("build", "run"))  # circular dependency
