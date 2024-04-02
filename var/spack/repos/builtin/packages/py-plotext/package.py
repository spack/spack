# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPlotext(PythonPackage):
    """Plotext plots directly on terminal."""

    pypi = "plotext/plotext-5.2.8.tar.gz"
    git = "https://github.com/piccolomo/plotext.git"

    license("MIT")

    version(
        "5.2.8",
        sha256="7364cf72e6c9bffaf96158340fd2e0058faf404edbbc1e7a2aed421c8638d475",
        url="https://pypi.org/packages/63/de/82df3f400392b586d18a8bd90714309c7e1fcf74c0f2e42a4f8abc347634/plotext-5.2.8-py3-none-any.whl",
    )

    # build dependencies
