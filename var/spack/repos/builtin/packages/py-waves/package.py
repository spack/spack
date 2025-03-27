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

import shutil
import pathlib

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

    variant("docs", default=False, description="Build HTML documentation")

    depends_on("python@3.9:", type=("build", "run"))

    depends_on("git", when="@develop", type="build")
    depends_on("py-pip", type="build")
    depends_on("py-build", type="build")
    depends_on("py-setuptools@64:", type="build")
    depends_on("py-setuptools-scm@8:", type="build")

    depends_on("scons@4:", type="build", when="+docs")
    # Conflicts with py-sphinx-book-theme dependencies sphinx@4:6
    # Documentation should still build but the ``maximum_signature_line_length`` will have no effect on sphinx<7.1
    #depends_on("py-sphinx@7.1:", type="build", when="+docs")
    depends_on("py-sphinx", type="build", when="+docs")
    depends_on("py-sphinx-argparse", type="build", when="+docs")
    # Only py-sphinx-copybutton build available in spack is 0.2.12
    #depends_on("py-sphinx-copybutton@0.5.1:", type="build", when="+docs")
    depends_on("py-sphinx-copybutton", type="build", when="+docs")
    depends_on("py-sphinx-book-theme", type="build", when="+docs")
    depends_on("py-sphinx-design", type="build", when="+docs")
    depends_on("py-sphinxcontrib-bibtex", type="build", when="+docs")

    depends_on("py-h5netcdf", type=("run", "test"))
    depends_on("py-h5py", type=("run", "test"))
    depends_on("py-matplotlib", type=("run", "test"))
    depends_on("py-networkx", type=("run", "test"))
    depends_on("py-numpy", type=("run", "test"))
    depends_on("py-pyyaml", type=("run", "test"))
    # SALib 1.4.6 is required for sobol sampler. Most up-to-date version of SALib is 1.4.4.
    # WAVES v0.12.9 upstream will introduce SALib>=1.4.6.
    depends_on("py-salib@1.4.6:", type=("run", "test"), when="@0.12.9:")
    depends_on("py-salib@1:", type=("run", "test"), when="@:0.12.8")
    depends_on("py-scipy@1.7:", type=("run", "test"))
    depends_on("scons@4:", type=("run", "test"))
    depends_on("py-xarray", type=("run", "test"))

    depends_on("py-pytest", type="test")
    depends_on("py-pytest-xdist", type="test")

    phases = ("build", "install")

    def setup_build_environment(self, env):
        if not self.spec.version.isdevelop():
            env.set("SETUPTOOLS_SCM_PRETEND_VERSION", self.version)

    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            # TODO: Patch upstream MANIFEST.in to include these files in py-build/pip package builds
            shutil.copy2("pyproject.toml", "waves/")
            shutil.copy2("README.rst", "waves/")

            if "+docs" in self.spec:
                scons = which("scons")
                scons("html", "man")
                # FIXME: Is there a spack preferred API for including additional files in the build?
                documentation_directory = pathlib.Path("waves/docs")
                #documentation_directory.mkdir(parents=True, exist_ok=True)
                shutil.copytree(
                    pathlib.Path("build/docs/html"),
                    documentation_directory,
                    symlinks=False,
                    #dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns(".doctrees", "*.doctree", ".buildinfo"),
                )
                shutil.copy2(pathlib.Path("build/docs/man/waves.1"), documentation_directory)

            python("-m", "build", "--no-isolation")

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            # TODO: install the man page to a spack recognized MANPATH
            python(
                # Using the spack default python package install options
                "-m",
                "pip",
                "-vvv",
                "--no-input",
                "--no-cache-dir",
                "--disable-pip-version-check",
                "install",
                "--no-deps",
                "--ignore-installed",
                "--no-build-isolation",
                "--no-warn-script-location",
                "--no-index",
                f"--prefix={prefix}",
                # TODO: Figure out how to override the positional '.' of the spack install options to use following
                f"dist/waves-{self.version}.tar.gz",
            )
            if "+docs" in self.spec:
                man_page = pathlib.Path(self.prefix.site_packages_dir) / "waves/docs/waves.1"
                man_directory = pathlib.Path(self.prefix) / "man/man1"
                man_directory.mkdir(parents=True, exists_ok=True)
                share_man_directory = pathlib.Path(self.prefix) / "share/man/man1"
                share_man_directory.mkdir(parents=True, exists_ok=True)
                shutil.copy2(man_page, man_directory)
                shutil.copy2(man_page, share_man_directory)

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def install_test(self):
        installed_package = pathlib.Path(self.prefix.site_packages_dir) / "waves"
        with working_dir(installed_package):
            pytest = which("pytest")
            pytest("-vvv", "-n", "4", "-m", "not systemtest")
