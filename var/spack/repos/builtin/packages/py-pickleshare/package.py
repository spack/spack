# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPickleshare(PythonPackage):
    """Tiny 'shelve'-like database with concurrency support"""

    homepage = "https://pypi.python.org/pypi/pickleshare"
    url      = "https://pypi.io/packages/source/p/pickleshare/pickleshare-0.7.4.tar.gz"

    version('0.7.4', '6a9e5dd8dfc023031f6b7b3f824cab12')

    depends_on('py-setuptools', type='build')
