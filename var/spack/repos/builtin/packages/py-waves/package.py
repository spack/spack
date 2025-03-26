# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
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
#     spack install waves
#
# You can edit this file again by typing:
#
#     spack edit waves
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class PyWaves(PythonPackage):
    """WAVES (LANL code C23004) is a computational science and engineering workflow tool that integrates parametric
    studies with traditional software build systems.
    """

    homepage = "https://lanl-aea.github.io/waves/"
    git = "https://github.com/lanl-aea/waves.git"
    url = "https://github.com/lanl-aea/waves/archive/refs/tags/0.12.5.tar.gz"

    maintainers("kbrindley", "Prabhu-LANL")

    license("BSD-3-Clause", checked_by="kbrindley")

    version("develop", branch="main", get_full_repo=True)
    version("0.12.5", sha256="3868f1592a21e4b671ed31e66951151d73ff0535e0209c9621629994b25c0cd4")

    depends_on("python@3.9", type=("build", "run"))

    depends_on("git", when="@develop", type="build")
    depends_on("py-pip", type="build")
    depends_on("py-build", type="build")
    #depends_on("py-setuptools@64", type="build")
    depends_on("py-setuptools", type="build")
    #depends_on("py-setuptools-scm@8", type="build")
    depends_on("py-setuptools-scm", type="build")

    depends_on("py-h5netcdf", type="run")
    depends_on("py-h5py", type="run")
    depends_on("py-matplotlib", type="run")
    depends_on("py-networkx", type="run")
    depends_on("py-numpy", type="run")
    depends_on("py-pyyaml", type="run")
    #depends_on("py-salib@1", type="run")
    depends_on("py-salib", type="run")
    #depends_on("py-scipy@1.7", type="run")
    depends_on("py-scipy", type="run")
    depends_on("scons@4", type="run")
    depends_on("py-xarray", type="run")

    depends_on("py-pytest", type="test")

    def setup_build_environment(self, env):
        if not self.spec.version.isdevelop():
            env.set("SETUPTOOLS_SCM_PRETEND_VERSION", self.version)

    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            python("-m build --no-isolation")

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def build_test(self):
        pytest = which("pytest")
        pytest("waves")
