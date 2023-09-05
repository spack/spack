# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyKnockknock(PythonPackage):
    homepage = "https://pypi.org/project/knockknock"

    url = "https://pypi.org/project/knockknock/#files/knockknock-0.1.8.1.tar.gz"

    version("0.1.8.1", sha256="c7fa2038ddd5a10379b5ef11b775865298c637cbd9a6a175c2c40d8e2b8df773")

    depends_on("py-hatchling", type="build")
    depends_on("py-flit-core", type="build")
    depends_on("py-poetry-core", type="build")
