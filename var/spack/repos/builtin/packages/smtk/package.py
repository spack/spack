# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.We've put "FIXME"
# next to all the things you 'll want to change. Once you' ve handled
# them, you can save this file and test your package like this:
#
# spack install smtk
#
# You can edit this file again by typing:
#
# spack edit smtk
#
# See the Spack documentation for more information on packaging.
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
from spack.package import *


class Smtk(CMakePackage):
    """SMTK is an open-source, multi-platform Simulation Modeling
    Toolkit. This package includes libraries and plugins for
    working with CAD and other types of models used in simulation
    set up.
    """

    homepage = "https://www.computationalmodelbuilder.org/"
    url = "https://gitlab.kitware.com/cmb/smtk"
    git = "https://gitlab.kitware.com/cmb/smtk.git"

    maintainers = ["kwryankrattiger"]
    tags = ["cmb"]

    version("master", branch="master", submodules=True)

    releases = [
        "22.08.0",
        "22.07.00",
        "22.05.0",
        "22.04.0",
        "22.02.0",
        "21.12.0",
        "21.11.0",
        "21.10.0",
        "21.09.0",
        "21.07.0",
        "21.05.0",
        "21.04.0",
    ]

    for ver in releases:
        version(ver, branch="v{0}".format(ver), submodules=True)

    variant("shared", default=True, description="Build using shared libraries.")
    variant("paraview", default=True, description="Enable ParaView extensions.")
    variant("vtk", default=False, description="Enable VTK extensions.")
    variant("gdal", default=False, description="Enable GDal extensions.")
    variant("python", default=True, description="Enable Python wrappings.")
    variant("qt", default=True, description="Enable Qt extensions", when="+paraview")
    variant("doc", default=False, description="Build documentation")

    boost_libraries = [
        "+atomic",
        "+chrono",
        "+date_time",
        "+filesystem",
        "+iostreams",
        "+log",
        "+program_options",
        "+serialization",
        "+system",
        "+thread",
        "+timer",
    ]
    with when("%gcc@:4.9"):
        boost_libraries.append("+regex")
    depends_on("boost@1.64: " + " ".join(boost_libraries))
    depends_on("eigen")
    depends_on("hdf5")
    depends_on("libarchive")
    depends_on("moab ~mpi ~parmetis")
    depends_on("netcdf-c")
    depends_on("nlohmann-json")
    depends_on("pegtl@2:2.7.1")

    depends_on("gdal@3.5.1", when="+gdal")

    depends_on("paraview +smtk_extensions +visitbridge ~mpi build_edition=canonical", when="+paraview")
    depends_on("paraview +qt", when="+paraview +qt")
    depends_on("paraview ~qt", when="+paraview ~qt")
    depends_on("paraview +gdal", when="+paraview +gdal")
    depends_on("paraview ~gdal", when="+paraview ~gdal")
    depends_on("paraview +python3", when="+paraview +python")
    depends_on("paraview ~python3", when="+paraview ~python")
    depends_on("paraview +shared", when="+paraview +shared")
    depends_on("paraview ~shared", when="+paraview ~shared")
    depends_on("paraview@5.9", when="@21:21.09")
    depends_on("paraview@5.10", when="@21.10:22.02")
    depends_on("paraview@5.11", when="@22.04:")

    extends("python", when="+python")
    depends_on("python@3.6:", when="+python")
    depends_on("py-pybind11", when="+python")
    depends_on("py-matplotlib", when="+python")

    depends_on("py-sphinx", type="build", when="+doc")
    depends_on("doxygen", type="build", when="+doc")

    depends_on("qt@5:", when="+qt")

    depends_on("vtk@9:", when="+vtk ~paraview")

    # Conflicts
    conflicts("+paraview", when="~vtk", msg="SMTK with ParaView support implies VTK support")

    # Patches
    patch("smtk-common-boost-regex.patch", when="@:22.08")

    def cmake_args(self):
        spec = self.spec

        cmake_args = [
            self.define("SMTK_UNIFIED_INSTALL_TREE", True),
            self.define("SMTK_RELOCATABLE_INSTALL", False),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define("CMAKE_INSTALL_RPATH_USE_LINK_PATH", False),
            self.define("SMTK_ENABLE_OPERATION_THREADS", False),
            # Set CMAKE_INSTALL_LIBDIR to "lib" for to
            # override OS - specific libdirs that GNUInstallDirs.cmake would otherwise
            # set.
            self.define("CMAKE_INSTALL_LIBDIR", "lib"),
            self.define("SMTK_RELOCATABLE_INSTALL", True),
            self.define("BUILD_TESTING", False),
            self.define("SMTK_ENABLE_APPLICATIONS", False),
            self.define("SMTK_ENABLE_TESTING", False),
            self.define_from_variant("SMTK_ENABLE_GDAL_SUPPORT", "gdal"),
            self.define_from_variant("SMTK_ENABLE_QT_SUPPORT", "qt"),
            self.define("SMTK_QT_VERSION", "5"),
            self.define_from_variant("SMTK_ENABLE_PARAVIEW_SUPPORT", "paraview"),
            self.define_from_variant("SMTK_ENABLE_EXODUS_SESSION", "paraview"),
            self.define_from_variant("SMTK_ENABLE_PYTHON_WRAPPING", "python"),
            self.define_from_variant("SMTK_ENABLE_MATPLOTLIB", "python"),
            self.define("SMTK_USE_PYBIND11", "python"),
            self.define("PYBIND11_INSTALL", "python"),
            self.define("SMTK_PYTHON_VERSION", "3"),
            self.define("SMTK_ENABLE_PROJECT_UI", True),
            self.define("SMTK_USE_SYSTEM_MOAB", True),
            # This should be off by default because vtkCmbMoabReader in discrete
            # session may only be needed for debugging purpose
            self.define("SMTK_ENABLE_MOAB_DISCRETE_READER", False),
        ]

        if "+paraview" in spec or "+vtk" in spec:
            cmake_args.append(self.define("SMTK_ENABLE_VTK_SUPPORT", True))

        if "+doc" in spec:
            cmake_args.append(self.define("SMTK_BUILD_DOCUMENTATION", "always"))
        else:
            cmake_args.append(self.define("SMTK_BUILD_DOCUMENTATION", "never"))

        return cmake_args

    # def install_plugins(self, spec, prefix):
