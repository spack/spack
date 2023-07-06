# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Vtk(CMakePackage):
    """The Visualization Toolkit (VTK) is an open-source, freely
    available software system for 3D computer graphics, image
    processing and visualization."""

    homepage = "https://www.vtk.org"
    url = "https://www.vtk.org/files/release/9.0/VTK-9.0.0.tar.gz"
    list_url = "https://www.vtk.org/download/"

    maintainers("chuckatkins", "danlipsa")

    version("9.2.6", sha256="06fc8d49c4e56f498c40fcb38a563ed8d4ec31358d0101e8988f0bb4d539dd12")
    version("9.2.2", sha256="1c5b0a2be71fac96ff4831af69e350f7a0ea3168981f790c000709dcf9121075")
    version("9.1.0", sha256="8fed42f4f8f1eb8083107b68eaa9ad71da07110161a3116ad807f43e5ca5ce96")
    version("9.0.3", sha256="bc3eb9625b2b8dbfecb6052a2ab091fc91405de4333b0ec68f3323815154ed8a")
    version("9.0.1", sha256="1b39a5e191c282861e7af4101eaa8585969a2de05f5646c9199a161213a622c7")
    version("9.0.0", sha256="15def4e6f84d72f82386617fe595ec124dda3cbd13ea19a0dcd91583197d8715")
    version("8.2.0", sha256="34c3dc775261be5e45a8049155f7228b6bd668106c72a3c435d95730d17d57bb")
    version("8.1.2", sha256="0995fb36857dd76ccfb8bb07350c214d9f9099e80b1e66b4a8909311f24ff0db")
    version("8.1.1", sha256="71a09b4340f0a9c58559fe946dc745ab68a866cf20636a41d97b6046cb736324")
    version("8.1.0", sha256="6e269f07b64fb13774f5925161fb4e1f379f4e6a0131c8408c555f6b58ef3cb7")
    version("8.0.1", sha256="49107352923dea6de05a7b4c3906aaf98ef39c91ad81c383136e768dcf304069")
    version("7.1.0", sha256="5f3ea001204d4f714be972a810a62c0f2277fbb9d8d2f8df39562988ca37497a")
    version("7.0.0", sha256="78a990a15ead79cdc752e86b83cfab7dbf5b7ef51ba409db02570dbdd9ec32c3")
    version("6.3.0", sha256="92a493354c5fa66bea73b5fc014154af5d9f3f6cee8d20a826f4cd5d4b0e8a5e")
    version("6.1.0", sha256="bd7df10a479606d529a8b71f466c44a2bdd11fd534c62ce0aa44fad91883fa34")

    # VTK7 defaults to OpenGL2 rendering backend
    variant("opengl2", default=True, description="Enable OpenGL2 backend")
    variant("osmesa", default=False, description="Enable OSMesa support")
    variant("python", default=False, description="Enable Python support", when="@8:")
    variant("qt", default=False, description="Build with support for Qt")
    variant("xdmf", default=False, description="Build XDMF file support")
    variant("ffmpeg", default=False, description="Build with FFMPEG support")
    variant("mpi", default=True, description="Enable MPI support")

    patch("gcc.patch", when="@6.1.0")
    # patch to fix some missing stl includes
    # which lead to build errors on newer compilers

    patch(
        "https://gitlab.kitware.com/vtk/vtk/-/commit/e066c3f4fbbfe7470c6207db0fc3f3952db633c.diff",
        when="@9:9.0",
        sha256="0546696bd02f3a99fccb9b7c49533377bf8179df16d901cefe5abf251173716d",
    )

    # Patch for paraview 5.10: +hdf5 ^hdf5@1.13.2:
    # https://gitlab.kitware.com/vtk/vtk/-/merge_requests/9690
    patch("xdmf2-hdf51.13.2.patch", when="@9:9.2 +xdmf")

    # We cannot build with both osmesa and qt in spack
    conflicts("+osmesa", when="+qt")

    with when("+python"):
        # Depend on any Python, add bounds below.
        extends("python@2.7:", type=("build", "run"))
        # Python 3.8 support from vtk 9
        depends_on("python@:3.7", when="@:8", type=("build", "run"))
        # Python 3.10 support from vtk 9.2
        depends_on("python@:3.9", when="@:9.1", type=("build", "run"))

    # We need mpi4py if buidling python wrappers and using MPI
    depends_on("py-mpi4py", when="+python+mpi", type="run")

    # python3.7 compatibility patch backported from upstream
    # https://gitlab.kitware.com/vtk/vtk/commit/706f1b397df09a27ab8981ab9464547028d0c322
    patch("python3.7-const-char.patch", when="@7.0.0:8.1.1 ^python@3.7:")

    # Broken downstream FindMPI
    patch("vtkm-findmpi-downstream.patch", when="@9.0.0")

    # use internal FindHDF5
    patch("internal_findHDF5.patch", when="@:8")

    # Fix IOADIOS2 module to work with kits
    # https://gitlab.kitware.com/vtk/vtk/-/merge_requests/8653
    patch("vtk-adios2-module-no-kit.patch", when="@8.2.0:9.0.3")

    # The use of the OpenGL2 backend requires at least OpenGL Core Profile
    # version 3.2 or higher.
    depends_on("gl@3.2:", when="+opengl2")
    depends_on("gl@1.2:", when="~opengl2")

    with when("~osmesa"):
        depends_on("glx", when="platform=linux")
        depends_on("glx", when="platform=cray")
        depends_on("libxt", when="platform=linux")
        depends_on("libxt", when="platform=cray")

    depends_on("osmesa", when="+osmesa")

    # VTK will need Qt5OpenGL, and qt needs '-opengl' for that
    depends_on("qt+opengl", when="+qt")

    depends_on("boost", when="+xdmf")
    depends_on("boost+mpi", when="+xdmf +mpi")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants, when="+xdmf")
    depends_on("ffmpeg", when="+ffmpeg")
    depends_on("mpi", when="+mpi")

    depends_on("expat")
    # See <https://gitlab.kitware.com/vtk/vtk/-/issues/18033> for why vtk doesn't
    # work yet with freetype 2.10.3 (including possible patches)
    depends_on("freetype @:2.10.2", when="@:9.0.1")
    depends_on("freetype")
    depends_on("glew")
    depends_on("hdf5~mpi", when="~mpi")
    depends_on("hdf5+mpi", when="+mpi")
    depends_on("hdf5@1.8:", when="@8:9.0")
    depends_on("hdf5@1.10:", when="@9.1:")
    depends_on("jpeg")
    depends_on("jsoncpp")
    depends_on("libxml2")
    depends_on("lz4")
    depends_on("netcdf-c~mpi", when="~mpi")
    depends_on("netcdf-c+mpi", when="+mpi")
    depends_on("netcdf-cxx")
    depends_on("libpng")
    depends_on("libtiff")
    depends_on("zlib")
    depends_on("eigen", when="@8.2.0:")
    depends_on("double-conversion", when="@8.2.0:")
    depends_on("sqlite", when="@8.2.0:")
    depends_on("pugixml", when="@9:")
    depends_on("libogg")
    depends_on("libtheora")
    depends_on("utf8cpp", when="@9:")
    depends_on("gl2ps", when="@8.1:")
    depends_on("gl2ps@1.4.1:", when="@9:")
    depends_on("proj@4", when="@8.2")
    depends_on("proj@4:7", when="@9:")
    depends_on("cgns@4.1.1:+mpi", when="@9.1: +mpi")
    depends_on("cgns@4.1.1:~mpi", when="@9.1: ~mpi")
    depends_on("seacas@2021-05-12:+mpi", when="@9.1: +mpi")
    depends_on("seacas@2021-05-12:~mpi", when="@9.1: ~mpi")
    depends_on("nlohmann-json", when="@9.2:")

    # For finding Fujitsu-MPI wrapper commands
    patch("find_fujitsu_mpi.patch", when="@:8.2.0%fj")
    # Freetype@2.10.3 no longer exports FT_CALLBACK_DEF, this
    # patch replaces FT_CALLBACK_DEF with simple extern "C"
    # See https://gitlab.kitware.com/vtk/vtk/-/issues/18033
    patch(
        "https://gitlab.kitware.com/vtk/vtk/uploads/c6fa799a1a028b8f8a728a40d26d3fec/vtk-freetype-2.10.3-replace-FT_CALLBACK_DEF.patch",
        sha256="eefda851f844e8a1dfb4ebd8a9ff92d2b78efc57f205774052c5f4c049cc886a",
        when="@:9.0.1 ^freetype@2.10.3:",
    )

    patch(
        "https://gitlab.kitware.com/vtk/vtk/-/commit/5a1c96e12e9b4a660d326be3bed115a2ceadb573.patch",
        sha256="65175731c080961f85d779d613ac1f6bce89783745e54e864edec7637b03b18a",
        when="@9.1",
    )

    def url_for_version(self, version):
        url = "http://www.vtk.org/files/release/{0}/VTK-{1}.tar.gz"
        return url.format(version.up_to(2), version)

    def setup_build_environment(self, env):
        # VTK has some trouble finding freetype unless it is set in
        # the environment
        env.set("FREETYPE_DIR", self.spec["freetype"].prefix)

        # Force API compatibility with HDF5
        if "+hdf5" in self.spec:
            if "@9.1:" in self.spec:
                env.append_flags("CFLAGS", "-DH5_USE_110_API")
                env.append_flags("CXXFLAGS", "-DH5_USE_110_API")
            elif "@8:" in self.spec:
                env.append_flags("CFLAGS", "-DH5_USE_18_API")
                env.append_flags("CXXFLAGS", "-DH5_USE_18_API")

    def cmake_args(self):
        spec = self.spec

        opengl_ver = "OpenGL{0}".format("2" if "+opengl2" in spec else "")

        cmake_args = [
            "-DBUILD_SHARED_LIBS=ON",
            "-DVTK_RENDERING_BACKEND:STRING={0}".format(opengl_ver),
            # prevents installation into lib64 which might not be in the path
            # (solves #26314)
            "-DCMAKE_INSTALL_LIBDIR:PATH=lib",
            # Allow downstream codes (e.g. VisIt) to override VTK's classes
            "-DVTK_ALL_NEW_OBJECT_FACTORY:BOOL=ON",
        ]

        # Disable wrappers for other languages.
        cmake_args.append("-DVTK_WRAP_JAVA=OFF")
        if spec.satisfies("@:8.1"):
            cmake_args.append("-DVTK_WRAP_TCL=OFF")

        # In general, we disable use of VTK "ThirdParty" libs, preferring
        # spack-built versions whenever possible but there are exceptions.
        if spec.satisfies("@:8"):
            cmake_args.extend(
                ["-DVTK_USE_SYSTEM_LIBRARIES:BOOL=ON", "-DVTK_USE_SYSTEM_LIBHARU=OFF"]
            )
            if spec.satisfies("@:8.0"):
                cmake_args.append("-DVTK_USE_SYSTEM_GL2PS=OFF")
        else:
            cmake_args.extend(
                [
                    "-DVTK_USE_EXTERNAL:BOOL=ON",
                    "-DVTK_MODULE_USE_EXTERNAL_VTK_libharu:BOOL=OFF",
                    "-DVTK_MODULE_USE_EXTERNAL_VTK_pegtl:BOOL=OFF",
                    "-DHDF5_ROOT={0}".format(spec["hdf5"].prefix),
                ]
            )
            if spec.satisfies("@9.1:"):
                cmake_args.extend(
                    [
                        "-DVTK_MODULE_USE_EXTERNAL_VTK_exprtk:BOOL=OFF",
                        # uses an unreleased version of fmt
                        "-DVTK_MODULE_USE_EXTERNAL_VTK_fmt:BOOL=OFF",
                    ]
                )
            if spec.satisfies("@9.2:"):
                cmake_args.append("-DVTK_MODULE_USE_EXTERNAL_VTK_verdict:BOOL=OFF")

        # Some variable names have changed
        if spec.satisfies("@8.2.0"):
            cmake_args.append("-DVTK_USE_SYSTEM_PUGIXML:BOOL=OFF")
        elif spec.satisfies("@:8.1"):
            cmake_args.extend(
                [
                    "-DVTK_USE_SYSTEM_LIBPROJ4:BOOL=OFF",
                    "-DNETCDF_CXX_ROOT={0}".format(spec["netcdf-cxx"].prefix),
                ]
            )

        if "+mpi" in spec:
            if spec.satisfies("@:8.2.0"):
                cmake_args.extend(["-DVTK_Group_MPI:BOOL=ON", "-DVTK_USE_SYSTEM_DIY2:BOOL=OFF"])
            else:
                cmake_args.extend(["-DVTK_USE_MPI=ON"])
        else:
            cmake_args.append("-DVTK_USE_MPI=OFF")

        if "+ffmpeg" in spec:
            if spec.satisfies("@:8"):
                cmake_args.append("-DModule_vtkIOFFMPEG:BOOL=ON")
            else:
                cmake_args.append("-DVTK_MODULE_ENABLE_VTK_IOFFMPEG:STRING=YES")

        # Enable/Disable wrappers for Python.
        if "+python" in spec:
            cmake_args.append("-DVTK_WRAP_PYTHON=ON")
            if spec.satisfies("@:8"):
                cmake_args.append("-DPYTHON_EXECUTABLE={0}".format(spec["python"].command.path))
            if "+mpi" in spec and spec.satisfies("@:8"):
                cmake_args.append("-DVTK_USE_SYSTEM_MPI4PY:BOOL=ON")
            if spec.satisfies("@9.0.0: ^python@3:"):
                cmake_args.append("-DVTK_PYTHON_VERSION=3")
        else:
            cmake_args.append("-DVTK_WRAP_PYTHON=OFF")

        if "darwin" in spec.architecture:
            cmake_args.extend(["-DCMAKE_MACOSX_RPATH=ON"])

        if "+qt" in spec:
            qt_ver = spec["qt"].version.up_to(1)
            qt_bin = spec["qt"].prefix.bin
            qmake_exe = os.path.join(qt_bin, "qmake")

            # https://github.com/martijnkoopman/Qt-VTK-viewer/blob/master/doc/Build-VTK.md
            # The content of the above link changes over time with versions.
            # Older commits have information on VTK-8.
            if spec.satisfies("@:8"):
                cmake_args.extend(
                    [
                        "-DVTK_QT_VERSION:STRING={0}".format(qt_ver),
                        "-DQT_QMAKE_EXECUTABLE:PATH={0}".format(qmake_exe),
                        "-DVTK_Group_Qt:BOOL=ON",
                    ]
                )
            else:
                cmake_args.extend(
                    [
                        "-DVTK_GROUP_ENABLE_Qt:STRING=YES",
                        "-DVTK_MODULE_ENABLE_VTK_GUISupportQt:STRING=YES",
                    ]
                )

            # NOTE: The following definitions are required in order to allow
            # VTK to build with qt~webkit versions (see the documentation for
            # more info: http://www.vtk.org/Wiki/VTK/Tutorials/QtSetup).
            if "~webkit" in spec["qt"]:
                if spec.satisfies("@:8"):
                    cmake_args.extend(
                        [
                            "-DVTK_Group_Qt:BOOL=OFF",
                            "-DModule_vtkGUISupportQt:BOOL=ON",
                            "-DModule_vtkGUISupportQtOpenGL:BOOL=ON",
                        ]
                    )
                else:
                    cmake_args.extend(
                        [
                            "-DVTK_GROUP_ENABLE_Qt:STRING=NO",
                            "-DVTK_MODULE_ENABLE_VTK_GUISupportQt:STRING=YES",
                        ]
                    )

        if "+xdmf" in spec:
            if spec.satisfies("^cmake@3.12:"):
                # This policy exists only for CMake >= 3.12
                cmake_args.extend(["-DCMAKE_POLICY_DEFAULT_CMP0074=NEW"])

            if spec.satisfies("@:8"):
                cmake_args.extend(
                    [
                        # Enable XDMF Support here
                        "-DModule_vtkIOXdmf2:BOOL=ON",
                        "-DModule_vtkIOXdmf3:BOOL=ON",
                        "-DBOOST_ROOT={0}".format(spec["boost"].prefix),
                        "-DBOOST_LIBRARY_DIR={0}".format(spec["boost"].prefix.lib),
                        "-DBOOST_INCLUDE_DIR={0}".format(spec["boost"].prefix.include),
                        "-DBOOST_NO_SYSTEM_PATHS:BOOL=ON",
                        # This is needed because VTK has multiple FindBoost
                        # and they stick to system boost if there's a system boost
                        # installed with CMake
                        "-DBoost_NO_BOOST_CMAKE:BOOL=ON",
                        # The xdmf project does not export any CMake file...
                        "-DVTK_USE_SYSTEM_XDMF3:BOOL=OFF",
                        "-DVTK_USE_SYSTEM_XDMF2:BOOL=OFF",
                    ]
                )
            else:
                cmake_args.extend(
                    [
                        "-DVTK_MODULE_ENABLE_VTK_xdmf2:STRING=YES",
                        "-DVTK_MODULE_ENABLE_VTK_xdmf3:STRING=YES",
                        "-DVTK_MODULE_ENABLE_VTK_IOXdmf2:STRING=YES",
                        "-DVTK_MODULE_ENABLE_VTK_IOXdmf3:STRING=YES",
                    ]
                )

            if "+mpi" in spec:
                if spec.satisfies("@:8"):
                    cmake_args.append("-DModule_vtkIOParallelXdmf3:BOOL=ON")
                else:
                    cmake_args.append("-DVTK_MODULE_ENABLE_VTK_IOParallelXdmf3:STRING=YES")

        cmake_args.append("-DVTK_RENDERING_BACKEND:STRING=" + opengl_ver)

        if "+osmesa" in spec:
            cmake_args.extend(
                [
                    "-DVTK_USE_X:BOOL=OFF",
                    "-DVTK_USE_COCOA:BOOL=OFF",
                    "-DVTK_OPENGL_HAS_OSMESA:BOOL=ON",
                ]
            )

        else:
            cmake_args.append("-DVTK_OPENGL_HAS_OSMESA:BOOL=OFF")
            if spec.satisfies("@:7.9.9"):
                # This option is gone in VTK 8.1.2
                cmake_args.append("-DOpenGL_GL_PREFERENCE:STRING=LEGACY")

            if "platform=darwin" in spec:
                cmake_args.extend(["-DVTK_USE_X:BOOL=OFF", "-DVTK_USE_COCOA:BOOL=ON"])

            elif "platform=linux" in spec:
                cmake_args.extend(["-DVTK_USE_X:BOOL=ON", "-DVTK_USE_COCOA:BOOL=OFF"])

        compile_flags = []

        if spec.satisfies("@:6.1.0"):
            compile_flags.append("-DGLX_GLXEXT_LEGACY")

            # VTK 6.1.0 (and possibly earlier) does not use
            # NETCDF_CXX_ROOT to detect NetCDF C++ bindings, so
            # NETCDF_CXX_INCLUDE_DIR and NETCDF_CXX_LIBRARY must be
            # used instead to detect these bindings
            netcdf_cxx_lib = spec["netcdf-cxx"].libs.joined()
            cmake_args.extend(
                [
                    "-DNETCDF_CXX_INCLUDE_DIR={0}".format(spec["netcdf-cxx"].prefix.include),
                    "-DNETCDF_CXX_LIBRARY={0}".format(netcdf_cxx_lib),
                ]
            )

            # Garbage collection is unsupported in Xcode starting with
            # version 5.1; if the Apple clang version of the compiler
            # is 5.1.0 or later, unset the required Objective-C flags
            # to remove the garbage collection flags.  Versions of VTK
            # after 6.1.0 set VTK_REQUIRED_OBJCXX_FLAGS to the empty
            # string. This fix was recommended on the VTK mailing list
            # in March 2014 (see
            # https://public.kitware.com/pipermail/vtkusers/2014-March/083368.html)
            if self.spec.satisfies("%apple-clang@5.1.0:"):
                cmake_args.extend(["-DVTK_REQUIRED_OBJCXX_FLAGS="])

            # A bug in tao pegtl causes build failures with intel compilers
            if "%intel" in spec and spec.version >= Version("8.2"):
                cmake_args.append("-DVTK_MODULE_ENABLE_VTK_IOMotionFX:BOOL=OFF")

        # -no-ipo prevents an internal compiler error from multi-file
        # optimization (https://github.com/spack/spack/issues/20471)
        if "%intel" in spec:
            compile_flags.append("-no-ipo")

        if compile_flags:
            compile_flags = " ".join(compile_flags)
            cmake_args.extend(
                [
                    "-DCMAKE_C_FLAGS={0}".format(compile_flags),
                    "-DCMAKE_CXX_FLAGS={0}".format(compile_flags),
                ]
            )

        return cmake_args
