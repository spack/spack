# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDill(PythonPackage):
    """Serialize all of python """

    homepage = "https://github.com/uqfoundation/dill"
    url      = "https://pypi.io/packages/source/d/dill/dill-0.2.6.zip"

    version('0.2.6', 'f8b98b15223d23431024349f2102b4f9')
    version('0.2.5', 'c9eecc32351f4934e2e67740a40397f6')
    version('0.2.4', '5d10cd1cafea38a45bcd4542f2ca3adc')
    version('0.2.3', '0b6c4f55da320893991cc32628a6e9be')
    version('0.2.2', 'a282b81a6d289f91218bba8d07f49bd8')
    version('0.2.1', 'b2354a5717da6228acae33cb13bc407b')
    version('0.2', '759002d9b71605cde2a7a052dad96b5d')

    depends_on('python@2.5:2.8,3.1:')

    depends_on('py-setuptools@0.6:', type='build')
