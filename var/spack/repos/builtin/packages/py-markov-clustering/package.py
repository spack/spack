# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMarkovClustering(PythonPackage):
    """Implementation of the Markov clustering (MCL) algorithm in python"""

    homepage = "https://github.com/GuyAllard/markov_clustering"
    pypi = "markov_clustering/markov_clustering-0.0.6.dev0.tar.gz"

    license("MIT", checked_by="A-N-Other")

    version(
        "0.0.6.dev0",
        sha256="75a1fd0c05552e3bf0804ec4879346a7691b4453d43e48079079378bee21887c",
        url="https://pypi.org/packages/76/42/19e11a42fa952d35116b90577e2cde31c541ce78364a52167f852864ba29/markov_clustering-0.0.6.dev0-py3-none-any.whl",
    )

    variant("drawing", default=False, description="Include graphing capabilities")

    with default_args(type="run"):
        depends_on("python@:3")
        depends_on("py-matplotlib", when="@:0.0.3,0.0.6:+drawing")
        depends_on("py-networkx", when="@:0.0.3,0.0.6:+drawing")
        depends_on("py-numpy", when="@:0.0.3,0.0.6:")
        depends_on("py-scikit-learn", when="@:0.0.3,0.0.6:")
        depends_on("py-scipy@0.19:", when="@0.0.6:")
