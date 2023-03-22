# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPennylane(PythonPackage):
    """PennyLane is a Python quantum machine learning library by Xanadu Inc."""

    homepage = "https://docs.pennylane.ai/"
    git = "https://github.com/PennyLaneAI/pennylane.git"
    url = "https://github.com/PennyLaneAI/pennylane/archive/refs/tags/v0.29.1.tar.gz"

    maintainers("mlxd", "AmintorDusko", "marcodelapierre")

    version("master", branch="master")
    version("0.29.1", sha256="6ecfb305a3898347df8c539a89a67e748766941d159dbef9e34864872f13c45c")
    version(
        "0.28.0",
        sha256="7736a17dc972d918e3a737ce4360d16ac84b9f9f6fca440f167de579c926c114",
        deprecated=True,
    )

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
    depends_on("py-pennylane-lightning@0.28.0:", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))

    # Test deps
    depends_on("py-pytest", type="test")
    depends_on("py-pytest-xdist@3.2:", type="test")
    depends_on("py-pytest-mock", type="test")
    depends_on("py-flaky", type="test")

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def install_test(self):
        with working_dir("tests"):
            pl_dev_test = Executable(join_path(self.prefix, "bin", "pl-device-test"))
            pl_dev_test("--device", "default.qubit", "--shots", "None", "--skip-ops")
            pl_dev_test("--device", "default.qubit", "--shots", "10000", "--skip-ops")
            pl_dev_test("--device", "lightning.qubit", "--shots", "None", "--skip-ops")
            pl_dev_test("--device", "lightning.qubit", "--shots", "10000", "--skip-ops")
