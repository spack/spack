# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNose(PythonPackage):
    """nose extends the test loading and running features of unittest,
    making it easier to write, find and run tests."""

    homepage = "https://pypi.python.org/pypi/nose"
    url      = "https://pypi.io/packages/source/n/nose/nose-1.3.4.tar.gz"

    import_modules = [
        'nose', 'nose.ext', 'nose.plugins', 'nose.sphinx', 'nose.tools'
    ]

    version('1.3.7', '4d3ad0ff07b61373d2cefc89c5d0b20b')
    version('1.3.6', '0ca546d81ca8309080fc80cb389e7a16')
    version('1.3.4', '6ed7169887580ddc9a8e16048d38274d')

    depends_on('py-setuptools', type='build')
