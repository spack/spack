# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMacs2(PythonPackage):
    """MACS2 Model-based Analysis of ChIP-Seq"""

    homepage = "https://github.com/taoliu/MACS"
    pypi = "MACS2/MACS2-2.2.4.tar.gz"

    version("2.2.4", sha256="b131aadc8f5fd94bec35308b821e1f7585def788d2e7c756fc8cac402ffee25b")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-cython", type="build")

    # Most Python packages only require py-setuptools as a build dependency.
    # However, py-macs2 requires py-setuptools during runtime as well.
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-numpy@1.17:", type=("build", "run"))
    depends_on("py-numpy@1.16:", type=("build", "run"))
