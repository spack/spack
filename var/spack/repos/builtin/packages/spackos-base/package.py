# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems.bundle import BundlePackageNoDep
from spack.package import *


class SpackosBase(BundlePackageNoDep):
    homepage = "https://github.com/spack/spack"
    # NOTE: this refers to glibc's 2.38 tarball to shut up the URL fetcher
    version("0")

    depends_on("glibc+stage2")
    depends_on("libxcrypt+stage2")

    def install(self, spec, prefix):
        with open(prefix.see_i_installed_something, "w+") as f:
            print("yup, definitely installed something", file=f)
