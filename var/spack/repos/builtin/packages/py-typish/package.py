# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTypish(PythonPackage):
    """Python library for type checking"""

    homepage = "https://github.com/ramonhagenaars/typish"
    url = "https://github.com/ramonhagenaars/typish/archive/v1.9.2.tar.gz"

    license("MIT")

    version(
        "1.9.3",
        sha256="03cfee5e6eb856dbf90244e18f4e4c41044c8790d5779f4e775f63f982e2f896",
        url="https://pypi.org/packages/9d/d6/3f56c9c0c12adf61dfcf4ed5c8ffd2c431db8dd85592067a57e8e1968565/typish-1.9.3-py3-none-any.whl",
    )
    version(
        "1.9.2",
        sha256="36f940e39d0f4d2bd4c524d167936024308bc52ef22ec718ce5c4e38a3ba5a95",
        url="https://pypi.org/packages/24/a7/83e450157d1613be0725821f8bd8aadab22217fa5dac4795dcfb9408be95/typish-1.9.2-py3-none-any.whl",
    )
