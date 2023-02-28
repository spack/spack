# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

import spack.build_systems.python
from spack.package import *


class PyGmxapi(spack.build_systems.python.PythonPackage):
    """Python bindings and ensemble workflow management for GROMACS.

    The GROMACS C++ API is affected by its package variants. You can
    specify a particular GROMACS API by making the dependency variant explicit.
    E.g. ``spack install gmxapi ^gromacs+mpi~double``
    """

    homepage = "https://manual.gromacs.org/current/gmxapi/index.html"
    maintainers("eirrgang", "peterkasson")

    pypi = "gmxapi/gmxapi-0.4.0.tar.gz"
    version("0.4.0", sha256="7fd58e6a4b1391043379e8ba55555ebeba255c5b394f5df9d676e6a5571d7eba")

    depends_on("gromacs")
    depends_on("mpi")
    depends_on("py-mpi4py")
    depends_on("py-networkx@2.0:", type="run")
    depends_on("py-numpy@1.7:", type="run")
    depends_on("py-setuptools@42:", type="build")
    depends_on("py-packaging", type="run")
    depends_on("py-pybind11@2.6:", type="build")
    depends_on("py-pytest", type="test")

    conflicts("gromacs+mdrun_only", msg="gmxapi requires the full GROMACS library installation.")
    conflicts("gromacs~shared", msg="gmxapi requires the full GROMACS library installation.")
    conflicts("gromacs@:2022.0", when="@0.4:", msg="Use GROMACS 2022.1 or newer for gmxapi 0.4.")
    conflicts(
        "gromacs+mpi", when="@:0.3.2", msg="Use gmxapi 0.4 or higher for MPI-enabled GROMACS."
    )


class PythonPipBuilder(spack.build_systems.python.PythonPipBuilder):
    """Extend the PythonPipBuilder for gromacs client software.

    Use the setup_dependent_build_environment hook to get environment variables
    needed for gromacs client build systems. Build a wheel and use it in the
    install phase.
    """

    def install(self, pkg, spec, prefix):
        global pip
        # `pip` is a module attribute that is injected by the py-pip package
        # via setup_dependent_package. It defines an extension of the `command`
        # from the `python` spec, an instance of spack.util.executable.Executable.
        pip.add_default_env("GROMACS_DIR", self.spec["gromacs"].prefix)
        pip.add_default_env("gmxapi_ROOT", self.spec["gromacs"].prefix)
        pip.add_default_env("Python3_ROOT", self.spec["python"].prefix)
        super().install(pkg, spec, prefix)

    @run_after("install")
    def install_test(self):
        if not self.pkg.run_tests:
            return

        with working_dir("spack-test", create=True):
            # test include helper points to right location
            python = self.spec["python"].command
            python("-m", "pytest", "-x", os.path.join(self.build_directory, "test"))
