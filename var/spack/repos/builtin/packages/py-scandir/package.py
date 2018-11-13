# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyScandir(PythonPackage):
    """scandir, a better directory iterator and faster os.walk()."""

    homepage = "https://github.com/benhoyt/scandir"
    url      = "https://pypi.io/packages/source/s/scandir/scandir-1.9.0.tar.gz"

    import_modules = ['scandir']

    version('1.9.0', '506c4cc5f38c00b301642a9cb0433910')
    version('1.6',   '0180ddb97c96cbb2d4f25d2ae11c64ac')

    depends_on('py-setuptools', type=('build'))
