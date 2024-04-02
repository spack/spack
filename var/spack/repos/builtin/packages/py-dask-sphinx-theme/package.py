# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDaskSphinxTheme(PythonPackage):
    """Sphinx theme for Dask documentation."""

    homepage = "https://github.com/dask/dask-sphinx-theme/"
    pypi = "dask_sphinx_theme/dask_sphinx_theme-1.3.5.tar.gz"

    license("BSD-3-Clause")

    version(
        "1.3.5",
        sha256="9b8560d014e6f0a721a9d8d2e8b5ac678152054c16fb8d33861174b09ef08e92",
        url="https://pypi.org/packages/52/c6/952594499619881c188e1bfe24e743f9f2837489513f0fe1f34684283afd/dask_sphinx_theme-1.3.5-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-sphinx-rtd-theme", when="@:1.3.5")
