# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPartd(PythonPackage):
    """Key-value byte store with appendable values."""

    homepage = "https://github.com/dask/partd/"
    pypi = "partd/partd-0.3.8.tar.gz"

    license("BSD-3-Clause")

    version(
        "1.4.0",
        sha256="7a63529348cf0dff14b986db641cd1b83c16b5cb9fc647c2851779db03282ef8",
        url="https://pypi.org/packages/1a/56/900aae94a28a7bcc0aa90a4be7b739d2221be98c2dfae6f51e34bba29aab/partd-1.4.0-py3-none-any.whl",
    )
    version(
        "1.1.0",
        sha256="7a491cf254e5ab09e9e6a40d80195e5e0e5e169115bfb8287225cb0c207536d2",
        url="https://pypi.org/packages/44/e1/68dbe731c9c067655bff1eca5b7d40c20ca4b23fd5ec9f3d17e201a6f36b/partd-1.1.0-py3-none-any.whl",
    )
    version(
        "0.3.10",
        sha256="826e8034dc1503005f86b67c8542bc8c71cc35b33741b413e82d25a09cc26ad9",
        url="https://pypi.org/packages/9e/f5/c02903ad5a444c9f80e4d1fe4d512afd76e3801de2fba80ea9ed28f9290c/partd-0.3.10-py3-none-any.whl",
    )
    version(
        "0.3.8",
        sha256="041ef0bd589e2d803b6ff6ac2b559adadcaf40a161a8eeb5a367d5e0f399ac1e",
        url="https://pypi.org/packages/4a/ca/207a28fd81111f6a88e79a006745ff432b9cae850fbafa27486e98d459da/partd-0.3.8-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@1.3:")
        depends_on("py-locket", when="@0.3.3,0.3.5,0.3.7:")
        depends_on("py-toolz", when="@0.3.3,0.3.5,0.3.7:")
