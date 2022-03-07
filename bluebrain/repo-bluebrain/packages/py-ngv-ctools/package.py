# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNgvCtools(PythonPackage):
    """C++ extensions tools for ngv building"""

    homepage = "https://bbpgitlab.epfl.ch/nse/ngv-ctools"
    git      = "git@bbpgitlab.epfl.ch:nse/ngv-ctools.git"

    version("develop", branch="main")
    version('1.0.1', tag="ngv-ctools-v1.0.1")

    depends_on("py-setuptools@42.0:", type="build")
    depends_on("py-pybind11@2.6.1", type=("build", "link"))

    depends_on("py-numpy", type="test")
    depends_on("py-mock", type="test")
    depends_on("py-pytest", type="test")

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def test(self):
        python("-m", "pytest", "tests")
