# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class PyTriton(PythonPackage):
    """A language and compiler for custom Deep Learning operations."""

    homepage = "https://github.com/triton-lang/triton"
    url = "https://github.com/triton-lang/triton/archive/refs/tags/v2.1.0.tar.gz"
    git = "https://github.com/triton-lang/triton.git"

    license("MIT")

    version("main", branch="main")
    version("2.1.0", sha256="4338ca0e80a059aec2671f02bfc9320119b051f378449cf5f56a1273597a3d99")

    if sys.platform.startswith("linux"):
        version(
            "3.2.0-py3.13",
            sha256="e5dfa23ba84541d7c0a531dfce76d8bcd19159d50a4a8b14ad01e91734a5c1b0",
            url="https://files.pythonhosted.org/packages/c7/30/37a3384d1e2e9320331baca41e835e90a3767303642c7a80d4510152cbcf/triton-3.2.0-cp313-cp313-manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
        )
        version(
            "3.2.0-py3.12",
            sha256="8d9b215efc1c26fa7eefb9a157915c92d52e000d2bf83e5f69704047e63f125c",
            url="https://files.pythonhosted.org/packages/06/00/59500052cb1cf8cf5316be93598946bc451f14072c6ff256904428eaf03c/triton-3.2.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
        )
        version(
            "3.2.0-py3.11",
            sha256="8009a1fb093ee8546495e96731336a33fb8856a38e45bb4ab6affd6dbc3ba220",
            url="https://files.pythonhosted.org/packages/a7/2e/757d2280d4fefe7d33af7615124e7e298ae7b8e3bc4446cdb8e88b0f9bab/triton-3.2.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
        )
        version(
            "3.2.0-py3.10",
            sha256="b3e54983cd51875855da7c68ec05c05cf8bb08df361b1d5b69e05e40b0c9bd62",
            url="https://files.pythonhosted.org/packages/01/65/3ffa90e158a2c82f0716eee8d26a725d241549b7d7aaf7e4f44ac03ebd89/triton-3.2.0-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
        )
        version(
            "3.2.0-py3.9",
            sha256="30ceed0eff2c4a73b14eb63e052992f44bbdf175f3fad21e1ac8097a772de7ee",
            url="https://files.pythonhosted.org/packages/bc/74/9f12bdedeb110242d8bb1bd621f6605e753ee0cbf73cf7f3a62b8173f190/triton-3.2.0-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
        )
        for py_ver in ["3.9", "3.10", "3.11", "3.12", "3.13"]:
            depends_on(
                "python@" + py_ver + ".0:" + py_ver,
                when="@3.2.0-py" + py_ver,
                type=("build", "run"),
            )

        version(
            "3.1.0-py3.12",
            sha256="c8182f42fd8080a7d39d666814fa36c5e30cc00ea7eeeb1a2983dbb4c99a0fdc",
            url="https://files.pythonhosted.org/packages/78/eb/65f5ba83c2a123f6498a3097746607e5b2f16add29e36765305e4ac7fdd8/triton-3.1.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
        )
        version(
            "3.1.0-py3.11",
            sha256="0f34f6e7885d1bf0eaaf7ba875a5f0ce6f3c13ba98f9503651c1e6dc6757ed5c",
            url="https://files.pythonhosted.org/packages/86/17/d9a5cf4fcf46291856d1e90762e36cbabd2a56c7265da0d1d9508c8e3943/triton-3.1.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
        )
        version(
            "3.1.0-py3.10",
            sha256="6b0dd10a925263abbe9fa37dcde67a5e9b2383fc269fdf59f5657cac38c5d1d8",
            url="https://files.pythonhosted.org/packages/98/29/69aa56dc0b2eb2602b553881e34243475ea2afd9699be042316842788ff5/triton-3.1.0-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
        )
        version(
            "3.1.0-py3.9",
            sha256="aafa9a20cd0d9fee523cd4504aa7131807a864cd77dcf6efe7e981f18b8c6c11",
            url="https://files.pythonhosted.org/packages/c4/69/57e0fed438d547524e08bfedc587078314176ad1c15c8be904d3f03149ec/triton-3.1.0-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
        )
        version(
            "3.1.0-py3.8",
            sha256="6dadaca7fc24de34e180271b5cf864c16755702e9f63a16f62df714a8099126a",
            url="https://files.pythonhosted.org/packages/15/3c/e972ac0dd0f35ba5fb7058152dd52127a225f579eba2d7527eb1ffb3891a/triton-3.1.0-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
        )

        for py_ver in ["3.8", "3.9", "3.10", "3.11", "3.12"]:
            depends_on(
                "python@" + py_ver + ".0:" + py_ver,
                when="@3.1.0-py" + py_ver,
                type=("build", "run"),
            )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools@40.8:", type="build")
    depends_on("cmake@3.18:", type="build")
    depends_on("py-filelock", type=("build", "run"))
    depends_on("zlib-api", type="link")
    conflicts("^openssl@3.3.0")

    def setup_build_environment(self, env):
        """Set environment variables used to control the build"""
        if self.spec.satisfies("%clang"):
            env.set("TRITON_BUILD_WITH_CLANG_LLD", "True")

    @property
    def build_directory(self):
        if str(self.version) in [
            triton_ver + "-py" + py_ver
            for py_ver in ["3.8", "3.9", "3.10", "3.11", "3.12", "3.13"]
            for triton_ver in ["3.1.0", "3.2.0"]
        ]:
            return "."
        return "python"
