# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyVoxcell(PythonPackage):
    """Python library for handling volumetric data"""

    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/nse/voxcell"
    git      = "ssh://bbpcode.epfl.ch/nse/voxcell"

    version('develop', branch='master')
    version('2.5.5', tag='voxcell-v2.5.5', preferred=True)

    depends_on('py-setuptools', type='build')

    depends_on('py-future', type='run')
    depends_on('py-h5py~mpi', type='run')
    depends_on('py-numpy', type='run')
    depends_on('py-pandas', type='run')
    depends_on('py-pynrrd', type='run')
    depends_on('py-requests', type='run')
    depends_on('py-scipy', type='run')
    depends_on('py-six', type='run')
