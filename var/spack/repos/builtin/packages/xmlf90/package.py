# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Xmlf90(AutotoolsPackage):
    """xmlf90 is a suite of libraries to handle XML in Fortran."""

    homepage = "https://xmlf90.readthedocs.io/en/latest/"
    git = "https://gitlab.com/siesta-project/libraries/xmlf90"

    license("BSD-2-Clause")

    version("1.6.3", tag="1.6.3")
    version("1.6.2", tag="1.6.2")
    version("1.6.1", tag="1.6.1")
    version("1.6.0", tag="1.6.0")
    version("1.5.6", tag="1.5.6")
    version("1.5.5", tag="1.5.5")
    version("1.5.4", tag="xmlf90-1.5.4")
    version("1.5.3", tag="xmlf90-1.5.3")
    version("1.5.2", tag="xmlf90-1.5.2")

    depends_on("autoconf@2.69:", type="build")
    depends_on("automake@1.14:", type="build")
    depends_on("libtool@2.4.2:", type="build")
    depends_on("m4", type="build")
    
    build_directory = "spack-build"
    patch("fj_modmakefile.patch", when="%fj")

    @when("@1.5.2")
    def autoreconf(self, spec, prefix):
        sh = which("sh")
        sh("autogen.sh")

    def configure_args(self):
        if self.spec.satisfies("%gcc"):
            return ["FCFLAGS=-ffree-line-length-none"]
        return []

    @run_after("install")
    def fix_mk(self):
        install(join_path(self.prefix, "share", "org.siesta-project", "xmlf90.mk"), prefix)
