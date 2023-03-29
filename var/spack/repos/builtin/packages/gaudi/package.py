# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Gaudi(CMakePackage):
    """An experiment-independent HEP event data processing framework"""

    homepage = "https://gaudi.web.cern.ch/gaudi/"
    git = "https://gitlab.cern.ch/gaudi/Gaudi.git"
    url = "https://gitlab.cern.ch/gaudi/Gaudi/-/archive/v33r1/Gaudi-v33r1.tar.gz"

    tags = ["hep"]

    version("master", branch="master")
    version("36.10", sha256="2c1f181c54a76b493b913aeecbd6595236afc08e41d7f1d80be6fe65ac95adb3")
    version("36.9", sha256="b4e080094771f111bd0bcdf744bcab7b028c7e2af7c5dfaa4a977ebbf0160a8f")
    version("36.8", sha256="64b4300a57335af7c1f74c736d7610041a1ef0c1f976e3342a22385b60519afc")
    version("36.7", sha256="8dca43185ba11e1b33f5535d2e384542d84500407b0d1f8cb920be00f05c9716")
    version("36.6", sha256="8fc7be0ce32f99cc6b0be4ebbb246f4bb5008ffbf0c012cb39c0aff813dce6af")
    version("36.5", sha256="593e0316118411a5c5fde5d4d87cbfc3d2bb748a8c72a66f4025498fcbdb0f7e")
    version("36.4", sha256="1a5c27cdc21ec136b47f5805406c92268163393c821107a24dbb47bd88e4b97d")
    version("36.3", sha256="9ac228d8609416afe4dea6445c6b3ccebac6fab1e46121fcc3a056e24a5d6640")
    version("36.2", sha256="a1b4bb597941a7a5b8d60382674f0b4ca5349c540471cd3d4454efbe7b9a09b9")
    version("36.1", sha256="9f718c832313676249e5c3ac76ba4346978ee2328f8cdcb29176498b080402e9")
    version("36.0", sha256="8a0458cef5b616532f9db7cca9fa0e892e602b64c9e93dc0cc6d972e03034830")
    version("35.0", sha256="c01b822f9592a7bf875b9997cbeb3c94dea97cb13d523c12649dbbf5d69b5fa6")
    version("34.0", sha256="28fc4abb5a6b08da5a6b1300451c7e8487f918b055939877219d454abf7668ae")
    version("33.2", sha256="26aaf9c4ff237a60ec79af9bd18ad249fc91c16e297ba77e28e4a256123db6e5")
    version("33.1", sha256="7eb6b2af64aeb965228d4b6ea66c7f9f57f832f93d5b8ad55c9105235af5b042")
    version("33.0", sha256="76a967c41f579acc432593d498875dd4dc1f8afd5061e692741a355a9cf233c8")
    version("32.2", sha256="e9ef3eb57fd9ac7b9d5647e278a84b2e6263f29f0b14dbe1321667d44d969d2e")

    maintainers("drbenmorgan", "vvolkl")

    variant("aida", default=False, description="Build AIDA interfaces support")
    variant("cppunit", default=False, description="Build with CppUnit unit testing")
    variant("docs", default=False, description="Build documentation with Doxygen")
    variant("examples", default=False, description="Build examples")
    variant("gperftools", default=False, description="Build with Google PerfTools support")
    variant("heppdt", default=False, description="Build with HEP Particle Data Table support")
    variant("jemalloc", default=False, description="Build with jemalloc allocator support")
    variant("unwind", default=False, description="Build with unwind call-chains")
    variant("vtune", default=False, description="Build with Intel VTune profiler support")
    variant("xercesc", default=False, description="Build with Xerces-C XML support")

    # only build subdirectory GaudiExamples when +examples
    patch("build_testing.patch", when="@:34")
    # fixes for the cmake config which could not find newer boost versions
    patch("link_target_fixes.patch", when="@33.0:34")
    patch("link_target_fixes32.patch", when="@:32.2")

    # These dependencies are needed for a minimal Gaudi build
    depends_on("aida")
    depends_on("boost@1.67.0: +python")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on("clhep")
    depends_on("cmake", type="build")
    depends_on("cppgsl")
    depends_on("fmt", when="@33.2:")
    depends_on("fmt@:8", when="@:36.9")
    depends_on("intel-tbb")
    depends_on("uuid")
    depends_on("nlohmann-json", when="@35.0:")
    depends_on("python", type=("build", "run"))
    depends_on("python@:3.7", when="@32.2:34", type=("build", "run"))
    depends_on("py-networkx", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
    depends_on("py-xenv@1:", when="@:34.9", type=("build", "run"))
    depends_on("range-v3")
    depends_on("root +python +root7 +ssl +tbb +threads")
    depends_on("zlib")

    # Testing dependencies
    # Note: gaudi only builds examples when testing enabled
    for pv in (
        ["catch2", "@36.8:"],
        ["py-nose", "@35:"],
        ["py-pytest", "@36.2:"],
        ["py-qmtest", "@35:"],
    ):
        depends_on(pv[0], when=pv[1], type="test")
        depends_on(pv[0], when=pv[1] + " +examples")

    # Adding these dependencies triggers the build of most optional components
    depends_on("cppgsl", when="+cppunit")
    depends_on("cppunit", when="+cppunit")
    depends_on("doxygen +graphviz", when="+docs")
    depends_on("gperftools", when="+gperftools")
    depends_on("gdb")
    depends_on("gsl", when="@:31 +examples")
    depends_on("heppdt", when="@:34 +examples")
    depends_on("heppdt", when="+heppdt")
    depends_on("jemalloc", when="+jemalloc")
    depends_on("libpng", when="@:34 +examples")
    depends_on("libunwind", when="+unwind")
    depends_on("relax", when="@:34 +examples")
    depends_on("xerces-c", when="+xercesc")
    # NOTE: pocl cannot be added as a minimal OpenCL implementation because
    #       ROOT does not like being exposed to LLVM symbols.

    # The Intel VTune dependency is taken aside because it requires a license
    depends_on("intel-parallel-studio -mpi +vtune", when="+vtune")

    def cmake_args(self):
        args = [
            # Note: gaudi only builds examples when testing enabled
            self.define("BUILD_TESTING", self.run_tests or self.spec.satisfies("+examples")),
            self.define_from_variant("GAUDI_USE_AIDA", "aida"),
            self.define_from_variant("GAUDI_USE_CPPUNIT", "cppunit"),
            self.define_from_variant("GAUDI_USE_GPERFTOOLS", "gperftools"),
            self.define_from_variant("GAUDI_USE_HEPPDT", "heppdt"),
            self.define_from_variant("GAUDI_USE_JEMALLOC", "jemalloc"),
            self.define_from_variant("GAUDI_USE_UNWIND", "unwind"),
            self.define_from_variant("GAUDI_USE_XERCESC", "xercesc"),
            self.define_from_variant("GAUDI_USE_DOXYGEN", "docs"),
            # needed to build core services like rndmsvc
            self.define("GAUDI_USE_CLHEP", True),
            self.define("GAUDI_USE_PYTHON_MAJOR", str(self.spec["python"].version.up_to(1))),
            # todo:
            self.define("GAUDI_USE_INTELAMPLIFIER", False),
        ]
        # this is not really used in spack builds, but needs to be set
        if self.spec.version < Version("34"):
            args.append("-DHOST_BINARY_TAG=x86_64-linux-gcc9-opt")
        return args

    def setup_run_environment(self, env):
        # environment as in Gaudi.xenv
        env.prepend_path("PATH", self.prefix.scripts)
        env.prepend_path("PYTHONPATH", self.prefix.python)

    def url_for_version(self, version):
        major = str(version[0])
        minor = str(version[1])
        url = "https://gitlab.cern.ch/gaudi/Gaudi/-/archive/v{0}r{1}/Gaudi-v{0}r{1}.tar.gz".format(
            major, minor
        )
        return url
