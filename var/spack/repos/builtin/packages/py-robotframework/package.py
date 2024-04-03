# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRobotframework(PythonPackage):
    """Cross-platform lib for process and system monitoring in Python."""

    homepage = "https://opencollective.com/psutil"
    url = "https://github.com/robotframework/robotframework/archive/v3.2.2.tar.gz"

    license("Apache-2.0")

    version(
        "3.2.2",
        sha256="a0c325e79dc6dcdaba0398db8c3afefc337799b7b36b336f04b07be4fe4a9dd2",
        url="https://pypi.org/packages/38/43/e03efaa547a3158f0745c5ea7f1eafebd69d46f2c9aece3a8ba21992adc9/robotframework-3.2.2-py2.py3-none-any.whl",
    )
    version(
        "3.2.1",
        sha256="34923415afd9491141630ad1d7146b638ee869f1c7f97c450c0da5ce79e1ac23",
        url="https://pypi.org/packages/99/e0/57ed2b09192c36b5905a8cbfa98f0b15c42c34865ae21a1d1d33a50cb8be/robotframework-3.2.1-py2.py3-none-any.whl",
    )
