# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyIntervaltree(PythonPackage):
    """Editable interval tree data structure for Python 2 and 3."""

    homepage = "https://github.com/chaimleib/intervaltree"
    url      = "https://github.com/chaimleib/intervaltree/archive/3.0.2.tar.gz"

    version('3.0.2', sha256='cb4f61c81dcb4fea6c09903f3599015a83c9bdad1f0bbd232495e6681e19e273')

    depends_on('py-sortedcontainers@2:3', type=('build', 'run'))
    depends_on('py-pytest', type=('build', 'run'))
