# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from llnl.util.lang import dedupe

import spack.builder
from spack.build_systems import autotools, cmake
from spack.package import *
from spack.util.environment import is_system_path


class NetcdfC(CMakePackage, AutotoolsPackage):
    """NetCDF (network Common Data Form) is a set of software libraries and
    machine-independent data formats that support the creation, access, and
    sharing of array-oriented scientific data. This is the C distribution."""

    homepage = "https://www.unidata.ucar.edu/software/netcdf"
    git = "https://github.com/Unidata/netcdf-c.git"
    url = "https://github.com/Unidata/netcdf-c/archive/refs/tags/v4.8.1.tar.gz"

    maintainers("skosukhin", "WardF")

    version("main", branch="main")
    version("4.9.2", sha256="bc104d101278c68b303359b3dc4192f81592ae8640f1aee486921138f7f88cb7")
    version("4.9.0", sha256="9f4cb864f3ab54adb75409984c6202323d2fc66c003e5308f3cdf224ed41c0a6")
    version("4.8.1", sha256="bc018cc30d5da402622bf76462480664c6668b55eb16ba205a0dfb8647161dd0")
    version("4.8.0", sha256="aff58f02b1c3e91dc68f989746f652fe51ff39e6270764e484920cb8db5ad092")
    version("4.7.4", sha256="99930ad7b3c4c1a8e8831fb061cb02b2170fc8e5ccaeda733bd99c3b9d31666b")
    version("4.7.3", sha256="05d064a2d55147b83feff3747bea13deb77bef390cb562df4f9f9f1ce147840d")
    version("4.7.2", sha256="7648db7bd75fdd198f7be64625af7b276067de48a49dcdfd160f1c2ddff8189c")
    version("4.7.1", sha256="583e6b89c57037293fc3878c9181bb89151da8c6015ecea404dd426fea219b2c")
    version("4.7.0", sha256="26d03164074363b3911ed79b7cddd045c22adf5ebaf978943db11a1d9f15e9d3")
    version("4.6.3", sha256="734a629cdaed907201084d003cfa091806d6080eeffbd4204e7c7f73ff9d3564")
    version("4.6.2", sha256="673936c76ae0c496f6dde7e077f5be480afc1e300adb2c200bf56fbe22e5a82a")
    version("4.6.1", sha256="a2fabf27c72a5ee746e3843e1debbaad37cd035767eaede2045371322211eebb")
    version("4.6.0", sha256="6d740356399aac12290650325a05aec2fe92c1905df10761b2b0100994197725")
    version("4.5.0", sha256="f7d1cb2a82100b9bf9a1130a50bc5c7baf0de5b5022860ac3e09a0a32f83cf4a")
    # Version 4.4.1.1 is having problems in tests
    #    https://github.com/Unidata/netcdf-c/issues/343
    version("4.4.1.1", sha256="7f040a0542ed3f6d27f3002b074e509614e18d6c515b2005d1537fec01b24909")
    # Version 4.4.1 can crash on you (in real life and in tests).  See:
    #    https://github.com/Unidata/netcdf-c/issues/282
    version("4.4.1", sha256="17599385fd76ccdced368f448f654de2ed000fece44dece9fb5d598798b4c9d6")
    version("4.4.0", sha256="09b78b152d3fd373bee4b5738dc05c7b2f5315fe34aa2d94ee9256661119112f")
    version("4.3.3.1", sha256="f2ee78eb310637c007f001e7c18e2d773d23f3455242bde89647137b7344c2e2")
    version("4.3.3", sha256="3f16e21bc3dfeb3973252b9addf5defb48994f84fc9c9356081f871526a680e7")

    # configure fails if curl is not installed.
    # See https://github.com/Unidata/netcdf-c/issues/1390
    patch(
        "https://github.com/Unidata/netcdf-c/commit/e5315da1e748dc541d50796fb05233da65e86b6b.patch?full_index=1",
        sha256="c551ca2f5b6bcefa07dd7f8b7bac426a5df9861e091df1ab99167d8d401f963f",
        when="@4.7.0",
    )
    # fix headers
    patch(
        "https://github.com/Unidata/netcdf-c/pull/1505.patch?full_index=1",
        sha256="495b3e5beb7f074625bcec2ca76aebd339e42719e9c5ccbedbdcc4ffb81a7450",
        when="@4.7.2",
    )
    patch(
        "https://github.com/Unidata/netcdf-c/pull/1508.patch?full_index=1",
        sha256="19e7f31b96536928621b1c29bb6d1a57bcb7aa672cea8719acf9ac934cdd2a3e",
        when="@4.7.2",
    )

    patch("4.8.1-win-hdf5-with-zlib.patch", when="@4.8.1: platform=windows")

    patch("netcdfc-mpi-win-support.patch", when="platform=windows")
    # See https://github.com/Unidata/netcdf-c/pull/1752
    patch("4.7.3-spectrum-mpi-pnetcdf-detect.patch", when="@4.7.3:4.7.4 +parallel-netcdf")

    # See https://github.com/Unidata/netcdf-c/pull/2293
    patch("4.8.1-no-strict-aliasing-config.patch", when="@4.8.1")

    # See https://github.com/Unidata/netcdf-c/pull/2618
    patch("4.9.0-no-mpi-yes-pnetcdf.patch", when="@4.9.0: ~mpi+parallel-netcdf")

    variant("mpi", default=True, description="Enable parallel I/O for netcdf-4")
    variant("parallel-netcdf", default=False, description="Enable parallel I/O for classic files")
    variant("hdf4", default=False, description="Enable HDF4 support")
    variant("pic", default=True, description="Produce position-independent code (for shared libs)")
    variant("shared", default=True, description="Enable shared library")
    variant("dap", default=False, description="Enable DAP support")
    variant("jna", default=False, description="Enable JNA support")
    variant("fsync", default=False, description="Enable fsync support")
    variant("nczarr_zip", default=False, description="Enable NCZarr zipfile format storage")
    variant("optimize", default=True, description="Enable -O2 for a more optimized lib")

    variant("szip", default=True, description="Enable Szip compression plugin")
    variant("blosc", default=True, description="Enable Blosc compression plugin")
    variant("zstd", default=True, description="Enable Zstandard compression plugin")

    # The patch for 4.7.0 touches configure.ac. See force_autoreconf below.
    with when("build_system=autotools"):
        depends_on("autoconf", type="build", when="@4.7.0,main")
        depends_on("automake", type="build", when="@4.7.0,main")
        depends_on("libtool", type="build", when="@4.7.0,main")
    # CMake system can use m4, but Windows does not yet support
    depends_on("m4", type="build", when=sys.platform != "win32")

    depends_on("hdf~netcdf", when="+hdf4")

    # curl 7.18.0 or later is required:
    # https://docs.unidata.ucar.edu/nug/current/getting_and_building_netcdf.html
    depends_on("curl@7.18.0:", when="+dap")

    # Need to include libxml2 when using DAP in 4.9.0 and newer to build
    # https://github.com/Unidata/netcdf-c/commit/53464e89635a43b812b5fec5f7abb6ff34b9be63
    depends_on("libxml2", when="@4.9.0:+dap")

    depends_on("parallel-netcdf", when="+parallel-netcdf")

    # We need to build with MPI wrappers if any of the two
    # parallel I/O features is enabled:
    # https://docs.unidata.ucar.edu/nug/current/getting_and_building_netcdf.html#build_parallel
    depends_on("mpi", when="+mpi")
    depends_on("mpi", when="+parallel-netcdf")

    # High-level API of HDF5 1.8.9 or later is required for netCDF-4 support:
    # https://docs.unidata.ucar.edu/nug/current/getting_and_building_netcdf.html
    depends_on("hdf5@1.8.9:+hl")

    # Starting version 4.4.0, it became possible to disable parallel I/O even
    # if HDF5 supports it. For previous versions of the library we need
    # HDF5 without mpi support to disable parallel I/O:
    depends_on("hdf5~mpi", when="@:4.3~mpi")

    # We need HDF5 with mpi support to enable parallel I/O.
    depends_on("hdf5+mpi", when="+mpi")

    # NetCDF 4.4.0 and prior have compatibility issues with HDF5 1.10 and later
    # https://github.com/Unidata/netcdf-c/issues/250
    depends_on("hdf5@:1.8", when="@:4.4.0")

    # NetCDF 4.7.4 and prior require HDF5 1.10 or older
    # https://github.com/Unidata/netcdf-c/pull/1671
    depends_on("hdf5@:1.10", when="@:4.7.3")

    # Although NetCDF 4.8.0 builds and passes the respective tests against HDF5 1.12.0 with the
    # default API (i.e. the problem reported in https://github.com/Unidata/netcdf-c/issues/1965 is
    # not reproducible), the configure script fails if HDF5 1.12.0 is built without api=v18
    # (according to the error message emitted by the configure script) or api=v110 (according to
    # the comments in the configure script and its implementation). The check that led to the
    # failure was removed in version 4.8.1 (https://github.com/Unidata/netcdf-c/pull/2044). To
    # keep it simple, we require HDF5 1.10.x or older:
    depends_on("hdf5@:1.10", when="@4.8.0")

    depends_on("libzip", when="+nczarr_zip")

    # According to the documentation (see
    # https://docs.unidata.ucar.edu/nug/current/getting_and_building_netcdf.html), zlib 1.2.5 or
    # later is required for netCDF-4 compression. However, zlib became a direct dependency only
    # starting NetCDF 4.9.0 (for the deflate plugin):
    depends_on("zlib@1.2.5:", when="@4.9.0:+shared")
    depends_on("bzip2", when="@4.9.0:+shared")
    depends_on("szip", when="+szip")
    depends_on("c-blosc", when="+blosc")
    depends_on("zstd", when="+zstd")

    # NCZarr was added in version 4.8.0 as an experimental feature and became a supported one in
    # version 4.8.1:
    conflicts("+nczarr_zip", when="@:4.8.0")

    # The features were introduced in version 4.9.0:
    with when("@:4.8"):
        conflicts("+szip")
        conflicts("+blosc")
        conflicts("+zstd")

    # The plugins are not built when the shared libraries are disabled:
    with when("~shared"):
        conflicts("+szip")
        conflicts("+blosc")
        conflicts("+zstd")

    default_build_system = "cmake" if sys.platform == "win32" else "autotools"

    build_system("cmake", "autotools", default=default_build_system)

    def setup_run_environment(self, env):
        if self.spec.satisfies("@4.9.0:+shared"):
            # Both HDF5 and NCZarr backends honor the same environment variable:
            env.append_path("HDF5_PLUGIN_PATH", self.prefix.plugins)

    def flag_handler(self, name, flags):
        if self.builder.build_system == "autotools":
            if name == "cflags":
                if "+pic" in self.spec:
                    flags.append(self.compiler.cc_pic_flag)
                if "+optimize" in self.spec:
                    flags.append("-O2")
        return flags, None, None

    @property
    def libs(self):
        shared = "+shared" in self.spec
        return find_libraries("libnetcdf", root=self.prefix, shared=shared, recursive=True)


