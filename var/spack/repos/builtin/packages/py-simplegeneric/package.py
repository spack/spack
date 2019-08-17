# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySimplegeneric(PythonPackage):
    """Simple generic functions (similar to Python's own len(),
    pickle.dump(), etc.)"""

    homepage = "https://pypi.python.org/pypi/simplegeneric"
    url      = "https://pypi.io/packages/source/s/simplegeneric/simplegeneric-0.8.zip"

    version('0.8.1', 'f9c1fab00fd981be588fc32759f474e3')
    version('0.8', 'eaa358a5f9517a8b475d03fbee3ec90f')

    depends_on('py-setuptools', type='build')
