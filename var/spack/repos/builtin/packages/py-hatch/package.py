# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHatch(PythonPackage):
    """Modern, extensible Python project management"""

    homepage = "https://hatch.pypa.io/latest/"
    pypi = "hatch/hatch-1.12.0.tar.gz"

    license("MIT")

    version("1.12.0", sha256="ae80478d10312df2b44d659c93bc2ed4d33aecddce4b76378231bdf81c8bf6ad")

    depends_on("py-setuptools", type="build")
    depends_on("py-hatchling", type="build")
    depends_on("py-hatch-vcs", type="build")

