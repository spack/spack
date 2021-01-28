# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDiameterSynthesis(PythonPackage):
    """Python library to generate synthetic diameters for neurons."""

    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/cells/diameter-synthesis"
    git      = "ssh://bbpcode.epfl.ch/cells/diameter-synthesis"

    version('0.1.7', tag='diameter-synthesis-v0.1.7')

    depends_on('py-setuptools', type='build')

    depends_on('py-click@7.0:', type='run')
    depends_on('py-numpy@1.15.0:', type='run')
    depends_on('py-scipy@0.13:', type='run')
    depends_on('py-h5py@2.9:', type='run')
    depends_on('py-morphio@2.3.4:', type='run')
    depends_on('py-matplotlib@2.2:', type='run')
    depends_on('py-pandas@0.24:', type='run')
    depends_on('py-neurom@1.4.2:', type='run')
