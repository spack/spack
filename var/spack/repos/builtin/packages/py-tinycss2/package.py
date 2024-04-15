# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTinycss2(PythonPackage):
    """tinycss2 is a low-level CSS parser and generator written in Python: it can parse
    strings, return objects representing tokens and blocks, and generate CSS strings
    corresponding to these objects."""

    homepage = "https://www.courtbouillon.org/tinycss2"
    pypi = "tinycss2/tinycss2-1.1.1.tar.gz"
    git = "https://github.com/Kozea/tinycss2.git"

    license("BSD-3-Clause")

    version(
        "1.2.1",
        sha256="2b80a96d41e7c3914b8cda8bc7f705a4d9c49275616e886103dd839dfc847847",
        url="https://pypi.org/packages/da/99/fd23634d6962c2791fb8cb6ccae1f05dcbfc39bce36bba8b1c9a8d92eae8/tinycss2-1.2.1-py3-none-any.whl",
    )
    version(
        "1.1.1",
        sha256="fe794ceaadfe3cf3e686b22155d0da5780dd0e273471a51846d0a02bc204fec8",
        url="https://pypi.org/packages/53/7b/5dba39bf0572f1f28e2844f08f74a73482a381de1d1feac3bbc6b808051e/tinycss2-1.1.1-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@1.2:")
        depends_on("py-webencodings@0.4:", when="@1:")
