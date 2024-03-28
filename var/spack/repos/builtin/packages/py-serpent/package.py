# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

# Package automatically generated using 'pip2spack' converter


class PySerpent(PythonPackage):
    """
    Serialization based on ast.literal_eval
    """

    homepage = "https://github.com/irmen/Serpent"
    pypi = "serpent/serpent-1.40.tar.gz"
    maintainers("liuyangzhuan")

    license("MIT")

    version(
        "1.40",
        sha256="14d531cedeed593e793bae4e14eb1463445e8b161cb24ddf795800a50973d3d3",
        url="https://pypi.org/packages/48/fa/b8208cd568abdc3b99ac4d6a27a5a4d897d7304d93f0ffde32ba91f85d7c/serpent-1.40-py3-none-any.whl",
    )
