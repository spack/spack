# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cppunit(AutotoolsPackage):
    """Obsolete Unit testing framework for C++"""

    homepage = "https://wiki.freedesktop.org/www/Software/cppunit/"
    url = "https://dev-www.libreoffice.org/src/cppunit-1.13.2.tar.gz"
    git = "https://anongit.freedesktop.org/git/libreoffice/cppunit.git"

    version("master", branch="master")
    version("1.15_20220904", commit="78e64f0edb4f3271a6ddbcdf9cba05138597bfca")
    version(
        "1.14.0",
        sha256="3d569869d27b48860210c758c4f313082103a5e58219a7669b52bfd29d674780",
        preferred=True,
    )
    version("1.13.2", sha256="3f47d246e3346f2ba4d7c9e882db3ad9ebd3fcbd2e8b732f946e0e3eeb9f429f")

    # https://github.com/cms-sw/cmsdist/blob/IB/CMSSW_12_6_X/master/cppunit-1.14-defaulted-function-deleted.patch
    patch("cppunit-1.14-defaulted-function-deleted.patch", when="@1.15:")

    variant(
        "cxxstd",
        default="default",
        values=("default", "98", "11", "14", "17"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    variant(
        "libs",
        default="shared,static",
        values=("shared", "static"),
        multi=True,
        description="Build shared libs, static libs or both",
    )

    depends_on("autoconf", type="build", when="@1.15_20220904")
    depends_on("automake", type="build", when="@1.15_20220904")
    depends_on("libtool", type="build", when="@1.15_20220904")

    def setup_build_environment(self, env):
        cxxstd = self.spec.variants["cxxstd"].value
        cxxstdflag = (
            "" if cxxstd == "default" else getattr(self.compiler, "cxx{0}_flag".format(cxxstd))
        )
        env.append_flags("CXXFLAGS", cxxstdflag)

    def configure_args(self):
        args = ["--disable-doxygen"]
        args += self.enable_or_disable("libs")

        return args
