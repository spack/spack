# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAgateDbf(PythonPackage):
    """agate-dbf adds read support for dbf files to agate."""

    homepage = "https://agate-dbf.readthedocs.io/en/latest/"
    pypi = "agate-dbf/agate-dbf-0.2.1.tar.gz"

    license("MIT")

    version(
        "0.2.2",
        sha256="632a8826ecde3dffb28f15e3ccb9d523bc15b79eb157f063f2febc2c4078957a",
        url="https://pypi.org/packages/fc/75/32847937627c8fe2271606d71de85486ffaf01b28a091ecdc43e58876b1b/agate_dbf-0.2.2-py2.py3-none-any.whl",
    )
    version(
        "0.2.1",
        sha256="f618fadb413d41468c90d72fca945681d82d9e4d1b3d89f9bda52e607b828c0b",
        url="https://pypi.org/packages/3d/d0/5a161b906a7eaa2b3d5690bbf0de5ceb4398e21d3e915f69869cfeef906f/agate_dbf-0.2.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-agate@1.5:", when="@0.2.2:")
        depends_on("py-dbfread@2.0.5:", when="@0.2.2:")
