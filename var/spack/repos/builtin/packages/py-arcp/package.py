# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyArcp(PythonPackage):
    """arcp (Archive and Package) URI parser and generator"""

    homepage = "https://arcp.readthedocs.io"
    pypi = "arcp/arcp-0.2.1.tar.gz"

    license("Apache-2.0")

    version(
        "0.2.1",
        sha256="4e09b2d8a9fc3fda7ec112b553498ff032ea7de354e27dbeb1acc53667122444",
        url="https://pypi.org/packages/66/df/32574bc8f1d440d40f4aaf3b455316b2b1536c7243c985a90f8516cf3074/arcp-0.2.1-py2.py3-none-any.whl",
    )
