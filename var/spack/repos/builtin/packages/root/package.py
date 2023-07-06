# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import sys

from spack.operating_systems.mac_os import macos_version
from spack.package import *
from spack.util.environment import is_system_path


class Root(CMakePackage):
    """ROOT is a data analysis framework."""

    homepage = "https://root.cern.ch"
    url = "https://root.cern/download/root_v6.16.00.source.tar.gz"
    git = "https://github.com/root-project/root.git"

    executables = ["^root$", "^root-config$"]

    tags = ["hep"]

    maintainers(
        "drbenmorgan", "gartung", "greenc-FNAL", "HadrienG2", "marcmengel", "vitodb", "vvolkl"
    )

    # ###################### Versions ##########################

    # Master branch
    version("master", branch="master")

    # Development version (when more recent than production).

    # Production version
    version("6.28.04", sha256="70f7f86a0cd5e3f2a0befdc59942dd50140d990ab264e8e56c7f17f6bfe9c965")
    version("6.28.02", sha256="6643c07710e68972b00227c68b20b1016fec16f3fba5f44a571fa1ce5bb42faa")
    version("6.28.00", sha256="afa1c5c06d0915411cb9492e474ea9ab12b09961a358e7e559013ed63b5d8084")
    version("6.26.10", sha256="8e56bec397104017aa54f9eb554de7a1a134474fe0b3bb0f43a70fc4fabd625f")
    version("6.26.08", sha256="4dda043e7918b40743ad0299ddd8d526b7078f0a3822fd06066df948af47940e")
    version("6.26.06", sha256="b1f73c976a580a5c56c8c8a0152582a1dfc560b4dd80e1b7545237b65e6c89cb")
    version("6.26.04", sha256="a271cf82782d6ed2c87ea5eef6681803f2e69e17b3036df9d863636e9358421e")
    version("6.26.02", sha256="7ba96772271a726079506c5bf629c3ceb21bf0682567ed6145be30606d7cd9bb")
    version("6.26.00", sha256="5fb9be71fdf0c0b5e5951f89c2f03fcb5e74291d043f6240fb86f5ca977d4b31")
    version("6.24.06", sha256="907f69f4baca1e4f30eeb4979598ca7599b6aa803ca046e80e25b6bbaa0ef522")
    version("6.24.02", sha256="0507e1095e279ccc7240f651d25966024325179fa85a1259b694b56723ad7c1c")
    version("6.24.00", sha256="9da30548a289211c3122d47dacb07e85d35e61067fac2be6c5a5ff7bda979989")
    version("6.22.08", sha256="6f061ff6ef8f5ec218a12c4c9ea92665eea116b16e1cd4df4f96f00c078a2f6f")
    version("6.22.06", sha256="c4688784a7e946cd10b311040b6cf0b2f75125a7520e04d1af0b746505911b57")
    version("6.22.02", sha256="89784afa9c9047e9da25afa72a724f32fa8aa646df267b7731e4527cc8a0c340")
    version("6.22.00", sha256="efd961211c0f9cd76cf4a486e4f89badbcf1d08e7535bba556862b3c1a80beed")
    version("6.20.08", sha256="d02f224b4908c814a99648782b927c353d44db79dea2cadea86138c1afc23ae9")
    version("6.20.06", sha256="9a734758a91598d8a58a3d64d7d606aeb17bdf6fd8214e33f5c4d9947d391951")
    version("6.20.04", sha256="1f8c76ccdb550e64e6ddb092b4a7e9d0a10655ef80044828cba12d5e7c874472")
    version("6.20.02", sha256="0997586bf097c0afbc6f08edbffcebf5eb6a4237262216114ba3f5c8087dcba6")
    version("6.20.00", sha256="68421eb0434b38b66346fa8ea6053a0fdc9a6d254e4a72019f4e3633ae118bf0")
    version("6.18.04", sha256="315a85fc8363f8eb1bffa0decbf126121258f79bd273513ed64795675485cfa4")

    # Old versions
    version("6.18.02", sha256="50ffffdbf2585a536c77a03f54aa631926138275ffeee02e5a16dde87e978c1d")
    version("6.18.00", sha256="e6698d6cfe585f186490b667163db65e7d1b92a2447658d77fa831096383ea71")
    version("6.16.00", sha256="2a45055c6091adaa72b977c512f84da8ef92723c30837c7e2643eecc9c5ce4d8")
    version("6.14.08", sha256="1b63b51cfb4dc20f1f5749faac6bbd1098eccab777f8b49911257d77186c73c4")
    version("6.14.06", sha256="0fb943b61396f282b289e35c455a9ab60126229be1bd3f04a8f00b37c13ab432")
    version("6.14.04", sha256="463ec20692332a422cfb5f38c78bedab1c40ab4d81be18e99b50cf9f53f596cf")
    version("6.14.02", sha256="93816519523e87ac75924178d87112d1573eaa108fc65691aea9a9dd5bc05b3e")
    version("6.14.00", sha256="7946430373489310c2791ff7a3520e393dc059db1371272bcd9d9cf0df347a0b")
    version("6.12.06", sha256="aedcfd2257806e425b9f61b483e25ba600eb0ea606e21262eafaa9dc745aa794")
    version("6.10.08", sha256="2cd276d2ac365403c66f08edd1be62fe932a0334f76349b24d8c737c0d6dad8a")
    version("6.08.06", sha256="ea31b047ba6fc04b0b312667349eaf1498a254ccacd212144f15ffcb3f5c0592")
    version("6.06.08", sha256="7cb836282014cce822ef589cad27811eb7a86d7fad45a871fa6b0e6319ec201a")
    version("6.06.06", sha256="0a7d702a130a260c72cb6ea754359eaee49a8c4531b31f23de0bfcafe3ce466b")
    version("6.06.04", sha256="ab86dcc80cbd8e704099af0789e23f49469932ac4936d2291602301a7aa8795b")
    version("6.06.02", sha256="18a4ce42ee19e1a810d5351f74ec9550e6e422b13b5c58e0c3db740cdbc569d1")

    # ###################### Patches ##########################

    # Widely used patch (CMS, FNAL) to increase the size of static
    # buffers used to improve the operation of TString.
    patch("format-stringbuf-size.patch", level=0)
    # Support use of `mariadb-c-client` and `mariadb` to provide the
    # MySQL API _cf_
    # https://github.com/root-project/root/commit/9c0fa8c554a569c971185249f9acfff4418c0c13.
    patch("find-mysql.patch", level=1, when="@:6.16.00")
    # Some ROOT versions did not honor the option to avoid building an
    # internal version of unuran, _cf_
    # https://github.com/root-project/ROOT/commit/3e60764f133218b6938e5aa4986de760e8f058d9.
    patch("honor-unuran-switch.patch", level=1, when="@6.08.06:6.13")
    # 6.16.00 fails to handle particular build option combinations, _cf_
    # https://github.com/root-project/ROOT/commit/e0ae0483985d90a71a6cabd10d3622dfd1c15611.
    patch("root7-webgui.patch", level=1, when="@6.16.00")
    # 6.26.00:6.26.06 can fail with empty string COMPILE_DEFINITIONS, which this patch
    # protects against
    patch(
        "https://github.com/root-project/root/pull/11111.patch?full_index=1",
        sha256="3115be912bd948979c9c2a3d89ffe6437fe17bd3b81396958c6cb6f51f64ae62",
        when="@6.26:6.26.06",
    )
    # 6.26.00:6.26.06 fails for recent nlohmann-json single headers versions
    patch(
        "https://github.com/root-project/root/pull/11225.patch?full_index=1",
        sha256="397f2de7db95a445afdb311fc91c40725fcfad485d58b4d72e6c3cdd0d0c5de7",
        when="@6.26:6.26.06 +root7 ^nlohmann-json@3.11:",
    )

    if sys.platform == "darwin":
        # Resolve non-standard use of uint, _cf_
        # https://sft.its.cern.ch/jira/browse/ROOT-7886.
        patch("math_uint.patch", when="@6.06.02")
        # Resolve circular dependency, _cf_
        # https://sft.its.cern.ch/jira/browse/ROOT-8226.
        patch("root6-60606-mathmore.patch", when="@6.06.06")

    # ###################### Variants ##########################
    # See README.md for specific notes about what ROOT configuration
    # options are or are not supported, and why.

    variant("aqua", default=False, description="Enable Aqua interface")
    variant("arrow", default=False, description="Enable Arrow interface")
    variant("davix", default=True, description="Compile with external Davix")
    variant("dcache", default=False, description="Enable support for dCache")
    variant("emacs", default=False, description="Enable Emacs support")
    variant("examples", default=True, description="Install examples")
    variant("fftw", default=False, description="Enable Fast Fourier Transform support")
    variant(
        "fits", default=False, description="Enable support for images and data from FITS files"
    )
    variant("fortran", default=False, description="Enable the Fortran components of ROOT")
    variant("graphviz", default=False, description="Enable graphviz support")
    variant("gdml", default=True, description="Enable GDML writer and reader")
    variant(
        "gminimal",
        default=True,
        description="Ignore most of Root's feature defaults except for " "basic graphic options",
    )
    variant("gsl", default=True, description="Enable linking against shared libraries for GSL")
    variant("http", default=False, description="Enable HTTP server support")
    variant(
        "jemalloc",
        when="@:6.28",
        default=False,
        description="Enable using the jemalloc allocator (deprecated in 6.28)",
    )
    variant("math", default=True, description="Build the new libMathMore extended math library")
    variant(
        "memstat",
        when="@:6.17",
        default=False,
        description="Enable a memory stats utility to detect memory leaks",
    )
    # Minuit must not be installed as a dependency of root
    # otherwise it crashes with the internal minuit library
    variant("minuit", default=True, description="Automatically search for support libraries")
    variant(
        "mlp",
        default=False,
        description="Enable support for TMultilayerPerceptron " "classes' federation",
    )
    variant("mysql", default=False)
    variant("opengl", default=True, description="Enable OpenGL support")
    variant("oracle", default=False, description="Enable support for Oracle databases")
    variant("postgres", default=False, description="Enable postgres support")
    variant("pythia6", default=False, description="Enable pythia6 support")
    variant("pythia8", default=False, description="Enable pythia8 support")
    variant("python", default=True, description="Enable Python ROOT bindings")
    variant("qt4", when="@:6.17", default=False, description="Enable Qt graphics backend")
    variant("r", default=False, description="Enable R ROOT bindings")
    variant("rpath", default=True, description="Enable RPATH")
    variant("roofit", default=True, description="Build the libRooFit advanced fitting package")
    variant("root7", default=False, description="Enable ROOT 7 support")
    variant("shadow", default=False, description="Enable shadow password support")
    variant("spectrum", default=False, description="Enable support for TSpectrum")
    variant("sqlite", default=False, description="Enable SQLite support")
    variant("ssl", default=False, description="Enable SSL encryption support")
    variant("table", when="@:6.17", default=False, description="Build libTable contrib library")
    variant("tbb", default=True, description="TBB multi-threading support")
    variant("threads", default=True, description="Enable using thread library")
    variant("tmva", default=False, description="Build TMVA multi variate analysis library")
    variant("unuran", default=True, description="Use UNURAN for random number generation")
    variant("vc", default=False, description="Enable Vc for adding new types for SIMD programming")
    variant("vdt", default=True, description="Enable set of fast and vectorisable math functions")
    variant(
        "veccore", default=False, description="Enable support for VecCore SIMD abstraction library"
    )
    variant(
        "vmc", when="@:6.25", default=False, description="Enable the Virtual Monte Carlo interface"
    )
    variant(
        "webgui", default=True, description="Enable web-based UI components of ROOT", when="+root7"
    )
    variant("x", default=True, description="Enable set of graphical options")
    variant("xml", default=True, description="Enable XML parser interface")
    variant("xrootd", default=False, description="Build xrootd file server and its client")

    # ###################### Compiler variants ########################

    variant(
        "cxxstd",
        default="11",
        values=("11", "14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    # ###################### Dependencies ######################

    depends_on("cmake@3.4.3:", type="build", when="@:6.16")
    depends_on("cmake@3.9:", type="build", when="@6.18.00:")
    depends_on("cmake@3.16:", type="build", when="@6.26.00:")
    depends_on("cmake@3.19:", type="build", when="@6.28.00: platform=darwin")
    depends_on("pkgconfig", type="build")

    depends_on("blas")
    depends_on("freetype")
    depends_on("jpeg")
    depends_on("libice")
    depends_on("libpng")
    depends_on("lz4", when="@6.13.02:")  # See cmake_args, below.
    depends_on("ncurses")
    depends_on("nlohmann-json", when="@6.24:")
    depends_on("nlohmann-json@:3.10", when="@6.24:6.26.07")
    depends_on("pcre")
    depends_on("xxhash", when="@6.13.02:")  # See cmake_args, below.
    depends_on("xz")
    depends_on("zlib")
    depends_on("zstd", when="@6.20:")

    # X-Graphics
    depends_on("libx11", when="+x")
    depends_on("libxext", when="+x")
    depends_on("libxft", when="+x")
    depends_on("libxpm", when="+x")
    depends_on("libsm", when="+x")

    # OpenGL
    depends_on("ftgl@2.4.0:", when="+opengl")
    depends_on("glew", when="+opengl")
    depends_on("gl2ps", when="+opengl")
    depends_on("gl", when="+opengl")
    depends_on("glu", when="+opengl")

    # Qt4
    depends_on("qt@:4", when="+qt4")

    # Python
    depends_on("python@2.7:", when="+python", type=("build", "run"))
    depends_on("python@2.7:3.10", when="@:6.26.09 +python", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"), when="+tmva")
    # This numpy dependency was not intended and will hopefully
    # be fixed in 6.20.06.
    # See: https://sft.its.cern.ch/jira/browse/ROOT-10626
    depends_on("py-numpy", type=("build", "run"), when="@6.20.00:6.20.05 +python")

    # Optional dependencies
    depends_on("arrow", when="+arrow")
    depends_on("davix @0.7.1:", when="+davix")
    depends_on("dcap", when="+dcache")
    depends_on("cfitsio", when="+fits")
    depends_on("fcgi", when="+http")
    depends_on("fftw", when="+fftw")
    depends_on("graphviz", when="+graphviz")
    depends_on("gsl", when="+gsl")
    depends_on("jemalloc", when="+jemalloc")
    depends_on("mysql-client", when="+mysql")
    depends_on("openssl", when="+ssl")
    depends_on("openssl", when="+davix")  # Also with davix
    depends_on("oracle-instant-client@19.10.0.0.0", when="+oracle @:6.24.01")
    depends_on("postgresql", when="+postgres")
    depends_on("pythia6+root", when="+pythia6")
    depends_on("pythia8", when="+pythia8")
    depends_on("r", when="+r", type=("build", "run"))
    depends_on("r-rcpp", when="+r", type=("build", "run"))
    depends_on("r-rinside", when="+r", type=("build", "run"))
    depends_on("readline", when="+r")
    depends_on("shadow", when="+shadow")
    depends_on("sqlite", when="+sqlite")
    depends_on("tbb", when="+tbb")
    # See: https://github.com/root-project/root/issues/6933
    conflicts("^intel-tbb@2021.1:", when="@:6.22", msg="Please use an older intel-tbb version")
    conflicts(
        "^intel-oneapi-tbb@2021.1:",
        when="@:6.22",
        msg="Please use an older intel-tbb/intel-oneapi-tbb version",
    )
    # depends_on('intel-tbb@:2021.0', when='@:6.22 ^intel-tbb')
    depends_on("unuran", when="+unuran")
    depends_on("vc@1.0:", when="@6.07.04: +vc")
    depends_on("vc@1.3.0:", when="@6.09.02: +vc")
    depends_on("vdt", when="+vdt")
    depends_on("veccore", when="+veccore")
    depends_on("libxml2", when="+xml")
    depends_on("xrootd", when="+xrootd")
    depends_on("xrootd@:4", when="@:6.22.03 +xrootd")

    # ###################### Conflicts ######################

    # I was unable to build root with any Intel compiler
    # See https://sft.its.cern.ch/jira/browse/ROOT-7517
    conflicts("%intel")

    # ROOT <6.08 was incompatible with the GCC 5+ ABI
    conflicts("%gcc@5.0.0:", when="@:6.07")

    # The version of Clang featured in ROOT <6.12 fails to build with
    # GCC 9.2.1, which we can safely extrapolate to the GCC 9 series.
    conflicts("%gcc@9.0.0:", when="@:6.11")

    # See https://github.com/root-project/root/issues/9297
    conflicts("target=ppc64le:", when="@:6.24")

    # Incompatible variants
    if sys.platform != "darwin":
        conflicts("+opengl", when="~x", msg="OpenGL requires X")
    conflicts("+math", when="~gsl", msg="Math requires GSL")
    conflicts("+tmva", when="~gsl", msg="TVMA requires GSL")
    conflicts("+tmva", when="~mlp", msg="TVMA requires MLP")
    conflicts("cxxstd=11", when="+root7", msg="root7 requires at least C++14")
    conflicts("cxxstd=11", when="@6.25.02:", msg="This version of root requires at least C++14")
    conflicts("cxxstd=20", when="@:6.28.02", msg="C++20 support requires at least version 6.28.04")

    # See https://github.com/root-project/root/issues/11128
    conflicts("%clang@16:", when="@:6.26.07", msg="clang 16+ support was added in 6.26.08")

    # See https://github.com/root-project/root/issues/11714
    if sys.platform == "darwin" and macos_version() >= Version("13"):
        conflicts("@:6.26.09", msg="macOS 13 support was added in 6.26.10")

    # ROOT <6.14 is incompatible with Python >=3.7, which is the minimum supported by spack
    conflicts("+python", when="@:6.13", msg="Spack wants python >=3.7, too new for ROOT <6.14")

    # ROOT does not support LTO builds
    # See https://github.com/root-project/root/issues/11135
    conflicts("+ipo", msg="LTO is not a supported configuration for building ROOT")

    @classmethod
    def filter_detected_exes(cls, prefix, exes_in_prefix):
        result = []
        for exe in exes_in_prefix:
            # no need to check the root executable itself
            # we can get all information from root-config
            if exe.endswith("root"):
                continue
            result.append(exe)
        return result

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        # turn the output of root-config --version
        # (something like 6.22/06)
        # into the format used in this recipe (6.22.06)
        return output.strip().replace("/", ".")

    @classmethod
    def determine_variants(cls, exes, version_str):
        v = []  # list of determined variants
        # there is a fairly direct mapping between build options ( which
        # root-config helpfully outputs) and variants
        output = Executable(exes[0])("--features", output=str, error=str)
        f = set(output.strip().split())  # features as reported by root-config
        # only multivalued variant: cxxstd
        if "cxx11" in f:
            v.append("cxxstd=11")
        elif "cxx14" in f:
            v.append("cxxstd=14")
        elif "cxx17" in f:
            v.append("cxxstd=17")
        elif "cxx20" in f:
            v.append("cxxstd=20")

        # helper function: check if featurename is in features, and if it is,
        # append variantname to variants. featurename may be a list/tuple, in
        # which case the variant is only added if all of them are present
        def _add_variant(variants, features, featurename, variantname):
            if isinstance(featurename, str):
                if featurename in features:
                    variants.append("%s" % variantname)
                else:
                    variants.append("~%s" % variantname[1:])
            else:
                if set(featurename).issubset(features):
                    variants.append("%s" % variantname)
                else:
                    variants.append("~%s" % variantname[1:])

        _add_variant(v, f, "cocoa", "+aqua")
        _add_variant(v, f, "davix", "+davix")
        _add_variant(v, f, "dcache", "+dcache")
        _add_variant(v, f, "fftw3", "+fftw")
        _add_variant(v, f, "fitsio", "+fits")
        _add_variant(v, f, ("ftgl", "opengl"), "+opengl")
        _add_variant(v, f, "gdml", "+gdml")
        _add_variant(v, f, "mathmore", "+math")
        _add_variant(v, f, "gviz", "+graphviz")
        _add_variant(v, f, "http", "+http")
        _add_variant(v, f, ("imt", "tbb"), "+tbb")
        _add_variant(v, f, "jemalloc", "+jemalloc")
        _add_variant(v, f, "memstat", "+memstat")
        _add_variant(v, f, ("minuit", "minuit2"), "+minuit")
        _add_variant(v, f, "mlp", "+mlp")
        _add_variant(v, f, "mysql", "+mysql")
        _add_variant(v, f, "oracle", "+oracle")
        _add_variant(v, f, "pgsql", "+postgres")
        _add_variant(v, f, "pythia6", "+pythia6")
        _add_variant(v, f, "pythia8", "+pythia8")
        _add_variant(v, f, "pyroot", "+python")
        _add_variant(v, f, ("qt", "qtgsi"), "+qt4")
        _add_variant(v, f, "r", "+r")
        _add_variant(v, f, "roofit", "+roofit")
        # webui feature renamed to webgui in 6.18
        if Version(version_str).satisfies("@6.18:"):
            _add_variant(v, f, ("root7", "webgui"), "+webgui")
        else:
            _add_variant(v, f, ("root7", "webui"), "+webgui")
        _add_variant(v, f, "rpath", "+rpath")
        _add_variant(v, f, "shadowpw", "+shadow")
        _add_variant(v, f, "spectrum", "+spectrum")
        _add_variant(v, f, "sqlite", "+sqlite")
        _add_variant(v, f, "ssl", "+ssl")
        _add_variant(v, f, "table", "+table")
        _add_variant(v, f, "thread", "+threads")
        _add_variant(v, f, "tmva", "+tmva")
        _add_variant(v, f, "unuran", "+unuran")
        _add_variant(v, f, "vc", "+vc")
        _add_variant(v, f, "vdt", "+vdt")
        _add_variant(v, f, "veccore", "+veccore")
        _add_variant(v, f, "vmc", "+vmc")
        _add_variant(v, f, ("x11", "xft"), "+x")
        _add_variant(v, f, "xml", "+xml")
        _add_variant(v, f, "xrootd", "+xrootd")
        return " ".join(v)

    def cmake_args(self):
        spec = self.spec
        define = self.define
        define_from_variant = self.define_from_variant
        options = []

        # ###################### Boolean Options ######################
        # For option list format see _process_opts(), below.

        # Options controlling gross build / config behavior.
        options += [
            define("cxxmodules", False),
            define("exceptions", True),
            define("explicitlink", True),
            define("fail-on-missing", True),
            define_from_variant("fortran"),
            define_from_variant("gminimal"),
            define("gnuinstall", True),
            define("libcxx", False),
            define("pch", True),
            define("roottest", False),
            define_from_variant("rpath"),
            define("runtime_cxxmodules", False),
            define("shared", True),
            define("soversion", True),
            define("testing", self.run_tests),
            define_from_variant("thread", "threads"),
            # The following option makes sure that Cling will call the compiler
            # it was compiled with at run time; see #17488, #18078 and #23886
            define("CLING_CXX_PATH", self.compiler.cxx),
        ]

        # Options related to ROOT's ability to download and build its own
        # dependencies. Per Spack convention, this should generally be avoided.

        afterimage_enabled = ("+x" in self.spec) if "platform=darwin" not in self.spec else True

        options += [
            define("builtin_afterimage", afterimage_enabled),
            define("builtin_cfitsio", False),
            define("builtin_davix", False),
            define("builtin_fftw3", False),
            define("builtin_freetype", False),
            define("builtin_ftgl", False),
            define("builtin_gl2ps", False),
            define("builtin_glew", False),
            define("builtin_gsl", False),
            define("builtin_llvm", True),
            define("builtin_lz4", self.spec.satisfies("@6.12.02:6.12")),
            define("builtin_lzma", False),
            define("builtin_nlohmannjson", False),
            define("builtin_openssl", False),
            define("builtin_pcre", False),
            define("builtin_tbb", False),
            define("builtin_unuran", False),
            define("builtin_vc", False),
            define("builtin_vdt", False),
            define("builtin_veccore", False),
            define("builtin_xrootd", False),
            define("builtin_xxhash", self.spec.satisfies("@6.12.02:6.12")),
            define("builtin_zlib", False),
        ]

        # Features
        options += [
            define("afdsmrgd", False),
            define("afs", False),
            define("alien", False),
            define_from_variant("arrow"),
            define("asimage", True),
            define("astiff", True),
            define("bonjour", False),
            define("castor", False),
            define("ccache", False),
            define("chirp", False),
            define("cling", True),
            define_from_variant("cocoa", "aqua"),
            define("dataframe", True),
            define_from_variant("davix"),
            define_from_variant("dcache"),
            define_from_variant("fftw3", "fftw"),
            define_from_variant("fitsio", "fits"),
            define_from_variant("ftgl", "opengl"),
            define_from_variant("gdml"),
            define_from_variant("genvector", "math"),
            define("geocad", False),
            define("gfal", False),
            define_from_variant("gl2ps", "opengl"),
            define("glite", False),
            define("globus", False),
            define_from_variant("gviz", "graphviz"),
            define("hdfs", False),
            define_from_variant("http"),  # See conflicts
            define_from_variant("imt", "tbb"),
            define_from_variant("jemalloc"),
            define("krb5", False),
            define("ldap", False),
            define_from_variant("mathmore", "math"),
            define_from_variant("memstat"),  # See conflicts
            define("minimal", False),
            define_from_variant("minuit"),
            define_from_variant("minuit2", "minuit"),
            define_from_variant("mlp"),
            define("monalisa", False),
            define_from_variant("mysql"),
            define("odbc", False),
            define_from_variant("opengl"),
            define_from_variant("oracle"),
            define_from_variant("pgsql", "postgres"),
            define_from_variant("pythia6"),
            define_from_variant("pythia8"),
            define_from_variant("qt", "qt4"),  # See conflicts
            define_from_variant("qtgsi", "qt4"),  # See conflicts
            define_from_variant("r"),
            define("rfio", False),
            define_from_variant("roofit"),
            define_from_variant("root7"),  # See conflicts
            define("ruby", False),
            define("sapdb", False),
            define_from_variant("shadowpw", "shadow"),
            define_from_variant("spectrum"),
            define_from_variant("sqlite"),
            define("srp", False),
            define_from_variant("ssl"),
            define_from_variant("table"),
            define_from_variant("tbb"),
            define("tcmalloc", False),
            define_from_variant("tmva"),
            define_from_variant("unuran"),
            define_from_variant("vc"),
            define_from_variant("vdt"),
            define_from_variant("veccore"),
            define_from_variant("vmc"),
            define_from_variant("x11", "x"),
            define_from_variant("xft", "x"),
            define_from_variant("xml"),
            define_from_variant("xrootd"),
        ]

        # Necessary due to name change of variant (webui->webgui)
        # https://github.com/root-project/root/commit/d631c542909f2f793ca7b06abc622e292dfc4934
        if self.spec.satisfies("@:6.17.02"):
            options.append(define_from_variant("webui", "webgui"))
        if self.spec.satisfies("@6.18.00:"):
            options.append(define_from_variant("webgui", "webgui"))

        # Some special features
        if self.spec.satisfies("@6.20.02:"):
            options.append(define_from_variant("pyroot", "python"))
        else:
            options.append(define_from_variant("python"))

        # #################### Compiler options ####################

        if sys.platform == "darwin" and self.compiler.cc == "gcc":
            cflags = "-D__builtin_unreachable=__builtin_trap"
            options.extend([define("CMAKE_C_FLAGS", cflags), define("CMAKE_CXX_FLAGS", cflags)])

        # Method for selecting C++ standard depends on ROOT version
        if self.spec.satisfies("@6.18.00:"):
            options.append(define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"))
        else:
            options.append(define("cxx" + self.spec.variants["cxxstd"].value, True))

        if "+x+opengl" in self.spec:
            ftgl_prefix = self.spec["ftgl"].prefix
            options.append(define("FTGL_ROOT_DIR", ftgl_prefix))
            options.append(define("FTGL_INCLUDE_DIR", ftgl_prefix.include))
        if "+python" in self.spec:
            # See https://github.com/spack/spack/pull/11579
            options.append(define("PYTHON_EXECUTABLE", spec["python"].command.path))

        return options

    def setup_build_environment(self, env):
        spec = self.spec

        if "lz4" in spec:
            env.append_path("CMAKE_PREFIX_PATH", spec["lz4"].prefix)

        # This hack is made necessary by a header name collision between
        # asimage's "import.h" and Python's "import.h" headers...
        env.set("SPACK_INCLUDE_DIRS", "", force=True)

        # ...but it breaks header search for any ROOT dependency which does not
        # use CMake. To resolve this, we must bring back those dependencies's
        # include paths into SPACK_INCLUDE_DIRS.
        #
        # But in doing so, we must be careful not to inject system header paths
        # into SPACK_INCLUDE_DIRS, even in a deprioritized form, because some
        # system/compiler combinations don't like having -I/usr/include around.
        def add_include_path(dep_name):
            include_path = spec[dep_name].prefix.include
            if not is_system_path(include_path):
                env.append_path("SPACK_INCLUDE_DIRS", include_path)

        # With that done, let's go fixing those deps
        if spec.satisfies("@:6.12"):
            add_include_path("zlib")
        if "+x" in spec:
            if spec.satisfies("@:6.08") or spec.satisfies("@6.22:"):
                add_include_path("xextproto")
            add_include_path("fontconfig")
            add_include_path("libx11")
            add_include_path("xproto")
        if "+opengl" in spec and "platform=darwin" not in spec:
            add_include_path("glew")
            add_include_path("mesa-glu")
        if "platform=darwin" in spec:
            # Newer deployment targets cause fatal errors in rootcling, so
            # override with an empty value even though it may lead to link
            # warnings when building against ROOT
            env.unset("MACOSX_DEPLOYMENT_TARGET")

    def setup_run_environment(self, env):
        env.set("ROOTSYS", self.prefix)
        env.set("ROOT_VERSION", "v{0}".format(self.version.up_to(1)))
        env.prepend_path("PYTHONPATH", self.prefix.lib.root)
        # the following vars are copied from thisroot.sh; silence a cppyy warning
        env.set("CLING_STANDARD_PCH", "none")
        env.set("CPPYY_API_PATH", "none")

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set("ROOTSYS", self.prefix)
        env.set("ROOT_VERSION", "v{0}".format(self.version.up_to(1)))
        env.prepend_path("PYTHONPATH", self.prefix.lib.root)
        env.prepend_path("PATH", self.prefix.bin)
        env.append_path("CMAKE_MODULE_PATH", self.prefix.cmake)
        env.prepend_path("ROOT_INCLUDE_PATH", dependent_spec.prefix.include)
        if "+rpath" not in self.spec:
            env.prepend_path("LD_LIBRARY_PATH", self.prefix.lib.root)
        if "platform=darwin" in self.spec:
            # Newer deployment targets cause fatal errors in rootcling
            env.unset("MACOSX_DEPLOYMENT_TARGET")

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.set("ROOTSYS", self.prefix)
        env.set("ROOT_VERSION", "v{0}".format(self.version.up_to(1)))
        env.prepend_path("PYTHONPATH", self.prefix.lib.root)
        env.prepend_path("PATH", self.prefix.bin)
        env.prepend_path("ROOT_INCLUDE_PATH", dependent_spec.prefix.include)
        if "+rpath" not in self.spec:
            env.prepend_path("LD_LIBRARY_PATH", self.prefix.lib.root)
