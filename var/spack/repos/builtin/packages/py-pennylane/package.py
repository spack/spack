# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPennylane(PythonPackage):
    """PennyLane is a Python quantum machine learning library by Xanadu Inc."""

    homepage = "https://github.com/XanaduAI/pennylane"
    pypi = "PennyLane/PennyLane-0.28.0.tar.gz"

    maintainers("marcodelapierre")

    version("0.28.0", sha256="2a6100c00277c1eb59eab6856cdad7b1237e9d1fbda98b1e15020bd5a64b10a8")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-numpy@:1.23", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-networkx", type=("build", "run"))
    depends_on("py-retworkx", type=("build", "run"))
    depends_on("py-autograd", type=("build", "run"))
    depends_on("py-toml", type=("build", "run"))
    depends_on("py-appdirs", type=("build", "run"))
    depends_on("py-semantic-version@2.7:", type=("build", "run"))
    depends_on("py-autoray@0.3.1:", type=("build", "run"))
    depends_on("py-cachetools", type=("build", "run"))
    depends_on("py-pennylane-lightning@0.28:", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
