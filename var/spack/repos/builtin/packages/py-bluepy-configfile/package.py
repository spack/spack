# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBluepyConfigfile(PythonPackage):
    """Python library for accessing BlueConfig`s"""

    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/nse/bluepy-configfile"
    git      = "ssh://bbpcode.epfl.ch/nse/bluepy-configfile"

    version('develop', branch='master')
    version('0.1.7', tag='bluepy-configfile-v0.1.7', preferred=True)

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-future@0.16:', type='run')
    depends_on('py-six@1.0:', type='run')
