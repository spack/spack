# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re
import shutil

from spack.package import *


class Ghostscript(AutotoolsPackage):
    """An interpreter for the PostScript language and for PDF."""

    homepage = "https://ghostscript.com/"
    url = "https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs926/ghostscript-9.26.tar.gz"

    executables = [r"^gs$"]

    version("10.0.0", sha256="a57764d70caf85e2fc0b0f59b83b92e25775631714dcdb97cc6e0cea414bb5a3")
    version("9.56.1", sha256="1598b9a38659cce8448d42a73054b2f9cbfcc40a9b97eeec5f22d4d6cd1de8e6")
    version("9.54.0", sha256="0646bb97f6f4d10a763f4919c54fa28b4fbdd3dff8e7de3410431c81762cade0")
    version("9.53.3", sha256="6eaf422f26a81854a230b80fd18aaef7e8d94d661485bd2e97e695b9dce7bf7f")
    version("9.50", sha256="0f53e89fd647815828fc5171613e860e8535b68f7afbc91bf89aee886769ce89")
    version("9.27", sha256="9760e8bdd07a08dbd445188a6557cb70e60ccb6a5601f7dbfba0d225e28ce285")
    version("9.26", sha256="831fc019bd477f7cc2d481dc5395ebfa4a593a95eb2fe1eb231a97e450d7540d")
    version("9.21", sha256="02bceadbc4dddeb6f2eec9c8b1623d945d355ca11b8b4df035332b217d58ce85")
    version("9.18", sha256="5fc93079749a250be5404c465943850e3ed5ffbc0d5c07e10c7c5ee8afbbdb1b")

    # https://www.ghostscript.com/ocr.html
    variant("tesseract", default=False, description="Use the Tesseract library for OCR")

    depends_on("pkgconfig", type="build")
    depends_on("krb5", type="link")

    depends_on("freetype@2.4.2:")
    depends_on("jpeg")
    depends_on("lcms")
    depends_on("libpng")
    depends_on("libtiff")
    depends_on("zlib-api")
    depends_on("libxext")
    depends_on("gtkplus")

    # https://www.ghostscript.com/doc/9.53.0/News.htm
    conflicts("+tesseract", when="@:9.52", msg="Tesseract OCR engine added in 9.53.0")

    # https://trac.macports.org/ticket/62832
    conflicts(
        "+tesseract", when="platform=darwin", msg="Tesseract does not build correctly on macOS"
    )

    patch("nogoto.patch", when="%fj@:4.1.0")

    # Related bug report: https://bugs.ghostscript.com/show_bug.cgi?id=702985
    patch(
        "https://github.com/ArtifexSoftware/ghostpdl/commit/41ef9a0bc36b9db7115fbe9623f989bfb47bbade.patch?full_index=1",
        when="@:9.53.3^freetype@2.10.3:",
        sha256="f3c2e56aa552a030c6db2923276ff2d140e39c511f92d9ef6c74a24776940af7",
    )

    def url_for_version(self, version):
        baseurl = "https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs{0}/ghostscript-{1}.tar.gz"
        return baseurl.format(version.joined, version.dotted)

    def patch(self):
        """Ghostscript comes with all of its dependencies vendored.
        In order to build with Spack versions of these dependencies,
        we have to remove these vendored dependencies.

        Note that this approach is also recommended by Linux from Scratch:
        https://www.linuxfromscratch.org/blfs/view/svn/pst/gs.html
        """
        directories = ["freetype", "jpeg", "libpng", "zlib"]
        if self.spec.satisfies("@:9.21"):
            directories.append("lcms2")
        else:
            directories.append("lcms2mt")
        for directory in directories:
            shutil.rmtree(directory)

        filter_file(
            "ZLIBDIR=src",
            "ZLIBDIR={0}".format(self.spec["zlib-api"].prefix.include),
            "configure.ac",
            "configure",
            string=True,
        )

    def configure_args(self):
        args = ["--disable-compile-inits", "--enable-dynamic", "--with-system-libtiff"]

        if self.spec.satisfies("@9.53:"):
            args.extend(self.with_or_without("tesseract"))

        return args

    def build(self, spec, prefix):
        make()
        make("so")

    def install(self, spec, prefix):
        make("install")
        make("soinstall")

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--help", output=str, error=str)
        match = re.search(r"GPL Ghostscript (\S+)", output)
        return match.group(1) if match else None
