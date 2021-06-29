# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Lorene(MakefilePackage):
    """LORENE: Langage Objet pour la RElativite NumeriquE

    LORENE is a set of C++ classes to solve various problems
    arising in numerical relativity, and more generally in
    computational astrophysics. It provides tools to solve
    partial differential equations by means of multi-domain
    spectral methods."""

    homepage = "https://lorene.obspm.fr/index.html"
    cvs      = ":pserver:anonymous:anonymous@octane.obspm.fr:/cvsroot%module=Lorene"

    maintainers = ['eschnett']

    version('2021.4.22', date='2021-04-22')

    variant('fftw', default=True,
            description='Use external FFTW for spectral transformations')
    variant('bin_star', default=True,
            description='Build Bin_star solver for binary neutron star systems')

    # Create a file `local_settings`. This is how Lorene is configured,
    # defining specifying compilers, paths, etc. We just point to the
    # respective Spack wrappers.
    patch('local_settings')

    depends_on('fftw @3:', when='+fftw')
    depends_on('gsl')
    depends_on('lapack')
    depends_on('pgplot')

    parallel = False

    def build(self, spec, prefix):
        args = ['HOME_LORENE=' + self.build_directory,
                'GSL_INCDIRS=' + spec['gsl'].prefix.include,
                'GSL_LIBDIRS=' + spec['gsl'].prefix.lib,
                'PGPLOT_INCDIRS=' + spec['pgplot'].prefix.include,
                'PGPLOT_LIBDIRS=' + spec['pgplot'].prefix.lib]
        if '+fftw' in spec:
            args.extend(['FFTW_INCDIRS=' + spec['fftw'].prefix.include,
                         'FFTW_LIBDIRS=' + spec['fftw'].prefix.lib])
        # (We could build the documentation as well.)
        # (We could circumvent the build system and simply compile all
        # source files, and do so in parallel.)
        make('cpp', 'fortran', 'export', *args)
        if '+Bin_star' in spec:
            with working_dir(join_path('Codes', 'Bin_star')):
                make('-f', 'Makefile_O2',
                     'coal', 'lit_bin', 'init_bin', 'coal_regu', 'init_bin_regu',
                     'analyse', 'prepare_seq',
                     *args)

    def install(self, spec, prefix):
        mkdirp(prefix.lib)
        install_tree('Lib', prefix.lib)
        mkdirp(prefix.bin)
        if '+Bin_star' in spec:
            install_tree(join_path('Codes', 'Bin_star'), prefix.bin)
