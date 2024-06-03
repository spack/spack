# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mepo(PythonPackage):
    """Tool to manage (m)ultiple git r(epo)sitories"""

    homepage = "https://github.com/GEOS-ESM/mepo"
    git = "https://github.com/GEOS-ESM/mepo.git"
    pypi = "mepo/mepo-2.0.0rc3.tar.gz"

    maintainers("pchakraborty", "mathomp4")

    license("Apache-2.0", checked_by="mathomp4")

    version("2.0.0rc3", sha256="c0c897a33f5018489e6cc14892961831c8922a3378ac30436496c52bf877aff7")

    depends_on("python@3.9:", type=("build", "run"))
    depends_on("py-colorama", type=("build", "run"))
    depends_on("py-pyyaml@6:", type=("build", "run"))

    depends_on("py-hatchling", type="build")
