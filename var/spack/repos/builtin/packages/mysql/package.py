# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import tempfile

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Mysql(CMakePackage):
    """MySQL is an open source relational database management system."""

    homepage = "https://www.mysql.com/"
    url = "https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-8.0.15.tar.gz"


    version("8.0.29", sha256="fc02246f39764b7b2b7815bb260d52983296919ba13246f3de8873b3e86dc579")

    version("8.0.19", sha256="323b11dc35e25f13ed55d5b1c2f8f511fbead3c02675472f1f00c88e3a878a1d")
    version("8.0.18", sha256="e60f1e1e008ae7fb1114f50c3b7e58aedea169e694528e9222a11013dbb2516b")
    version("8.0.17", sha256="c1a3e0a502abbb7b3863033c721d4e4d853c072f8d472737407245043a2eab39")
    version("8.0.16", sha256="03e1632236b6d4fd72351c414a07287d78a39ad5ec5807772ec751d2fdc6351a")
    version("8.0.15", sha256="2eb8b4c8f475558d7e0084f253519eb8164e278f7706c6b5393a65f5ae7ae52f")
    version("8.0.14", sha256="e8dd08b83b856ae350f93a8a52c38e619197c735f27d76e7e317dd461932323a")
    version("8.0.13", sha256="5a90ab5d98fc05caacea1a9799324460efcd69d869d376ceecee0ec72301b53d")
    version("8.0.12", sha256="758c744c15d2d82345e2059815db3b99a605106afa0a5e9e307fa20df81799d3")
    version("8.0.11", sha256="62e11ca424e7199884083cd137687bf667e7aa229aff767844b09d768385482b")
    version("5.7.27", sha256="f7fe9b0ac3f880f8a836e833cddc97ca15f6589cbbfd8799dad83ba0e7e7a171")
    version("5.7.26", sha256="44826b185c5cd0a0a4175ce46ec9aa7af0c313b78225d0e1253c54abecb81051")
    version("5.7.25", sha256="0e836c0d99b330287d9a2083d3b33bebef497e893671c27096de4f94c3c13eaf")
    version("5.7.24", sha256="555895c0754f9624af81c0717fd37937167bcdcd53f955cc368f237ecb4a0e20")
    version("5.7.23", sha256="bc2c017b77d97e0cb564b0027c6c3a16a38e5b40f2b072ddfd1bb8bdba321eb6")
    version("5.7.22", sha256="f27d7172c39af6bc6ca1645d659d252670626385ca3d1440a5c930f830e1252e")
    version("5.7.21", sha256="ef9720a4793d101a17b81dc11056716aca8a4db0e20c2af7cd62d51f3ef13aa0")
    version("5.7.20", sha256="5a1359488991fac8f14274d2f697101b4e6f53b7923fa3b21777c17fc3f720c6")
    version("5.7.19", sha256="91df9c2f90bd2dc439b2dd67ef6e783ea07bf8c98f9b4ba7b1ef5d44e2d849bd")
    version("5.7.18", sha256="1532cbee65d64766ae546ad8ab00f761ad9655a4ecf90d40ae1aef8d31462f46")
    version("5.7.17", sha256="878ac3c4f00aac2e71aa596a3ee55d88ddc535470f0da6487aae5c82209d0e6f")
    version("5.7.16", sha256="33483ae61846ba441eef9bdd49e055cbf1e2f22e822932b9c435aeef6ee7fec6")
    version("5.7.15", sha256="0366322a45ea9c016532f09c51a654817c6c87436e2d01295c7cd7a271362156")
    version("5.7.14", sha256="15effb24fb9c80075ad94e71e54d9c2888bc81439ebbb99928dd4e3eb0b25b50")
    version("5.7.13", sha256="938b72871c02ef8563921e4b364fdf9b95692b0dcaf199c12e9965cb5798e2e0")
    version("5.7.12", sha256="ec9bcdb4be9e28566a585c266029464eb0d8f7582d68f4ff749f5954fde31203")
    version("5.7.11", sha256="706c04e1e9c3f95f54418fa72d347d3b8abff6d17b46832d380ddcdb1e764f2f")
    version("5.7.10", sha256="d3cc318e91e1546e0a2a5ff63301b1d85887eb6e44f3100d27668a21f051a144")
    version("5.7.9", sha256="bb890b1e6f34b41d1a1bc2266f960d1d5890d5dd4bc4b7dfdafdbe5d85936232")
    version("5.6.44", sha256="5c8d2996d4cad09316ea177438fc325b2a795dc8d42622ed8c919c8588ca2841")
    version("5.6.43", sha256="524d6adb0651c5a62d17405a802cb346b969311ebb48508f7c477f9d986ca63a")
    version("5.5.62", sha256="38c1038324e3146db5ecb1f5a218b039dd16b32391966bcf6361cf66746db7d2")

    variant("client_only", default=False, description="Build and install client only.")
    variant(
        "cxxstd",
        default="14",
        values=("98", "11", "14", "17"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    # 5.7.X cannot be compiled client-only.
    conflicts("+client_only", when="@5.7.0:5.7")
    # Server code has a macro 'byte', which conflicts with C++17's
    # std::byte.
    conflicts("cxxstd=17", when="@8.0.0:~client_only")

    provides("mysql-client")

    # https://dev.mysql.com/doc/refman/8.0/en/source-installation.html

    # See CMAKE_MINIMUM_REQUIRED in CMakeLists.txt
    depends_on("cmake@3.1.0:", type="build", when="@5.7.0:5.7 platform=win32")
    depends_on("cmake@3.8.0:", type="build", when="@8.0.0: platform=win32")
    depends_on("cmake@3.9.2:", type="build", when="@8.0.0: platform=darwin")
    depends_on("cmake@3.4.0:", type="build", when="@8.0.0: platform=solaris")
    depends_on("cmake@2.6:", type="build", when="@:5.6")
    depends_on("cmake@2.8.9:", type="build", when="@5.7.0:5.7")
    depends_on("cmake@2.8.12:", type="build", when="@8.0.0:")

    depends_on("gmake@3.75:", type="build")
    depends_on("pkgconfig", type="build", when="@5.7.0:")
    depends_on("doxygen", type="build", when="@8.0.0:")

    # Each version of MySQL requires a specific version of boost
    # See BOOST_PACKAGE_NAME in cmake/boost.cmake
    # 8.0.29
    depends_on("boost@1.77.0 cxxstd=98", type="build", when="@8.0.29 cxxstd=98")
    depends_on("boost@1.77.0 cxxstd=11", type="build", when="@8.0.29 cxxstd=11")
    depends_on("boost@1.77.0 cxxstd=14", type="build", when="@8.0.29 cxxstd=14")
    depends_on("boost@1.77.0 cxxstd=17", type="build", when="@8.0.29 cxxstd=17")
    # 8.0.19
    depends_on("boost@1.70.0 cxxstd=98", type="build", when="@8.0.19 cxxstd=98")
    depends_on("boost@1.70.0 cxxstd=11", type="build", when="@8.0.19 cxxstd=11")
    depends_on("boost@1.70.0 cxxstd=14", type="build", when="@8.0.19 cxxstd=14")
    depends_on("boost@1.70.0 cxxstd=17", type="build", when="@8.0.19 cxxstd=17")
    # 8.0.16--8.0.18
    depends_on("boost@1.69.0 cxxstd=98", type="build", when="@8.0.16:8.0.18 cxxstd=98")
    depends_on("boost@1.69.0 cxxstd=11", type="build", when="@8.0.16:8.0.18 cxxstd=11")
    depends_on("boost@1.69.0 cxxstd=14", type="build", when="@8.0.16:8.0.18 cxxstd=14")
    depends_on("boost@1.69.0 cxxstd=17", type="build", when="@8.0.16:8.0.18 cxxstd=17")
    # 8.0.14--8.0.15
    depends_on("boost@1.68.0 cxxstd=98", type="build", when="@8.0.14:8.0.15 cxxstd=98")
    depends_on("boost@1.68.0 cxxstd=11", type="build", when="@8.0.14:8.0.15 cxxstd=11")
    depends_on("boost@1.68.0 cxxstd=14", type="build", when="@8.0.14:8.0.15 cxxstd=14")
    depends_on("boost@1.68.0 cxxstd=17", type="build", when="@8.0.14:8.0.15 cxxstd=17")
    # 8.0.12--8.0.13
    depends_on("boost@1.67.0 cxxstd=98", type="build", when="@8.0.12:8.0.13 cxxstd=98")
    depends_on("boost@1.67.0 cxxstd=11", type="build", when="@8.0.12:8.0.13 cxxstd=11")
    depends_on("boost@1.67.0 cxxstd=14", type="build", when="@8.0.12:8.0.13 cxxstd=14")
    depends_on("boost@1.67.0 cxxstd=17", type="build", when="@8.0.12:8.0.13 cxxstd=17")
    # 8.0.11
    depends_on("boost@1.66.0 cxxstd=98", type="build", when="@8.0.11 cxxstd=98")
    depends_on("boost@1.66.0 cxxstd=11", type="build", when="@8.0.11 cxxstd=11")
    depends_on("boost@1.66.0 cxxstd=14", type="build", when="@8.0.11 cxxstd=14")
    depends_on("boost@1.66.0 cxxstd=17", type="build", when="@8.0.11 cxxstd=17")
    # 5.7.X
    depends_on("boost@1.59.0 cxxstd=98", when="@5.7.0:5.7 cxxstd=98")
    depends_on("boost@1.59.0 cxxstd=11", when="@5.7.0:5.7 cxxstd=11")
    depends_on("boost@1.59.0 cxxstd=14", when="@5.7.0:5.7 cxxstd=14")
    depends_on("boost@1.59.0 cxxstd=17", when="@5.7.0:5.7 cxxstd=17")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants, when="@5.7:")

    depends_on("rpcsvc-proto")
    depends_on("ncurses")
    depends_on("openssl")
    depends_on("libtirpc", when="@5.7.0: platform=linux")
    depends_on("libedit", type=["build", "run"])
    depends_on("perl", type=["build", "test"], when="@:7")
    depends_on("bison@2.1:", type="build")
    depends_on("m4", type="build", when="@develop platform=solaris")
    depends_on("cyrus-sasl", when="@:5.7")

    patch("fix-no-server-5.5.patch", level=1, when="@5.5.0:5.5")
    patch("old_ssl_fix.patch", when="@8.0.29")

    @property
    def command(self):
        return Executable(self.prefix.bin.mysql_config)

    @property
    def libs(self):
        return find_libraries("libmysqlclient", root=self.prefix, recursive=True)

    def url_for_version(self, version):
        #url = "https://dev.mysql.com/get/Downloads/MySQL-{0}/mysql-{1}.tar.gz"
        url = "https://github.com/mysql/mysql-server/archive/refs/tags/mysql-{0}.tar.gz"
        return url.format(version)

    def cmake_args(self):
        spec = self.spec
        options = []
        if "boost" in spec:
            options.append("-DBOOST_ROOT={0}".format(spec["boost"].prefix))
        if "+client_only" in self.spec:
            options.append("-DWITHOUT_SERVER:BOOL=ON")
        options.append("-DWITH_EDITLINE=system")
        options.append("-Dlibedit_INCLUDE_DIR={0}".format(spec["libedit"].prefix.include))
        options.append("-Dlibedit_LIBRARY={0}".format(spec["libedit"].libs.directories[0]))
        return options

    def _fix_dtrace_shebang(self, env):
        # dtrace may cause build to fail because it uses
        # '/usr/bin/python' in the shebang. To work around that we copy
        # the original script into a temporary folder, and change the
        # shebang to '/usr/bin/env python'. Treatment adapted from that
        # used in glib recipe per M. Culpo @b2822b258.
        dtrace = which("dtrace").path
        dtrace_copy_path = os.path.join(tempfile.mkdtemp(), "dtrace-copy")
        dtrace_copy = os.path.join(dtrace_copy_path, "dtrace")
        mkdirp(dtrace_copy_path)
        copy(dtrace, dtrace_copy)
        filter_file(
            "^#!/usr/bin/python",
            "#!/usr/bin/env {0}".format(os.path.basename(self.spec["python"].command)),
            dtrace_copy,
        )
        # To have our own copy of dtrace in PATH, we need to
        # prepend to PATH the temporary folder where it resides.
        env.prepend_path("PATH", dtrace_copy_path)

    def setup_build_environment(self, env):
        cxxstd = self.spec.variants["cxxstd"].value
        flag = getattr(self.compiler, "cxx{0}_flag".format(cxxstd))
        if flag:
            env.append_flags("CXXFLAGS", flag)
        if cxxstd != "98":
            if int(cxxstd) > 11:
                env.append_flags("CXXFLAGS", "-Wno-deprecated-declarations")
            if int(cxxstd) > 14:
                env.append_flags("CXXFLAGS", "-Wno-error=register")

        if self.spec.satisfies("@:7") and "python" in self.spec.flat_dependencies():
            self._fix_dtrace_shebang(env)
