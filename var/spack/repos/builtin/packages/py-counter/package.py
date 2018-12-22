# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCounter(PythonPackage):
    """Counter package defines the "counter.Counter" class similar to
       bags or multisets in other languages."""

    import_modules = ['counter']

    homepage = "https://github.com/KelSolaar/Counter"
    url      = "https://pypi.io/packages/source/C/Counter/Counter-1.0.0.tar.gz"

    version('1.0.0', '1b49029693c28813ff276c2b16673f98')

    depends_on('py-setuptools', type='build')
