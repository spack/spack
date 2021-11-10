# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBreathe(PythonPackage):
    """This is an extension to reStructuredText and Sphinx to be able to read
    and render the Doxygen xml output."""

    homepage = "https://github.com/michaeljones/breathe"
    url      = "https://github.com/michaeljones/breathe/archive/v4.11.1.tar.gz"

    version('4.31.0', sha256='63edd18240b7aeb155c6b3d7de13c1322dd7c150f2ad2e9742e95e51b0dc48a8')
    version('4.30.0', sha256='540ca6d694aa2e194ba33265f58e0070465799f6feabb726d198cb039972a5a3')
    version('4.29.2', sha256='e71dfb5dd1176b91bb27d26b7c210d8bd0be5e1f31f10e22ab8d38412a74b52e')
    version('4.29.1', sha256='72cf9ade88f3e9163e0730e4089fde7b92464f691d29250019983457a977df44')
    version('4.29.0', sha256='5fc965cfd248c01909a4ba78f3d7130d85e08b6f373b5224f4fc682cbfd760b4')
    version('4.21.0', sha256='7f97756a1b7f7998377b1153a976bf0d2879bb3ca1cb7bc846f455d37ca87ead')
    version('4.11.1', sha256='84723eefc7cc05da6895e2dd6e7c72926c5fd88a67de57edce42d99c058c7e06')
    version('4.11.0', sha256='8c9f900560529ca2f589f26759be94c2accad14fd83fee34d353cf6f446e09f6')
    version('4.10.0', sha256='10e294ca2927d40c83343674186ce6fad539acfb464ffd765fd371adc1126d4d')
    version('4.9.1',  sha256='3e1e31b879dcd1fe1ebdaf4d0b11356b8e348ac5af101cafa9e54956716a7f02')
    version('4.9.0',  sha256='a2b4b8cd2c4ef708ae69dd174e65731b1e18c24f8670036d2f5e608558be2613')
    version('4.8.0',  sha256='edac7732ad8702ea0425773f1f0c98e7ad5028dbba5fe6483f32a1df3afe2f31')
    version('4.7.3',  sha256='35e2e937fad97c6d7e287db6007184325284130ab50e1154fe126cffc09a1989')
    version('4.7.2',  sha256='982d47909d22fcd71b48bad5aef3644294340b24f612b2887cde2e3be464d960')
    version('4.7.1',  sha256='afb1ab0084b25d3670fa8f5cf2eeaee6fe61bfc77876e3816b140eacd4949875')
    version('4.7.0',  sha256='5629c67f5adb41f39375d36c5f0d60d34b1230be268125e535205d77f69211e4')

    depends_on('py-setuptools', type='build')
    depends_on('py-sphinx @1.4:', type=('build', 'run'))
    depends_on('py-docutils @0.5:', type=('build', 'run'))
    depends_on('py-six@1.4:', type=('build', 'run'))
    depends_on('doxygen @1.8.4:')
