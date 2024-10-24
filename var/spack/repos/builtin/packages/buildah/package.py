# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Buildah(MakefilePackage):
    """Lightweight tool for building Open Container Initiative (OCI) container images"""

    homepage = "https://buildah.io/"
    git = "https://github.com/containers/buildah"

    maintainers("upsj")

    license("Apache-2.0", checked_by="upsj")

    version("1.37.5", tag="v1.37.5", commit="5fd40b989860984a00f6fc1539ff53caceca1325")

    with default_args(type="build"):
        depends_on("gmake")
        depends_on("pkgconfig")
        depends_on("go@1.21:")
        depends_on("git")
        depends_on("go-md2man")

    depends_on("bats")
    depends_on("bzip2")
    depends_on("gpgme")
    depends_on("libassuan")
    depends_on("libseccomp")
    depends_on("runc")

    def install(self, spec, prefix):
        make(f"PREFIX={prefix}", "install")
