# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAtomicwrites(PythonPackage):
    """Atomic file writes."""

    homepage = "https://github.com/untitaker/python-atomicwrites"
    url      = "https://pypi.io/packages/source/a/atomicwrites/atomicwrites-1.1.5.tar.gz"

    import_modules = ['atomicwrites']

    version('1.1.5', sha256='240831ea22da9ab882b551b31d4225591e5e447a68c5e188db5b89ca1d487585')

    depends_on('py-setuptools', type='build')
