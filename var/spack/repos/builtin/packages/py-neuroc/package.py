# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyNeuroc(PythonPackage):
    """Python library neuron morphology analysis"""

    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/nse/neuroc"
    url = "https://bbpcode.epfl.ch/code/#/admin/projects/nse/neuroc"
    git = "ssh://bbpcode.epfl.ch/nse/NeuroC"

    version('develop', branch='master')
    version('0.1.7', tag='neuroc-v0.1.7')
    version('0.1.1', sha256='e541f6c8a11826caa2b2d1cf18015a10ec7009f12813edfc2655084c7cf5021b')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-attrs', type='run')
    depends_on('py-tqdm@4.23.4:', type='run')
    depends_on('py-morph-tool', type='run')
    depends_on('py-scikit-learn', type='run')
    # depends_on('py-dash', type='run')
    # depends_on('py-dash-html-components', type='run')
    # depends_on('py-dash-core-components', type='run')
    # depends_on('py-dash-table', type='run')

    def patch(self):
        filter_file(".*dash.*", "", "setup.py")
