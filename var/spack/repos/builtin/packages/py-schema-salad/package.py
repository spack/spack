# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySchemaSalad(PythonPackage):
    """Schema Annotations for Linked Avro Data (SALAD)"""

    homepage = "https://github.com/common-workflow-language/schema_salad"
    pypi = "schema-salad/schema-salad-8.3.20221209165047.tar.gz"

    version(
        "8.3.20221209165047",
        sha256="d97cc9a4d7c4255eb8000bcebaa8ac0d1d31801c921fd4113ab3051c1e326c7c",
    )

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-requests@1:", type=("build", "run"))
    depends_on("py-ruamel-yaml@0.17.6:0.17.21", when="^python@3.7:", type=("build", "run"))
    depends_on("py-ruamel-yaml@0.16.12:0.17.21", type=("build", "run"))
    depends_on("py-rdflib@4.2.2:6.999999", type=("build", "run"))
    depends_on("py-rdflib@4.2.2:5.999999", when="^python@:3.6", type=("build", "run"))
    depends_on("py-rdflib-jsonld@0.4.0:0.6.0", when="^python@:3.6", type=("build", "run"))
    depends_on("py-mistune@2.0.3:2.0", type=("build", "run"))
    depends_on("py-cachecontrol@0.11.7:0.12+filecache", type=("build", "run"))

    depends_on("py-black@19.10b0:22.12", type=("build", "run"))

    depends_on("py-mypy@0.991", type=("build", "run"))
    depends_on("py-types-pkg-resources", type=("build", "run"))
    depends_on("py-types-requests", type=("build", "run"))
    depends_on("py-types-dataclasses", type=("build", "run"))