class Setup:
    def setup_dependent_build_environment(self, env, dependent_spec):
        self.pkg.setup_run_environment(env)
        # Some packages, e.g. ncview, refuse to build if the compiler path returned by nc-config
        # differs from the path to the compiler that the package should be built with. Therefore,
        # we have to shadow nc-config from self.prefix.bin, which references the real compiler,
        # with a backed up version, which references Spack compiler wrapper.
        if os.path.exists(self._nc_config_backup_dir):
            env.prepend_path("PATH", self._nc_config_backup_dir)


class BackupStep(metaclass=spack.builder.PhaseCallbacksMeta):
    @property
    def _nc_config_backup_dir(self):
        return join_path(self.pkg.metadata_dir, "spack-nc-config")

    @run_after("install")
    def backup_nc_config(self):
        # We expect this to be run before filter_compiler_wrappers:
        nc_config_file = self.prefix.bin.join("nc-config")
        if os.path.exists(nc_config_file):
            mkdirp(self._nc_config_backup_dir)
            install(nc_config_file, self._nc_config_backup_dir)

    filter_compiler_wrappers("nc-config", relative_root="bin")


class CMakeBuilder(BackupStep, Setup, cmake.CMakeBuilder):
    def cmake_args(self):
        base_cmake_args = [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define("BUILD_UTILITIES", True),
            self.define("ENABLE_NETCDF_4", True),
            self.define_from_variant("ENABLE_DAP", "dap"),
            self.define("CMAKE_INSTALL_PREFIX", self.prefix),
            self.define_from_variant("ENABLE_HDF4", "hdf4"),
            self.define("ENABLE_PARALLEL_TESTS", False),
            self.define_from_variant("ENABLE_FSYNC", "fsync"),
            self.define("ENABLE_LARGE_FILE_SUPPORT", True),
        ]
        if "+parallel-netcdf" in self.pkg.spec:
            base_cmake_args.append(self.define("ENABLE_PNETCDF", True))
        if self.pkg.spec.satisfies("@4.3.1:"):
            base_cmake_args.append(self.define("ENABLE_DYNAMIC_LOADING", True))
        return base_cmake_args


