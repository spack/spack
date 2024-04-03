# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCycler(PythonPackage):
    """Composable style cycles."""

    homepage = "https://matplotlib.org/cycler/"
    pypi = "cycler/cycler-0.11.0.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.11.0",
        sha256="3a27e95f763a428a739d2add979fa7494c912a32c17c4c38c4d5f082cad165a3",
        url="https://pypi.org/packages/5c/f9/695d6bedebd747e5eb0fe8fad57b72fdf25411273a39791cde838d5a8f51/cycler-0.11.0-py3-none-any.whl",
    )
    version(
        "0.10.0",
        sha256="1d8a5ae1ff6c5cf9b93e8811e581232ad8920aeec647c37316ceac982b08cb2d",
        url="https://pypi.org/packages/f7/d2/e07d3ebb2bd7af696440ce7e754c59dd546ffe1bbe732c8ab68b9c834e61/cycler-0.10.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-six", when="@:0.10")
