# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNgvCtools(PythonPackage):
    """C++ extensions tools for ngv building"""

    homepage = "https://github.com/BlueBrain/ngv-ctools"
    git = "https://github.com/BlueBrain/ngv-ctools.git"
    pypi = "ngv-ctools/ngv_ctools-1.0.3.tar.gz"

    version("1.0.3", sha256="2062074bd4a472c09bb583613fbb058f9b01ce8aa55ee4faacabc2ec9a49e25d")

    depends_on("py-setuptools@42.0:", type="build")
    depends_on("py-pybind11", type=("build", "link"))

    depends_on("py-numpy", type="test")
    depends_on("py-mock", type="test")
    depends_on("py-pytest", type="test")

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def test(self):
        python("-m", "pytest", "tests")
