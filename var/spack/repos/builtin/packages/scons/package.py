# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Scons(PythonPackage):
    """SCons is a software construction tool"""

    homepage = "http://scons.org"
    url      = "https://pypi.io/packages/source/s/scons/scons-3.0.1.tar.gz"

    version('3.1.0', sha256='94e0d0684772d3e6d9368785296716e0ed6ce757270b3ed814e5aa72d3163890')
    version('3.0.5', sha256='e95eaae17d9e490cf12cd37f091a6cbee8a628b5c8dbd3cab1f348f602f46462')
    version('3.0.4', sha256='72c0b56db84f40d3558f351918a0ab98cb4345e8696e879d3e271f4df4a5913c')
    version('3.0.1', 'b6a292e251b34b82c203b56cfa3968b3')
    version('2.5.1', '3eac81e5e8206304a9b4683c57665aa4')
    version('2.5.0', 'bda5530a70a41a7831d83c8b191c021e')

    # Python 3 support was added in SCons 3.0.0
    depends_on('python@:2', when='@:2', type=('build', 'run'))
    depends_on('py-setuptools', when='@3.0.2:', type='build')

    # Prevent passing --single-version-externally-managed to
    # setup.py, which it does not support.
    @when('@3.0.2:')
    def install_args(self, spec, prefix):
        return ['--prefix={0}'.format(prefix), '--root=/']
