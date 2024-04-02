# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyArgparseDataclass(PythonPackage):
    """An immutable mapping type for Python."""

    homepage = "https://github.com/mivade/argparse_dataclass"
    pypi = "argparse_dataclass/argparse_dataclass-2.0.0.tar.gz"

    license("MIT")

    version(
        "2.0.0",
        sha256="3ffc8852a88d9d98d1364b4441a712491320afb91fb56049afd8a51d74bb52d2",
        url="https://pypi.org/packages/b3/66/e6c0a808950ba5a4042e2fcedd577fc7401536c7db063de4d7c36be06f84/argparse_dataclass-2.0.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@2:")
