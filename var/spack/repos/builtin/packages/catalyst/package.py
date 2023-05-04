# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import subprocess
import sys

import llnl.util.tty as tty

from spack.package import *


class Catalyst(CMakePackage):
    """Catalyst is an in situ library, with an adaptable application
    programming interface (API), that orchestrates the alliance
    between simulation and analysis and/or visualization tasks. For
    versions 5.7 and greater use the paraview package.

    """

    homepage = "http://www.paraview.org"
    url = "https://www.paraview.org/files/v5.6/ParaView-v5.6.0.tar.xz"

    maintainers("chuckatkins", "danlipsa")

    version("5.6.0", sha256="5b49cb96ab78eee0427e25200530ac892f9a3da7725109ce1790f8010cb5b377")

    variant("python", default=False, description="Enable Python support")
    variant("essentials", default=False, description="Enable Essentials support")
    variant("extras", default=False, description="Enable Extras support. Implies Essentials.")
    variant(
        "rendering",
        default=True,
        description="Enable Rendering support. Implies Extras and Essentials.",
    )
    variant("osmesa", default=True, description="Use offscreen rendering")
    conflicts("+osmesa", when="~rendering")

    extends("python", when="+python")
    # VTK < 8.2.1 can't handle Python 3.8
    # This affects Paraview <= 5.7 (VTK 8.2.0)
    # https://gitlab.kitware.com/vtk/vtk/-/issues/17670
    depends_on("python@3:3.7", when="@:5.7 +python", type=("build", "run"))
    depends_on("python@3:", when="@5.8:+python", type=("build", "run"))

    depends_on("git", type="build")
    depends_on("mpi")

    depends_on("py-numpy", when="+python", type=("build", "run"))
    depends_on("py-mpi4py", when="+python", type=("build", "run"))

    depends_on("gl@3.2:", when="+rendering")
    depends_on("osmesa", when="+osmesa")
    depends_on("glx", when="~osmesa")
    depends_on("cmake@3.3:", type="build")

    @property
    def paraview_subdir(self):
        """The paraview subdirectory name as paraview-major.minor"""
        return "paraview-{0}".format(self.spec.version.up_to(2))

    @property
    def editions(self):
        """Transcribe spack variants into names of Catalyst Editions"""
        selected = ["Base"]  # Always required

        if "+python" in self.spec:
            selected.append("Enable-Python")

        if "+essentials" in self.spec:
            selected.append("Essentials")

        if "+extras" in self.spec:
            selected.append("Essentials")
            selected.append("Extras")

        if "+rendering" in self.spec:
            selected.append("Essentials")
            selected.append("Extras")
            selected.append("Rendering-Base")

        return selected

    def do_stage(self, mirror_only=False):
        """Unpacks and expands the fetched tarball.
        Then, generate the catalyst source files."""
        super(Catalyst, self).do_stage(mirror_only)

        # extract the catalyst part
        catalyst_script = os.path.join(self.stage.source_path, "Catalyst", "catalyze.py")
        editions_dir = os.path.join(self.stage.source_path, "Catalyst", "Editions")
        catalyst_source_dir = os.path.abspath(self.root_cmakelists_dir)

        python_path = os.path.realpath(
            self.spec["python"].command.path if "+python" in self.spec else sys.executable
        )

        command = [
            python_path,
            catalyst_script,
            "-r",
            self.stage.source_path,
            "-o",
            catalyst_source_dir,
        ]

        for edition in self.editions:
            command.extend(["-i", os.path.join(editions_dir, edition)])

        if not os.path.isdir(catalyst_source_dir):
            os.mkdir(catalyst_source_dir)
            subprocess.check_call(command)
            tty.msg("Generated catalyst source in %s" % self.stage.source_path)
        else:
            tty.msg("Already generated %s in %s" % (self.name, self.stage.source_path))

    def setup_run_environment(self, env):
        # paraview 5.5 and later
        # - cmake under lib/cmake/paraview-5.5
        # - libs  under lib
        # - python bits under lib/python2.8/site-packages
        if os.path.isdir(self.prefix.lib64):
            lib_dir = self.prefix.lib64
        else:
            lib_dir = self.prefix.lib

        env.set("ParaView_DIR", self.prefix)
        env.prepend_path("LIBRARY_PATH", lib_dir)
        env.prepend_path("LD_LIBRARY_PATH", lib_dir)

        if "+python" in self.spec:
            python_version = self.spec["python"].version.up_to(2)
            env.prepend_path(
                "PYTHONPATH",
                join_path(lib_dir, "python{0}".format(python_version), "site-packages"),
            )

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set("ParaView_DIR", self.prefix)

    @property
    def root_cmakelists_dir(self):
        """The relative path to the directory containing CMakeLists.txt

        This path is relative to the root of the extracted tarball,
        not to the ``build_directory``. Defaults to the current directory.

        :return: directory containing CMakeLists.txt
        """
        return os.path.join(self.stage.source_path, "Catalyst-v" + str(self.version))

    @property
    def build_directory(self):
        """Returns the directory to use when building the package

        :return: directory where to build the package
        """
        return join_path(os.path.abspath(self.root_cmakelists_dir), "spack-build")

    def cmake_args(self):
        """Populate cmake arguments for Catalyst."""
        spec = self.spec

        def variant_bool(feature, on="ON", off="OFF"):
            """Ternary for spec variant to ON/OFF string"""
            if feature in spec:
                return on
            return off

        def nvariant_bool(feature):
            """Negated ternary for spec variant to OFF/ON string"""
            return variant_bool(feature, on="OFF", off="ON")

        cmake_args = [
            "-DPARAVIEW_GIT_DESCRIBE=v%s" % str(self.version),
            "-DVTK_USE_SYSTEM_EXPAT:BOOL=ON",
            "-DVTK_USE_X:BOOL=%s" % nvariant_bool("+osmesa"),
            "-DVTK_USE_OFFSCREEN:BOOL=%s" % variant_bool("+osmesa"),
            "-DVTK_OPENGL_HAS_OSMESA:BOOL=%s" % variant_bool("+osmesa"),
        ]
        if "+python" in spec:
            cmake_args.extend(
                [
                    "-DPARAVIEW_ENABLE_PYTHON:BOOL=ON",
                    "-DPYTHON_EXECUTABLE:FILEPATH=%s" % spec["python"].command.path,
                    "-DVTK_USE_SYSTEM_MPI4PY:BOOL=ON",
                ]
            )
        else:
            cmake_args.append("-DPARAVIEW_ENABLE_PYTHON:BOOL=OFF")

        if spec.platform == "linux" and spec.target.family == "aarch64":
            cmake_args.append("-DCMAKE_CXX_FLAGS=-DPNG_ARM_NEON_OPT=0")
            cmake_args.append("-DCMAKE_C_FLAGS=-DPNG_ARM_NEON_OPT=0")

        return cmake_args

    def cmake(self, spec, prefix):
        """Runs ``cmake`` in the build directory through the cmake.sh script"""
        cmake_script_path = os.path.join(os.path.abspath(self.root_cmakelists_dir), "cmake.sh")
        with working_dir(self.build_directory, create=True):
            subprocess.check_call(
                [cmake_script_path, os.path.abspath(self.root_cmakelists_dir)]
                + self.cmake_args()
                + self.std_cmake_args
            )
