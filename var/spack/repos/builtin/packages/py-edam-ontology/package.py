# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyEdamOntology(PythonPackage):
    """Versioned, Python packaged EDAM ontology (http://edamontology.org/) data."""

    homepage = "https://github.com/edamontology/edam-ontology.py"
    pypi = "edam-ontology/edam-ontology-1.25.2.tar.gz"

    license("MIT")

    version(
        "1.25.2",
        sha256="7258e0ae1aed6976ab5b292e3f665fb5105efcd654313890840c7554f226d140",
        url="https://pypi.org/packages/72/11/2ce89a7d5f018bce4c8aa26f815f0001774f9594afa17396aced9de52b0a/edam_ontology-1.25.2-py2.py3-none-any.whl",
    )
