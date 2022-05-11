# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class Scons(PythonPackage):
    """SCons is a software construction tool"""

    homepage = "https://scons.org"
    pypi = "SCons/SCons-4.3.0.tar.gz"

    tags = ['build-tools']

    version('4.3.0', sha256='d47081587e3675cc168f1f54f0d74a69b328a2fc90ec4feb85f728677419b879')
    version('4.2.0', sha256='691893b63f38ad14295f5104661d55cb738ec6514421c6261323351c25432b0a')
    version('4.1.0.post1', sha256='ecb062482b9d80319b56758c0341eb717735437f86a575bac3552804428bd73e')
    version('4.0.1', sha256='722ed104b5c624ecdc89bd4e02b094d2b14d99d47b5d0501961e47f579a2007c')
    version('4.0.0', sha256='de8599189ee87bb84234e3d6e30bef0298d6364713979856927576b252c411f3')
    version('3.1.2', sha256='8aaa483c303efeb678e6f7c776c8444a482f8ddc3ad891f8b6cdd35264da9a1f')
    version('3.1.1', sha256='fd44f8f2a4562e7e5bc8c63c82b01e469e8115805a3e9c2923ee54cdcd6678b3')
    version('3.1.0', sha256='94e0d0684772d3e6d9368785296716e0ed6ce757270b3ed814e5aa72d3163890')
    version('3.0.5', sha256='e95eaae17d9e490cf12cd37f091a6cbee8a628b5c8dbd3cab1f348f602f46462')
    version('3.0.4', sha256='72c0b56db84f40d3558f351918a0ab98cb4345e8696e879d3e271f4df4a5913c')
    version('3.0.1', sha256='24475e38d39c19683bc88054524df018fe6949d70fbd4c69e298d39a0269f173')
    version('2.5.1', sha256='c8de85fc02ed1a687b1f2ac791eaa0c1707b4382a204f17d782b5b111b9fdf07')
    version('2.5.0', sha256='01f1b3d6023516a8e1b5e77799e5a82a23b32953b1102d339059ffeca8600493')

    # Python 3 support was added in SCons 3.0.0
    depends_on('python@:2', when='@:2', type=('build', 'run'))
    # Python 2 support was dropped in SCons 4.0.0
    depends_on('python@3.5:', when='@4:4.2.0')
    # Python 3.5 support was dropped in SCons 4.3.0
    depends_on('python@3.6:', when='@4.3.0:')
    depends_on('py-setuptools', type=('build', 'run'))

    patch('fjcompiler.patch', when='%fj')
    patch('py3-hashbang.patch', when='@:3^python@3:')  # not needed for @4.0.0:

    def url_for_version(self, version):
        url = 'https://files.pythonhosted.org/packages/source/{0}/{1}/{1}-{2}.tar.gz'
        if version >= Version('4.0.0'):
            name = 'SCons'
        else:
            name = 'scons'
        return url.format(name[0], name, version)

    def setup_run_environment(self, env):
        env.prepend_path('PYTHONPATH', self.prefix.lib.scons)

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.prepend_path('PYTHONPATH', self.prefix.lib.scons)

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.prepend_path('PYTHONPATH', self.prefix.lib.scons)
