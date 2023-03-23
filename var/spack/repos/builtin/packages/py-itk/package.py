# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.itk import Itk


class PyItk(BundlePackage):
    """ITK is an open-source toolkit for multidimensional image analysis"""

    homepage = "https://itk.org/"

    for ver in Itk.versions:
        ver = str(ver)
        version(ver)
        depends_on("itk+python@" + ver, when="@" + ver, type=("build", "run"))
