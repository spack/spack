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

    version("master", branch="master")
    version("0.32.0", sha256="8a2206268d7cae0a59f9067b6075175eec93f4843519b371f02716c49a22e750")
    version("0.31.0", sha256="f3b68700825c120e44434ed2b2ab71d0be9d3111f3043077ec0598661ec33477")
    version("0.30.0", sha256="7fe4821fbc733e3e40d7011e054bd2e31edde3151fd9539025c827a5a3579d6b")
    version("0.29.1", sha256="6ecfb305a3898347df8c539a89a67e748766941d159dbef9e34864872f13c45c")

    depends_on("python@3.8:", type=("build", "run"), when="@:0.31.0")
    depends_on("python@3.9:", type=("build", "run"), when="@0.32.0:")
    depends_on("py-pip", type=("build", "run"))  # Runtime req for pennylane.about()
    depends_on("py-setuptools", type="build")

    depends_on("py-numpy@:1.23", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-scipy@:1.10", type=("build", "run"), when="@:0.31.0")
    depends_on("py-networkx", type=("build", "run"))
    depends_on("py-rustworkx", type=("build", "run"), when="@0.30.0:")
    depends_on("py-retworkx", type=("build", "run"), when="@0.28.0:0.29.1")
    depends_on("py-autograd@:1.5", type=("build", "run"))
    depends_on("py-toml", type=("build", "run"))
    depends_on("py-appdirs", type=("build", "run"))
    depends_on("py-semantic-version@2.7:", type=("build", "run"))
    depends_on("py-autoray@0.3.1:", type=("build", "run"))
    depends_on("py-cachetools", type=("build", "run"))
    for v in range(30, 33):
        depends_on(f"py-pennylane-lightning@0.{v}.0:", type=("build", "run"), when=f"@0.{v}.0:")
    depends_on(
        "py-pennylane-lightning@0.28.0:0.29.0", type=("build", "run"), when="@0.28.0:0.29.1"
    )
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-typing-extensions", type=("build", "run"), when="@0.32.0:")

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
