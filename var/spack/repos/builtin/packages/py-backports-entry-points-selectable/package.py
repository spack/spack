# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBackportsEntryPointsSelectable(PythonPackage):
    """Compatibility shim providing selectable entry points for older implementations"""

    homepage = "https://github.com/jaraco/backports.entry_points_selectable"
    pypi = "backports.entry_points_selectable/backports.entry_points_selectable-1.1.0.tar.gz"

    license("MIT")

    version(
        "1.1.1",
        sha256="7fceed9532a7aa2bd888654a7314f864a3c16a4e710b34a58cfc0f08114c663b",
        url="https://pypi.org/packages/6d/2e/a6789183415658c7f2c41da8599d53077bd222233039f5c92bffbf23b28d/backports.entry_points_selectable-1.1.1-py2.py3-none-any.whl",
    )
    version(
        "1.1.0",
        sha256="a6d9a871cde5e15b4c4a53e3d43ba890cc6861ec1332c9c2428c92f977192acc",
        url="https://pypi.org/packages/0c/cd/1e156227cad9f599524eb10af62a2362f872910a49402dbd2bea2dedc91c/backports.entry_points_selectable-1.1.0-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-importlib-metadata", when="^python@:3.7")
