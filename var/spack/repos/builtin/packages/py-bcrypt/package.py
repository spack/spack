# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBcrypt(PythonPackage):
    """Modern password hashing for your software and your servers"""

    homepage = "https://github.com/pyca/bcrypt/"
    url      = "https://github.com/pyca/bcrypt/archive/3.1.4.tar.gz"

    version('3.1.4', '2db1e1bf4a9e92f78297e1f090d7a30e')

    depends_on('py-setuptools', type='build')
    depends_on('py-cffi@1.1:', type=('build', 'run'))
    depends_on('py-six@1.4.1:', type=('build', 'run'))
