# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySimpleeval(PythonPackage):
    """A quick single file library for easily adding evaluatable expressions into python
    projects."""

    homepage = "https://github.com/danthedeckie/simpleeval"
    pypi = "simpleeval/simpleeval-0.9.12.tar.gz"

    license("MIT")

    version(
        "0.9.12",
        sha256="d82faa7dc88379614ea3b385fd84cc24f0aa4853432e267718526e5aeac6b1b9",
        url="https://pypi.org/packages/7d/39/d5be0242308735b87bea7dc8fdadaca1056d4e73a3e7db6c5f0d20a90f7f/simpleeval-0.9.12-py2.py3-none-any.whl",
    )
