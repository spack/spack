# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class GeneExpressionVolume(PythonPackage):
    """BBP command line interface for the re-alignment of 2D images and
    the creation of 3D gene expression volumes.
    Used by the atlas building pipeline.
    """
    homepage = "https://bbpgitlab.epfl.ch/nse/gene-expression-volume"
    git      = "git@bbpgitlab.epfl.ch:nse/gene-expression-volume.git"

    version('0.1.0', tag='gene-expression-volume-v0.1.0')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-atlalign@0.6.0', type=('build', 'run'))
    depends_on('py-click@7.0:', type=('build', 'run'))
    depends_on('py-nptyping@1.0.1:', type=('build', 'run'))
    depends_on('py-numpy@1.15.0:', type=('build', 'run'))
    depends_on('py-scikit-image@0.17.2:', type=('build', 'run'))
    depends_on('py-types-pyyaml@5.4.0:', type=('build', 'run'))
    depends_on('py-voxcell@2.7.4:2.999', type=('run', 'build'))
    depends_on('py-pyyaml@5.3.1:', type=('build', 'run'))
    depends_on('py-pytest', type='test')
    depends_on('py-mock', type='test')

    def patch(self):
        filter_file('"lpips_tf.+egg=lpips_tf",', '', 'setup.py')
        filter_file('"tensorflow==[0-9.]+",', '', 'setup.py')

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def test_install(self):
        python("-m", "pytest", "tests")
