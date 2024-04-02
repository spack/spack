# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytestFilterSubpackage(PythonPackage):
    """Pytest plugin for filtering based on sub-packages."""

    homepage = "https://github.com/astropy/pytest-filter-subpackage"
    pypi = "pytest-filter-subpackage/pytest-filter-subpackage-0.1.2.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.1.2",
        sha256="39a1fb6f559e0579851c1e447d3c876f6a5c2e49ab356c568b90e4f5b0d4a19e",
        url="https://pypi.org/packages/f0/23/67097daf438eef3b4c7bf90939445e89983801c1c40e2c377ebd234c55ad/pytest_filter_subpackage-0.1.2-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@0.1.2:0.1")
        depends_on("py-pytest@3:", when="@:0.1")
