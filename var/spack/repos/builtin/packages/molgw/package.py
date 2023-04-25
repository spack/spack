# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install molgw
#
# You can edit this file again by typing:
#
#     spack edit molgw
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *

class Molgw(Package):
    """A package for MolGW."""

    homepage = "https://github.com/bruneval/molgw"
    url      = "https://github.com/bruneval/molgw/archive/v3.1.tar.gz"

    version('3.1', sha256='9eb5eadf59d8715c46e9ee8f6eb94e65b7167b9012fc15013803aeafb8ec3a8c')

    depends_on('blas')
    depends_on('lapack')
    depends_on('libxc')
    depends_on('libcint+pypzpx+coulomb_erf')

    variant('openmp', default=False, description='Build with OpenMP support')
    #depends_on('llvm-openmp', when='+openmp')

    variant('scalapack', default=False, description='Build with ScaLAPACK support')
    depends_on('scalapack', when='+scalapack')
    depends_on('mpi', when='+scalapack')

    #variant('hdf5', default=False, description='Build with HDF5 support')
    #depends_on('hdf5', when='+hdf5')

    def install(self, spec, prefix):
        #configure_args = [
        #    '--prefix={0}'.format(prefix),
        #    '--with-blas={0}'.format(spec['blas'].libs.ld_flags),
        #    '--with-lapack={0}'.format(spec['lapack'].libs.ld_flags),
        #    '--with-libxc={0}'.format(spec['libxc'].prefix),
        #    '--with-libcint={0}'.format(spec['libcint'].prefix),
        #]

        if '+openmp' in spec:
            #configure_args.append('--with-openmp={0}'.format(spec['llvm-openmp'].prefix))
            flags['FFLAGS'] = self.compiler.openmp_flag + flags['FFLAGS']

        if '+scalapack' in spec:
            #configure_args.append('--with-scalapack={0}'.format(spec['scalapack'].prefix))
            flags['CPPFLAGS'] = '-DHAVE_SCALAPACK -DHAVE_MPI' + flags.get('CPPFLAGS', '')

        if '^intel-mkl' in spec:
            flags['CPPFLAGS'] = '-DHAVE_MKL' + flags.get('CPPFLAGS', '')

        #if '+hdf5' in spec:
        #    configure_args.append('--with-hdf5={0}'.format(spec['hdf5'].prefix))

        #configure(*configure_args)
        make()
        #make('install')

