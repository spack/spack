# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *


class Openlibm(MakefilePackage):
    """OpenLibm is an effort to have a high quality, portable, standalone C
    mathematical library"""

    homepage = "https://github.com/JuliaMath/openlibm"
    url = "https://github.com/JuliaMath/openlibm/archive/refs/tags/v0.8.0.tar.gz"

    maintainers("haampie")

    license("MIT AND BSD-2-Clause AND ISC AND LGPL-2.1-or-later")

    version("0.8.6", sha256="347998968cfeb2f9b91de6a8e85d2ba92dec0915d53500a4bc483e056f85b94c")
    version("0.8.5", sha256="d380c2d871f6dc16e22893569d57bda9121742cc8f6534510526e5278867c6cf")
    version("0.8.4", sha256="c0bac12a6596f2315341790a7f386f9162a5b1f98db9ec40d883fce64e231942")
    version("0.8.3", sha256="9f83e40d1180799e580371691be522f245da4c2fdae3f09cd33031706de4c59c")
    version("0.8.2", sha256="7244f9aa468584744e260cef740d57d10eab6e9c05f62084f8f2ba457f4b4b1d")
    version("0.8.1", sha256="ba8a282ecd92d0033f5656bb20dfc6ea3fb83f90ba69291ac8f7beba42dcffcf")
    version("0.8.0", sha256="03620768df4ca526a63dd675c6de95a5c9d167ff59555ce57a61c6bf49e400ee")
    version("0.7.5", sha256="be983b9e1e40e696e8bbb7eb8f6376d3ca0ae675ae6d82936540385b0eeec15b")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    def make(self, spec, prefix):
        args = [
            "prefix={0}".format(prefix),
            "USE_GCC={0}".format("1" if self.compiler.name == "gcc" else "0"),
            "USE_CLANG={0}".format("1" if self.compiler.name == "clang" else "0"),
        ]
        make(*args)

    def install(self, spec, prefix):
        args = ["prefix={0}".format(prefix)]
        make("install", *args)
