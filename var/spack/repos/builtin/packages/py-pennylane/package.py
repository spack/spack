# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPennylane(PythonPackage):
    """PennyLane is a Python quantum machine learning library by Xanadu Inc."""

    homepage = "https://docs.pennylane.ai/"
    git = "https://github.com/PennyLaneAI/pennylane.git"
    url = "https://github.com/PennyLaneAI/pennylane/archive/refs/tags/v0.32.0.tar.gz"

    maintainers("mlxd", "AmintorDusko", "marcodelapierre")

    license("Apache-2.0")

    version(
        "0.32.0",
        sha256="3fe85394de25d0e189c93c6b92171bcff09bf392618ebed57a7401a3c819713d",
        url="https://pypi.org/packages/ec/12/783161913f263cc311fb686b05c0e7abb42f87b158f49664f95472aa2135/PennyLane-0.32.0-py3-none-any.whl",
    )
    version(
        "0.31.0",
        sha256="a62a30760f6d4b4c3b88449eb8a98e9a03860ae61ec6d5178d83d3140c5c9ae0",
        url="https://pypi.org/packages/ef/07/34c305ba50e4ea662143e10d8f566078df5e4d71b8d8b376c532e30147de/PennyLane-0.31.0-py3-none-any.whl",
    )
    version(
        "0.30.0",
        sha256="6b8189bf34d84d39dbdda343c1bb1402117545443f57c6a6dd2480e6ab6c538c",
        url="https://pypi.org/packages/f1/10/c84ea151654cc4f754ba362eb99db2321edbd5c96b08bdd30bfe1e6bc4a3/PennyLane-0.30.0-py3-none-any.whl",
    )
    version(
        "0.29.1",
        sha256="d6feac06958a8a324745e8094c4535a30a97f64e9befca039edb559d7e78e036",
        url="https://pypi.org/packages/31/5d/1b645e719900f59c8f4c654f95e5ce62d040153f2f36562de9793dfea10c/PennyLane-0.29.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-appdirs")
        depends_on("py-autograd@:1.5", when="@0.31:0.32")
        depends_on("py-autograd", when="@:0.30,0.33:")
        depends_on("py-autoray@0.3:", when="@0.23.1:0.31.0,0.32")
        depends_on("py-cachetools")
        depends_on("py-networkx")
        depends_on("py-numpy@:1.23", when="@0.28:0.32")
        depends_on("py-pennylane-lightning@0.32:", when="@0.32")
        depends_on("py-pennylane-lightning@0.31:", when="@0.31")
        depends_on("py-pennylane-lightning@0.30:", when="@0.30")
        depends_on("py-pennylane-lightning@0.28:", when="@0.28:0.29")
        depends_on("py-requests", when="@0.27:")
        depends_on("py-retworkx", when="@:0.29")
        depends_on("py-rustworkx", when="@0.30:")
        depends_on("py-scipy@:1.10.0", when="@0.31:0.31.0")
        depends_on("py-scipy", when="@:0.30,0.31.1:")
        depends_on("py-semantic-version@2.7:", when="@0.25:")
        depends_on("py-toml")
        depends_on("py-typing-extensions", when="@0.31.1:")

    # Test deps
