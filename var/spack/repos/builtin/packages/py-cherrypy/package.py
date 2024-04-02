# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCherrypy(PythonPackage):
    """CherryPy is a pythonic, object-oriented HTTP framework."""

    homepage = "https://cherrypy.readthedocs.io/en/latest/"
    pypi = "CherryPy/CherryPy-18.1.1.tar.gz"

    license("BSD-3-Clause")

    version(
        "18.1.1",
        sha256="3c7b27fd1af4964434d821cd139b8d05c8f7fe4f37ae146fddb3f861d80a1da7",
        url="https://pypi.org/packages/aa/0e/4e353c47789ccb50130a44e765dae55b3e85abca01ff21930533ab36afc9/CherryPy-18.1.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-cheroot@6.2.4:", when="@:18.3")
        depends_on("py-more-itertools", when="@17.2:")
        depends_on("py-portend@2.1.1:")
        depends_on("py-pywin32", when="@:18.6.0 platform=windows")
        depends_on("py-zc-lockfile", when="@17.3:")
