# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMultiscaleRun(PythonPackage):
    """BBP multiscale simulation orchestrator"""

    homepage = "https://bbpgitlab.epfl.ch/-/ide/project/molsys/multiscale_run"
    git = "ssh://git@bbpgitlab.epfl.ch/molsys/multiscale_run.git"

    maintainers("tristan0x", "cattabiani")

    version("develop", branch="main")
    version("0.6", tag="0.6")
    version("0.5.1", tag="0.5.1")
    version("0.4", tag="0.4")
    version("0.3", tag="0.3")
    version("0.2", tag="0.2")

    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-setuptools-scm", type=("build", "run"))

    depends_on("gmsh", type=("build", "run"))
    depends_on("julia", type=("build", "run"))
    depends_on("neurodamus-neocortex+ngv+metabolism~~coreneuron", type=("build", "run"))
    depends_on("py-astrovascpy@:0.1.2", type=("build", "run"), when="@:0.6")
    depends_on("py-astrovascpy@0.1.5:", type=("build", "run"), when="@0.7:")
    depends_on("py-bluepysnap", type=("build", "run"))
    depends_on("py-diffeqpy@1.1", type=("build", "run"))
    depends_on("py-jinja2", type=("build", "run"))
    depends_on("py-julia", type=("build", "run"))
    depends_on("py-libsonata", type=("build", "run"))
    depends_on("py-mpi4py", type=("build", "run"))
    depends_on("py-notebook", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-psutil", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("steps@5.0.0b", type=("build", "run"))

    depends_on("py-pytest", type="test")

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def test_install(self):
        python("-m", "pytest", "tests/pytests")
