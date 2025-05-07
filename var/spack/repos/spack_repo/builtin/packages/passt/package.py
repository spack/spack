# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Passt(MakefilePackage):
    """Passt provides full, quasi-native network connectivity to
    virtual machines in user-mode without requiring any capabilities or privileges."""

    homepage = "https://passt.top"
    git = "https://passt.top/passt"

    license("GPL-2.0-or-later AND BSD-3-Clause", checked_by="cmelone")

    version("2025_01_21.4f2c8e7", tag="2025_01_21.4f2c8e7")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        make()
        install("passt", prefix.bin)
        install("pasta", prefix.bin)
