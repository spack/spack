# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMissingno(PythonPackage):
   
    homepage = "https://www.example.com"

    url = "https://pypi.org/project/missingno/#files/missingno-0.5.2.tar.gz"

    version("0.5.2", sha256="4a4baa9ca9f9e4e0d9402455df26b656632e94b99e87fa64c0cdbbbc722837ac")

    depends_on("py-wheel@X.Y:", type="build")
    depends_on("py-hatchling", type="build")
    depends_on("py-flit-core", type="build")
    depends_on("py-poetry-core", type="build")