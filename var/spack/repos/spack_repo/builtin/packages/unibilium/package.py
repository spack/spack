# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *


class Unibilium(MakefilePackage, AutotoolsPackage):
    """A terminfo parsing library"""

    homepage = "https://github.com/neovim/unibilium/"
    url = "https://github.com/neovim/unibilium/archive/v2.1.2.tar.gz"

    license("LGPL-3.0-or-later")

    version("2.1.2", sha256="370ecb07fbbc20d91d1b350c55f1c806b06bf86797e164081ccc977fc9b3af7a")
    version("2.1.1", sha256="6f0ee21c8605340cfbb458cbd195b4d074e6d16dd0c0e12f2627ca773f3cabf1")
    version("2.1.0", sha256="05bf97e357615e218126f7ac086e7056a23dc013cfac71643b50a18ad390c7d4")
    version("2.0.0", sha256="78997d38d4c8177c60d3d0c1aa8c53fd0806eb21825b7b335b1768d7116bc1c1")
    version("1.2.0", sha256="623af1099515e673abfd3cae5f2fa808a09ca55dda1c65a7b5c9424eb304ead8")

    depends_on("c", type="build")

    build_system(
        conditional("makefile", when="@:2.1.1"),
        conditional("autotools", when="@2.1.2:"),
        default="autotools",
    )

    depends_on("gmake", type="build")
    depends_on("libtool", type="build")
    depends_on("perl", type="build")
    depends_on("gzip", type="build")

    with when("build_system=autotools"):
        depends_on("autoconf", when="@2.1.2:", type="build")
        depends_on("automake", when="@2.1.2:", type="build")

    def install(self, spec, prefix):
        make("PREFIX=" + prefix)
        make("install", "PREFIX=" + prefix)
