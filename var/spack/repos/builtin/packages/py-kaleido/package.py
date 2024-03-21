# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

from spack.package import *

arch, os = platform.machine(), platform.system()

class PyKaleido(PythonPackage):
    """Static image export for web-based visualization libraries with zero dependencies"""

    homepage = "https://github.com/plotly/Kaleido"
    pypi = "kaleido/kaleido-0.2.1-py2.py3-none-manylinux1_x86_64.whl"
    
    if (arch == "x86_64" or arch == "x64") and os == "Linux": # 64-bit x86 Linux
        version(
            "0.2.1-linux-x86_64",
            sha256="aa21cf1bf1c78f8fa50a9f7d45e1003c387bd3d6fe0a767cfbbf344b95bdc3a8",
            url="https://files.pythonhosted.org/packages/ae/b3/a0f0f4faac229b0011d8c4a7ee6da7c2dca0b6fd08039c95920846f23ca4/kaleido-0.2.1-py2.py3-none-manylinux1_x86_64.whl",
            expand=False
        )

    # TODO: 32-bit systems, MacOS, Windows, and ARM

    depends_on("python@:3.4")
