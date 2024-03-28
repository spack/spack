# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTroveClassifiers(PythonPackage):
    """The trove-classifiers pacakge is the canonical source for classifiers
    on PyPI. Classifiers categorize projects per PEP 301."""

    homepage = "https://github.com/pypa/trove-classifiers"
    pypi = "trove-classifiers/trove-classifiers-2023.3.9.tar.gz"

    license("Apache-2.0")

    version(
        "2023.8.7",
        sha256="a676626a31286130d56de2ea1232484df97c567eb429d56cfcb0637e681ecf09",
        url="https://pypi.org/packages/14/c6/35e478a586e857c2a6d31fc7b1586d4ff965f729a290552b5c2eb7b9f807/trove_classifiers-2023.8.7-py3-none-any.whl",
    )
    version(
        "2023.3.9",
        sha256="06fd10c95d285e7ddebd59e6a4ba299f03d7417d38d369248a4a40c9754a68fa",
        url="https://pypi.org/packages/c9/27/f1a53dbb6c5062bf216c3f145ec6f76c828c08b6ea843acda2eb2ba24b33/trove_classifiers-2023.3.9-py3-none-any.whl",
    )
