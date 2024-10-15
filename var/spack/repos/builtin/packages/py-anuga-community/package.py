# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install py-anuga-community
#
# You can edit this file again by typing:
#
#     spack edit py-anuga-community
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class PyAnugaCommunity(PythonPackage):
    """ANUGA (pronounced "AHnooGAH") is open-source software for the simulation of the shallow water equation, in particular it can be used to model tsunamis and floods.
ANUGA is a python 3 package with some C and Cython extensions (and an optional fortran extension)."""

    homepage = "https://github.com/anuga-community/anuga_core"

    url = "https://github.com/anuga-community/anuga_core.git"
    git = "https://github.com/anuga-community/anuga_core.git"

    maintainers("samcom12")

    version("main", branch="main")

    depends_on("python@3:", type=("build", "run"))
    depends_on("gdal+geos+python", type=("build", "run"))
    depends_on("py-future", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-setuptools", type=("build"))
    depends_on("py-mpi4py", type=("build", "run"))

    depends_on("py-utm", type=("build", "run"))
    depends_on("py-pybind11", type=("build", "run"))
    depends_on("py-pymetis", type=("build", "run"))
    depends_on("py-cython", type=("build"))
    depends_on("py-wheel", type=("build"))
    depends_on("py-gitpython", type=("build"))
    depends_on("py-netcdf4", type=("build", "run"))
    depends_on("py-dill", type=("build", "test"))
    depends_on("py-nose", type=("build", "test"))
    depends_on("py-pytest", type=("build", "test"))
    depends_on("py-scipy", type=("build", "test"))
    depends_on("py-triangle", type=("build", "run", "test"))
    depends_on("py-pytz", type=("build", "run", "test"))
    depends_on("py-pmw", type=("build", "run", "test"))
    depends_on("mpi", type=("test", "run"))

    def setup_run_environment(self, env):
        if self.run_tests:
            env.prepend_path("PATH", self.spec["mpi"].prefix.bin)
    install_time_test_callbacks = ["test", "installtest"]


    def installtest(self):
        python("runtests.py", "--no-build")
