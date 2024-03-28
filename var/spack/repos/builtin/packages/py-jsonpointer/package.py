# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJsonpointer(PythonPackage):
    """Library to resolve JSON Pointers according to RFC 6901"""

    homepage = "https://github.com/stefankoegl/python-json-pointer"
    pypi = "jsonpointer/jsonpointer-2.0.tar.gz"

    license("BSD-3-Clause")

    version(
        "2.0",
        sha256="ff379fa021d1b81ab539f5ec467c7745beb1a5671463f9dcc2b2d458bd361c1e",
        url="https://pypi.org/packages/18/b0/a80d29577c08eea401659254dfaed87f1af45272899e1812d7e01b679bc5/jsonpointer-2.0-py2.py3-none-any.whl",
    )
    version(
        "1.9",
        sha256="7c8e37f3fad01a3d5990e538114c4574aeaa617ac1994bbe8c44d330f5a206c4",
        url="https://pypi.org/packages/e9/79/683a3318610ad3d950d3fadd25c0b76923b749d0ba828a9466150ac641ac/jsonpointer-1.9-py2-none-any.whl",
    )
