# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gvproxy(MakefilePackage):
    """A new network stack based on gVisor."""

    homepage = "https://github.com/containers/gvisor-tap-vsock"
    url = "https://github.com/containers/gvisor-tap-vsock/archive/refs/tags/v0.8.5.tar.gz"

    license("Apache-2.0", checked_by="cmelone")

    version("0.8.4", sha256="6a2645a3627bdf1d8bfe4a41ecf97956df987464aade18e1574f67e21950e0d1")

    depends_on("go@1.23.0:", type="build")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        make("gvproxy")
        install("bin/gvproxy", prefix.bin)
