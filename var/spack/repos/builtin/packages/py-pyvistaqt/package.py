# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyvistaqt(PythonPackage):
    """PyQT support for PyVista."""

    homepage = "https://github.com/pyvista/pyvistaqt"
    pypi = "pyvistaqt/pyvistaqt-0.5.0.tar.gz"

    license("MIT")

    version(
        "0.11.0",
        sha256="21f88d7e6fb6cf11767807bf13684975759e61d642582a16ff5fcf8e12aa6a60",
        url="https://pypi.org/packages/ac/92/043070db56638897574ad7cdf3de08dce2170e0a1779c26b25c0de4ca5f6/pyvistaqt-0.11.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:")
        depends_on("py-pyvista@0.32.0:")
        depends_on("py-qtpy@1.9:")
