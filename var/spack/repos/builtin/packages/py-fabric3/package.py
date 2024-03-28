# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyFabric3(PythonPackage):
    """Fabric is a simple, Pythonic tool for
    remote execution and deployment (py2.7/py3.4+ compatible fork).
    """

    homepage = "https://github.com/mathiasertl/fabric/"
    pypi = "fabric3/Fabric3-1.14.post1.tar.gz"

    license("BSD-2-Clause")

    version(
        "1.14.post1",
        sha256="7c5a5f2eb3079eb6bd2a69931f1ca298844c730ce3fdc68111db16e8857a0408",
        url="https://pypi.org/packages/85/14/0b4f34e1f9a351bbe0f1ddea8b12f8103e77e9b5dc7b935c25c2260fc2e5/Fabric3-1.14.post1-py3-none-any.whl",
    )
