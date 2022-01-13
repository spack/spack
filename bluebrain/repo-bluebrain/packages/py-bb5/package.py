##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class PyBb5(PythonPackage):
    """Utilities for Blue Brain 5 Super Computer
    """
    homepage = "https://github.com/BlueBrain/pybb5"
    url      = "git@github.com:BlueBrain/pybb5.git"

    version('develop', git=url)
    version('0.2', git=url, tag='v0.2', preferred=True, get_full_repo=True)

    patch('purge-scaffold.patch')

    depends_on('python@3.6:')
    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm', type='build')

    depends_on('py-clustershell', type=('build', 'run'))
    depends_on('py-docopt', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-pandas', type=('build', 'run'))
    depends_on('py-requests', type=('build', 'run'))
    depends_on('py-seaborn', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
