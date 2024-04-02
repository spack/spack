# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAppnope(PythonPackage):
    """Disable App Nap on OS X 10.9"""

    homepage = "https://github.com/minrk/appnope"
    pypi = "appnope/appnope-0.1.0.tar.gz"

    version(
        "0.1.3",
        sha256="265a455292d0bd8a72453494fa24df5a11eb18373a60c7c0430889f22548605e",
        url="https://pypi.org/packages/41/4a/381783f26df413dde4c70c734163d88ca0550a1361cb74a1c68f47550619/appnope-0.1.3-py2.py3-none-any.whl",
    )
    version(
        "0.1.0",
        sha256="5b26757dc6f79a3b7dc9fab95359328d5747fcb2409d331ea66d0272b90ab2a0",
        url="https://pypi.org/packages/87/a9/7985e6a53402f294c8f0e8eff3151a83f1fb901fa92909bb3ff29b4d22af/appnope-0.1.0-py2.py3-none-any.whl",
    )
