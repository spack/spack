# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySwaggerSpecValidator(PythonPackage):
    """
    A Python library that validates Swagger Specs against
    the Swagger 1.2 or Swagger 2.0 specification.
    """

    homepage = "https://github.com/Yelp/swagger_spec_validator"
    pypi = "swagger-spec-validator/swagger-spec-validator-2.7.6.tar.gz"

    version(
        "2.7.6",
        sha256="ff55d671f4cf8a386e7ecda60267d6cdd2cfbe0b3521a8ccf09b0669cbb72ab6",
        url="https://pypi.org/packages/5b/0f/d7f6a7f610487a25583db19d2ce2808ad8be356e0067b4f2758d076af8a5/swagger_spec_validator-2.7.6-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-jsonschema", when="@:2.7.4,2.7.6:")
        depends_on("py-pyyaml")
        depends_on("py-six", when="@:2")
