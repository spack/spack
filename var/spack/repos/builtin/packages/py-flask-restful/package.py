# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFlaskRestful(PythonPackage):
    """Simple framework for creating REST APIs"""

    homepage = "https://www.github.com/flask-restful/flask-restful/"
    pypi = "Flask-RESTful/Flask-RESTful-0.3.8.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.3.9",
        sha256="4970c49b6488e46c520b325f54833374dc2b98e211f1b272bd4b0c516232afe2",
        url="https://pypi.org/packages/a9/02/7e21a73564fe0d9d1a3a4ff478dfc407815c4e2fa4e5121bcfc646ba5d15/Flask_RESTful-0.3.9-py2.py3-none-any.whl",
    )
