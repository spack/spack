# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SquashfsMount(MakefilePackage):
    """Allows non-root users to mount squashfs files without the overhead of
    squashfuse."""

    homepage = "https://github.com/eth-cscs/squashfs-mount"
    url = "https://github.com/eth-cscs/squashfs-mount/archive/refs/tags/v0.1.0.tar.gz"

    maintainers("haampie")

    version("0.1.0", sha256="37841ede7a7486d437fd06ae13e432560f81806f69addc72cfc8e564c8727bc6")

    variant("suid", default=False, description="Make squashfs-mount a suid executable")

    depends_on("util-linux", type="link")

    def install(self, spec, prefix):
        tgt = "install" if "~suid" in spec else "install-suid"
        make(tgt, "prefix=" + prefix)
