# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPsmon(PythonPackage):
    """Monitors and limits process resource."""

    homepage = "https://github.com/rkkautsar/psmon"
    pypi = "psmon/psmon-1.1.1.tar.gz"

    maintainers("valmar")

    license("MIT")

    version(
        "1.1.1",
        sha256="c8427569fa3e65ac23802e3746b811142a5811d3a99311350be63d9ae2be53b2",
        url="https://pypi.org/packages/d6/2f/ef2a0518327e91de5a45ce5809783d40f790a96f33d0d3d207fe47a00626/psmon-1.1.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-loguru@0.2.5:0.2", when="@0.2:")
        depends_on("py-psutil@5.5:")
