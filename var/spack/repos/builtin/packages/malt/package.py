# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Malt(CMakePackage):
    """
    MALT is a memory profile tool to track mallocs in a C/C++ application and report
    allocation information (lifetime, sizes...) in a friendly web graphical interface
    by annotating the source code and proving charts.
    """

    # Project infos
    homepage = "https://memtt.github.io/malt"
    url = "https://github.com/memtt/malt/archive/v1.2.1.tar.gz"
    maintainers("svalat")

    # Versions
    version("1.2.1", sha256="0e4c0743561f9fcc04dc83457386167a9851fc9289765f8b4f9390384ae3618a")

    # Variants
    variant(
        "nodejs",
        default=True,
        description="Enable the installation of the Web GUI based on NodeJS",
    )
    variant(
        "qt",
        default=False,
        when="+nodejs",
        description="Build the viewer based on NodeJS + QT web toolkit (requires NodeJS too)",
    )

    # Dependencies
    depends_on("node-js@18:", type=("build", "run"), when="+nodejs")
    depends_on("libelf")
    depends_on("libunwind")
    depends_on("binutils", type="run")
    depends_on("qt", when="+qt")
