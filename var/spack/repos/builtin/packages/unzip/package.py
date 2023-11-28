# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Unzip(MakefilePackage):
    """Unzip is a compression and file packaging/archive utility."""

    homepage = "http://www.info-zip.org/Zip.html"
    url = "http://downloads.sourceforge.net/infozip/unzip60.tar.gz"

    version("6.0", sha256="036d96991646d0449ed0aa952e4fbe21b476ce994abc276e49d30e686708bd37")

    patch("configure-cflags.patch", when="%clang@16:")

    # The Cray cc wrapper doesn't handle the '-s' flag (strip) cleanly.
    @when("platform=cray")
    def patch(self):
        filter_file(r"^LFLAGS2=.*", "LFLAGS2=", join_path("unix", "configure"))

    def get_make_args(self):
        make_args = ["-f", join_path("unix", "Makefile")]

        cflags = []
        if self.spec.satisfies("%clang@16:"):
            cflags.append("-Wno-error=implicit-function-declaration")
            cflags.append("-Wno-error=implicit-int")
        cflags.append("-DLARGE_FILE_SUPPORT")

        make_args.append('LOC="{}"'.format(" ".join(cflags)))
        return make_args

    @property
    def build_targets(self):
        target = "macosx" if "platform=darwin" in self.spec else "generic"
        return self.get_make_args() + [target]

    def url_for_version(self, version):
        return "http://downloads.sourceforge.net/infozip/unzip{0}.tar.gz".format(version.joined)

    @property
    def install_targets(self):
        return self.get_make_args() + ["prefix={0}".format(self.prefix), "install"]
