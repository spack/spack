# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RpcsvcProto(AutotoolsPackage):
    """rpcsvc protocol definitions from glibc."""

    homepage = "https://github.com/thkukuk/rpcsvc-proto"
    url = "https://github.com/thkukuk/rpcsvc-proto/releases/download/v1.4.3/rpcsvc-proto-1.4.3.tar.xz"

    version("1.4.3", sha256="69315e94430f4e79c74d43422f4a36e6259e97e67e2677b2c7d7060436bd99b1")
    version("1.4.2", sha256="678851b9f7ddf4410d2859c12016b65a6dd1a0728d478f18aeb54d165352f17c")
    version("1.4.1", sha256="9429e143bb8dd33d34bf0663f571d4d4a1103e1afd7c49791b367b7ae1ef7f35")
    version("1.4", sha256="4149d5f05d8f7224a4d207362fdfe72420989dc1b028b28b7b62b6c2efe22345")

    depends_on("gettext")

    def configure_args(self):
        return ["LIBS=-lintl"]

    @run_before("build")
    def change_makefile(self):
        # Add 'cpp' path for rpcgen
        filter_file(
            "rpcgen/rpcgen",
            "rpcgen/rpcgen -Y {0}/lib/spack/env".format(spack.paths.spack_root),
            "rpcsvc/Makefile",
        )
