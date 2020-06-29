# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPbr(PythonPackage):
    """PBR is a library that injects some useful and sensible default
       behaviors into your setuptools run."""

    homepage = "https://pypi.python.org/pypi/pbr"
    url      = "https://pypi.io/packages/source/p/pbr/pbr-5.4.3.tar.gz"

    version('5.4.3',  sha256='2c8e420cd4ed4cec4e7999ee47409e876af575d4c35a45840d59e8b5f3155ab8')
    version('5.2.1',  sha256='93d2dc6ee0c9af4dbc70bc1251d0e545a9910ca8863774761f92716dece400b6')
    version('3.1.1',  sha256='05f61c71aaefc02d8e37c0a3eeb9815ff526ea28b3b76324769e6158d7f95be1')
    version('2.0.0',  sha256='0ccd2db529afd070df815b1521f01401d43de03941170f8a800e7531faba265d')
    version('1.10.0', sha256='186428c270309e6fdfe2d5ab0949ab21ae5f7dea831eab96701b86bd666af39c')
    version('1.8.1',  sha256='e2127626a91e6c885db89668976db31020f0af2da728924b56480fc7ccf09649')

    depends_on('python@2.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')

    # test-requirements.txt
    depends_on('py-wheel@0.32.0:', type='test')
    depends_on('py-fixtures@3.0.0:', type='test')
    depends_on('py-hacking@0.12.0:0.12.999,0.13.1:0.13.999', type='test')
    depends_on('py-mock@2.0.0:', type='test')
    depends_on('py-six@1.10.0:', type='test')
    depends_on('py-stestr@2.1.0:', type='test')
    depends_on('py-testresources@2.0.0:', type='test')
    depends_on('py-testscenarios@0.4:', type='test')
    depends_on('py-testtools@2.2.0:', type='test')
    depends_on('py-virtualenv@14.0.6:', type='test')
    depends_on('py-coverage@4.0:4.3,4.5:', type='test')
    depends_on('py-sphinx@1.6.2:1.6.5,1.6.8:1.999', when='^python@:2', type='test')
    depends_on('py-sphinx@1.6.2:1.6.5,1.6.8:', type='test')
    depends_on('py-testrepository@0.0.18:', type='test')
