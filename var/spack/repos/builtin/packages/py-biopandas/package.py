# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBiopandas(PythonPackage):
    """Working with molecular structures in pandas DataFrames"""

    homepage = "https://rasbt.github.io/biopandas"
    pypi = "biopandas/biopandas-0.2.5.tar.gz"
    git = "https://github.com/rasbt/biopandas.git"

    # Note that the source package on PyPi is broken as it
    # is missing the requirements.txt so we have to download
    # from github

    license("BSD-3-Clause")

    version(
        "0.2.5",
        sha256="cd4672321106a0c8d40ec91047623dae51699f38b96d928ee6f33baca1a61f4f",
        url="https://pypi.org/packages/67/7d/e116656ca9b9790b18e41a00036f4a646a893dc0a9d5344c91af7d55b4ef/biopandas-0.2.5-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-numpy@1.16.2:", when="@0.2.5:")
        depends_on("py-pandas@0.24.2:", when="@0.2.5:")
        depends_on("py-setuptools", when="@0.2.5:")
