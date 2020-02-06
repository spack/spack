# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPickleshare(PythonPackage):
    """Tiny 'shelve'-like database with concurrency support"""

    homepage = "https://pypi.python.org/pypi/pickleshare"
    url      = "https://pypi.io/packages/source/p/pickleshare/pickleshare-0.7.4.tar.gz"

    version('0.7.4', sha256='84a9257227dfdd6fe1b4be1319096c20eb85ff1e82c7932f36efccfe1b09737b')

    depends_on('py-setuptools', type='build')
