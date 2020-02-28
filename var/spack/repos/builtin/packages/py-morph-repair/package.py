# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyMorphRepair(PythonPackage):
    """Python morphology manipulation toolkit"""

    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/nse/morph-repair"
    git      = "ssh://bbpcode.epfl.ch/nse/morph-repair"

    version('develop', branch='master')
    version('0.2.2', tag='morph-repair-v0.2.2')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-morph-tool', type='run')
    depends_on('py-cut-plane', type='run')
    depends_on('py-pandas', type='run')
