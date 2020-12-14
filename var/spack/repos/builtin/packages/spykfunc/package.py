##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack import *


class Spykfunc(PythonPackage):
    """Spykfunc - Spark functionalizer developed by Blue Brain Project, EPFL
    """
    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/building/Spykfunc"
    url      = "ssh://bbpcode.epfl.ch/building/Spykfunc"
    git      = "ssh://bbpcode.epfl.ch/building/Spykfunc"

    version('develop', submodules=True, get_full_repo=True)
    version('0.15.9', tag='v0.15.9', submodules=True, get_full_repo=True)
    version('0.15.7', tag='v0.15.7', submodules=True, get_full_repo=True)
    version('0.15.6', tag='v0.15.6', submodules=True, get_full_repo=True)
    version('0.15.3', tag='v0.15.3', submodules=True, get_full_repo=True)
    version('0.15.2', tag='v0.15.2', submodules=True, get_full_repo=True)
    version('0.15.1', tag='v0.15.1', submodules=True, get_full_repo=True)
    version('0.15.0', tag='v0.15.0', submodules=True, get_full_repo=True)
    # versions 0.13.2-0.14.x require legacy mvdtool+python
    version('0.13.1', tag='v0.13.1', submodules=True, get_full_repo=True)
    version('0.12.2', tag='v0.12.2', submodules=True, get_full_repo=True)

    depends_on('cmake', type='build', when='@0.15.4:')
    depends_on('boost', type=('build', 'link'), when='@0.15.4:')
    depends_on('morpho-kit', type=('build', 'link'), when='@0.15.4:')

    depends_on('py-mvdtool~mpi', type=('build', 'run'), when='@0.14.4:')

    depends_on('python@3.6:')
    depends_on('py-cython', type='run', when='@:0.15.3')
    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('spark+hadoop@3.0.0:', type='run')
    depends_on('hadoop@:2.999', type='run')

    depends_on('py-docopt', type=('build', 'run'))
    depends_on('py-future', type=('build', 'run'))
    depends_on('py-funcsigs', type=('build', 'run'))
    depends_on('py-h5py~mpi', type=('build', 'run'))
    depends_on('py-hdfs', type=('build', 'run'))
    depends_on('py-jprops', type=('build', 'run'))
    depends_on('py-lazy-property', type=('build', 'run'))
    depends_on('py-libsonata', type='run', when='@0.15.3:')
    depends_on('py-lxml', type=('build', 'run'))
    depends_on('py-morpho-kit', type=('build', 'run'), when='@0.14.4:')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-pandas', type=('build', 'run'))
    depends_on('py-progress', type=('build', 'run'))
    depends_on('py-pyarrow+parquet@0.15.1', type=('build', 'run'))
    depends_on('py-pyspark@3.0.0', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'), when='@0.15.7:')

    depends_on('py-bb5', type=('build', 'run'), when='@:0.15.6')
    depends_on('py-sparkmanager', type=('build', 'run'), when='@:0.15.6')

    patch('setup-spark3.patch', when='@:0.15.6 ^spark@3:')
    patch('properties-spark3.patch', when='@:0.15.6 ^spark@3:')

    def setup_build_environment(self, env):
        # This is a rather ugly setup to run spykfunc without having to
        # activate all python packages.
        env.set('BOOST_ROOT', self.spec['boost'].prefix)

    def setup_run_environment(self, env):
        env.set('JAVA_HOME', self.spec['java'].prefix)
        env.set('SPARK_HOME', self.spec['spark'].prefix)
        env.set('HADOOP_HOME', self.spec['hadoop'].prefix)

        if self.spec.satisfies('@:0.15.6'):
            env.prepend_path('PATH',
                             os.path.join(self.spec['py-bb5'].prefix, 'bin'))
            env.prepend_path('PATH',
                             os.path.join(self.spec['py-sparkmanager'].prefix,
                                          'bin'))
        env.prepend_path('PATH',
                         os.path.join(self.spec['spark'].prefix, 'bin'))
