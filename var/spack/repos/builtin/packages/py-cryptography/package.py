# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *


class PyCryptography(PythonPackage):
    """cryptography is a package which provides cryptographic recipes
       and primitives to Python developers"""

    homepage = "https://github.com/pyca/cryptography"
    pypi = "cryptography/cryptography-1.8.1.tar.gz"

    version('3.4.4', sha256='ee5e19f0856b6fbbdbab15c2787ca65d203801d2d65d0b8de6218f424206c848')
    version('3.4.3', sha256='d70065c42de45e15776a53216000283a2a183ae37379badb37f527a2bdfd6221')
    version('3.4.2', sha256='c460e296c8cb3a796cdcc7d56c62a78fcd0a09409ccd9c658ace4f987ce935c4')
    version('3.4.1', sha256='be70bdaa29bcacf70896dae3a6f3eef91daf51bfba8a49dbfb9c23bb2cc914ba')
    version('3.4',   sha256='9f7aa11ea95723359f914be3217d8b378bc3897f65a1ec1ab4e0118c336f51fc')
    version('3.3.2', sha256='5a60d3780149e13b7a6ff7ad6526b38846354d11a15e21068e57073e29e19bed')
    version('3.3.1', sha256='7e177e4bea2de937a584b13645cab32f25e3d96fc0bc4a4cf99c27dc77682be6')
    version('3.3',   sha256='d9f1e520f2ee08c5a88e1ae0b31159bdb13da40a486bea3e9f7d338564850ea6')
    version('3.2.1', sha256='d3d5e10be0cf2a12214ddee45c6bd203dab435e3d83b4560c03066eda600bfe3')
    version('3.2',   sha256='e4789b84f8dedf190148441f7c5bfe7244782d9cbb194a36e17b91e7d3e1cca9')
    version('3.1.1', sha256='9d9fc6a16357965d282dd4ab6531013935425d0dc4950df2e0cf2a1b1ac1017d')
    version('3.1',   sha256='26409a473cc6278e4c90f782cd5968ebad04d3911ed1c402fc86908c17633e08')
    version('3.0',   sha256='8e924dbc025206e97756e8903039662aa58aa9ba357d8e1d8fc29e3092322053')
    version('2.9.2', sha256='a0c30272fb4ddda5f5ffc1089d7405b7a71b0b0f51993cb4e5dbb4590b2fc229')
    version('2.9.1', sha256='ce0bd68b4b946bd4bcebc3d4d1325bf0e938e445ae18cedddd60e33dd85a368e')
    version('2.9',   sha256='0cacd3ef5c604b8e5f59bf2582c076c98a37fe206b31430d0cd08138aff0986e')
    version('2.8',   sha256='3cda1f0ed8747339bbdf71b9f38ca74c7b592f24f65cdb3ab3765e4b02871651')
    version('2.7',   sha256='e6347742ac8f35ded4a46ff835c60e68c22a536a8ae5c4422966d06946b6d4c6')
    version('2.3.1', sha256='8d10113ca826a4c29d5b85b2c4e045ffa8bad74fb525ee0eceb1d38d4c70dfd6')
    version('1.8.1', sha256='323524312bb467565ebca7e50c8ae5e9674e544951d28a2904a50012a8828190')

    variant('idna', default=False, description='Deprecated U-label support')
    conflicts('+idna', when='@:2.4')

    # dependencies taken from https://github.com/pyca/cryptography/blob/master/setup.py
    depends_on('python@2.6:2.8,3.4:',                 type=('build', 'run'))
    depends_on('python@2.7:2.8,3.4:', when='@2.3.1:', type=('build', 'run'))

    depends_on('py-setuptools@20.5:',   type='build')

    depends_on('py-cffi@1.4.1:',             type=('build', 'run'))
    depends_on('py-cffi@1.8:1.11.2,1.11.4:', type=('build', 'run'), when='@2.7:')

    depends_on('py-asn1crypto@0.21.0:', type=('build', 'run'))
    depends_on('py-six@1.4.1:',         type=('build', 'run'))
    depends_on('py-idna@2.1:',          type=('build', 'run'), when='@:2.4')  # deprecated
    depends_on('py-idna@2.1:',          type=('build', 'run'), when='@2.5: +idna')  # deprecated
    depends_on('py-enum34',             type=('build', 'run'), when='^python@:3.4')
    depends_on('py-ipaddress',          type=('build', 'run'), when='^python@:3.3')
    depends_on('openssl@:1.0', when='@:1.8.1')
    depends_on('openssl')
