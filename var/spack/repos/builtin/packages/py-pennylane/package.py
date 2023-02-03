# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPennylane(PythonPackage):
    """PennyLane is a Python quantum machine learning library by Xanadu Inc."""

    homepage = "https://docs.pennylane.ai/"
    git = "https://github.com/PennyLaneAI/pennylane.git"
    pypi = "PennyLane/PennyLane-0.28.0.tar.gz"

    maintainers = ["mlxd", "AmintorDusko"]

    version("0.28.0", sha256="2a6100c00277c1eb59eab6856cdad7b1237e9d1fbda98b1e15020bd5a64b10a8")

    version("develop", branch="master")
    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-semantic-version@2.7:", type=("build", "run"))
    depends_on("py-pip", type="build")
    depends_on("py-wheel", type="build")

    depends_on("py-appdirs", type="run")
    depends_on("py-autograd", type="run")
    depends_on("py-autoray", type="run")
    depends_on("py-cachetools", type="run")
    depends_on("py-networkx", type="run")
    depends_on("py-numpy@:1.23", type="run")
    depends_on("py-pennylane-lightning+python", type="run")
    depends_on("py-retworkx", type="run")
    depends_on("py-requests", type="run")
    depends_on("py-scipy", type="run")
    depends_on("py-toml", type="run")

    # Test deps
    depends_on("py-pytest", type=("run", "test"))
    depends_on("py-pytest-xdist", type=("run", "test"))
    depends_on("py-pytest-mock", type=("run", "test"))
    depends_on("py-flaky", type=("run", "test"))

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def install_test(self):
        with working_dir("tests"):
            pl_dev_test = Executable(join_path(self.prefix, "bin", "pl-device-test"))
            pl_dev_test("--device", "default.qubit", "--shots", "None", "--skip-ops")
            pl_dev_test("--device", "default.qubit", "--shots", "10000", "--skip-ops")
            pl_dev_test("--device", "lightning.qubit", "--shots", "None", "--skip-ops")
            pl_dev_test("--device", "lightning.qubit", "--shots", "10000", "--skip-ops")
