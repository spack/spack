# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTypesPythonDateutil(PythonPackage):
    """Typing stubs for python-dateutil."""

    homepage = "https://github.com/python/typeshed"
    pypi = "types-python-dateutil/types-python-dateutil-2.8.19.tar.gz"

    version(
        "2.8.19.14",
        sha256="f977b8de27787639986b4e28963263fd0e5158942b3ecef91b9335c130cb1ce9",
        url="https://pypi.org/packages/1c/af/5af2e2a02bc464c1c7818c260606343020b96c0d5b64f637d9e91aee24fe/types_python_dateutil-2.8.19.14-py3-none-any.whl",
    )
    version(
        "2.8.19",
        sha256="6284df1e4783d8fc6e587f0317a81333856b872a6669a282f8a325342bce7fa8",
        url="https://pypi.org/packages/e9/02/232ffb54d392a41b538eb060ce0a92817366c475f6f49af2d76b89812fac/types_python_dateutil-2.8.19-py3-none-any.whl",
    )
