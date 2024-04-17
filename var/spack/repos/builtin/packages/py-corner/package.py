# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCorner(PythonPackage):
    """Make some beautiful corner plots."""

    homepage = "https://corner.readthedocs.io"
    pypi = "corner/corner-2.2.2.tar.gz"

    maintainers("LydDeb")

    license("BSD-2-Clause")

    version(
        "2.2.2",
        sha256="e7577cdb59cfa304effa243b0c7ac0e3777030d3dc2f2e217a387e87a47074bb",
        url="https://pypi.org/packages/e8/c0/dca9f4801daa879f3bd483299e4f3829fc73a405641ebd12888d21cf98ec/corner-2.2.2-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.9:", when="@2.2.2-rc3:")
        depends_on("py-matplotlib@2.1.0:", when="@2.1,2.2.1:")
