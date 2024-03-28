# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyepsg(PythonPackage):
    """Provides simple access to https://epsg.io/."""

    homepage = "https://pyepsg.readthedocs.io/en/latest/"
    pypi = "pyepsg/pyepsg-0.3.2.tar.gz"

    license("LGPL-3.0-or-later")

    version(
        "0.4.0",
        sha256="ecb29d351f66221d951989f7443f747be0b078162e71384c96612764e18265eb",
        url="https://pypi.org/packages/ea/19/3f735df5ce32162c761bdb1b984319061294b2f140336dec6053dd3e913e/pyepsg-0.4.0-py3-none-any.whl",
    )
    version(
        "0.3.2",
        sha256="a7f91263ed171586b6c502d22474af3870a87487f327324e93ae2e0ac6e63775",
        url="https://pypi.org/packages/1f/85/d0206d40f74d56c9328d646d04071d429df087bb1f7d1ee0c39accc1e0af/pyepsg-0.3.2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-requests", when="@0.4:")
