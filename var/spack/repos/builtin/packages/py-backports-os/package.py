# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBackportsOs(PythonPackage):
    """Backport of new features in Python's os module"""

    homepage = "https://github.com/pjdelport/backports.os"
    pypi     = "backports.os/backports.os-0.1.1.tar.gz"

    version('0.1.1', sha256='b472c4933094306ca08ec90b2a8cbb50c34f1fb2767775169a1c1650b7b74630')

    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm', type='build')
    depends_on('py-future',     type=('build', 'run'), when='^python@:2')
