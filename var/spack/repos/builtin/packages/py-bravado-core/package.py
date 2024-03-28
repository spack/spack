# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBravadoCore(PythonPackage):
    """
    bravado-core is a Python library that adds client-side and server-side
    support for the OpenAPI Specification v2.0.
    """

    homepage = "https://github.com/Yelp/bravado-core"
    pypi = "bravado-core/bravado-core-5.17.1.tar.gz"

    version(
        "5.17.1",
        sha256="e231567cdc471337d23dfc950c45c5914ade8a78cde7ccf2ebb9433fcda29f40",
        url="https://pypi.org/packages/31/2e/38770d846b798a8ad84e32dab5bdd1ba6eaccbe4a3069f92660e5c86e8ed/bravado_core-5.17.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-jsonref", when="@1:1.0,1.1.0:2.0,2.2:2.3,2.4.1:3,4.11.3:6.1.0")
        depends_on("py-jsonschema@2.5.1:+format", when="@4.11.3:6.1.0")
        depends_on("py-msgpack@0.5.2:", when="@5.16.1:6.1.0")
        depends_on("py-python-dateutil", when="@1:1.0,1.1.0:2.0,2.2:2.3,2.4.1:4.2.2,4.11.3:6.1.0")
        depends_on("py-pytz", when="@4.11.3:6.1.0")
        depends_on("py-pyyaml", when="@4.1:4.2.2,4.11.3:6.1.0")
        depends_on("py-requests", when="@5.17.1:6.1.0")
        depends_on("py-simplejson", when="@1:1.0,1.1.0:2.0,2.2:2.3,2.4.1:4.2.2,4.11.3:6.1.0")
        depends_on("py-six", when="@1.1.0:2.0,2.2:2.3,2.4.1:4.2.2,4.11.3:6.1.0")
        depends_on("py-swagger-spec-validator@2.0.1:", when="@4:4.2.2,4.11.3:6.1.0")
