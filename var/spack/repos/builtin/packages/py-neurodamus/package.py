# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class PyNeurodamus(PythonPackage):
    """The BBP simulation control suite, Python API
    """

    homepage = "https://bbpteam.epfl.ch/project/spaces/display/BGLIB/Neurodamus"
    git      = "ssh://bbpcode.epfl.ch/sim/neurodamus-py"

    version('develop', branch='master')
    version('2.8.1', commit='6b66cba')
    version('2.8.0',   tag='2.8.0')
    version('2.7.1',   tag='2.7.1')
    version('2.7.0',   tag='2.7.0')
    version('2.6.0',   tag='2.6.0')
    version('2.5.3',   tag='2.5.3')
    version('2.5.0',   tag='2.5.0')
    version('2.4.0',   tag='2.4.0')
    version('2.3.1',   tag='2.3.1')
    version('1.3.2',   tag='1.3.2')

    variant("all_deps",
            default=False,
            description="Add more dependencies to support advanced use cases")

    # Note: we depend on Neurodamus but let the user decide which one.
    # Note: avoid Neuron dependency due to issues with Intel and GCC conflicts.
    depends_on('python@3.4:',      type=('build', 'run'))
    depends_on('py-setuptools',    type=('build', 'run'))
    depends_on('py-h5py',          type='run')
    depends_on('py-numpy',         type='run')
    depends_on('py-docopt',        type='run')
    depends_on('py-libsonata',     type='run', when='@2.5.3:')
    depends_on('py-morphio',       type='run', when='@2.6.0:')
    depends_on('py-scipy',         type='run', when='+all_deps@2.5.3:')

    @run_after('install')
    def install_scripts(self):
        mkdirp(self.prefix.share)
        for script in ('init.py', '_debug.py'):
            copy(script, self.prefix.share)

    def setup_run_environment(self, env):
        PythonPackage.setup_run_environment(self, env)
        env.set('NEURODAMUS_PYTHON', self.prefix.share)
