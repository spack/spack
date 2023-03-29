# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIpyvue(PythonPackage):
    """Jupyter widgets base for Vue libraries"""

    homepage = "https://github.com/mariobuikhuizen/ipyvue"
    pypi = "ipyvue/ipyvue-1.9.0.tar.gz"

    version("1.9.0", sha256="841a8dbe0e9d2b1e8fe58a35ee7500f73b66bd08f3f8284d1569c3d8e38fa775")

    depends_on("python@2.7:,3.3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
