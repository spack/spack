# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *
from spack.util.environment import is_system_path


class Groff(AutotoolsPackage, GNUMirrorPackage):
    """Groff (GNU troff) is a typesetting system that reads
    plain text mixed with formatting commands and produces
    formatted output. Output may be PostScript or PDF, html, or
    ASCII/UTF8 for display at the terminal."""

    homepage = "https://www.gnu.org/software/groff/"
    gnu_mirror_path = "groff/groff-1.22.3.tar.gz"

    tags = ["build-tools"]

    version("1.22.4", sha256="e78e7b4cb7dec310849004fa88847c44701e8d133b5d4c13057d876c1bad0293")
    version("1.22.3", sha256="3a48a9d6c97750bfbd535feeb5be0111db6406ddb7bb79fc680809cda6d828a5")

    # TODO: add html variant, spack doesn't have netpbm and its too
    # complicated for me to find out at this point in time.
    # See brew scripts for groff for guidance:
    # https://github.com/Homebrew/homebrew-core/blob/master/Formula/groff.rb
    # Seems troublesome...netpbm requires groff?
    variant("pdf", default=False, description="Build the `gropdf` executable.")
    variant("x", default=False, description="Enable set of graphical options")
    variant(
        "uchardet",
        default=True,
        description="Builds preconv with uchardet library for "
        "automatic file encoding detection",
    )

    conflicts("+uchardet", when="@:1.22.3")

    depends_on("gawk", type="build")
    depends_on("gmake", type="build")
    depends_on("sed", type="build")
    depends_on("ghostscript", when="+pdf")
    # iconv is being asked whatever the release
    depends_on("iconv")
    # makeinfo is being searched for
    depends_on("texinfo", type="build", when="@1.22.4:")
    # configure complains when there is no uchardet that enhances preconv
    depends_on("uchardet", when="@1.22.4:")
    depends_on("pkgconfig", type="build")

    depends_on("libice", when="+x")
    depends_on("libxaw", when="+x")
    depends_on("libxmu", when="+x")
    depends_on("libx11", when="+x")

    # The perl interpreter line in scripts might be too long as it has
    # not been transformed yet. Call scripts with spack perl explicitly.
    patch("BuildFoundries.patch", when="@1.22.3")
    patch("pdfmom.patch", when="@1.22.3")

    executables = ["^groff$"]

    @property
    def parallel(self):
        return False

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"GNU groff version\s+(\S+)", output)
        return match.group(1) if match else None

    def configure_args(self):
        args = ["--disable-silent-rules"]
        args.extend(self.with_or_without("x"))
        if "@1.22.4:" in self.spec:
            args.extend(self.with_or_without("uchardet"))
        if self.spec["iconv"].name == "libc":
            args.append("--without-libiconv-prefix")
        elif not is_system_path(self.spec["iconv"].prefix):
            args.append("--with-libiconv-prefix={0}".format(self.spec["iconv"].prefix))
        return args

    def setup_run_environment(self, env):
        if self.spec.satisfies("+x"):
            dir = join_path(self.prefix.lib, "X11", "app-defaults")
            env.set_path("XFILESEARCHPATH", dir)
