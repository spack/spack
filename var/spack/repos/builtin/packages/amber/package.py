# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Amber(Package, CudaPackage):
    """Amber is a suite of biomolecular simulation programs.

       Note: A manual download is required for Amber.
       Spack will search your current directory for the download file.
       Alternatively, add this file to a mirror so that Spack can find it.
       For instructions on how to set up a mirror, see
       http://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "http://ambermd.org/"
    url      = "file://{0}/Amber16.tar.bz2".format(os.getcwd())

    version('16', sha256='3b7ef281fd3c46282a51b6a6deed9ed174a1f6d468002649d84bfc8a2577ae5d')

    variant('mpi', description='Build MPI executables', default=True)

    resource(
        name='AmberTools',
        sha256='7b876afe566e9dd7eb6a5aa952a955649044360f15c1f5d4d91ba7f41f3105fa',
        url='file://{0}/AmberTools16.tar.bz2'.format(os.getcwd()),
        destination='.',
    )

    depends_on('mpi', when='+mpi')
    depends_on('cuda@7.5.18', when='+cuda')

    depends_on('netcdf-fortran')
    depends_on('python+tkinter@2.7:2.8', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-matplotlib@:2.9', type=('build', 'run'))
    depends_on('zlib')

    def setup_environment(self, spack_env, run_env):
        sp_dir = join_path(self.prefix, 'python2.7/site-packages')

        run_env.set('AMBERHOME', self.prefix)
        run_env.prepend_path('PYTHONPATH', sp_dir)

    def install(self, spec, prefix):
        # install AmberTools where it should be
        install_tree('amber16', '.')

        base_args = [
            '-noX11',
            '--no-updates',
            '--skip-python',
            '--with-netcdf', self.spec['netcdf-fortran'].prefix
        ]

        configure_env = {
            'AMBERHOME': self.stage.source_path,
            'CUDA_HOME': self.spec['cuda'].prefix,
        }

        conf = Executable('./configure')

        conf(*(base_args + ['gnu']), extra_env=configure_env)
        make('install', extra_env=configure_env)

        if '+mpi' in spec:
            conf(*(base_args + ['-mpi', 'gnu']), extra_env=configure_env)
            make('install', extra_env=configure_env)

        if '+cuda' in spec:
            conf(*(base_args + ['-cuda', 'gnu']), extra_env=configure_env)
            make('install', extra_env=configure_env)

        # just install everything that was built
        install_tree('.', prefix)
