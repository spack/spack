# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyScp(PythonPackage):
    """scp module for paramiko"""

    homepage = "https://github.com/jbardin/scp.py"
    pypi = "scp/scp-0.13.2.tar.gz"

    license("LGPL-2.1-or-later")

    version(
        "0.13.2",
        sha256="26c0bbc7ea29c30ec096ae67b0afa7a6b7c557b2ce8f740109ee72a0d52af7d1",
        url="https://pypi.org/packages/4d/7a/3d76dc5ad8deea79642f50a572e1c057cb27e8b427f83781a2c05ce4e5b6/scp-0.13.2-py2.py3-none-any.whl",
    )
