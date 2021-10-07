# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Attr(AutotoolsPackage):
    """Commands for Manipulating Filesystem Extended Attributes"""

    homepage = "https://savannah.nongnu.org/projects/attr"
    url = "http://download.savannah.gnu.org/releases/attr/attr-2.4.47.src.tar.gz"

    maintainers("cosmicexplorer")

    # FIXME: spack does not validate any of the checksums for this package for some reason!
    version("2.5.1", sha256="bae1c6949b258a0d68001367ce0c741cebdacdd3b62965d17e5eb23cd78adaf8")
    version("2.5.0", sha256="421501c3f7a56ab12e2c34a187bcae44f7d141f965ade18d01e6261d138f163b")
    version("2.4.48", sha256="5ead72b358ec709ed00bbf7a9eaef1654baad937c001c044fe8b74c57f5324e7")
    version("2.4.47", sha256="25772f653ac5b2e3ceeb89df50e4688891e21f723c460636548971652af0a859")
    version("2.4.46", sha256="dcd69bdca7ff166bc45141eddbcf21967999a6b66b0544be12a1cc2fd6340e1f")

    variant("nls", default=True, description="Enable Native Language Support")

    depends_on("gettext", when="+nls")

    def url_for_version(self, version):
        if version >= Version("2.4.48"):
            url = "http://download.savannah.gnu.org/releases/attr/attr-{0}.tar.gz"
        else:
            url = "http://download.savannah.gnu.org/releases/attr/attr-{0}.src.tar.gz"
        return url.format(version)

    # Ref. https://www.linuxfromscratch.org/blfs/view/7.5/postlfs/attr.html
    def configure_args(self):
        args = []
        args.append("--disable-static")

        if "+nls" in self.spec:
            args.extend(
                [
                    "LDFLAGS={0}".format(self.spec["gettext"].libs.search_flags),
                    "LIBS=-lintl",
                    "--enable-nls",
                ]
            )
        else:
            args.append("--disable-nls")

        return args

    @when("@:2.4.47")
    def install(self, spec, prefix):
        make("install", "install-dev", "install-lib")

        make("install", "install-dev", "install-lib")
