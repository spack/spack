# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBluepyConfigfile(PythonPackage):
    """Python library for accessing BlueConfig`s"""

    homepage = "https://bbpgitlab.epfl.ch/nse/bluepy-configfile"
    git      = "git@bbpgitlab.epfl.ch:nse/bluepy-configfile.git"

    version('develop')
    version('0.1.17', tag='bluepy-configfile-v0.1.17')
    version('0.1.15', tag='bluepy-configfile-v0.1.15')
    version('0.1.14', tag='bluepy-configfile-v0.1.14')
    version('0.1.11', tag='bluepy-configfile-v0.1.11')
    version('0.1.7', tag='bluepy-configfile-v0.1.7')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-future@0.16:', type='run')
    depends_on('py-six@1.0:', type='run')
