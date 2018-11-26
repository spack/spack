# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTornado(PythonPackage):
    """Tornado is a Python web framework and asynchronous networking
    library."""
    homepage = "https://github.com/tornadoweb/tornado"
    url      = "https://github.com/tornadoweb/tornado/archive/v4.4.0.tar.gz"

    version('4.4.0', 'c28675e944f364ee96dda3a8d2527a87ed28cfa3')

    depends_on('py-setuptools', type='build')

    # requirements from setup.py
    depends_on('py-backports-ssl-match-hostname', when='^python@:2.7.8', type=('build', 'run'))
    depends_on('py-singledispatch', when='^python@:3.3', type=('build', 'run'))
    depends_on('py-certifi', when='^python@:3.3', type=('build', 'run'))
    depends_on('py-backports-abc@0.4:', when='^python@:3.4', type=('build', 'run'))
