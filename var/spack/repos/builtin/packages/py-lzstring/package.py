# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyLzstring(PythonPackage):
    """lz-string for python."""

    homepage = "https://github.com/gkovacs/lz-string-python"
    url      = "https://pypi.io/packages/source/l/lzstring/lzstring-1.0.3.tar.gz"

    version('1.0.3', '1c636543484629020a26432740f81443')

    depends_on('py-setuptools', type='build')
    depends_on('py-future', type=('build', 'run'))
