# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPennylaneLightning(PythonPackage):
    """PennyLane-Lightning plugin"""

    homepage = "https://github.com/PennyLaneAI/pennylane-lightning"
    pypi = "pennylane-lightning/PennyLane-Lightning-0.27.0.tar.gz"

    version("0.27.0", sha256="f11e7501ea955b8b38e728083955f144e90ed75a43418b3b31fde31252466d0d")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-ninja", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    #depends_on("py-pennylane@0.19:", type=("build", "run"))  # circular dep
