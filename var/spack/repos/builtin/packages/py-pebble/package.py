# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPebble(PythonPackage):
    """Python API to manage threads and processes within an application."""

    homepage = "https://github.com/noxdafox/pebble"
    url = "https://pypi.io/packages/source/p/pebble/Pebble-4.5.0.tar.gz"
    git = "https://github.com/noxdafox/pebble.git"

    version('4.5.0', sha256='2de3cd11aa068e0c4a4abbaf8d4ecfdac409d8bfb78a4c211a01f6a4fb17a35f')
    version('4.4.1', sha256='7c4d68a3479140cba74d7454d8190e2cb1a93213b44b5befe3c53c201beb8317')
    version('4.3.10', sha256='c39a7bf99af6525fcf0783a8859fb10a4f20f4f988ddb66fd6fa7588f9c91731')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-futures', type='run', when='^python@:2.9.9')
