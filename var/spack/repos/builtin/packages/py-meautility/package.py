# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMeautility(PythonPackage):
    """Python package for multi-electrode array (MEA) handling and stimulation."""

    homepage = "https://github.com/alejoe91/MEAutility"
    pypi = "meautility/MEAutility-1.5.1.tar.gz"

    license("GPL-3.0-or-later")

    version(
        "1.5.1",
        sha256="93d0ed4fcd9f65fb10376b53c846ac0942332e06c6144e12e5c7a5b1f31accf6",
        url="https://pypi.org/packages/c6/20/de3443888225574e1e42675e8d740f6cecc5873a6da7640b2c798e22fc81/MEAutility-1.5.1-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-matplotlib", when="@1.5:")
        depends_on("py-numpy", when="@1.5:")
        depends_on("py-pyyaml", when="@1.5:")
