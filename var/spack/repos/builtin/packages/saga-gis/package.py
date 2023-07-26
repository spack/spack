# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class SagaGis(AutotoolsPackage, SourceforgePackage, CMakePackage):
    """
    SAGA is a GIS for Automated Geoscientific Analyses and has been designed
    for an easy and effective implementation of spatial algorithms. It offers
    a comprehensive, growing set of geoscientific methods and provides an
    easily approachable user interface with many visualisation options
    """

    build_system(
        conditional("autotools", when="@:8.2"), conditional("cmake", when="@8.3:"), default="cmake"
    )

    homepage = "http://saga-gis.org/"
    sourceforge_mirror_path = "SAGA%20-%205.0.0/saga-5.0.0.tar.gz"
    git = "git://git.code.sf.net/p/saga-gis/code"

    maintainers("jsquar")

    version("develop", branch="master")
    version("9.1.0", tag="saga-9.1.0")
    version("9.0.3", tag="saga-9.0.3")
    version("8.5.1", tag="saga-8.5.1")
    version("7.4.0", branch="release-7.4.0")
    version("7.3.0", branch="release-7.3.0")
    version("7.1.1", branch="release-7.1.1")
    version("7.1.0", branch="release-7.1.0")
    version("7.0.0", branch="release-7.0.0")
    version("6.4.0", branch="release-6.4.0")
    version("6.3.0", branch="release-6.3.0")
    version("6.2.0", branch="release-6.2.0")
    version("6.1.0", branch="release-6.1.0")
    version("6.0.0", branch="release-6.0.0")
    version("5.0.1", branch="release-5-0-1")
    version("5.0.0", branch="release-5.0.0")
    version("4.1.0", branch="release-4.1.0")
    version("4.0.0", branch="release-4.0.0")
    version("3.0.0", branch="release-3.0.0", deprecated=True)
    version("2.3-lts", branch="release-2-3-lts", deprecated=True)
    version("2.3.1", branch="release-2-3-1", deprecated=True)
    version("2.3.0", branch="release-2-3-0", deprecated=True)

    variant("gui", default=True, description="Build GUI and interactive SAGA tools")
    # non free for commercial use
    variant(
        "libfire",
        default=True,
        description="Build tool using BEHAVE fire modeling system (non free for commercial usage)",
    )

    variant("openmp", default=True, description="Build with OpenMP enabled")
    # triangle non free for commercial use
    variant(
        "convex_lib",
        default="triangle",
        values=["qhull", "triangle"],
        multi=False,
        when="@:8",
        description=(
            "Implementation of convex hull algorithms "
            "(triangle is only free for non-commercial usage"
        ),
    )
    variant("python", default=True, description="Build Python extension")
    variant("postgresql", default=True, description="Build tools using PostgreSQL")
    variant("opencv", default=True, description="Build tools using OpenCV")

    variant("haru", default=True, description="Enable PDF creation using Haru")
    variant("vigra", default=True, description="Build tools using VIGRA")
    variant("curl", default=True, description="Enable https support in webservices")

    depends_on("autoconf", type="build", when="@7.4.0 build_system=autotools")
    depends_on("automake", type="build", when="@7.4.0 build_system=autotools")
    depends_on("libtool", type="build", when="@7.4.0 build_system=autotools")
    # avoid deprecation warning of distutils, which makes configure fail https://peps.python.org/pep-0632/
    depends_on("python@:3.9", type=["build", "run"], when="build_system=autotools +python")
    depends_on("python", type=["build", "run"], when="+python")

    depends_on("wxwidgets")
    # SAGA-GIS requires projects.h from proj
    depends_on("proj")
    # https://sourceforge.net/p/saga-gis/bugs/271/
    depends_on("proj@:5", when="@:7.3")
    depends_on("gdal+hdf5+netcdf")
    depends_on("gdal@2.3:2.4+grib+hdf5+netcdf", when="@:7.2")
    depends_on("libgeotiff@:1.4", when="@:7.2")
    depends_on("libgeotiff")
    depends_on("unixodbc")
    depends_on("libharu", when="+haru")
    depends_on("postgresql")
    # Saga-Gis depends on legacy opencv API removed in opencv 4.x
    depends_on("opencv@:3.4.6+jpeg+video+objdetect+ml+openmp+photo", when="+opencv")
    depends_on("jpeg", when="+opencv")
    depends_on("vigra", when="+vigra")
    depends_on("hdf5")
    depends_on("swig", type="build", when="+python")

    extends("python", when="+python")

    configure_directory = "saga-gis"
    root_cmakelists_dir = "saga-gis"

    def patch(self):
        if "+opencv" in self.spec:
            opencv_dir = self.spec["opencv"].prefix
            opencv_makefile = join_path(
                "saga-gis", "src", "tools", "imagery", "imagery_opencv", "Makefile.am"
            )

            filter_file(r"/usr(/include/opencv)", r"{0}\1".format(opencv_dir), opencv_makefile)

    def cmake_args(self):
        args = []
        args += [self.define_from_variant("WITH_FIRE_SPREADING", "libfire")]
        args += [self.define_from_variant("WITH_GUI", "gui")]
        args += [self.define_from_variant("WITH_PYTHON", "python")]
        args += [self.define_from_variant("WITH_TOOLS_POSTGRES", "postgresql")]
        args += [self.define_from_variant("WITH_TOOLS_VIGRA", "vigra")]

        # avoid to use newer system installation of python
        # https://gitlab.kitware.com/cmake/cmake/-/issues/21186
        args += [self.define("CMAKE_POLICY_DEFAULT_CMP0094", "NEW")]
        return args

    def configure_args(self):
        args = []
        args += self.enable_or_disable("gui")
        args += self.enable_or_disable("libfire")
        args += self.enable_or_disable("openmp")
        args += self.enable_or_disable("python")
        args += self.with_or_without("postgresql")
        if "convex_lib" in self.spec and self.spec["convex_lib"] == "qhull":
            args += ["--disable-triangle"]

        return args

    def setup_run_environment(self, env):
        # Point saga to its tool set, will be loaded during runtime
        env.set("SAGA_MLB", self.prefix.lib.saga)
        env.set("SAGA_TLB", self.prefix.lib.saga)
