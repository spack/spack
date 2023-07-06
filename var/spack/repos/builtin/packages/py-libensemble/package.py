# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class PyLibensemble(PythonPackage):
    """Library for managing ensemble-like collections of computations."""

    homepage = "https://libensemble.readthedocs.io"
    pypi = "libensemble/libensemble-0.10.0.tar.gz"
    git = "https://github.com/Libensemble/libensemble.git"
    maintainers("shuds13", "jlnav")

    tags = ["e4s"]

    version("develop", branch="develop")
    version("0.10.0", sha256="f800f38d02def526f1d2a325710d01fdd3637cd1e33a9a083a3cf4a7f419a726")
    version("0.9.3", sha256="00e5a65d6891feee6a686c048d8de72097b8bff164431f163be96ec130a9c390")
    version("0.9.2", sha256="e46598e5696f770cbff4cb90507b52867faad5654f1b80de35405a95228c909f")
    version("0.9.1", sha256="684e52b0ea64f5ec610e7868b7e4c9fa5fd2316a370a726870aa5fd5fb1b0ede")
    version("0.9.0", sha256="34976e775f0d2ba5955744560104eab214fd22cb47173440eb5136e852a8ec38")
    version("0.8.0", sha256="1102e56c6381c9692de6888add23780ec69f18ad33f12119dc0391776a9a7300")
    version("0.7.2", sha256="69b64304d1ecce4d57687ea6062f89bd813ae93b2a290bb1f595c5626ab6f197")
    version("0.7.1", sha256="5cb294269624c1284ea25be9ed3bc668a2333e21e97a97b57ad339eb85435e46")
    version("0.7.0", sha256="4c3c16ef3d4750b7a54198fae5d7ae402c5f5411ae85189da41afd20e20027dc")
    version("0.6.0", sha256="3f6a926d3868da53835ed93fc2e2a047b368dacb648c7608ee3a66debcee4d38")
    version("0.5.2", sha256="3e36c29a4a2adc0984ecfcc998cb5bb8a2cdfbe7a1ae92f7b35b06e41d21b889")
    version("0.5.1", sha256="522e0cc086a3ed75a101b704c0fe01eae07f2684bd8d6da7bdfe9371d3187362")
    version("0.5.0", sha256="c4623171dee049bfaa38a9c433609299a56b1afb774db8b71321247bc7556b8f")
    version("0.4.1", sha256="282c32ffb79d84cc80b5cc7043c202d5f0b8ebff10f63924752f092e3938db5e")
    version("0.4.0", sha256="9384aa3a58cbc20bbd1c6fddfadb5e6a943d593a3a81c8665f030dbc6d76e76e")
    version("0.3.0", sha256="c8efdf45d0da0ef6299ee778cea1c285c95972af70d3a729ee6dc855e66f9294")
    version("0.2.0", sha256="ecac7275d4d0f4a5e497e5c9ef2cd998da82b2c020a0fb87546eeea262f495ff")
    version("0.1.0", sha256="0b27c59ae80f7af8b1bee92fcf2eb6c9a8fd3494bf2eb6b3ea17a7c03d3726bb")

    variant("mpi", default=True, description="Install with MPI")
    variant("scipy", default=False, description="Install with scipy")
    variant("petsc4py", default=False, description="Install with petsc4py")
    variant("nlopt", default=False, description="Install with nlopt")
    variant("mpmath", default=False, description="Install with mpmath")
    variant("deap", default=False, description="Install with DEAP")
    variant("tasmanian", default=False, description="Install with tasmanian")

    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-psutil", type=("build", "run"), when="@0.7.1:")
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-pydantic", type=("build", "run"), when="@0.10:")
    depends_on("py-tomli", type=("build", "run"), when="@0.10:")
    depends_on("py-pyyaml", type=("build", "run"), when="@0.10:")
    depends_on("mpi", when="@:0.4.1")
    depends_on("mpi", when="+mpi")
    depends_on("py-mpi4py@2.0:", type=("build", "run"), when="@:0.4.1")
    depends_on("py-mpi4py@2.0:", type=("build", "run"), when="+mpi")
    depends_on("py-scipy", type=("build", "run"), when="+scipy")
    depends_on("py-petsc4py", type=("build", "run"), when="+petsc4py")
    depends_on("py-petsc4py@main", type=("build", "run"), when="@develop+petsc4py")
    depends_on("nlopt", type=("build", "run"), when="+nlopt")
    depends_on("py-mpmath", type=("build", "run"), when="+mpmath")
    depends_on("py-deap", type=("build", "run"), when="+deap")
    depends_on("tasmanian+python", type=("build", "run"), when="+tasmanian")
    conflicts("~mpi", when="@:0.4.1")

    @run_after("install")
    def cache_test_sources(self):
        """Copy the example source files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        self.cache_extra_test_sources(join_path("examples", "calling_scripts", "regression_tests"))

    def run_tutorial_script(self, script):
        """run the tutorial example regression test"""

        exe = (
            self.test_suite.current_test_cache_dir.examples.calling_scripts.regression_tests.join(
                script
            )
        )
        if not os.path.isfile(exe):
            raise SkipTest(f"{script} is missing")

        python = self.spec["python"].command
        python(exe, "--comms", "local", "--nworkers", "2")

    def test_uniform_sampling(self):
        """run test_uniform_sampling.py"""
        self.run_tutorial_script("test_uniform_sampling.py")

    def test_1d_sampling(self):
        """run test_1d_sampling.py"""
        self.run_tutorial_script("test_1d_sampling.py")
