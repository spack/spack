# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFiona(PythonPackage):
    """Fiona reads and writes spatial data files."""

    homepage = "https://github.com/Toblerity/Fiona"
    pypi = "Fiona/Fiona-1.8.18.tar.gz"
    git = "https://github.com/Toblerity/Fiona.git"

    maintainers("adamjstewart")

    version("master", branch="master")
    version("1.9.1", sha256="3a3725e94840a387fef48726d60db6a6791563f366939d22378a4661f8941be7")
    version("1.9.0", sha256="6e487cbfba5a849fbdf06e45169fd7e1f1662f44f3d717ab4b946046b2457eae")
    version("1.8.22", sha256="a82a99ce9b3e7825740157c45c9fb2259d4e92f0a886aaac25f0db40ffe1eea3")
    version("1.8.21", sha256="3a0edca2a7a070db405d71187214a43d2333a57b4097544a3fcc282066a58bfc")
    version("1.8.20", sha256="a70502d2857b82f749c09cb0dea3726787747933a2a1599b5ab787d74e3c143b")
    version("1.8.18", sha256="b732ece0ff8886a29c439723a3e1fc382718804bb057519d537a81308854967a")
    version(
        "1.8.6",
        sha256="fa31dfe8855b9cd0b128b47a4df558f1b8eda90d2181bff1dd9854e5556efb3e",
        deprecated=True,
    )
    version(
        "1.7.12",
        sha256="8b54eb8422d7c502bb7776b184018186bede1a489cf438a7a47f992ade6a0e51",
        deprecated=True,
    )

    # pyproject.toml
    depends_on("python@3.7:", when="@1.9:", type=("build", "link", "run"))
    depends_on("python@2.6:", when="@1.8.22:1.8", type=("build", "link", "run"))
    depends_on("python@2.6:3.10", when="@1.8.21", type=("build", "link", "run"))
    depends_on("python@2.6:3.9", when="@1.8.12:1.8.20", type=("build", "link", "run"))
    depends_on("python@2.6:3.8", when="@:1.8.11", type=("build", "link", "run"))
    depends_on("py-cython@0.29.29:0.29", when="@1.9:", type="build")
    depends_on("py-setuptools@61:", when="@1.9:", type="build")
    depends_on("py-attrs@19.2:", when="@1.9:", type=("build", "run"))
    depends_on("py-attrs@17:", type=("build", "run"))
    depends_on("py-certifi", when="@1.8.18:", type=("build", "run"))
    depends_on("py-click@8", when="@1.9:", type=("build", "run"))
    depends_on("py-click@4:", type=("build", "run"))
    depends_on("py-click-plugins@1:", type=("build", "run"))
    depends_on("py-cligj@0.5:", type=("build", "run"))
    depends_on("py-munch@2.3.2:", when="@1.9:", type=("build", "run"))
    depends_on("py-munch", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))

    # setup.py or release notes
    depends_on("gdal@3.1:", when="@1.9:", type=("build", "link", "run"))
    depends_on("gdal@1.8:", type=("build", "link", "run"))

    # Historical dependencies
    depends_on("py-six@1.7:", when="@:1.8", type=("build", "run"))

    # error: implicit declaration of function 'OSRFixup' is invalid in C99
    conflicts("%apple-clang@12:", when="@:1.8.9")
