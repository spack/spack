# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: MIT

# ----------------------------------------------------------------------------
#
#     spack install py-gitdb
#
# You can edit this file again by typing:
#
#     spack edit py-gitdb
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyGitdb(PythonPackage):
    """The GitDB project implements interfaces to allow read and write access to git repositories."""

    homepage = "https://gitdb.readthedocs.io"
    url      = "https://github.com/gitpython-developers/gitdb/archive/2.0.5.tar.gz"

    version('2.0.5', sha256='3ccb0cf0015e29f251674f33ec8de549fc876cf9360da09609cb645cc3092524')

    depends_on('py-setuptools', type='build')
    depends_on('py-smmap',      type=('build', 'run'))

