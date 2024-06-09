# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Litestream(GoPackage):
    """Streaming replication for SQLite."""

    homepage = "https://github.com/benbjohnson/litestream"
    url = "https://github.com/benbjohnson/litestream/archive/refs/tags/v0.3.13.tar.gz"

    license("Apache-2.0", checked_by="cmelone")

    version("0.3.13", sha256="92cb22323b8168f6efdfcad270772fea9e78c709a7149b1bf35d81fcb88bdaf9")


class GoBuilder(spack.build_systems.go.GoBuilder):
    @property
    def build_directory(self):
        return os.path.join(self.pkg.stage.source_path, "cmd", "litestream")
