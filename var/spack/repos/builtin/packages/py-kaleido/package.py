# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyKaleido(PythonPackage):
    """Static image export for web-based visualization libraries with zero dependencies"""

    homepage = "https://github.com/wdecoster/nanostat"
    url = "https://github.com/plotly/Kaleido/archive/refs/tags/v0.2.1.tar.gz"

    maintainers("Pandapip1")

    version("0.2.1", sha256="fdb673a9759835d4f455990fc1ff8919bd100a0d34f2d3de7bd5eeb2162b57ec")

    depends_on("py-setuptools", type="build")

    build_directory = join_path("repos", "kaleido", "py")
