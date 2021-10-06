# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyScikitImage(PythonPackage):
    """Image processing algorithms for SciPy, including IO, morphology,
    filtering, warping, color manipulation, object detection, etc."""

    homepage = "https://scikit-image.org/"
    pypi = "scikit-image/scikit-image-0.17.2.tar.gz"

    version('0.18.3', sha256='ecae99f93f4c5e9b1bf34959f4dc596c41f2f6b2fc407d9d9ddf85aebd3137ca')
    version('0.18.1', sha256='fbb618ca911867bce45574c1639618cdfb5d94e207432b19bc19563d80d2f171')
    version('0.17.2', sha256='bd954c0588f0f7e81d9763dc95e06950e68247d540476e06cb77bcbcd8c2d8b3')
    version('0.14.2', sha256='1afd0b84eefd77afd1071c5c1c402553d67be2d7db8950b32d6f773f25850c1f')
    version('0.12.3', sha256='82da192f0e524701e89c5379c79200bc6dc21373f48bf7778a864c583897d7c7')

    extends('python', ignore=r'bin/.*\.py$')

    # get dependencies for
    # @:0.13.1 from requirements.txt, DEPENDS.txt
    # @0.14: from requirements/build.txt, requirements/default.txt
    # @0.18: from requirements/build.txt, requirements/default.txt, pyproject.toml
    depends_on('python@3.7:', when='@0.18:', type=('build', 'link', 'run'))
    depends_on('python@3.6:', when='@0.16:', type=('build', 'link', 'run'))
    depends_on('python@2.7:', when='@0.13:', type=('build', 'link', 'run'))
    depends_on('python@2.6:', type=('build', 'link', 'run'))
    depends_on('py-setuptools@51:', when='@0.18:', type='build')
    depends_on('py-setuptools', type='build')
    depends_on('py-cython@0.29.21:', when='@0.18:', type='build')  # from build.txt
    depends_on('py-cython@0.29.13:', when='@0.17:', type='build')
    depends_on('py-cython@0.25:0.28.1,0.28.3:0.28,0.29.1:', when='@0.15:', type='build')
    depends_on('py-cython@0.23.4:0.28.1,0.28.3:0.28,0.29.1:', when='@0.14.3:0.14', type='build')
    depends_on('py-cython@0.23.4:0.28.1', when='@0.14.2', type='build')
    depends_on('py-cython@0.23.4:', when='@0.14.1', type='build')
    depends_on('py-cython@0.21:', type='build')
    depends_on('py-numpydoc@0.6:', when='@0.13.0:0.13', type='build')
    depends_on('py-numpy@1.16.5:1.17,1.18.1:', when='@0.18:', type=('build', 'link', 'run'))
    depends_on('py-numpy@1.15.1:1.17,1.18.1:', when='@0.17.0:0.17', type=('build', 'link', 'run'))
    depends_on('py-numpy@1.14.1:', when='@0.16:', type=('build', 'link', 'run'))
    depends_on('py-numpy@1.11:', when='@0.13:', type=('build', 'link', 'run'))
    depends_on('py-numpy@1.7.2:', type=('build', 'run'))
    depends_on('py-scipy@1.0.1:', when='@0.17:', type=('build', 'run'))
    depends_on('py-scipy@0.19:', when='@0.16:', type=('build', 'run'))
    depends_on('py-scipy@0.17:', when='@0.13:', type=('build', 'run'))
    depends_on('py-scipy@0.9:', type=('build', 'run'))
    depends_on('py-matplotlib@2.0:2,3.0.1:', when='@0.15:', type=('build', 'run'))
    depends_on('py-matplotlib@2:', when='@0.14:', type=('build', 'run'))
    depends_on('py-matplotlib@1.3.1:', type=('build', 'run'))
    depends_on('py-networkx@2:', when='@0.15:', type=('build', 'run'))
    depends_on('py-networkx@1.8:', type=('build', 'run'))
    depends_on('py-six@1.10:', when='@0.14.0:0.14', type=('build', 'run'))
    depends_on('py-six@1.7.3:', when='@:0.14', type=('build', 'run'))
    depends_on('pil@4.3:7.0,7.1.2:', when='@0.17:', type=('build', 'run'))
    depends_on('pil@4.3:', when='@0.14:', type=('build', 'run'))
    depends_on('pil@2.1:', type=('build', 'run'))
    depends_on('py-imageio@2.3:', when='@0.16:', type=('build', 'run'))
    depends_on('py-imageio@2.0.1:', when='@0.15:', type=('build', 'run'))
    depends_on('py-tifffile@2019.7.26:', when='@0.17:', type=('build', 'run'))
    depends_on('py-pywavelets@1.1.1:', when='@0.17:', type=('build', 'run'))
    depends_on('py-pywavelets@0.4:', when='@0.13:', type=('build', 'run'))
    depends_on('py-pooch@0.5.2:', when='@0.17.0:0.17.1', type=('build', 'run'))
    depends_on('py-dask+array@1:', when='@0.14.2', type=('build', 'run'))
    depends_on('py-dask+array@0.9:', when='@0.14.0:0.14.1', type=('build', 'run'))
    depends_on('py-dask+array@0.5:', when='@:0.13', type=('build', 'run'))
    depends_on('py-cloudpickle@0.2.1:', when='@0.14.0:0.14', type=('build', 'run'))
