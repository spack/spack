# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyArchspec(PythonPackage):
    """A library for detecting, labeling and reasoning about
    microarchitectures.
    """

    homepage = "https://archspec.readthedocs.io/en/latest/"
    pypi = "archspec/archspec-0.2.0.tar.gz"

    maintainers("alalazo")

    version("0.2.2", sha256="d922c9fd80a5234d8cef883fbe0e146b381c449062c0405f91714ebad1edc035")
    version("0.2.1", sha256="0974a8a95831d2d43cce906c5b79a35d5fd2bf9be478b0e3b7d83ccc51ac815e")
    version("0.2.0", sha256="6aaba5ebdb5c3633c400d8c221a6a18716da0c64b367a8509f4217b22e91a5f5")

    depends_on("py-poetry-core@1.0.0:", type="build")
    depends_on("py-click@8", type=("build", "run"), when="@:0.2.0")
