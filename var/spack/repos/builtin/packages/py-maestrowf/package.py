# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMaestrowf(PythonPackage):
    """A general purpose workflow conductor for running multi-step
       simulation studies."""

    homepage = "https://github.com/LLNL/maestrowf/"
    url      = "https://github.com/LLNL/maestrowf/archive/v1.1.2.tar.gz"

    version('1.1.2', 'a9e05d82910cd2dd077321fb9b0c8dcd')
    version('1.1.1', 'd38bbf634de4f29fd01d1864ba2f70e0')
    version('1.1.0', '3c20bf36fbb85d14c3bfdb865944a409')
    version('1.0.1', '6838fc8bdc7ca0c1adbb6a0333f005b4')

    depends_on('py-setuptools', type='build')
    depends_on('py-pyyaml',     type=('build', 'run'))
    depends_on('py-six',        type=('build', 'run'))
    depends_on('py-enum34',     type=('build', 'run'))
    depends_on('py-tabulate',   type=('build', 'run'), when='@1.1.0:')
    depends_on('py-filelock',   type=('build', 'run'), when='@1.1.0:')
