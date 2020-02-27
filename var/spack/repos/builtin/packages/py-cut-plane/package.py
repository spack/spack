# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyCutPlane(PythonPackage):
    """Python morphology manipulation toolkit"""

    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/nse/cut-plane"
    git      = "ssh://bbpcode.epfl.ch/nse/cut-plane"

    version('develop', branch='master')
    version('0.0.7', tag='cut-plane-v0.0.7')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-neurom@mut_morphio', type='run', when='@0.1.14:')
    depends_on('py-pyquaternion', type='run')
    depends_on('py-entity-management', type='run')
    depends_on('py-plotly-helper', type='run')

    def patch(self):
        filter_file(".*dash.*", "", "setup.py")
