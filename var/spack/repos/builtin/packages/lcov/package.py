# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Lcov(MakefilePackage):
    """LCOV is a graphical front-end for GCC's coverage testing tool gcov.
    It collects gcov data for multiple source files and creates HTML pages
    containing the source code annotated with coverage information. It also
    adds overview pages for easy navigation within the file structure. LCOV
    supports statement, function and branch coverage measurement."""

    homepage = "http://ltp.sourceforge.net/coverage/lcov.php"
    url = "https://github.com/linux-test-project/lcov/releases/download/v2.0/lcov-2.0.tar.gz"
    maintainers("KineticTheory")

    version("2.0", sha256="1857bb18e27abe8bcec701a907d5c47e01db4d4c512fc098d1a6acd29267bf46")
    version("1.16", sha256="987031ad5528c8a746d4b52b380bc1bffe412de1f2b9c2ba5224995668e3240b")
    version("1.15", sha256="c1cda2fa33bec9aa2c2c73c87226cfe97de0831887176b45ee523c5e30f8053a")
    version("1.14", sha256="14995699187440e0ae4da57fe3a64adc0a3c5cf14feab971f8db38fb7d8f071a")

    depends_on("perl", type=("build", "run"))
    def install(self, spec, prefix):
        make(
            "LCOV_PERL_PATH=%s" % self.spec["perl"].command.path,
            "DESTDIR=",
            "PREFIX=%s" % prefix,
            "install",
        )

