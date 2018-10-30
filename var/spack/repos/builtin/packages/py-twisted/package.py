# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTwisted(PythonPackage):
    """An asynchronous networking framework written in Python"""
    homepage = "https://twistedmatrix.com/"
    url      = "https://pypi.io/packages/source/T/Twisted/Twisted-15.3.0.tar.bz2"

    version('15.4.0', '5337ffb6aeeff3790981a2cd56db9655')
    version('15.3.0', 'b58e83da2f00b3352afad74d0c5c4599')

    depends_on('py-setuptools', type='build')
