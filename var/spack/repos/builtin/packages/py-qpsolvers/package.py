# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyQpsolvers(PythonPackage):
    """Unified interface to convex Quadratic Programming (QP) solvers available in
    Python."""

    homepage = "https://github.com/qpsolvers/qpsolvers"
    pypi = "qpsolvers/qpsolvers-3.1.0.tar.gz"

    maintainers("meyersbs")

    license("LGPL-3.0-only")

    version(
        "3.2.0",
        sha256="ba1651a45ce23c49786bcf8327d83943092a124f84024da3dfdc44735c25aae9",
        url="https://pypi.org/packages/b6/c5/2afcb9c856385f7a1c8d804ff7a52f45bc44b20a5e936f01005213fe24fc/qpsolvers-3.2.0-py3-none-any.whl",
    )
    version(
        "3.1.0",
        sha256="2b17ca23eb87124aa6f3844fcdb3affbc55b78ac7f89dcb0d2e706df899783c1",
        url="https://pypi.org/packages/cd/d1/b877f55bc00f2ea99c3862ecb07c1c0ef5ccc7b0cbfb49636d3505911d88/qpsolvers-3.1.0-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:")
        depends_on("py-ecos@2.0.8:", when="@3:4.2")
        depends_on("py-numpy@1.15.4:", when="@2.6:")
        depends_on("py-osqp@0.6.2:", when="@3:4.2")
        depends_on("py-scipy@1.2.0:")
        depends_on("py-scs@3.2:", when="@3:4.2")
