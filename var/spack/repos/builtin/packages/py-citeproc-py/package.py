# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCiteprocPy(PythonPackage):
    """Citations and bibliography formatter."""

    homepage = "https://github.com/brechtm/citeproc-py"
    pypi = "citeproc-py/citeproc-py-0.6.0.tar.gz"

    license("BSD-2-Clause-FreeBSD")

    version(
        "0.6.0",
        sha256="ca4c7a5158d6f68cb00a89bb47d9aa0eec7b89b18e574eb08a061b011b602bbe",
        url="https://pypi.org/packages/23/e8/5e42b253c40d1087a4ef341d78d88b7a9beb46e6ab9cec19c75e4e3cba78/citeproc_py-0.6.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-lxml", when="@0.5.1:")
