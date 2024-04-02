# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBackportsAbc(PythonPackage):
    """Backports_ABC: A backport of recent additions to the 'collections.abc'
    module."""

    homepage = "https://github.com/cython/backports_abc"
    url = "https://github.com/cython/backports_abc/archive/0.4.tar.gz"

    license("PSF-2.0")

    version(
        "0.5",
        sha256="52089f97fe7a9aa0d3277b220c1d730a85aefd64e1b2664696fe35317c5470a7",
        url="https://pypi.org/packages/7d/56/6f3ac1b816d0cd8994e83d0c4e55bc64567532f7dc543378bd87f81cebc7/backports_abc-0.5-py2.py3-none-any.whl",
    )
    version(
        "0.4",
        sha256="c64508e766dfe09a94a442c12b57c6e098a402921ecb340a4ec57c7e10fd464c",
        url="https://pypi.org/packages/f5/5e/57e1afdc63d8c37496b2f6d9cb0ddfc4a3d55c949074debeab7594c19b54/backports_abc-0.4-py2.py3-none-any.whl",
    )
