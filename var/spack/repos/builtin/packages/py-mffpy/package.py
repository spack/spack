# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMffpy(PythonPackage):
    """Reader and Writer for Philips' MFF file format."""

    homepage = "https://github.com/BEL-Public/mffpy"
    pypi = "mffpy/mffpy-0.6.3.tar.gz"

    license("Apache-2.0")

    version(
        "0.6.3",
        sha256="e10cbdaeb56c5c743c28ddae8b1e694bcc36c3fdba01f6f9210fea717caf8efb",
        url="https://pypi.org/packages/05/bf/9f59c5c9ad675efe44240e205c730fa4b9d363d5235646dd58a06fd099e4/mffpy-0.6.3-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-deprecated@1.2.12:", when="@0.6.3:")
        depends_on("py-numpy@1.15.1:", when="@0.5.5:")
        depends_on("py-pytz@2019.2:", when="@0.5.5:")
