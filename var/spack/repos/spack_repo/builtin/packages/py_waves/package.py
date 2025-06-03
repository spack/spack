# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pathlib

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyWaves(PythonPackage):
    """WAVES (LANL code C23004) is a computational science and engineering workflow tool that
    integrates parametric studies with traditional software build systems.
    """

    homepage = "https://lanl-aea.github.io/waves/"
    git = "https://github.com/lanl-aea/waves.git"
    url = "https://github.com/lanl-aea/waves/archive/refs/tags/0.12.5.tar.gz"

    maintainers("kbrindley", "Prabhu-LANL")

    license("BSD-3-Clause", checked_by="kbrindley")

    version("main", branch="main", get_full_repo=True)
    version("0.12.8", sha256="6055b4e92075c0168bf9d85b75375f2f40fa37cd3be2dce80a9b304f3523dc81")
    version("0.12.7", sha256="53d4f389351b89eb9f852f7a999a9119384aa9b62a21c27920de006f37a2e7c4")
    version("0.12.6", sha256="f25ec014b04319512d4227f7f6fb788056de60e5686795d9b5c189f1cc61b7f2")
    version("0.12.5", sha256="3868f1592a21e4b671ed31e66951151d73ff0535e0209c9621629994b25c0cd4")

    depends_on("python@3.9:", type=("build", "run"))

    depends_on("git", when="@develop", type="build")
    depends_on("py-pip", type="build")
    depends_on("py-build", type="build")
    depends_on("py-setuptools@64:", type="build")
    depends_on("py-setuptools-scm@8:", type="build")
    depends_on("scons@4:", type="build")
    # TODO: add upstream spec ``py-sphinx@7.1:`` when py-sphinx-book-theme build allows.
    # Conflicts with py-sphinx-book-theme dependency spec sphinx@4:6
    # Documentation should still build but the ``maximum_signature_line_length`` will have no
    # effect on sphinx<7.1
    depends_on("py-sphinx", type="build")
    depends_on("py-sphinx-argparse", type="build")
    # TODO: add upstream spec ``py-sphinx-copybutton@0.5.1:`` when available
    # Only py-sphinx-copybutton build available in spack is 0.2.12
    # Documentation should still build but the copy button behavior may not work as nicely
    depends_on("py-sphinx-copybutton", type="build")
    depends_on("py-sphinx-book-theme", type="build")
    depends_on("py-sphinx-design", type="build")
    depends_on("py-sphinxcontrib-bibtex", type="build")

    depends_on("py-h5netcdf", type=("run", "test"))
    depends_on("py-h5py", type=("run", "test"))
    depends_on("py-matplotlib", type=("run", "test"))
    depends_on("py-networkx", type=("run", "test"))
    depends_on("py-numpy", type=("run", "test"))
    depends_on("py-pyyaml", type=("run", "test"))
    # SALib 1.4.6 is required for sobol sampler. Most up-to-date version of SALib is 1.4.4.
    # WAVES v0.12.9 upstream will introduce SALib>=1.4.6.
    depends_on("py-salib@1:", type=("run", "test"), when="@:0.12.8")
    depends_on("py-scipy@1.7:", type=("run", "test"))
    depends_on("scons@4:", type=("run", "test"))
    depends_on("py-xarray", type=("run", "test"))

    depends_on("py-pytest", type="test")
    depends_on("py-pytest-xdist", type="test")

    phases = ("install",)

    # Limit import tests to the public API
    import_modules = [
        "waves",
        "waves.exceptions",
        "waves.parameter_generators",
        "waves.scons_extensions",
    ]

    def setup_build_environment(self, env: EnvironmentModifications) -> None:
        env.set("PREFIX", self.prefix)
        env.set("PKG_NAME", "waves")
        if not self.spec.version.isdevelop():
            env.set("SETUPTOOLS_SCM_PRETEND_VERSION", self.version)

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            python("-m", "build", "--no-isolation")
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
                # TODO: Figure out how to override the positional '.' of the spack install options
                # to use the py-build output path instead of overriding the entire default install
                # function Will require the follow on documentation installation logic to be a
                # ``@run_after("install")`` function.
                f"dist/waves-{self.version}.tar.gz",
            )
            scons = which("scons")
            scons("html", "man")

            site_packages_directory = list(pathlib.Path(self.prefix).rglob("**/site-packages"))[0]
            python_package_documentation = python.copy()
            python_package_documentation.add_default_env("SP_DIR", site_packages_directory),
            python_package_documentation("package_documentation.py")

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def install_test(self):
        site_packages_directory = list(pathlib.Path(self.prefix).rglob("**/site-packages"))[0]
        installed_package = site_packages_directory / "waves"
        custom_arguments = ["-vvv", "-n", "4", "-m", "not systemtest"]

        # Until WAVES v0.12.9, the SALib minimum spec is >1. If spack installs SALib <1.4.6, the
        # SALib unit tests fail when trying to import the missing "sobol" module. There is no
        # upstream solution to skip the "sobol" tests without skiping the entire module's tests.
        # Package is functional as long as the end user doesn't try to use the sobol sampler with
        # SALib <1.4.6
        if self.spec.satisfies("@:0.12.8"):
            custom_arguments.insert(0, "--ignore=_tests/test_salib_sampler.py")

        with working_dir(installed_package):
            pytest = which("pytest")
            pytest(*custom_arguments)
