# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNodeSemver(PythonPackage):
    """python version of node-semver (https://github.com/isaacs/node-semver)"""

    homepage = "https://github.com/podhmo/python-semver"
    pypi = "node-semver/node-semver-0.8.1.tar.gz"

    license("MIT")

    version(
        "0.8.1",
        sha256="3b3594c2d87e1a44fd332ce7f00e87a235a0a4fb9cb46d62b243e43c019c27fd",
        url="https://pypi.org/packages/bc/9d/299d024bbf3d73f158aa836c955c29574b351cfcfd92dfbc9f97c2762e46/node_semver-0.8.1-py3-none-any.whl",
    )
    version(
        "0.6.1",
        sha256="d4bf83873894591a0cbb6591910d96917fbadc9731e8e39e782d3a2fbc2b841e",
        url="https://pypi.org/packages/08/51/6cf3a2b18ca35cbe4ad3c7538a7c3dc0cb24e71629fb16e729c137d06432/node_semver-0.6.1-py3-none-any.whl",
    )
