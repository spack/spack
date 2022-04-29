# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
#
# Important feature: a version of salome-medcoupling depand on
# a specific version of salome-med package

from spack.pkgkit import *


class SalomeMedcoupling(CMakePackage):
    """salome-medcoupling is a part of SALOME platform to manipulate meshes and
    fields in memory, and use salome-med format for files."""

    maintainers = ['franciskloss']

    homepage = "https://docs.salome-platform.org/latest/dev/MEDCoupling/developer/index.html"
    git      = "https://git.salome-platform.org/gitpub/tools/medcoupling.git"

    version('9.7.0', tag='V9_7_0')
    version('9.6.0', tag='V9_6_0')
    version('9.5.0', tag='V9_5_0')
    version('9.4.0', tag='V9_4_0')
    version('9.3.0', tag='V9_3_0')

    variant('static',      default=False, description='Enable static library build')
    variant('mpi',         default=False, description='Enable MPI')
    variant('in64',        default=False, description='Enable 64 bits indexes')
    variant('partitioner', default=False, description='Enable partitioner')
    variant('metis',       default=False, description='Enable Metis')
    variant('scotch',      default=False, description='Enable Scotch')

    depends_on('libxml2@2.9.1:')
    depends_on('libtirpc')
    depends_on('cppunit')
    depends_on('python@3.6.5:')
    depends_on('py-scipy@0.19.1:', type=('build', 'run'))
    depends_on('py-numpy@1.15.1:', type=('build', 'run'))
    depends_on('boost+python+numpy@1.58.0:')
    depends_on('swig@3.0.12:', type='build')

    depends_on('metis@5.1.0:',  when='+metis')
    depends_on('scotch@6.0.4:', when='+scotch')
    depends_on('mpi',           when='+mpi')

    depends_on('salome-configuration@9.7.0',  when='@9.7.0')
    depends_on('salome-med@4.1.0+mpi+static', when='@9.7.0+mpi+static')
    depends_on('salome-med@4.1.0+mpi',        when='@9.7.0+mpi')
    depends_on('salome-med@4.1.0+static',     when='@9.7.0~mpi+static')
    depends_on('salome-med@4.1.0',            when='@9.7.0~mpi')

    depends_on('salome-configuration@9.6.0',  when='@9.6.0')
    depends_on('salome-med@4.1.0+mpi+static', when='@9.6.0+mpi+static')
    depends_on('salome-med@4.1.0+mpi',        when='@9.6.0+mpi')
    depends_on('salome-med@4.1.0+static',     when='@9.6.0~mpi+static')
    depends_on('salome-med@4.1.0',            when='@9.6.0~mpi')

    depends_on('salome-configuration@9.5.0',  when='@9.5.0')
    depends_on('salome-med@4.1.0+mpi+static', when='@9.5.0+mpi+static')
    depends_on('salome-med@4.1.0+mpi',        when='@9.5.0+mpi')
    depends_on('salome-med@4.1.0+static',     when='@9.5.0~mpi+static')
    depends_on('salome-med@4.1.0',            when='@9.5.0~mpi')

    depends_on('salome-configuration@9.4.0',  when='@9.4.0')
    depends_on('salome-med@4.0.0+mpi+static', when='@9.4.0+mpi+static')
    depends_on('salome-med@4.0.0+mpi',        when='@9.4.0+mpi')
    depends_on('salome-med@4.0.0+static',     when='@9.4.0~mpi+static')
    depends_on('salome-med@4.0.0',            when='@9.4.0~mpi')

    depends_on('salome-configuration@9.3.0',  when='@9.3.0')
    depends_on('salome-med@4.0.0+mpi+static', when='@9.3.0+mpi+static')
    depends_on('salome-med@4.0.0+mpi',        when='@9.3.0+mpi')
    depends_on('salome-med@4.0.0+static',     when='@9.3.0~mpi+static')
    depends_on('salome-med@4.0.0',            when='@9.3.0~mpi')

    def check(self):
        pass

    def setup_build_environment(self, env):
        if '+metis' in self.spec:
            env.set('METIS_ROOT_DIR', self.spec['metis'].prefix)

        if '+scotch' in self.spec:
            env.set('SCOTCH_ROOT_DIR', self.spec['scotch'].prefix)

    def setup_run_environment(self, env):
        env.prepend_path(
            'PYTHONPATH',
            join_path(
                self.prefix.lib,
                'python{0}'.format(self.spec['python'].version.up_to(2)),
                'site-packages'))

    def cmake_args(self):
        spec    = self.spec
        options = []

        if '+static' in spec:
            options.extend(['-DMEDCOUPLING_BUILD_STATIC=ON'])
        else:
            options.extend(['-DMEDCOUPLING_BUILD_STATIC=OFF'])

        if '+mpi' in spec:
            options.extend([
                '-DMEDCOUPLING_USE_MPI=ON',
                '-DSALOME_USE_MPI=ON'])
        else:
            options.extend([
                '-DMEDCOUPLING_USE_MPI=OFF',
                '-DSALOME_USE_MPI=OFF'])

        if '+in64' in spec:
            options.extend(['-DMEDCOUPLING_USE_64BIT_IDS=ON'])
        else:
            options.extend(['-DMEDCOUPLING_USE_64BIT_IDS=OFF'])

        if '+partitioner' in spec:
            options.extend(['-DMEDCOUPLING_ENABLE_PARTITIONER=ON'])
        else:
            options.extend(['-DMEDCOUPLING_ENABLE_PARTITIONER=OFF'])

        if '+metis' in spec:
            options.extend(['-DMEDCOUPLING_ENABLE_PARTITIONER=ON'])
            options.extend(['-DMEDCOUPLING_PARTITIONER_METIS=ON'])
        else:
            options.extend(['-DMEDCOUPLING_PARTITIONER_METIS=OFF'])

        if '+scotch' in spec:
            options.extend(['-DMEDCOUPLING_ENABLE_PARTITIONER=ON'])
            options.extend(['-DMEDCOUPLING_PARTITIONER_SCOTCH=ON'])
        else:
            options.extend(['-DMEDCOUPLING_PARTITIONER_SCOTCH=OFF'])

        options.extend([
            '-DMEDCOUPLING_BUILD_DOC=OFF',
            '-DMEDCOUPLING_ENABLE_PYTHON=ON',
            '-DMEDCOUPLING_ENABLE_RENUMBER=OFF',
            '-DMEDCOUPLING_PARTITIONER_PARMETIS=OFF',
            '-DMEDCOUPLING_PARTITIONER_PTSCOTCH=OFF',
            '-DMEDCOUPLING_MICROMED=OFF',
            '-DMEDCOUPLING_BUILD_TESTS=OFF'])

        return options
