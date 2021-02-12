# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gpdb(AutotoolsPackage):
    """
    Greenplum Database (GPDB) is an advanced, fully featured, open source
    data warehouse, based on PostgreSQL. It provides powerful and rapid
    analytics on petabyte scale data volumes. Uniquely geared toward big
    data analytics, Greenplum Database is powered by the world's most
    advanced cost-based query optimizer delivering high analytical query
    performance on large data volumes.
    """

    homepage = "https://github.com/greenplum-db/gpdb"
    url      = "https://github.com/greenplum-db/gpdb/archive/6.2.1.tar.gz"

    version('6.14.0', sha256='9fba6b4410d983ed060d59c069e48af3347565c50b191ca996b75cb9da8056d3')
    version('6.13.0', sha256='eef823cef85fa1bc92f4ecca9730513fe714ab742d1d51a14c5f50e791ad0380')
    version('6.12.1', sha256='560549b73f24bfd112a7e19b82c2091770861bb08c72d55ab0ff6f63da5c322f')
    version('6.12.0', sha256='ef98bff177a7eb38d521cde3ad41f3387a7121d65ec636c06f6ca7e10b6d5893')
    version('6.11.2', sha256='b6c2717718324906138569131e1e0a7ff12e37afc9c82d185981b25ef5cfeaff')
    version('6.11.1', sha256='970871ad06063417faf419a63b88f2e76b9dc60267fbc31401c5e8ccfe817e4c')
    version('6.2.1',     sha256='60c81d71665d623ea98a0e9bd8e6df7fecf6b30eb60a5881ccef781ff5214438')
    version('6.1.0',     sha256='81fa854b0ac5fe4e0de5fdee9a7b7c2514e1ea1feefa4e4d10518538a5c5b2a8')
    version('6.0.1',     sha256='8902f5d64386447f61c25686f283a785858760e0dcf9a049266db058d3597156')
    version('6.0.0',     sha256='8514140bee9db514d18a769034562e7f3464f74828595903a64dbf3d175ab71a')
    version('5.24.0',    sha256='4ea5cfcc20f149669bb3713378158e15b5c5949b367351a0f497ba1602d61fc1')
    version('5.23.0',    sha256='b06a797eb941362d5473b84d5def349b5ce12ce87ab116bea7c74ad193738ae9')

    depends_on('zstd')
    depends_on('py-setuptools@:44.99.99')
    depends_on('apr')
    depends_on('libevent')
    depends_on('curl')
    depends_on('xerces-c')
    depends_on('bison', type='build')
    depends_on('libxml2')
    depends_on('flex')
    depends_on('readline')
    depends_on('py-subprocess32', type=('build', 'run'))
    depends_on('python@:2.8.0', type=('build', 'run'))
    depends_on('py-lockfile', type=('build', 'run'))
    depends_on('py-psutil', type=('build', 'run'))
    depends_on('py-utils@:1.0.0', type=('build', 'run'))

    def configure_args(self):
        args = ['--with-python', '--disable-orca', '--enable-depend',
                '--with-libxml']
        return args

    def setup_run_environment(self, env):
        env.append_path('GPHOME', self.prefix)
        env.append_path('PYTHONPATH', self.prefix.lib.python)
