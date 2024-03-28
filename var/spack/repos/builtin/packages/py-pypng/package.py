# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPypng(PythonPackage):
    """PyPNG allows PNG image files to be read and written using pure Python."""

    homepage = "https://gitlab.com/drj11/pypng"
    pypi = "pypng/pypng-0.0.20.tar.gz"

    maintainers("snehring")

    license("MIT")

    version(
        "0.20220715.0",
        sha256="4a43e969b8f5aaafb2a415536c1a8ec7e341cd6a3f957fd5b5f32a4cfeed902c",
        url="https://pypi.org/packages/3e/b9/3766cc361d93edb2ce81e2e1f87dd98f314d7d513877a342d31b30741680/pypng-0.20220715.0-py3-none-any.whl",
    )
    version(
        "0.0.20",
        sha256="1f9c9cc24030459abbb2813a62b2bbcdb43ad0867e2f2232a302655308b3d25f",
        url="https://pypi.org/packages/f7/24/36654d22e5750517f53b823fafe1c6f128f7ff9c319af811947f410b64d4/pypng-0.0.20-py3-none-any.whl",
    )
