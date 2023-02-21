# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCleo(PythonPackage):
    """Cleo allows you to create beautiful and testable command-line interfaces."""

    homepage = "https://github.com/sdispater/cleo"
    pypi = "cleo/cleo-0.8.1.tar.gz"

    version("1.0.0a5", sha256="097c9d0e0332fd53cc89fc11eb0a6ba0309e6a3933c08f7b38558555486925d3")
    version(
        "0.8.1",
        sha256="3d0e22d30117851b45970b6c14aca4ab0b18b1b53c8af57bed13208147e4069f",
        preferred=True,
    )

    depends_on("python@2.7,3.4:3", type=("build", "run"))
    depends_on("python@3.7:3", when="@1:", type=("build", "run"))
    depends_on("py-poetry-core@1:", type="build")
    depends_on("py-poetry-core@1", when="@1:", type="build")
    depends_on("py-clikit@0.6.0:0.6", when="@0.8.1", type=("build", "run"))
    depends_on("py-pylev@1.3:1", when="@1:", type=("build", "run"))
    depends_on("py-crashtest@0.3.1:0.3", when="@1:", type=("build", "run"))
