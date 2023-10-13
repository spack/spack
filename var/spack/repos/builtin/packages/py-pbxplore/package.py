# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPbxplore(PythonPackage):
    """PBxplore is a suite of tools dedicated to Protein Block (PB) analysis."""

    homepage = "https://pbxplore.readthedocs.io/en/latest/"
    pypi = "pbxplore/pbxplore-1.4.0.tar.gz"

    maintainers("gabrielctn")

    version("1.4.0", sha256="f7f51f64c66b8976715b214da33f033c13c7a8378eea8faf97e006f6ad66e84d")

    depends_on("py-setuptools", type="build")

    depends_on("python@3.6:3.11", type=("build", "run"))

    depends_on("py-mdanalysis", type="run")
    depends_on("py-numpy", type="run")
    depends_on("py-matplotlib", type="run")
    depends_on("py-weblogo", type="run")

    depends_on("py-pytest", type=("run", "test"))
    depends_on("py-coverage", type=("run", "test"))
    depends_on("py-pytest-runner", type=("run", "test"))

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def install_test(self):
        with working_dir("spack-test", create=True):
            python("-c", "import pbxplore; pbxplore.test()")
