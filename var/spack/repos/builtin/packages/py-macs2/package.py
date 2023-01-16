# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import glob

from spack.package import *


class PyMacs2(PythonPackage):
    """MACS2 Model-based Analysis of ChIP-Seq"""

    homepage = "https://github.com/taoliu/MACS"
    pypi = "MACS2/MACS2-2.2.4.tar.gz"

    version("2.2.7.1", sha256="ad2ca69bdd02a8942a68aae23133289b5c16ba382bcbe20c39fabf3948929de5")
    version("2.2.4", sha256="b131aadc8f5fd94bec35308b821e1f7585def788d2e7c756fc8cac402ffee25b")
    version("2.1.4", sha256="e4966d001914320829ab859c7bc8e92c6410aa7bdbddfd00b7625e9a0fb15c97")
    version("2.1.3.3", sha256="00959e523f45ed92b8429f55944eca6984623ac008d7cdb488c3ffe59c21984a")
    version(
        "2.1.1.20160309", sha256="2008ba838f83f34f8e0fddefe2a3a0159f4a740707c68058f815b31ddad53d26"
    )

    # patch to correctly identify python-3.10 as greater than required version
    patch(
        "https://github.com/macs3-project/MACS/pull/497.patch?full_index=1",
        sha256="eaff891b9b3c6a910bd5d454dcc6e21288c8d1ad4d6d6f77e370bc8f90921cbd",
        when="^python@3.10:",
    )

    depends_on("python@3.6:", when="@2.2.7.1:", type=("build", "run"))
    depends_on("python@3.5:", when="@2.2:", type=("build", "run"))
    depends_on("python@2.7:2.8", when="@:2.1", type=("build", "run"))
    depends_on("py-cython", type="build")

    # Most Python packages only require py-setuptools as a build dependency.
    # However, py-macs2 requires py-setuptools during runtime as well.
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-setuptools@41.2:", when="@2.2.4:", type=("build", "run"))
    depends_on("py-numpy@1.17:", when="@2.2:", type=("build", "run"))
    depends_on("py-numpy@1.16:", when="@2.1.4", type=("build", "run"))
    depends_on("py-numpy@1.15:", when="@2.1.3.3", type=("build", "run"))
    depends_on("py-numpy@1.6:", when="@2.1.1.20160309", type=("build", "run"))
    depends_on("py-cython@0.29:", when="@2.1.4:", type="build")
    depends_on("py-cython@0.25:", when="@2.1.3.3", type="build")

    def patch(self):
        # regenerate C files from pyx files with cython
        files = glob.glob("MACS2/**/[!c]*.c", recursive=True)
        force_remove(*files)
