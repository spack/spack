# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ultraliser(CMakePackage):
    """Mesh and volume reconstruction of neuroscientific models
    """
    homepage = "https://github.com/BlueBrain/Ultraliser"
    git = "git@github.com:BlueBrain/Ultraliser.git"

    version('0.3.0', tag='v0.3.0')

    depends_on('libtiff')
    depends_on('ilmbase')
    depends_on('hdf5+hl+cxx')
