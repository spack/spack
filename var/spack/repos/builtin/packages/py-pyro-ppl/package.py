# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyroPpl(PythonPackage):
    """A Python library for probabilistic modeling and inference."""

    homepage = "https://pyro.ai/"
    pypi = "pyro-ppl/pyro-ppl-1.8.1.tar.gz"

    maintainers("adamjstewart", "meyersbs")

    license("Apache-2.0")

    version(
        "1.8.4",
        sha256="294f78f28f2fe7bbea2792bd6bd8c69b7cfe493cf8940cac97a9b5d0e7f194cd",
        url="https://pypi.org/packages/b5/b1/ccceeae368b7e2b5504229e74ad584e4b8071faeef23b0e888d1c9d8ef3d/pyro_ppl-1.8.4-py3-none-any.whl",
    )
    version(
        "1.8.1",
        sha256="ca01ab4565eb9a1af4a60dbc481da5cb6f5fe5a72efa19e83638e03683efbca6",
        url="https://pypi.org/packages/68/01/507d1b150701800d90d45f3ba06c296a0e1eaa7f3caba4db15d7495ff6bb/pyro_ppl-1.8.1-py3-none-any.whl",
    )
    version(
        "1.8.0",
        sha256="69e234faf37b9752eef7f780cb6e2b2489e88abc34dfa4706eb92c8f6b811cf6",
        url="https://pypi.org/packages/aa/a0/c94b31968713f1bbb8978094cb65ef992ac09e6637f905d7062467bceba8/pyro_ppl-1.8.0-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@1.8.1:1.8")
        depends_on("py-numpy@1.7:")
        depends_on("py-opt-einsum@2.3.2:")
        depends_on("py-pyro-api@0.1.1:")
        depends_on("py-torch@1.11:", when="@1.8.1:1.8.4,1.8.6:1.8")
        depends_on("py-torch@1.9:", when="@1.7:1.8.0")
        depends_on("py-tqdm@4.36:")
