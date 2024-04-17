# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCiInfo(PythonPackage):
    """Continuous Integration Information.

    A Python implementation of watson/ci-info. Get details about the current
    Continuous Integration environment.
    """

    homepage = "https://github.com/mgxd/ci-info"
    pypi = "ci-info/ci-info-0.2.0.tar.gz"

    license("MIT")

    version(
        "0.3.0",
        sha256="e9e05d262a6c48aa03cd904475de5ce8c4da8a5435e516631c795d0487dc9e07",
        url="https://pypi.org/packages/13/c3/8ac768b389d5b6dda1c3ce7992b3acd2b46401f9b71439123858b17b1a2c/ci_info-0.3.0-py3-none-any.whl",
    )
    version(
        "0.2.0",
        sha256="c59143d3aef96efcf46e6ec924275b3967eb9f6e922b1fbcb59bacc6bb77fc5c",
        url="https://pypi.org/packages/cf/01/664a10490000d7154fa71358af87681696b8116a12d869a267063c470fbc/ci_info-0.2.0-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@0.3:")
