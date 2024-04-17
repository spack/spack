# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.build_systems.python
from spack.package import *


class PyPlatformdirs(PythonPackage):
    """A small Python module for determining appropriate
    platform-specific dirs, e.g. a "user data dir" """

    homepage = "https://github.com/platformdirs/platformdirs"
    pypi = "platformdirs/platformdirs-2.4.0.tar.gz"

    license("MIT")

    version(
        "3.10.0",
        sha256="d7c24979f292f916dc9cbf8648319032f551ea8c49a4c9bf2fb556a02070ec1d",
        url="https://pypi.org/packages/14/51/fe5a0d6ea589f0d4a1b97824fb518962ad48b27cd346dcdfa2405187997a/platformdirs-3.10.0-py3-none-any.whl",
    )
    version(
        "3.5.3",
        sha256="0ade98a4895e87dc51d47151f7d2ec290365a585151d97b4d8d6312ed6132fed",
        url="https://pypi.org/packages/6d/1a/96efea7b36835ce89911d7813fe68f5b1db7ecae4023bf209a7aeba93017/platformdirs-3.5.3-py3-none-any.whl",
    )
    version(
        "3.5.0",
        sha256="47692bc24c1958e8b0f13dd727307cff1db103fca36399f457da8e05f222fdc4",
        url="https://pypi.org/packages/ce/cf/279b73aae00f7ba9d5d7664156ef323ebbf16fb556285bb223ecc45031aa/platformdirs-3.5.0-py3-none-any.whl",
    )
    version(
        "3.1.1",
        sha256="e5986afb596e4bb5bde29a79ac9061aa955b94fca2399b7aaac4090860920dd8",
        url="https://pypi.org/packages/7b/e1/593f693096c50411a2bf9571f66bc3be9d0f79a4a50e95aab581458b0e3c/platformdirs-3.1.1-py3-none-any.whl",
    )
    version(
        "2.5.2",
        sha256="027d8e83a2d7de06bbac4e5ef7e023c02b863d7ea5d079477e722bb41ab25788",
        url="https://pypi.org/packages/ed/22/967181c94c3a4063fe64e15331b4cb366bdd7dfbf46fcb8ad89650026fec/platformdirs-2.5.2-py3-none-any.whl",
    )
    version(
        "2.4.1",
        sha256="1d7385c7db91728b83efd0ca99a5afb296cab9d0ed8313a45ed8ba17967ecfca",
        url="https://pypi.org/packages/9f/3d/4606ee54e0af98aa8f9a672b5acfd69318a5917fbb9f8e2c3aaf9c2f293f/platformdirs-2.4.1-py3-none-any.whl",
    )
    version(
        "2.4.0",
        sha256="8868bbe3c3c80d42f20156f22e7131d2fb321f5bc86a2a345375c6481a67021d",
        url="https://pypi.org/packages/b1/78/dcfd84d3aabd46a9c77260fb47ea5d244806e4daef83aa6fe5d83adb182c/platformdirs-2.4.0-py3-none-any.whl",
    )
    version(
        "2.3.0",
        sha256="8003ac87717ae2c7ee1ea5a84a1a61e87f3fbd16eb5aadba194ea30a9019f648",
        url="https://pypi.org/packages/15/4d/23989bdcb80a095a4b92a54a1f568e95bfc9793c70707be623dc75c11257/platformdirs-2.3.0-py3-none-any.whl",
    )

    variant(
        "wheel",
        default=False,
        sticky=True,
        description="Install from wheel (required for bootstrapping Spack)",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@2.4.1:4.0")
        depends_on("py-typing-extensions@4.7.1:", when="@3.10:4.0 ^python@:3.7")
        depends_on("py-typing-extensions@4.6.3:", when="@3.5.2:3.9 ^python@:3.7")
        depends_on("py-typing-extensions@4.5:", when="@3.2:3.5.1 ^python@:3.7")
        depends_on("py-typing-extensions@4.4:", when="@2.6.2:3.1 ^python@:3.7")


class PythonPipBuilder(spack.build_systems.python.PythonPipBuilder):
    @when("+wheel")
    def install(self, pkg, spec, prefix):
        args = list(filter(lambda x: x != "--no-index", self.std_args(self.pkg)))
        args += [f"--prefix={prefix}", self.spec.format("platformdirs=={version}")]
        pip(*args)
