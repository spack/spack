# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPooch(PythonPackage):
    """Pooch manages your Python library's sample data files: it automatically
    downloads and stores them in a local directory, with support for versioning
    and corruption checks."""

    homepage = "https://github.com/fatiando/pooch"
    pypi = "pooch/pooch-1.3.0.tar.gz"

    license("BSD-3-Clause")

    version(
        "1.7.0",
        sha256="74258224fc33d58f53113cf955e8d51bf01386b91492927d0d1b6b341a765ad7",
        url="https://pypi.org/packages/84/8c/4da580db7fb4cfce8f5ed78e7d2aa542e6f201edd69d3d8a96917a8ff63c/pooch-1.7.0-py3-none-any.whl",
    )
    version(
        "1.5.2",
        sha256="debb159655de9eeccc366deb111fe1e33e76efac19724436b6878c09deca4293",
        url="https://pypi.org/packages/76/1e/5092523703289aa1a9c14b1ed09d4eda6de76d7eee9ee6b26b54d675e73f/pooch-1.5.2-py3-none-any.whl",
    )
    version(
        "1.3.0",
        sha256="2cec8cbd0515462da1f84446113e77a785029b8514841e0ad344dd57f7924902",
        url="https://pypi.org/packages/40/b9/9876662636ba451d4406543047c0b45ca5b4e830f931308c8274dad1db43/pooch-1.3.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@1.7:")
        depends_on("py-appdirs", when="@:1.5")
        depends_on("py-packaging@20:", when="@1.6:")
        depends_on("py-packaging", when="@:1.5")
        depends_on("py-platformdirs@2.5:", when="@1.7:")
        depends_on("py-requests@2.19:", when="@1.6:")
        depends_on("py-requests", when="@:1.5")

    # Historical dependencies
