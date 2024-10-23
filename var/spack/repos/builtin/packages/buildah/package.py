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

    version("1.37.5", commit="5fd40b989860984a00f6fc1539ff53caceca1325")

    depends_on("gmake", type="build")
    depends_on("go@1.21:", type="build")
    depends_on("git", type="build")
    depends_on("go-md2man", type="build")
    depends_on("bats")
    depends_on("bzip2")
    depends_on("gpgme")
    depends_on("libassuan")
    depends_on("libseccomp")
    depends_on("runc")

    def install(self, spec, prefix):
        make(f"PREFIX={prefix}", "install")
