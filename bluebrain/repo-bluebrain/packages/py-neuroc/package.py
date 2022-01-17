# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyNeuroc(PythonPackage):
    """Python library neuron morphology analysis"""

    homepage = "https://bbpgitlab.epfl.ch/nse/neuroc"
    git = "git@bbpgitlab.epfl.ch:nse/neuroc.git"

    version('develop', branch='main')
    version('0.2.8', tag='neuroc-v0.2.8')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-attrs@19.1.0:', type=('build', 'run'))
    depends_on('py-tqdm@4.23.4:', type=('build', 'run'))
    depends_on('py-morph-tool@2.9.0:2.999', type=('build', 'run'))
    depends_on('py-scikit-learn@0.21.3:', type=('build', 'run'))
    depends_on('py-morphio@3.0:3.999', type=('build', 'run'))
    depends_on('py-neurom@3:3.999', type=('build', 'run'))
    depends_on('py-pandas@1.0.3:', type=('build', 'run'))
    depends_on('py-click@6.7:', type=('build', 'run'))
    depends_on('py-numpy@1.15.1:', type=('build', 'run'))
    # plotly extra requirements
    # depends_on('py-dash', type=('build', 'run'))
    # depends_on('py-dash-html-components', type=('build', 'run'))
    # depends_on('py-dash-core-components', type=('build', 'run'))
    # depends_on('py-dash-table', type=('build', 'run'))

    def patch(self):
        filter_file(".*dash.*", "", "setup.py")
