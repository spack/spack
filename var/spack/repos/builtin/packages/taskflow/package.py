# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.compiler import UnsupportedCompilerFlag
from spack.package import *


class Taskflow(CMakePackage):
    """Taskflow helps you quickly write parallel tasks programs in
    modern C++."""

    homepage = "https://github.com/taskflow/taskflow"
    url = "https://github.com/taskflow/taskflow/archive/v2.7.0.tar.gz"
    git = "https://github.com/taskflow/taskflow.git"

    version("master", branch="master")
    version("3.6.0", sha256="5a1cd9cf89f93a97fcace58fd73ed2fc8ee2053bcb43e047acb6bc121c3edf4c")
    version("3.5.0", sha256="33c44e0da7dfda694d2b431724d6c8fd25a889ad0afbb4a32e8da82e2e9c2a92")
    version("3.4.0", sha256="8f449137d3f642b43e905aeacdf1d7c5365037d5e1586103ed4f459f87cecf89")
    version("3.3.0", sha256="66b891f706ba99a5ca5ed239d520ad6943ebe94728d1c89e07a939615a6488ef")
    version("3.2.0", sha256="26c37a494789fedc5de8d1f8452dc8a7774a220d02c14d5b19efe0dfe0359c0c")
    version("3.1.0", sha256="b83e9a78c254d831b8401d0f8a766e3c5b60d8d20be5af6e2d2fad4aa4a8b980")
    version("3.0.0", sha256="553c88a6e56e115d29ac1520b8a0fea4557a5fcda1af1427bd3ba454926d03a2")
    version(
        "2.7.0", 
        sha256="bc2227dcabec86abeba1fee56bb357d9d3c0ef0184f7c2275d7008e8758dfc3e",
        deprecated=True
    )

    # Compiler must offer C++17 support
    conflicts("%gcc@:8.4", when="@3.0:")
    conflicts("%clang@:6.0", when="@3.0:")
    conflicts("%apple-clang@:12.0.0", when="@3.0:")

    def cmake_args(self):
        try:
            self.compiler.cxx17_flag
        except UnsupportedCompilerFlag:
            InstallError("Taskflow requires a C++17-compliant C++ compiler")

        args = []
        return args
