# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDebtcollector(PythonPackage):
    """
    A collection of Python deprecation patterns and strategies that help you
    collect your technical debt in a non-destructive manner.
    """

    homepage = "https://docs.openstack.org/debtcollector/latest"
    pypi = "debtcollector/debtcollector-2.2.0.tar.gz"

    maintainers("haampie")

    version(
        "2.2.0",
        sha256="34663e5de257c67bf38827cfbea259c4d4ad27eba6b5a9d9242cb54076bfb4ad",
        url="https://pypi.org/packages/8e/50/07a7ccf4dbbe90b58e96f97b747ff98aef9d8c841d2616c48cc05b07db33/debtcollector-2.2.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-pbr@2:2.0,3:", when="@:2.4")
        depends_on("py-six@1.10:", when="@1.19:2.3")
        depends_on("py-wrapt@1.7:")
