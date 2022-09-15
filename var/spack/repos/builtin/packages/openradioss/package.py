# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import inspect
import os
from shutil import move

from spack.package import *


class Openradioss(CMakePackage):
    """Altair Radioss is an industry-proven analysis solution that helps users evaluate and
    optimize product performance for highly nonlinear problems under dynamic loadings. For more
    than 30 years, organizations have used Altair Radioss to streamline and optimize the digital
    design process, replace costly physical tests with quick and efficient simulation, and speed
    up design optimization iterations – all so users and organizations can improve product quality,
    reduce costs, and shorten development cycles."""

    homepage = "https://www.openradioss.org/"
    url = "https://github.com/OpenRadioss/OpenRadioss/archive/refs/tags/latest-20220914.tar.gz"

    version("20220914", sha256="8e160707dacd729c72ebeb7c6ef4daa10d71859c444f00810c4896dc2f6edd0a")

    variant(
        "arch",
        values=["linux64_gf"],
        default="linux64_gf",
        multi=False,
        description="Architecture and Compiler",
    )

    variant(
        "precision",
        values=["sp", "dp"],
        multi=False,
        default="dp",
        description="set precision - dp (default) |sp",
    )

    variant(
        "debug",
        values=["0", "1", "2"],
        multi=False,
        default="0",
        description="debug version 0 no debug flags (default), 1 usual debug flag",
    )

    variant("static-link", default=False, description="Enable static linked binary.")

    variant("mpi", default=False, description="Enable MPI support")

    variant(
        "build_type",
        default="Release",
        description="CMake build type",
        values=("Debug", "Release", "None"),
    )

    depends_on("cmake@2.8:", type="build")
    depends_on("openmpi", type=["link", "run"], when="+mpi")

    # TODO: Add aocc
    # Only gcc supported
    for __compiler in spack.compilers.supported_compilers():
        if __compiler != "gcc":
            conflicts("%{}".format(__compiler))

    def cmake_args(self):
        spec = self.spec
        debug = spec.variants["debug"].value

        if debug == "2":
            sanitize = "1"
        else:
            sanitize = "0"

        if "+mpi" in spec:
            mpi_def = [
                self.define("MPI", "ompi"),
                self.define("mpi_root", spec["mpi"].prefix),
                self.define("mpi_libdir", spec["mpi"].prefix.lib),
                self.define("mpi_incdir", spec["mpi"].prefix.include),
            ]
        else:
            mpi_def = [self.define("MPI", "smp")]

        args = [
            self.define_from_variant("arch", "arch"),
            self.define_from_variant("precision", "precision"),
            self.define_from_variant("debug", "debug"),
            self.define_from_variant("static_link", "static-link"),
            self.define("sanitize", sanitize),
        ] + mpi_def

        return args

    # Openradioss contains two separate cmake projects
    # We install "engine" using the default cmake(), build() provided by
    # CmakePackage and "starter" by repeating those two functions.
    @property
    def root_cmakelists_dir(self):
        return "engine"

    @property
    def build_directory(self):
        return os.path.join(self.stage.source_path, self.root_cmakelists_dir, "build_dir")

    # Run cmake in "starter" directory as well. This is a copy of lib/spack/spack/build_systems.py:cmake()
    @run_before("cmake")
    def cmake_starter(self):
        """Runs ``cmake`` in the build directory"""
        options = self.std_cmake_args
        options += self.cmake_args()
        options.append(os.path.abspath("starter"))
        with working_dir(
            os.path.join(self.stage.source_path, "starter", "build_dir"), create=True
        ):
            inspect.getmodule(self).cmake(*options)

    # Run build in "starter" directory as well. This is a copy of lib/spack/spack/build_systems.py:build()
    @run_before("build")
    def build_starter(self):
        """Make the build targets"""
        with working_dir(os.path.join(self.stage.source_path, "starter", "build_dir")):
            if self.generator == "Unix Makefiles":
                inspect.getmodule(self).make(*self.build_targets)
            elif self.generator == "Ninja":
                self.build_targets.append("-v")
                inspect.getmodule(self).ninja(*self.build_targets)

    def install(self, spec, prefix):
        """Installation is just moving executables."""
        if spec.variants["debug"].value == "1":
            ddebug = "_db"
        else:
            ddebug = ""
        if spec.variants["precision"].value == "sp":
            suffix = "_sp"
        else:
            suffix = ""
        extension = "_" + spec.variants["arch"].value + suffix + ddebug
        os.mkdir(self.prefix.bin)
        os.mkdir(self.prefix.lib64)

        move(
            os.path.join(self.stage.source_path, "starter", "build_dir", "starter" + extension),
            os.path.join(self.prefix.bin, "starter" + extension),
        )
        if "+mpi" in spec:
            extension = "_" + spec.variants["arch"].value + "_ompi" + suffix + ddebug
        move(
            os.path.join(self.build_directory, "engine" + extension),
            os.path.join(self.prefix.bin, "engine" + extension),
        )
        move(
            os.path.join(
                self.stage.source_path, "extlib/hm_reader/linux64/libhm_reader_linux64.so"
            ),
            os.path.join(self.prefix.lib64, "libhm_reader_linux64.so"),
        )
        move(
            os.path.join(self.stage.source_path, "extlib/h3d/lib/linux64/libh3dwriter.so"),
            os.path.join(self.prefix.lib64, "libh3dwriter.so"),
        )
        move(
            os.path.join(self.stage.source_path, "hm_cfg_files"),
            os.path.join(self.prefix, "hm_cfg_files"),
        )

    def setup_run_environment(self, env):
        env.set("RAD_CFG_PATH", os.path.join(self.prefix, "hm_cfg_files"))
        env.set("OMP_STACKSIZE", "400m")
