# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJson5(PythonPackage):
    """The JSON5 Data Interchange Format (JSON5) is a superset of JSON that aims
    to alleviate some of the limitations of JSON by expanding its syntax to
    include some productions from ECMAScript 5.1."""

    homepage = "https://github.com/dpranke/pyjson5"
    pypi = "json5/json5-0.9.4.tar.gz"

    license("Apache-2.0")

    version(
        "0.9.14",
        sha256="740c7f1b9e584a468dbb2939d8d458db3427f2c93ae2139d05f47e453eae964f",
        url="https://pypi.org/packages/70/ba/fa37123a86ae8287d6678535a944f9c3377d8165e536310ed6f6cb0f0c0e/json5-0.9.14-py2.py3-none-any.whl",
    )
    version(
        "0.9.10",
        sha256="993189671e7412e9cdd8be8dc61cf402e8e579b35f1d1bb20ae6b09baa78bbce",
        url="https://pypi.org/packages/75/8c/c6f242154ee057e8f5b9491ee2a095646e489fcbad18dd73b99ed88cc5b2/json5-0.9.10-py2.py3-none-any.whl",
    )
    version(
        "0.9.6",
        sha256="823e510eb355949bed817e1f3e2d682455dc6af9daf6066d5698d6a2ca4481c2",
        url="https://pypi.org/packages/7e/8e/ebde0a31c71e7098b3014faf46c80bdbcadb3c23b0ac7c7646b2af7d302e/json5-0.9.6-py2.py3-none-any.whl",
    )
    version(
        "0.9.4",
        sha256="4e0fc461b5508196a3ddb3b981dc677805923b86d6eb603c7f58f2459ab1458f",
        url="https://pypi.org/packages/e4/4b/c0b4c7e238a98165a0281d6ad52ee4a8401318580d2fc9d3844dda2ef5f7/json5-0.9.4-py2.py3-none-any.whl",
    )
