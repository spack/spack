# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTorchgeo(PythonPackage):
    """TorchGeo: datasets, transforms, and models for geospatial data.

    TorchGeo is a PyTorch domain library, similar to torchvision, that provides
    datasets, transforms, samplers, and pre-trained models specific to geospatial data.
    """

    homepage = "https://github.com/microsoft/torchgeo"
    git = "https://github.com/microsoft/torchgeo.git"

    maintainers = ['adamjstewart', 'calebrob6']

    version('main', branch='main')

    variant('datasets', default=False, description='Install optional dataset dependencies')
    variant('docs', default=False, description='Install documentation dependencies')
    variant('style', default=False, description='Install style checking tools')
    variant('tests', default=False, description='Install testing tools')
    variant('train', default=False, description='Install optional trainer dependencies')

    # Required dependencies
    depends_on('python@3.6:+bz2', type=('build', 'run'))
    depends_on('py-setuptools@30.4:', type='build')
    depends_on('py-einops', type=('build', 'run'))
    depends_on('py-fiona@1.5:', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('pil@2.9:', type=('build', 'run'))
    depends_on('py-pyproj@2.2:', type=('build', 'run'))
    depends_on('py-rasterio@1.0.16:', type=('build', 'run'))
    depends_on('py-rtree@0.5:', type=('build', 'run'))
    depends_on('py-shapely@1.3:', type=('build', 'run'))
    depends_on('py-torch@1.7:', type=('build', 'run'))
    depends_on('py-torchvision@0.3:', type=('build', 'run'))

    # Optional dependencies
    with when('+datasets'):
        depends_on('py-h5py', type='run')
        depends_on('opencv+python3+imgcodecs+tiff+jpeg+png', type='run')
        depends_on('py-pycocotools', type='run')
        depends_on('py-radiant-mlhub@0.2.1:', type='run')
        depends_on('py-rarfile@3:', type='run')
        depends_on('py-scipy@0.9:', type='run')

    with when('+docs'):
        depends_on('py-ipywidgets@7:', type='run')
        depends_on('py-jupyterlab', type='run')
        depends_on('py-nbmake@0.1:', type='run')
        depends_on('py-nbsphinx@0.8.5:', type='run')
        depends_on('py-sphinx@3:', type='run')
        depends_on('py-pydocstyle@6.1:+toml', type='run')
        depends_on('py-pytorch-sphinx-theme', type='run')

    with when('+style'):
        depends_on('py-black@21:', type='run')
        depends_on('py-flake8@3.8:', type='run')
        depends_on('py-isort@5.8:+colors', type='run')

    with when('+tests'):
        depends_on('py-mypy@0.900:', type='run')
        depends_on('py-pytest@6:', type='run')
        depends_on('py-pytest-cov@2.4:', type='run')

    with when('+train'):
        depends_on('py-omegaconf@2.1:', type='run')
        depends_on('py-pytorch-lightning@1.3:', type='run')
        depends_on('py-scikit-learn@0.18:', type='run')
        depends_on('py-segmentation-models-pytorch@0.2:', type='run')
        depends_on('py-torchmetrics', type='run')
