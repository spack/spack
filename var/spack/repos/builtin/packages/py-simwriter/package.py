# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySimwriter(PythonPackage):
    """Simwriter."""

    homepage = 'https://bbpcode.epfl.ch/code/#/admin/projects/project/proj1/simwriter'
    git      = 'ssh://bbpcode.epfl.ch/project/proj1/simwriter'

    version('1.0.1', commit='5e6ed1a3e58894bdc7869d5685a1027c745e8eeb')

    depends_on('py-setuptools', type=('build'))

    depends_on('py-bluepy', type='run')
    depends_on('py-numpy', type='run')
    depends_on('py-matplotlib', type='run')
    depends_on('py-scipy', type='run')
    depends_on('py-cheetah3', type='run')
    depends_on('py-progressbar', type='run')
    depends_on('py-elephant', type='run')
    depends_on('py-neo', type='run')
    depends_on('py-quantities', type='run')
    depends_on('py-h5py~mpi', type='run')
