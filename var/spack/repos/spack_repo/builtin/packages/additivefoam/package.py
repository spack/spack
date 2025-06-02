# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import inspect
import os

from spack_repo.builtin.build_systems.generic import Package

from spack.package import *

from ..openfoam import package as openfoam


class Additivefoam(Package):
    """AdditiveFOAM is a heat and mass transfer software for Additive Manufacturing (AM)"""

    homepage = "https://ornl.github.io/AdditiveFOAM/"
    git = "https://github.com/ORNL/AdditiveFOAM.git"
    url = "https://github.com/ORNL/AdditiveFOAM/archive/1.1.0.tar.gz"

    maintainers("streeve", "colemanjs", "gknapp1")

    tags = ["ecp"]

    license("GPL-3.0-only")

    version("main", branch="main")
    version("1.1.0", sha256="a13770bd66fe10224705fb3a2bfb557e63e0aea98c917b0084cf8b91eaa53ee2")
    version("1.0.0", sha256="abbdf1b0230cd2f26f526be76e973f508978611f404fe8ec4ecdd7d5df88724c")

    depends_on("cxx", type="build")  # generated

    depends_on("openfoam-org@10")

    common = []
    assets = ["Allwmake"]

    build_script = "./Allwmake"

    phases = ["configure", "build", "install"]

    def add_extra_files(self, common, local_prefix, local):
        """Copy additional common and local files into the stage.source_path
        from the openfoam/common and the package/assets directories,
        respectively. Modified from `..openfoam.package.OpenFoam.add_extra_files()`.
        """
        outdir = self.stage.source_path
        indir = join_path(os.path.dirname(inspect.getfile(openfoam)), "common")
        for f in common:
            tty.info("Added file {0}".format(f))
            openfoam.install(join_path(indir, f), join_path(outdir, f))

        indir = join_path(self.package_dir, "assets", local_prefix)
        for f in local:
            tty.info("Added file {0}".format(f))
            openfoam.install(join_path(indir, f), join_path(outdir, f))

    def patch(self):
        """Patches build by adding Allwmake from the asset directory based on
        the spec version.

        For all versions after 1.0.0 there is an Allwmake script in
        the AdditiveFOAM repository that can be called by the spack assets_main/Allwmake
        script, whereas the assets_1.0.0/Allwmake script contains the
        build instructions."""
        spec = self.spec
        asset_dir = "assets_main"
        if Version("1.0.0") in spec.versions:
            asset_dir = "assets_1.0.0"
        self.add_extra_files(self.common, asset_dir, self.assets)

    def setup_build_environment(self, env):
        """Set up the build environment variables."""

        # Ensure that the directories exist
        mkdirp(self.prefix.bin)
        mkdirp(self.prefix.lib)

        # Add to the environment
        env.set("FOAM_USER_APPBIN", self.prefix.bin)
        env.set("FOAM_USER_LIBBIN", self.prefix.lib)

    def setup_run_environment(self, env):
        """Set up the run environment variables."""

        # Add to the environment
        env.prepend_path("PATH", self.prefix.bin)
        env.prepend_path("LD_LIBRARY_PATH", self.prefix.lib)

    def activate(self, spec, prefix):
        """Activate the package to modify the environment."""
        self.setup_run_environment(self.spec.environment())

    def deactivate(self, spec, prefix):
        """Deactivate the package and clean up the environment."""
        env = self.spec.environment()
        env.pop("FOAM_USER_APPBIN", None)
        env.pop("FOAM_USER_LIBBIN", None)

    def configure(self, spec, prefix):
        """Configure the environment for building."""
        pass

    def build(self, spec, prefix):
        """Build with Allwmake script, wrapped to source environment first."""
        args = []
        if self.parallel:  # Parallel build? - pass via environment
            os.environ["WM_NCOMPPROCS"] = str(make_jobs)
        builder = Executable(self.build_script)
        builder(*args)

    def install(self, spec, prefix):
        """Install under the prefix directory"""

        for f in ["README.md", "LICENSE"]:
            if os.path.isfile(f):
                install(f, join_path(self.prefix, f))

        dirs = ["tutorials", "applications"]
        for d in dirs:
            if os.path.isdir(d):
                install_tree(d, join_path(self.prefix, d), symlinks=True)
