# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack import *


class PyClangFormat(Package):
    """This project packages the clang-format utility as a Python package.
    It allows you to install clang-format directly from PyPI:"""

    if sys.platform == "darwin":
        version(
            "13.0.1",
            sha256="826d487b1cf0190e0c3a5e064b56e2f6e7c4c799c78e59ff6d8991df916f2222",
            expand=False,
            url="https://files.pythonhosted.org/packages/14/8e/93bb3094512d6bb515c28156373ac6cb786e0cc08ff6492aca0fc7d592d8/clang_format-13.0.1-py2.py3-none-macosx_10_9_universal2.whl",
        )
    elif sys.platform.startswith("linux"):
        version(
            "13.0.1",
            sha256="58e91debc2b2d14d174c73c678ffac676cb171152ee3f4239b6cbe6975e4ede1",
            expand=False,
            url="https://files.pythonhosted.org/packages/17/fd/723876a1e55397e4b060f2e9e3d4a5e4820f6e09ea05fe8c8cf4ddfd1ae8/clang_format-13.0.1-py2.py3-none-manylinux_2_12_x86_64.manylinux2010_x86_64.whl",
        )

    extends("python")
    depends_on("py-pip", type="build")

    def install(self, spec, prefix):
        pip = which("pip")
        pip("install", "--ignore-installed", "--no-deps",
            self.stage.archive_file, "--prefix={0}".format(prefix))
