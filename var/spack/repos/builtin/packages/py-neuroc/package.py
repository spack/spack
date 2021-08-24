# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyNeuroc(PythonPackage):
    """Python library neuron morphology analysis"""

    homepage = "https://bbpgitlab.epfl.ch/nse/neuroc"
    git = "git@bbpgitlab.epfl.ch:nse/neuroc.git"

    version('develop', branch='master')
    version('0.2.7', tag='neuroc-v0.2.7')
    version('0.2.6', tag='neuroc-v0.2.6')
    version('0.2.4', tag='neuroc-v0.2.4')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-attrs', type='run')
    depends_on('py-tqdm@4.23.4:', type='run')
    depends_on('py-morph-tool@0.1.12:', type='run')
    depends_on('py-scikit-learn@0.21.3', type='run')
    depends_on('py-morphio@2.0.6:', type='run')
    depends_on('py-neurom@2:2.999', type='run')
    depends_on('py-pandas@1.0.3:', type='run')
    depends_on('py-click@6.7:', type='run')
    depends_on('py-attrs@19.1.0:', type='run')
    depends_on('py-numpy@1.15.1:', type='run')
    # depends_on('py-dash', type='run')
    # depends_on('py-dash-html-components', type='run')
    # depends_on('py-dash-core-components', type='run')
    # depends_on('py-dash-table', type='run')

    def patch(self):
        filter_file(".*dash.*", "", "setup.py")
