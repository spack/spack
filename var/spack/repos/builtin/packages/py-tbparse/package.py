# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTbparse(PythonPackage):
    """Load tensorboard event logs as pandas DataFrames."""

    homepage = "https://github.com/j3soon/tbparse"
    pypi = "tbparse/tbparse-0.0.7.tar.gz"

    license("Apache-2.0")

    version(
        "0.0.7",
        sha256="f9a140f45b8ff00158fd406aba0b3b56a46793d6ea65db346e8d80db0e4fb90d",
        url="https://pypi.org/packages/69/84/bda53f22def6091216123e7e8cc89a916bfdc31c03f26f71a7ab871af5f6/tbparse-0.0.7-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:")
        depends_on("py-pandas@1.3.0:")
        depends_on("py-tensorboard@2:", when="@0.0.7:")
