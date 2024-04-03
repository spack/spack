# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGravity(PythonPackage):
    """Command-line utilities to assist in managing Galaxy servers"""

    homepage = "https://github.com/galaxyproject/gravity"
    pypi = "gravity/gravity-0.13.6.tar.gz"

    license("MIT")

    version(
        "0.13.6",
        sha256="887a59546cbd69b698bec95eb2239f2e6b99ac2faef432f4dd95cd3842c92b3e",
        url="https://pypi.org/packages/48/87/4a45eb0a1b608aee8de1d708b8ec36a8614ee896435c1de2469d5ebc7f53/gravity-0.13.6-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-click")
        depends_on("py-jsonref", when="@0.11:")
        depends_on("py-pydantic", when="@0.11:1.0.3")
        depends_on("py-pyyaml")
        depends_on("py-ruamel-yaml", when="@:0")
        depends_on("py-supervisor")
