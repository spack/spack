# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPipdeptree(PythonPackage):
    """Command line utility to show dependency tree of packages."""

    homepage = "https://github.com/tox-dev/pipdeptree"
    pypi = "pipdeptree/pipdeptree-2.13.0.tar.gz"

    license("MIT")

    version(
        "2.13.0",
        sha256="70c582224a41f20c4b69be7aaeeed40b59d3f247a93b4d6891b3d772c9befc94",
        url="https://pypi.org/packages/1a/16/dcf8dab5bde96006502d80c858676728364e307f23c3df210fc1f6f406ee/pipdeptree-2.13.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@2.10:")
