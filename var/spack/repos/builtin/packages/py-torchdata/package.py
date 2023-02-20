# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTorchdata(PythonPackage):
    """Composable data loading modules for PyTorch."""

    homepage = "https://github.com/pytorch/data"
    git = "https://github.com/pytorch/data.git"
    url = "https://github.com/pytorch/data/archive/refs/tags/v0.4.0.tar.gz"

    maintainers("adamjstewart")

    version("main", branch="main")
    version("0.5.1", sha256="69d80bd33ce8f08e7cfeeb71cefddfc29cede25a85881e33dbae47576b96ed29")
    version("0.5.0", sha256="b4e1a7015b34e3576111d495a00a675db238bfd136629fc443078bab9383ec36")
    version("0.4.1", sha256="71c0aa3aca3b04a986a2cd4cc2e0be114984ca836dc4def2c700bf1bd1ff087e")
    version("0.4.0", sha256="b4ec446a701680faa620fcb828b98ba36a63fa79da62a1e568d4a683889172da")
    version("0.3.0", sha256="ac36188bf133cf5f1041a28ccb3ee82ba52d4b5d99617be37d64d740acd6cfd4")

    # https://github.com/pytorch/data#version-compatibility
    depends_on("python@3.7:3.10", type=("build", "run"))
    depends_on("py-torch@master", when="@main", type=("build", "run"))
    depends_on("py-torch@1.13.1", when="@0.5.1", type=("build", "run"))
    depends_on("py-torch@1.13.0", when="@0.5.0", type=("build", "run"))
    depends_on("py-torch@1.12.1", when="@0.4.1", type=("build", "run"))
    depends_on("py-torch@1.12.0", when="@0.4.0", type=("build", "run"))
    depends_on("py-torch@1.11.0", when="@0.3.0", type=("build", "run"))

    # requirements.txt
    depends_on("py-setuptools", type="build")
    depends_on("py-urllib3@1.25:", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-portalocker@2:", when="@0.4:", type=("build", "run"))

    # third_party/CMakeLists.txt
    depends_on("py-pybind11", when="@0.4:")
    depends_on("aws-sdk-cpp", when="@0.4:")

    def setup_build_environment(self, env):
        env.set("USE_SYSTEM_LIBS", "ON")
