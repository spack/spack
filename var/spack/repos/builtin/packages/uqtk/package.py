# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class Uqtk(CMakePackage):
    """Sandia Uncertainty Quantification Toolkit. The UQ Toolkit (UQTk) is a
    collection of libraries and tools for the quantification of uncertainty
    in numerical model predictions"""

    homepage = "https://www.sandia.gov/UQToolkit/"
    url      = "https://github.com/sandialabs/UQTk/archive/v3.0.4.tar.gz"
    git      = "https://github.com/sandialabs/UQTk.git"

    version('master', branch='master')
    version('3.0.4', sha256='0a72856438134bb571fd328d1d30ce3d0d7aead32eda9b7fb6e436a27d546d2e')

    depends_on('expat')
