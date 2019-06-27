# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySimwriter(PythonPackage):
    """Simwriter."""

    homepage = 'https://bbpcode.epfl.ch/code/#/admin/projects/project/proj1/simwriter'
    git      = 'ssh://bbpcode.epfl.ch/project/proj1/simwriter'

    version('0.4.3', commit='6d7a618b542cf9364805ea6c8e565a54825cddef')

    # cheetah is python 2 only
    depends_on('python@:2', type=('build', 'run'))

    depends_on('py-setuptools', type=('build'))

    depends_on('py-bluepy', type='run')
    depends_on('py-numpy', type='run')
    depends_on('py-matplotlib', type='run')
    depends_on('py-scipy', type='run')
    depends_on('py-cheetah', type='run')
    depends_on('py-neurotools', type='run')
    depends_on('py-progressbar', type='run')
    depends_on('py-functools32', type='run')
