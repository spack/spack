# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyOwlrl(PythonPackage):
    """A simple implementation of the OWL2 RL Profile, as well as a basic
    RDFS inference, on top of RDFLib. Based mechanical forward chaining.
    """

    homepage = "https://github.com/RDFLib/OWL-RL"
    pypi = "owlrl/owlrl-5.2.3.tar.gz"

    version(
        "6.0.2",
        sha256="57eca06b221edbbc682376c8d42e2ddffc99f61e82c0da02e26735592f08bacc",
        url="https://pypi.org/packages/9d/56/11fe63c2c317347f69be17e9ece1991e0ec6c2cdb8225c0baa5b96e283ed/owlrl-6.0.2-py3-none-any.whl",
    )
    version(
        "5.2.3",
        sha256="0514239bfbf72fa67f3e5813a40bcc5bd88fd16093d9f76b45a0d4c84ee1c5e2",
        url="https://pypi.org/packages/d5/5b/c4d44d3b598036536e73fa5d2502e8e127ec617625c31b27db21b541836c/owlrl-5.2.3-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-rdflib@6.0.2:", when="@6:")
        depends_on("py-rdflib@5.0.0:", when="@5.2.2:5")
