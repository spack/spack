# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Btop(MakefilePackage):
    """Resource monitor that shows usage and stats for processor,
    memory, disks, network and processes.
    """

    homepage = "https://github.com/aristocratos/btop#documents"
    url = "https://github.com/aristocratos/btop/archive/refs/tags/v1.2.13.tar.gz"

    maintainers("alalazo")

    version("1.2.13", sha256="668dc4782432564c35ad0d32748f972248cc5c5448c9009faeb3445282920e02")

    conflicts("%gcc@:9", msg="C++ 20 is required")

    build_targets = ["STATIC=true", "VERBOSE=true"]

    @property
    def install_targets(self):
        return [f"PREFIX={self.prefix}", "install"]
