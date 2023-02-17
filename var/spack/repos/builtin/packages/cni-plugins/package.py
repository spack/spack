# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class CniPlugins(Package):
    """Standard networking plugins for container networking"""

    homepage = "https://github.com/containernetworking/plugins"
    url = "https://github.com/containernetworking/plugins/archive/v1.0.1.tar.gz"
    maintainers("bernhardkaindl")

    version("1.1.1", sha256="c86c44877c47f69cd23611e22029ab26b613f620195b76b3ec20f589367a7962")
    version("1.0.1", sha256="2ba3cd9f341a7190885b60d363f6f23c6d20d975a7a0ab579dd516f8c6117619")

    depends_on("go", type="build")

    def install(self, spec, prefix):
        utils = "github.com/containernetworking/plugins/pkg/utils/buildversion"
        which("./build_linux.sh")(
            "-ldflags", "-extldflags -static -X {0}.BuildVersion={1}".format(utils, self.version)
        )
        install_tree("bin", prefix.bin)
