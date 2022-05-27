# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
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
    pypi = "torchgeo/torchgeo-0.1.0.tar.gz"
    git = "https://github.com/microsoft/torchgeo.git"

    maintainers = ['adamjstewart', 'calebrob6']

    version('main', branch='main')
    version('0.2.1', sha256='218bd5aed7680244688dbf0f1398f5251ad243267eb19a6a7332668ac779a1cc')
    version('0.2.0', sha256='968c4bf68c7e487bf495f2f306d8bb0f5824eb67e24b26772a510e753e04ba4c')
    version('0.1.1', sha256='6e28132f75e9d8cb3a3a0e8b443aba3cde26c8f3140b9426139ee6e8f8058b26')
    version('0.1.0', sha256='44eb3cf10ab2ac63ff95e92fcd3807096bac3dcb9bdfe15a8edac9d440d2f323')

    variant('datasets', default=False, description='Install optional dataset dependencies')
    variant('style', default=False, description='Install style checking tools')
    variant('tests', default=False, description='Install testing tools')

    # Required dependencies
    depends_on('python@3.6:+bz2', type=('build', 'run'))
    depends_on('py-setuptools@42:', type='build')
    depends_on('py-dataclasses', when='@0.2: ^python@3.6', type=('build', 'run'))
    depends_on('py-einops', type=('build', 'run'))
    depends_on('py-fiona@1.5:', type=('build', 'run'))
    depends_on('py-kornia@0.5.11:', when='@0.2:', type=('build', 'run'))
    depends_on('py-kornia@0.5.4:', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-omegaconf@2.1:', type=('build', 'run'))
    depends_on('pil@2.9:', type=('build', 'run'))
    depends_on('py-pyproj@2.2:', type=('build', 'run'))
    depends_on('py-pytorch-lightning@1.3:', type=('build', 'run'))
    depends_on('py-rasterio@1.0.16:', type=('build', 'run'))
    depends_on('py-rtree@0.9.4:', when='@0.2.1:', type=('build', 'run'))
    depends_on('py-rtree@0.5:', type=('build', 'run'))
    depends_on('py-scikit-learn@0.18:', type=('build', 'run'))
    depends_on('py-segmentation-models-pytorch@0.2:', type=('build', 'run'))
    depends_on('py-shapely@1.3:', type=('build', 'run'))
    depends_on('py-timm@0.2.1:', type=('build', 'run'))
    depends_on('py-torch@1.7:', type=('build', 'run'))
    depends_on('py-torchmetrics@0.7:', when='@0.2.1:', type=('build', 'run'))
    depends_on('py-torchmetrics@:0.7', when='@:0.2.0', type=('build', 'run'))
    depends_on('py-torchvision@0.10:', when='@0.2:', type=('build', 'run'))
    depends_on('py-torchvision@0.3:', type=('build', 'run'))

    # Optional dependencies
    with when('+datasets'):
        depends_on('py-h5py', type='run')
        depends_on('py-laspy@2:', when='@0.2:', type='run')
        depends_on('libtiff+jpeg+zlib')
        depends_on('open3d@0.11.2:+python', when='@0.2:', type='run')
        depends_on('opencv+python3+imgcodecs+tiff+jpeg+png', type='run')
        depends_on('py-pandas@0.19.1:', when='@0.2:', type='run')
        depends_on('py-pycocotools', type='run')
        depends_on('py-radiant-mlhub@0.2.1:', type='run')
        depends_on('py-rarfile@3:', type='run')
        depends_on('py-scipy@0.9:', type='run')
        depends_on('py-zipfile-deflate64@0.2:', when='@0.2.1:', type='run')

    with when('+style'):
        depends_on('py-black@21:', type='run')
        depends_on('py-flake8@3.8:', type='run')
        depends_on('py-isort@5.8:+colors', type='run')
        depends_on('py-pydocstyle@6.1:+toml', type='run')

    with when('+tests'):
        depends_on('py-mypy@0.900:', type='run')
        depends_on('py-nbmake@0.1:', type='run')
        depends_on('py-pytest@6:', type='run')
        depends_on('py-pytest-cov@2.4:', type='run')
