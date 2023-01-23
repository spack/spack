# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPennylane(PythonPackage):
    """PennyLane is a Python quantum machine learning library by Xanadu Inc."""
    homepage = "https://docs.pennylane.ai/"
    git = "https://github.com/PennyLaneAI/pennylane.git"
    pypi = "PennyLane/PennyLane-0.28.0.tar.gz"

    maintainers = PythonPackage.maintainers + ["mlxd", "marcodelapierre"]

    version("0.28.0", sha256="7736a17dc972d918e3a737ce4360d16ac84b9f9f6fca440f167de579c926c114")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-semantic-version@2.7:", type=("build", "run"))
    depends_on("py-pip", type="build" )
    depends_on("py-wheel", type="build")

    depends_on("py-appdirs", type="run")
    depends_on("py-autograd", type="run")
    depends_on("py-autoray", type="run")
    depends_on("py-cachetools", type="run")
    depends_on("py-networkx", type="run")
    depends_on("py-numpy@:1.23", type="run")
    depends_on("py-pennylane-lightning@0.28:+python", type="run")
    depends_on("py-retworkx", type="run")
    depends_on("py-requests", type="run")
    depends_on("py-scipy", type="run")
    depends_on("py-toml", type="run")

    # Test deps
    depends_on("py-pytest", type="test")
    depends_on("py-pytest-mock", type="test")
    depends_on("py-flaky", type="test")