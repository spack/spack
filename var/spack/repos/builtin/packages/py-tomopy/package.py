# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyTomopy(PythonPackage):
    """TomoPy is an open-source Python package for tomographic data
       processing and image reconstruction."""

    homepage = "http://tomopy.readthedocs.io/en/latest/index.html"
    url      = "https://github.com/tomopy/tomopy/archive/1.0.0.tar.gz"

    version('1.9.1', sha256='fd61c52ec2419ea1996f32e21cbef94921d6ed8d733e018fabe542e94a355074')
    version('1.9.0', sha256='81cca1c34955bd827062d3b1ec06f90f816835effdc4d4e3358b2e37cf1d0106')
    version('1.8.2', sha256='dba03d769ae430781b80e00e17b7efb4f5c32c37025751a42ec60f9280c2dea9')
    version('1.8.1', sha256='6a4ccf9179ee3774f5a7738a9123a292b5ab5b38ce60c568f3c116f951d7b7c6')
    version('1.8.0', sha256='ba31b6eb55f32a084f1c9e06516a59eb7cd97c2876668619d8688ce6f9630ee9')
    version('1.7.2', sha256='d828d89988d190a27163fdcd718180246a7fe1a401dafc771c4a8da600bca3d7')
    version('1.7.1', sha256='605c7140599ee51272d4cb6fc4043d2828c5cf395e04b368037a29b70eb84b6d')
    version('1.7.0', sha256='5eec47f95b18a3e742e8bbea9e9a15bc9bc0d7c52b9cccd0280ff17a9eda57b0')
    version('1.6.0', sha256='c9b561e1f7496bfdf204fdd9c7294b84fbf055d35665620a5082d39fc25dda1d')
    version('1.5.2', sha256='68b06a8a8796bf6082579c6d92d134c1e208b0ba40a689288b0db1785b7605ce')
    version('1.0.0', sha256='ee45f7a062e5a66d6f18a904d2e204e48d85a1ce1464156f9e2f6353057dfe4c')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-h5py', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-scikit-image', type=('build', 'run'))
    depends_on('py-pywavelets', type=('build', 'run'))
    depends_on('py-pyfftw', type=('build', 'run'))
    depends_on('py-dxchange', type=('build', 'run'))
