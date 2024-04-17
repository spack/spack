# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFilecheck(PythonPackage):
    """Python port of LLVM's FileCheck, flexible pattern matching file verifier."""

    pypi = "filecheck/filecheck-0.0.23.tar.gz"

    license("Apache-2.0")

    version(
        "0.0.23",
        sha256="cc1dc3fc2fc682ccd059b0d535606d32235613a32c018211d93aa6a99047ceb2",
        url="https://pypi.org/packages/d8/6a/a864c347dcffa6ac6b97f3770b5f4642b26cb3acf04a5b5bc2b14a04149b/filecheck-0.0.23-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@:3", when="@:0.0.23")
