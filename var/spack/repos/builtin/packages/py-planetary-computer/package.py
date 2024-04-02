# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPlanetaryComputer(PythonPackage):
    """Python library for interacting with the Microsoft Planetary Computer."""

    homepage = "https://github.com/microsoft/PlanetaryComputer"
    pypi = "planetary-computer/planetary-computer-0.4.9.tar.gz"

    license("MIT")

    version(
        "0.4.9",
        sha256="2b3b8faeeb595fce9e7f5252851eb6aa47c590007bf42c072d86bd560511c586",
        url="https://pypi.org/packages/1b/db/6de887fbb29c62da2db3c4d69318a4fe2cf3ff9af29fd88b27e4ba0c04c9/planetary_computer-0.4.9-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:")
        depends_on("py-click@7.1:")
        depends_on("py-pydantic@1.7.3:+dotenv", when="@:0")
        depends_on("py-pystac@1.0.0:")
        depends_on("py-pystac-client@0.2.0:")
        depends_on("py-pytz@2020.5:")
        depends_on("py-requests@2.25.1:")
