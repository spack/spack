# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyPudb(PythonPackage):
    """Full-screen console debugger for Python"""

    homepage = "http://mathema.tician.de/software/pudb"
    url      = "https://pypi.io/packages/source/p/pudb/pudb-2017.1.1.tar.gz"

    version('2017.1.1', '4ec3302ef90f22b13c60db16b3557c56')
    version('2016.2',   '4573b70163329c1cb59836a357bfdf7c')

    # Most Python packages only require setuptools as a build dependency.
    # However, pudb requires setuptools during runtime as well.
    depends_on('py-setuptools',    type=('build', 'run'))
    depends_on('py-urwid@1.1.1:',  type=('build', 'run'))
    depends_on('py-pygments@1.0:', type=('build', 'run'))
