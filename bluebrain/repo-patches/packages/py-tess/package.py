# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTess(PythonPackage):
    """A 3D cell-bases Laguerre tesselation library based on voro++
    Internal mirror of: https://github.com/wackywendell/tess
    """

    homepage = "https://bbpgitlab.epfl.ch/nse/mirrors/tess"
    git      = "git@bbpgitlab.epfl.ch:nse/mirrors/tess.git"

    version("develop", branch="master")
    version("0.3.2", tag="tess-v0.3.2")

    depends_on("py-setuptools@42.0:", type="build")
    depends_on("py-cython@0.29:0.999", type="build")

    depends_on("py-pytest", type="test")
    depends_on("py-numpy", type="test")
    depends_on("py-scipy", type="test")

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def test(self):
        python("-m", "pytest", "tests")
