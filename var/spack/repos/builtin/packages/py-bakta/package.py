# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyBakta(PythonPackage):
    """Bakta: rapid & standardized annotation
    of bacterial genomes, MAGs & plasmids"""

    homepage = "https://github.com/oschwengers/bakta"
    pypi = "bakta/bakta-1.5.1.tar.gz"

    maintainers("oschwengers")

    license("GPL-3.0-only")

    version(
        "1.5.1",
        sha256="82298adca0476612487147c70b38a1118bb8c301c79009924b3c5e26422e1dcd",
        url="https://pypi.org/packages/41/56/afdcb385ae7e5ece17a2c6dee502787c67deda7038b67ee46204ac749c5f/bakta-1.5.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@:1.8.1")
        depends_on("py-alive-progress@1.6.2:1", when="@1.3.3:1.6")
        depends_on("py-biopython@1.78:", when="@:1.6,1.8.2:")
        depends_on("py-requests@2.25.1:")
        depends_on("py-xopen@1.1:", when="@:1.8.1")
