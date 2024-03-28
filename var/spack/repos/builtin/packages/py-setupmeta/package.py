# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySetupmeta(PythonPackage):
    """Simplify your setup.py."""

    homepage = "https://github.com/codrsquad/setupmeta"
    pypi = "setupmeta/setupmeta-3.3.0.tar.gz"

    license("MIT")

    version(
        "3.4.0",
        sha256="7a45f58e50ab3348df60a7e6656116b421ffa999acf727aa876f1f7eb442f9df",
        url="https://pypi.org/packages/76/5c/c032e5804fc9026c9e46a4048f71ace3d8b2d80e9f7f7d4837016f1dc707/setupmeta-3.4.0-py2.py3-none-any.whl",
    )
    version(
        "3.3.2",
        sha256="020a27e710bead9d48d49a9c00451d8d5f906e9fc1f64df54f6038889b087578",
        url="https://pypi.org/packages/66/69/3dda958268ca78b8a3e3c899a904742e48163ad807136f14650a9fc2d6cb/setupmeta-3.3.2-py2.py3-none-any.whl",
    )
    version(
        "3.3.0",
        sha256="e52f2af62e9ce7e163637c9a6fb36ba990a1949b30947c0f17b05979957e4256",
        url="https://pypi.org/packages/0e/2e/44f707e69af1f7502aaf5ddcd6460e2ba7e87494ebd46b1a63e2a635e684/setupmeta-3.3.0-py2.py3-none-any.whl",
    )
