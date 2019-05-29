# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyVscInstall(PythonPackage):
    """Shared setuptools functions and classes
    for Python libraries developed by HPC-UGent.
    """

    homepage = 'https://github.com/hpcugent/vsc-install/'
    url      = 'https://pypi.io/packages/source/v/vsc-install/vsc-install-0.10.25.tar.gz'

    version('0.10.25', 'd1b9453a75cb56dba0deb7a878047b51')

    depends_on('py-setuptools', type=('build', 'run'))
