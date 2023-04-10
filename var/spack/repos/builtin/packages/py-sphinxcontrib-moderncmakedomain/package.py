# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxcontribModerncmakedomain(PythonPackage):
    """Sphinx Domain for Modern CMake."""

    homepage = "https://github.com/scikit-build/moderncmakedomain"
    pypi = "sphinxcontrib_moderncmakedomain/sphinxcontrib_moderncmakedomain-3.25.0.tar.gz"

    maintainers("greenc-FNAL", "gartung", "marcmengel", "vitodb")

    version("3.25.0", sha256="4138e4d3f60e5c4b3982caa10033693bfc1009cdd851766754d5990d9d1e992a")

    conflicts("python@:3.5")

    depends_on("py-hatchling", type="build")

    depends_on("py-sphinx", type=("build", "run"))
