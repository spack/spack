# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMunch(PythonPackage):
    """A Munch is a Python dictionary that provides attribute-style
       access (a la JavaScript objects). """

    homepage = "https://github.com/Infinidat/munch"
    url      = "https://github.com/Infinidat/munch/archive/2.2.0.tar.gz"

    version('2.2.0', 'a50f0e4d770b5106f0c440a6cff3617f')

    depends_on('py-setuptools', type='build')
    depends_on('py-six', type=('build', 'run'))
