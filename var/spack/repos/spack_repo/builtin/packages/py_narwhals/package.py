# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyNarwhals(PythonPackage):
    """Extremely lightweight compatibility layer between dataframe libraries"""

    homepage = "https://github.com/narwhals-dev/narwhals"
    pypi = "narwhals/narwhals-1.8.1.tar.gz"

    version("1.38.0", sha256="0a356a21ad00de0db0e631332a823a6a6755544bd10b8e68a02d75029c71392e")
    version("1.8.1", sha256="97527778e11f39a1e5e2113b8fbb9ead788be41c0337f21852e684e378f583e8")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-hatchling", type=("build"))