class AutotoolsBuilder(BackupStep, Setup, autotools.AutotoolsBuilder):
    @property
    def force_autoreconf(self):
        # The patch for 4.7.0 touches configure.ac.
        return self.spec.satisfies("@4.7.0")

    def autoreconf(self, pkg, spec, prefix):
        if not os.path.exists(self.configure_abs_path):
            Executable("./bootstrap")()

    def configure_args(self):
        config_args = [
            "--enable-v2",
            "--enable-utilities",
            "--enable-static",
            "--enable-largefile",
            "--enable-netcdf-4",
        ]

        # NCZarr was added in version 4.8.0 as an experimental feature and became a supported one
        # in version 4.8.1:
        if self.spec.satisfies("@4.8.1:"):
            config_args.append("--enable-nczarr")
        elif self.spec.satisfies("@4.8.0"):
            config_args.append("--disable-nczarr")

        if self.spec.satisfies("@4.9.0:+shared"):
            # The plugins are not built when the shared libraries are disabled:
            config_args.extend(
                ["--enable-plugins", "--with-plugin-dir={0}".format(self.prefix.plugins)]
            )

        # Byte-range I/O was added in version 4.7.0 and we disable it until it becomes a variant:
        if self.spec.satisfies("@4.7.0:"):
            config_args.append("--disable-byterange")

        # The option was introduced in version 4.3.1 and does nothing starting version 4.6.1:
        if self.spec.satisfies("@4.3.1:4.6.0"):
            config_args.append("--enable-dynamic-loading")

        if self.spec.satisfies("@4.4:"):
            config_args += self.enable_or_disable("parallel4", variant="mpi")

        config_args += self.enable_or_disable("pnetcdf", variant="parallel-netcdf")

        config_args += self.enable_or_disable("hdf4")

        config_args += self.enable_or_disable("shared")

        config_args += self.enable_or_disable("dap")
        if self.spec.satisfies("@4.9.0:"):
            # Prevent linking to system libxml2:
            config_args += self.enable_or_disable("libxml2", variant="dap")

        if self.spec.satisfies("@4.3.2:"):
            config_args += self.enable_or_disable("jna")

        config_args += self.enable_or_disable("fsync")

        if "+mpi" in self.spec or "+parallel-netcdf" in self.spec:
            config_args.append("CC=%s" % self.spec["mpi"].mpicc)

        # In general, we rely on the compiler wrapper to inject the required CPPFLAGS and LDFLAGS.
        # However, the injected LDFLAGS are invisible for the configure script and are added
        # neither to the pkg-config nor to the nc-config files. Therefore, we generate LDFLAGS
        # based on the contents of the following list and pass them to the configure script:
        lib_search_dirs = []

        # In general, we rely on the configure script to generate the required linker flags in the
        # right order. However, the configure script does not know and does not check for several
        # possible transitive dependencies and we have to pass them as the LIBS argument. The list
        # is generated based on the contents of the following list:
        extra_libs = []

        if "+parallel-netcdf" in self.spec:
            lib_search_dirs.extend(self.spec["parallel-netcdf"].libs.directories)

        if "+hdf4" in self.spec:
            hdf = self.spec["hdf"]
            lib_search_dirs.extend(hdf.libs.directories)
            # The configure script triggers unavoidable overlinking to jpeg:
            lib_search_dirs.extend(hdf["jpeg"].libs.directories)
            if "~shared" in hdf:
                # We do not use self.spec["hdf:transitive"].libs to avoid even more duplicates
                # introduced by the configure script:
                if "+szip" in hdf:
                    extra_libs.append(hdf["szip"].libs)
                if "+external-xdr" in hdf:
                    extra_libs.append(hdf["rpc"].libs)
                extra_libs.append(hdf["zlib"].libs)

        hdf5 = self.spec["hdf5:hl"]
        lib_search_dirs.extend(hdf5.libs.directories)
        if "~shared" in hdf5:
            if "+szip" in hdf5:
                extra_libs.append(hdf5["szip"].libs)
            extra_libs.append(hdf5["zlib"].libs)

        if self.spec.satisfies("@4.9.0:+shared"):
            lib_search_dirs.extend(self.spec["zlib"].libs.directories)
        else:
            # Prevent overlinking to zlib:
            config_args.append("ac_cv_search_deflate=")

        if "+nczarr_zip" in self.spec:
            lib_search_dirs.extend(self.spec["libzip"].libs.directories)
        elif self.spec.satisfies("@4.9.2:"):
            # Prevent linking to libzip to disable the feature:
            config_args.append("ac_cv_search_zip_open=no")
        elif self.spec.satisfies("@4.8.0:"):
            # Prevent linking to libzip to disable the feature:
            config_args.append("ac_cv_lib_zip_zip_open=no")

        if "+szip" in self.spec:
            lib_search_dirs.extend(self.spec["szip"].libs.directories)
        elif self.spec.satisfies("@4.9.0:"):
            # Prevent linking to szip to disable the plugin:
            config_args.append("ac_cv_lib_sz_SZ_BufftoBuffCompress=no")

        if self.spec.satisfies("@4.9.0:"):
            if "+shared" in self.spec:
                lib_search_dirs.extend(self.spec["bzip2"].libs.directories)
            else:
                # Prevent redundant entries mentioning system bzip2 in nc-config and pkg-config
                # files:
                config_args.append("ac_cv_lib_bz2_BZ2_bzCompress=no")

        if "+zstd" in self.spec:
            lib_search_dirs.extend(self.spec["zstd"].libs.directories)
        elif self.spec.satisfies("@4.9.0:"):
            # Prevent linking to system zstd:
            config_args.append("ac_cv_lib_zstd_ZSTD_compress=no")

        if "+blosc" in self.spec:
            lib_search_dirs.extend(self.spec["c-blosc"].libs.directories)
        elif self.spec.satisfies("@4.9.0:"):
            # Prevent linking to system c-blosc:
            config_args.append("ac_cv_lib_blosc_blosc_init=no")

        if "+dap" in self.spec:
            lib_search_dirs.extend(self.spec["curl"].libs.directories)
        elif self.spec.satisfies("@4.8.0:"):
            # Prevent linking to system curl:
            config_args.append("ac_cv_lib_curl_curl_easy_setopt=no")

        lib_search_dirs.extend(d for libs in extra_libs for d in libs.directories)
        # Remove duplicates and system prefixes:
        lib_search_dirs = filter(lambda d: not is_system_path(d), dedupe(lib_search_dirs))
        config_args.append(
            "LDFLAGS={0}".format(" ".join("-L{0}".format(d) for d in lib_search_dirs))
        )

        extra_lib_names = [n for libs in extra_libs for n in libs.names]
        # Remove duplicates in the reversed order:
        extra_lib_names = reversed(list(dedupe(reversed(extra_lib_names))))
        config_args.append("LIBS={0}".format(" ".join("-l{0}".format(n) for n in extra_lib_names)))

        return config_args

    def check(self):
        # h5_test fails when run in parallel
        make("check", parallel=False)
