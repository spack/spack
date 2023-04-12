# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyXtb(PythonPackage):
    """Python API for the extended tight binding program package"""

    homepage = "https://xtb-python.readthedocs.org"
    pypi = "xtb/xtb-22.1.tar.gz"
    git = "https://github.com/grimme-lab/xtb-python.git"

    maintainers("awvwgk")

    version("22.1", "7a59e7b783fc6e8b7328f55211de681e535a83991b07c4bab73494063f5e9018")

    depends_on("pkgconfig", type="build")
    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-cffi", type=("build", "run"))
    depends_on("py-meson-python", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("xtb", type=("build", "run"))
