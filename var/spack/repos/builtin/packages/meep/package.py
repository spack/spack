# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Meep(AutotoolsPackage):
    """Meep (or MEEP) is a free finite-difference time-domain (FDTD) simulation
    software package developed at MIT to model electromagnetic systems."""

    homepage = "http://ab-initio.mit.edu/wiki/index.php/Meep"
    git      = "https://github.com/NanoComp/meep.git"
    url      = "https://github.com/NanoComp/meep/archive/refs/tags/v1.21.0.tar.gz"

    version('master', branch='master')

    version('1.21.0', sha256='71911cd2f38b15bdafe9a27ad111f706f24717894d5f9b6f9f19c6c10a0d5896')
    version('1.3',   sha256='564c1ff1b413a3487cf81048a45deabfdac4243a1a37ce743f4fcf0c055fd438',
            url='http://ab-initio.mit.edu/meep/meep-1.3.tar.gz')
    version('1.2.1', sha256='f1f0683e5688d231f7dd1863939677148fc27a6744c03510e030c85d6c518ea5',
            url='http://ab-initio.mit.edu/meep/meep-1.2.1.tar.gz')
    version('1.1.1', sha256='7a97b5555da1f9ea2ec6eed5c45bd97bcd6ddbd54bdfc181f46c696dffc169f2',
            url='http://ab-initio.mit.edu/meep/old/meep-1.1.1.tar.gz')

    variant('blas',    default=True,  description='Enable BLAS support')
    variant('lapack',  default=True,  description='Enable LAPACK support')
    variant('harminv', default=True,  description='Enable Harminv support')
    variant('guile',   default=True,  description='Enable Guilde support')
    variant('libctl',  default=True,  description='Enable libctl support')
    variant('mpi',     default=True,  description='Enable MPI support')
    variant('hdf5',    default=True,  description='Enable HDF5 support')
    variant('gsl',     default=True,  description='Enable GSL support')
    variant('python',  default=True,  description='Enable Python support')
    variant('single',  default=False, description='Enable Single Precision')

    depends_on('autoconf', type='build', when='@1.21.0')
    depends_on('automake', type='build', when='@1.21.0')
    depends_on('libtool', type='build', when='@1.21.0')

    depends_on('blas',        when='+blas')
    depends_on('lapack',      when='+lapack')
    depends_on('harminv',     when='+harminv')
    depends_on('guile@:2',    when='@:1.4+guile')
    depends_on('guile@2:',    when='@1.4:+guile')
    depends_on('libctl@3.2',  when='@:1.3+libctl')
    depends_on('libctl@4:',   when='+libctl')
    depends_on('mpi',         when='+mpi')
    depends_on('hdf5~mpi',    when='+hdf5~mpi')
    depends_on('hdf5+mpi',    when='+hdf5+mpi')
    depends_on('gsl',         when='+gsl')
    with when('+python'):
        depends_on('python')
        depends_on('py-numpy')
        depends_on('swig')
        depends_on('py-mpi4py', when='+mpi')

    def configure_args(self):
        spec = self.spec

        config_args = [
            '--enable-shared'
        ]

        if '+blas' in spec:
            config_args.append('--with-blas={0}'.format(
                spec['blas'].prefix.lib))
        else:
            config_args.append('--without-blas')

        if '+lapack' in spec:
            config_args.append('--with-lapack={0}'.format(
                spec['lapack'].prefix.lib))
        else:
            config_args.append('--without-lapack')

        if '+libctl' in spec:
            config_args.append('--with-libctl={0}'.format(
                join_path(spec['libctl'].prefix.share, 'libctl')))
        else:
            config_args.append('--without-libctl')

        if '+mpi' in spec:
            config_args.append('--with-mpi')
        else:
            config_args.append('--without-mpi')

        if '+hdf5' in spec:
            config_args.append('--with-hdf5')
        else:
            config_args.append('--without-hdf5')

        if '+python' in spec:
            config_args.append('--with-python')
        else:
            config_args.append('--without-python')
            config_args.append('--without-scheme')

        if '+single' in spec:
            config_args.append('--enable-single')

        if spec.satisfies('@1.21.0:'):
            config_args.append('--enable-maintainer-mode')

        return config_args

    def check(self):
        spec = self.spec

        # aniso_disp test fails unless installed with harminv
        # near2far test fails unless installed with gsl
        if '+harminv' in spec and '+gsl' in spec:
            # Most tests fail when run in parallel
            # 2D_convergence tests still fails to converge for unknown reasons
            make('check', parallel=False)
