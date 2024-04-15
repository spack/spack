# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyClimate(PythonPackage):
    """Command line arguments parsing"""

    homepage = "https://pypi.org/project/climate/"
    url = "https://pypi.io/packages/py3/c/climate/climate-0.1.0-py3-none-any.whl"

    license("Apache-2.0")

    version(
        "0.1.0",
        sha256="01026c764b34d8204b8f527a730ef667fa5827fca765993ff1ed3e9dab2c11ae",
        url="https://pypi.org/packages/1c/d6/ed62a152d3728f33e38528ba8d314e350c03d3699cba1fc63641ed05af58/climate-0.1.0-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:3")
