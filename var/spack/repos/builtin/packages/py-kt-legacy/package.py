# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyKtLegacy(PythonPackage):
    """This repository is to support the deprecated import name of Keras Tuner.
    With this repo, you can import Keras Tuner as kerastuner. In the main Keras
    Tuner repository the import name has been changed to keras_tuner."""

    homepage = "https://github.com/haifeng-jin/kt-legacy"
    pypi = "kt-legacy/kt-legacy-1.0.4.tar.gz"

    license("Apache-2.0")

    version(
        "1.0.4",
        sha256="8b6eaff78b01b3cf1d71390cbcc6498208433e2ae0ce4d3c6e072f980b9fc625",
        url="https://pypi.org/packages/09/83/7c3001c7826cd7194f36dc971c57a25c7a55373e7087c62a6d1d1193c022/kt_legacy-1.0.4-py3-none-any.whl",
    )
