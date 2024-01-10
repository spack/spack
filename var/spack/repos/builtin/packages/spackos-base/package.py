# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems.generic import PackageNoDep
from spack.build_systems.gnu import GNUMirrorPackageNoDep
from spack.package import *


class SpackosBase(PackageNoDep, GNUMirrorPackageNoDep):
    homepage = "https://github.com/spack/spack"
    gnu_mirror_path = "libc/glibc-2.33.tar.gz"
    # NOTE: this refers to glibc's 2.38 tarball to shut up the URL fetcher
    version("2.38", sha256="16e51e0455e288f03380b436e41d5927c60945abd86d0c9852b84be57dd6ed5e", expand=False)

    depends_on("glibc+stage1")
    depends_on("libxcrypt+stage1")

    def install(self, spec, prefix):
        with open(prefix.see_i_installed_something, "w+") as f:
            print("yup, definitely installed something", file=f)
