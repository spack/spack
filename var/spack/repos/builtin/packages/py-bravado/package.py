# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBravado(PythonPackage):
    """
    Bravado is a Yelp maintained fork of digium/swagger-py for use with
    OpenAPI Specification version 2.0 (previously known as Swagger).
    """

    homepage = "https://github.com/Yelp/bravado"
    pypi = "bravado/bravado-11.0.3.tar.gz"

    version(
        "11.0.3",
        sha256="8ac8bbb645e49607917a5c07808116c708521f51e80d9c29bc4a168ff4dd22c6",
        url="https://pypi.org/packages/21/ed/03b0c36b5bcafbe2938ed222f9a164a6c0367ce99a9d2d502e462853571d/bravado-11.0.3-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-bravado-core@5.16.1:", when="@10.5:")
        depends_on("py-monotonic")
        depends_on("py-msgpack", when="@10.6.3:")
        depends_on("py-python-dateutil")
        depends_on("py-pyyaml")
        depends_on("py-requests@2.17:", when="@10.5:")
        depends_on("py-simplejson")
        depends_on("py-six")
        depends_on("py-typing-extensions")
