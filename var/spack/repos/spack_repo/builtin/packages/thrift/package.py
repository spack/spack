# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsBuilder, AutotoolsPackage
from spack_repo.builtin.build_systems.cmake import CMakeBuilder, CMakePackage

from spack.package import *


class Thrift(CMakePackage, AutotoolsPackage):
    """Software framework for scalable cross-language services development.

    Thrift combines a software stack with a code generation engine to
    build services that work efficiently and seamlessly between C++,
    Java, Python, PHP, Ruby, Erlang, Perl, Haskell, C#, Cocoa,
    JavaScript, Node.js, Smalltalk, OCaml and Delphi and other languages.
    """

    homepage = "https://thrift.apache.org"
    url = "https://archive.apache.org/dist/thrift/0.16.0/thrift-0.16.0.tar.gz"
    list_url = "https://archive.apache.org/dist/thrift/"
    list_depth = 1

    maintainers("thomas-bouvier")

    license("Apache-2.0")

    version("0.21.0", sha256="9a24f3eba9a4ca493602226c16d8c228037db3b9291c6fc4019bfe3bd39fc67c")
    version("0.18.1", sha256="04c6f10e5d788ca78e13ee2ef0d2152c7b070c0af55483d6b942e29cff296726")
    version("0.17.0", sha256="b272c1788bb165d99521a2599b31b97fa69e5931d099015d91ae107a0b0cc58f")
    version("0.16.0", sha256="f460b5c1ca30d8918ff95ea3eb6291b3951cf518553566088f3f2be8981f6209")
    version("0.13.0", sha256="7ad348b88033af46ce49148097afe354d513c1fca7c607b59c33ebb6064b5179")
    version("0.12.0", sha256="c336099532b765a6815173f62df0ed897528a9d551837d627c1f87fadad90428")
    version("0.11.0", sha256="c4ad38b6cb4a3498310d405a91fef37b9a8e79a50cd0968148ee2524d2fa60c2")
    version("0.10.0", sha256="2289d02de6e8db04cbbabb921aeb62bfe3098c4c83f36eec6c31194301efa10b")
    version("0.9.3", sha256="b0740a070ac09adde04d43e852ce4c320564a292f26521c46b78e0641564969e")

    variant("openssl", default=False, description="Build with OpenSSL")
    variant("cpp", default=True, description="Build C++ library")
    with when("+cpp"):
        variant("shared", default=True, description="Build shared libraries")
        variant("libevent", default=False, description="Build with libevent support")
        variant("qt5", default=False, description="Build with Qt5 support")
        variant("zlib", default=False, description="Build with ZLIB support")
    variant("c_glib", default=False, description="Build C (GLib) library")
    variant("java", default=False, description="Build support for java")
    variant("javascript", default=False, description="Build Javascript library")
    variant("nodejs", default=False, description="Build NodeJS library")
    variant("python", default=True, description="Build support for python")

    build_system("cmake", "autotools", default="autotools")

    with default_args(type="build"):
        depends_on("c")
        depends_on("cxx")

        depends_on("pkgconfig")
        depends_on("bison")
        depends_on("flex")

        with when("build_system=cmake"):
            depends_on("cmake@3.4:", when="@0.13:")
            depends_on("cmake@3.1:", when="@0.11:")
            depends_on("cmake@2.8.12:")

        with when("build_system=autotools"):
            depends_on("autoconf")
            depends_on("automake")
            depends_on("libtool")

    # min ver in build/cmake/BoostMacros.cmake
    depends_on("boost@1.56:", when="@0.13:")
    depends_on("glib@2:", when="+c_glib")
    depends_on("openssl", when="+openssl")
    depends_on("libevent@2:", when="+libevent")
    depends_on("qt@5", when="+qt5")
    depends_on("zlib-api@1.2.3:", when="+zlib")

    with when("+java"):
        depends_on("ant@1.8:", type="build")
        depends_on("gradle", type="build")
        depends_on("java@7:")

    depends_on("npm", when="+javascript", type="build")
    depends_on("npm", when="+nodejs", type="build")

    with when("+python"):
        extends("python")
        depends_on("py-pip", type="build")
        depends_on("py-setuptools", type="build")
        depends_on("py-six@1.7.2:", type=("build", "run"))

    patch(
        "https://github.com/apache/thrift/commit/69b66a51f2d86746b78300fdf43dd098d6eac7cb.patch?full_index=1",
        sha256="e3c8d43963e3fd0835f1a7a0014bedc4a17480651e9d86ce602466fa1cabfee5",
        when="@0.16.0",
    )


class CMakeBuilder(CMakeBuilder):
    def setup_build_environment(self, env: EnvironmentModifications):
        # Don't install extensions to /usr
        env.set("PY_PREFIX", self.prefix)
        env.set("JAVA_PREFIX", self.prefix)

    def cmake_args(self):
        return [
            self.define_from_variant("BUILD_JAVASCRIPT", "javascript"),
            self.define_from_variant("BUILD_NODEJS", "nodejs"),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define("BUILD_TESTING", False),
            self.define("WITH_AS3", False),
            self.define_from_variant("WITH_CPP", "cpp"),
            self.define_from_variant("WITH_C_GLIB", "c_glib"),
            self.define_from_variant("WITH_JAVA", "java"),
            self.define_from_variant("WITH_JAVASCRIPT", "javascript"),
            self.define_from_variant("WITH_NODEJS", "nodejs"),
            self.define_from_variant("WITH_PYTHON", "python"),
            self.define_from_variant("WITH_ZLIB", "zlib"),
        ]


class AutotoolsBuilder(AutotoolsBuilder):
    def setup_build_environment(self, env: EnvironmentModifications):
        # Don't install extensions to /usr
        env.set("PY_PREFIX", self.prefix)
        env.set("JAVA_PREFIX", self.prefix)

    def configure_args(self):
        return [
            *self.enable_or_disable("shared"),
            "--enable-tests=no",
            *self.with_or_without("cpp"),
            *self.with_or_without("libevent"),
            *self.with_or_without("zlib"),
            *self.with_or_without("qt5"),
            *self.with_or_without("c_glib"),
            *self.with_or_without("openssl", "prefix"),
            *self.with_or_without("java"),
            "--without-kotlin",
            "--without-erlang",
            *self.with_or_without("nodejs"),
            "--without-nodets",
            "--without-lua",
            *self.with_or_without("python"),
            "--without-py3",
            "--without-perl",
            "--without-php",
            "--without-php_extension",
            "--without-dart",
            "--without-ruby",
            "--without-go",
            "--without-swift",
            "--without-rs",
            "--without-cl",
            "--without-haxe",
            "--without-netstd",
            "--without-d",
        ]
