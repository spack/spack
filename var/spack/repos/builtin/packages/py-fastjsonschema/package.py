# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyFastjsonschema(PythonPackage):
    """Fast JSON schema validator for Python."""

    homepage = "https://github.com/horejsek/python-fastjsonschema"
    pypi = "fastjsonschema/fastjsonschema-2.15.1.tar.gz"

    license("BSD-3-Clause")

    version(
        "2.16.3",
        sha256="04fbecc94300436f628517b05741b7ea009506ce8f946d40996567c669318490",
        url="https://pypi.org/packages/eb/e7/84b1571b866b8abd604f8b72234d16f01bd5944014ef9929b5cb0da198c1/fastjsonschema-2.16.3-py3-none-any.whl",
    )
    version(
        "2.16.2",
        sha256="21f918e8d9a1a4ba9c22e09574ba72267a6762d47822db9add95f6454e51cc1c",
        url="https://pypi.org/packages/e4/be/cf1b876348070a23cb0c3ebfee7a452ad3a91b07b456dade3bd514656009/fastjsonschema-2.16.2-py3-none-any.whl",
    )
    version(
        "2.15.1",
        sha256="fa2f4bb1e31419c5eb1150f2e0545921712c10c34165b86d33f08f5562ad4b85",
        url="https://pypi.org/packages/d1/fb/ea090e917b18320f79be31d754bbe496b715175e865603cfce1eaed2e774/fastjsonschema-2.15.1-py3-none-any.whl",
    )
