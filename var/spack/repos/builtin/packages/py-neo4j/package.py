# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyNeo4j(PythonPackage):

    """This is the neo4j bolt driver for python from the official repository"""

    pypi = "neo4j/neo4j-5.25.0.tar.gz"

    license("LGPL-3.0-only")
    maintainers("aquan9")

    version("5.25.0", sha256="7c82001c45319092cc0b5df4c92894553b7ab97bd4f59655156fa9acab83aec9")

    # Python dependencies
    depends_on("py-pytz", type="run")

    # Build dependency
    depends_on("py-setuptools@68.0.0", type="build")
    depends_on("py-tomlkit@0.11.8", type="build")

    depends_on("python@3.7.0:", type=("build", "run"))
