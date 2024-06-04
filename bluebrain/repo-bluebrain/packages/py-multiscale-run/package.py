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
    version("0.8", tag="0.8")
    version("0.7", tag="0.7")
    version("0.6", tag="0.6")
    version("0.5.1", tag="0.5.1")
    version("0.4", tag="0.4")
    version("0.3", tag="0.3")
    version("0.2", tag="0.2")

    depends_on("py-setuptools@42:", type=("build"))
    depends_on("py-setuptools-scm@3.4:", type=("build"))

    depends_on("gmsh@4:", type=("build", "run"))
    depends_on("julia@1.6:", type=("build", "run"))
    depends_on("neurodamus-neocortex+ngv+metabolism~~coreneuron@1.15:", type=("build", "run"))
    depends_on("py-astrovascpy@:0.1.2", type=("build", "run"), when="@:0.6")
    depends_on("py-astrovascpy@0.1.5:", type=("build", "run"), when="@0.7:")
    depends_on("py-bluepysnap@2:", type=("build", "run"))
    depends_on("py-diffeqpy@1.1:", type=("build", "run"))
    depends_on("py-jinja2@3:", type=("build", "run"))
    depends_on("py-julia@0.6:0.7", type=("build", "run"))
    depends_on("py-libsonata@0.1.20:", type=("build", "run"))
    depends_on("py-mpi4py@3:", type=("build", "run"))
    depends_on("py-notebook@6:", type=("build", "run"))
    depends_on("py-numpy@1.22:", type=("build", "run"))
    depends_on("py-pandas@1.4:", type=("build", "run"))
    depends_on("py-psutil@5.8:", type=("build", "run"))
    depends_on("py-pyyaml@5:", type=("build", "run"), when="@:0.6")
    depends_on("py-scipy@1.11.1:", type=("build", "run"))
    depends_on("py-simpleeval@0.9.13:", type=("build", "run"))
    depends_on("py-tqdm@4.65:", type=("build", "run"))
    depends_on("py-trimesh@3:", type=("build", "run"))
    depends_on("steps@5", type=("build", "run"))

    depends_on("py-pytest", type="test")

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def test_install(self):
        python("-m", "pytest", "tests/pytests")
