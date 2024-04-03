# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJsonargparse(PythonPackage):
    """An extension to python's argparse which simplifies parsing of configuration options from
    command line arguments, json configuration files (yaml or jsonnet supersets), environment
    variables and hard-coded defaults.
    """

    homepage = "https://github.com/omni-us/jsonargparse"
    pypi = "jsonargparse/jsonargparse-4.19.0.tar.gz"

    license("MIT")

    version(
        "4.27.5",
        sha256="95d1ff000efa759c171fca816685c1d1a66daab056fe30a73062a0fc4a734a05",
        url="https://pypi.org/packages/1a/dc/eb2ffcfbd529c3e6e9fe28d55b8663d2450370e6553f4f51cc89628efa2f/jsonargparse-4.27.5-py3-none-any.whl",
    )
    version(
        "4.25.0",
        sha256="90719b4070de26a2677d23f374c1cf52f6b9dbfd479e7ee5b96f47da893ee5b5",
        url="https://pypi.org/packages/46/1a/1687c20b1c7aa9df40120b8faff067fce77bfdac215f9efbe3f39b7a6227/jsonargparse-4.25.0-py3-none-any.whl",
    )
    version(
        "4.19.0",
        sha256="f4377718317c6f7b42d437ea08a1833e6afda4ecf8a2d0704d21dff1f21017af",
        url="https://pypi.org/packages/88/32/a68ac6cc18194fa88a56b1e7920e1a96deee14e759a906d902275a86c301/jsonargparse-4.19.0-py3-none-any.whl",
    )

    variant("signatures", default=False, description="Enable signature features")
    variant("typing-extensions", default=False, description="typing-extensions")

    with default_args(type="run"):
        depends_on("python@3.7:", when="@4.25:")
        depends_on("py-docstring-parser@0.15:", when="@4.14:+signatures")
        depends_on("py-pyyaml@3.13:")
        depends_on("py-typeshed-client@2.1:", when="@4.19:+signatures")
        depends_on("py-typing-extensions@3.10:", when="@4.21:+typing-extensions ^python@:3.9")
