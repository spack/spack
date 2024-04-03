# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyElasticTransport(PythonPackage):
    """Transport classes and utilities shared among Python Elastic client libraries"""

    homepage = "https://github.com/elastic/elastic-transport-python"
    pypi = "elastic-transport/elastic-transport-8.4.0.tar.gz"

    version(
        "8.4.0",
        sha256="19db271ab79c9f70f8c43f8f5b5111408781a6176b54ab2e54d713b6d9ceb815",
        url="https://pypi.org/packages/bd/3b/a2f4a4f1f7578ceaff490961753a75984efc17c17b1f6f59c3a866debeca/elastic_transport-8.4.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-certifi")
        depends_on("py-dataclasses", when="@:8.12 ^python@:3.6")
        depends_on("py-urllib3@1.26.2:1", when="@:8.4")
