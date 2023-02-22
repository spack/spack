# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Xyce(CMakePackage):
    """Xyce (rhymes with 'spice') is an open source, SPICE-compatible,
    high-performance analog circuit simulator, capable of solving extremely
    large circuit problems by supporting large-scale parallel computing
    platforms.
    Xyce also supports serial execution on all common desktop platforms,
    and small-scale parallel runs on Unix-like systems. In addition to analog
    electronic simulation, Xyce has also been used to investigate more general
    network systems, such as neural networks and power grids.
    """

    homepage = "https://xyce.sandia.gov"
    git = "https://github.com/Xyce/Xyce.git"
    url = "https://github.com/Xyce/Xyce/archive/Release-7.2.0.tar.gz"
    maintainers("kuberry", "tbird2001")

    version("master", branch="master")
    version("7.6.0", "fc25557e2edc82adbe0436a15fca2929a2f9ab08ddf91f1a47aab5e8b27ec88c")
    version("7.5.0", "854d7d5e19e0ee2138d1f20f10f8f27f2bebb94ec81c157040955cff7250dacd")
    version("7.4.0", "2d6bc1b7377834b2e0bf50131e96728c5be83dbb3548e765bb48911067c87c91")
    version("7.3.0", "43869a70967f573ff6f00451db3f4642684834bdad1fd3926380e3789016b446")
    version("7.2.0", "cf49705278ecda46373784bb24925cb97f9017b6adff49e4416de146bdd6a4b5")

    depends_on("cmake@3.13:", type="build")
    depends_on("flex")
    depends_on("bison")

    variant(
        "build_type",
        default="Release",
        description="CMake build type",
        values=("Debug", "Release", "RelWithDebInfo", "MinSizeRel"),
    )

    variant("mpi", default=True, description="Enable MPI support")
    depends_on("mpi", when="+mpi")

    variant("plugin", default=False, description="Enable plug-in support for Xyce")
    depends_on("adms", type=("build", "run"), when="+plugin")

    variant("shared", default=False, description="Enable shared libraries for Xyce")
    conflicts(
        "~shared",
        when="+plugin",
        msg="Disabling shared libraries is incompatible with the activation of plug-in support",
    )

    # any option other than cxxstd=11 would be ignored in Xyce
    # this defaults to 11, consistent with what will be used,
    # and produces an error if any other value is attempted
    cxxstd_choices = ["11"]
    variant("cxxstd", default="11", values=cxxstd_choices, multi=False)

    variant("pymi", default=False, description="Enable Python Model Interpreter for Xyce")
    # Downstream dynamic library symbols from pip installed numpy and other
    # pip installed python packages can cause conflicts. This is most often
    # seen with blas symbols from numpy, and building blas static resolves
    # this issue.
    variant(
        "pymi_static_tpls",
        default=True,
        sticky=True,
        when="+pymi",
        description="Require static blas build for PyMi",
    )

    depends_on("python@3:", type=("build", "link", "run"), when="+pymi")
    depends_on("py-pip", type="run", when="+pymi")
    depends_on("py-pybind11@2.6.1:", type=("build", "link"), when="+pymi")

    depends_on(
        "trilinos"
        "+amesos+amesos2+anasazi+aztec+basker+belos+complex+epetra+epetraext"
        "+explicit_template_instantiation+fortran+ifpack+kokkos+nox"
        "+sacado+suite-sparse+trilinoscouplings+stokhos+epetraextbtf"
        "+epetraextexperimental+epetraextgraphreorderings"
    )
    depends_on("trilinos+isorropia+zoltan", when="+mpi")

    # tested versions of Trilinos for everything up to 7.4.0
    depends_on("trilinos@12.12.1:13.4", when="@:7.5")
    depends_on("trilinos@13.5.0:develop", when="@7.6.0:master")
    depends_on("trilinos gotype=all cxxstd=11", when="^trilinos@:12.15")
    # pymi requires Kokkos/KokkosKernels >= 3.3, Trilinos 13.2 onward
    depends_on("trilinos@13.2.0:", when="+pymi")

    # Propagate variants to trilinos:
    for _variant in ("mpi",):
        depends_on("trilinos~" + _variant, when="~" + _variant)
        depends_on("trilinos+" + _variant, when="+" + _variant)

    # The default settings for various Trilinos variants would require the
    # installation of many more packages than are needed for Xyce.
    depends_on("trilinos~float~ifpack2~ml~muelu~zoltan2")

    # Issue #1712 forces explicitly enumerating blas packages to propagate variants
    with when("+pymi_static_tpls"):
        # BLAS
        depends_on("openblas~shared", when="^openblas")
        depends_on("netlib-lapack~shared", when="^netlib-lapack~external-blas")

        depends_on("armpl-gcc~shared", when="^armpl-gcc")
        depends_on("atlas~shared", when="^atlas")
        depends_on("blis libs=static", when="^blis+cblas")
        depends_on("blis libs=static", when="^blis+blas")
        depends_on("clblast~shared", when="^clblast+netlib")
        depends_on("intel-mkl~shared", when="^intel-mkl")
        depends_on("intel-oneapi-mkl~shared", when="^intel-oneapi-mkl")
        depends_on("intel-parallel-studio~shared", when="^intel-parallel-studio+mkl")
        depends_on("veclibfort~shared", when="^veclibfort")
        conflicts("^essl", msg="essl not supported with +pymi_static_tpls")
        conflicts("^flexiblas", msg="flexiblas not supported with +pymi_static_tpls")
        conflicts("^nvhpc", msg="nvhpc not supported with +pymi_static_tpls")
        conflicts("^cray-libsci", msg="cray-libsci not supported with +pymi_static_tpls")
        # netlib-xblas+plain_blas is always static

        # HDF5
        depends_on("hdf5~shared", when="^hdf5")

    # fix RPATH issue on mac
    patch(
        "https://github.com/xyce/xyce/commit/40dbc0e0341a5cf9a7fa82a87313869dc284fdd9.patch?full_index=1",
        sha256="3c32faeeea0bb29be44ec20e414670c9fd375f9ed921a7f6e9fd3de02c28859d",
        when="@7.3:7.5 +shared",
    )

    # fix parameter merging in pymi
    patch(
        "https://github.com/xyce/xyce/commit/fdf457fce1b1511b8a29d134d38e515fb7149246.patch?full_index=1",
        sha256="077f91d2ff0649b3f7e83c224f71a030521c6fb5a84b29acd772d5657cdb6c23",
        when="@7.4:7.6 +pymi",
    )

    def cmake_args(self):
        spec = self.spec

        options = []

        if "+mpi" in spec:
            options.append(self.define("CMAKE_CXX_COMPILER", spec["mpi"].mpicxx))
        else:
            options.append(self.define("CMAKE_CXX_COMPILER", spack_cxx))

        options.append(self.define_from_variant("BUILD_SHARED_LIBS", "shared"))
        options.append(self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"))
        options.append(self.define_from_variant("CMAKE_BUILD_TYPE", "build_type"))
        options.append(self.define_from_variant("Xyce_PLUGIN_SUPPORT", "plugin"))
        options.append(self.define("Trilinos_DIR", spec["trilinos"].prefix))

        if "+pymi" in spec:
            pybind11 = spec["py-pybind11"]
            python = spec["python"]
            options.append("-DXyce_PYMI:BOOL=ON")
            options.append("-Dpybind11_DIR:PATH={0}".format(pybind11.prefix))
            options.append("-DPython_ROOT_DIR:FILEPATH={0}".format(python.prefix))
            options.append("-DPython_FIND_STRATEGY=LOCATION")

        return options

    def flag_handler(self, name, flags):
        spec = self.spec
        if name == "cxxflags":
            flags.append("-DXyce_INTRUSIVE_PCE -Wreorder")
        elif name == "ldflags":
            # Fortran lib (assumes clang is built with gfortran!)
            if spec.compiler.name in ["gcc", "clang", "apple-clang"]:
                fc = Executable(self.compiler.fc)
                libgfortran = fc(
                    "--print-file-name", "libgfortran." + dso_suffix, output=str
                ).strip()
                # if libgfortran is equal to "libgfortran.<dso_suffix>" then
                # print-file-name failed, use static library instead
                if libgfortran == "libgfortran." + dso_suffix:
                    libgfortran = fc("--print-file-name", "libgfortran.a", output=str).strip()
                # -L<libdir> -lgfortran required for OSX
                # https://github.com/spack/spack/pull/25823#issuecomment-917231118
                flags.append("-L{0} -lgfortran".format(os.path.dirname(libgfortran)))

        return (flags, None, None)
