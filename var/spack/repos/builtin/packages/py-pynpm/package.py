# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPynpm(PythonPackage):
    """Python interface to your NPM and package.json."""

    homepage = "https://pynpm.readthedocs.io/en/latest/"
    pypi = "pynpm/pynpm-0.2.0.tar.gz"
    git = "https://github.com/inveniosoftware/pynpm"
    maintainers("jeremyfix")

    license("BSD-3-Clause")

    version(
        "0.2.0",
        sha256="a04d58e4c3d46be26eaae9abd1cf59109a7670c5edd9cacd90e1d3b3afdd77c0",
        url="https://pypi.org/packages/06/b2/2289344ef62fd677ec87a453849bcb21b6c1531f5fee821f3ffe343c58f7/pynpm-0.2.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@0.2:")
