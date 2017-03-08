##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

from spack import *


class PlanckLikelihood(Package):
    """2015 Cosmic Microwave Background (CMB) spectra and likelihood code"""

    homepage = "https://wiki.cosmos.esa.int/planckpla2015/index.php/CMB_spectrum_%26_Likelihood_Code"
    url      = "http://irsa.ipac.caltech.edu/data/Planck/release_2/software/COM_Likelihood_Code-v2.0.R2.00.tar.bz2"

    version('2.00', '7a081679ff249dc4f94fb7177e16e818',
            url="http://irsa.ipac.caltech.edu/data/Planck/release_2/software/COM_Likelihood_Code-v2.0.R2.00.tar.bz2")

    variant('lensing-ext', default=False,
            description="Provide lensing-ext data")
    variant('plik-DS', default=False,
            description="Provide plik-DS data")
    variant('plik-HM-ext', default=False,
            description="Provide plik-HM-ext data")
    variant('plik-unbinned', default=False,
            description="Provide plik-unbinned data")

    patch('fortran.patch')
    patch('make.patch')

    resource(
        name='baseline',
        url="http://irsa.ipac.caltech.edu/data/Planck/release_2/software/COM_Likelihood_Data-baseline_R2.00.tar.gz",
        md5='7e784819cea65dbc290ea3619420295a',
        destination='.')
    resource(
        name='lensing-ext',
        url="http://irsa.ipac.caltech.edu/data/Planck/release_2/software/COM_Likelihood_Data-extra-lensing-ext.R2.00.tar.gz",
        md5='091736f73b47a09162050bee27d68399',
        destination='.',
        when='+lensing-ext')
    resource(
        name='plik-DS',
        url="http://irsa.ipac.caltech.edu/data/Planck/release_2/software/COM_Likelihood_Data-extra-plik-DS.R2.00.tar.gz",
        md5='76ac04f989025eecab3825aba7e41f36',
        destination='.',
        when='+plik-DS')
    resource(
        name='plik-HM-ext',
        url="http://irsa.ipac.caltech.edu/data/Planck/release_2/software/COM_Likelihood_Data-extra-plik-HM-ext.R2.00.tar.gz",
        md5='1c3bd8221f973b7bf7e76647451fd6e5',
        destination='.',
        when='+plik-HM-ext')
    resource(
        name='plik-unbinned',
        url="http://irsa.ipac.caltech.edu/data/Planck/release_2/software/COM_Likelihood_Data-extra-plik-unbinned.R2.00.tar.gz",
        md5='c5869aa6b6581b6863d2a6e0ffd3826c',
        destination='.',
        when='+plik-unbinned')

    depends_on('blas')
    depends_on('cfitsio +shared')
    depends_on('lapack')

    # Note: Could also install Python bindings

    parallel = False

    def install(self, spec, prefix):
        # Configure

        # Don't hide build commands
        filter_file("^\t@", "\t", "Makefile")

        makeflags = [
            'PREFIX=%s' % prefix,
            'COLORS=0',
            'CFITSIOPATH=%s' % spec['cfitsio'].prefix,
            'CC=cc',
            'FC=fc',
            'IFORTLIBPATH=',
            'IFORTRUNTIME=-lintlc -limf -lsvml -liomp5 -lifportmt -lifcoremt',
            'GFORTRANLIBPATH=',
            'GFORTRANRUNTIME=-lgfortran -lgomp',
            'LAPACKLIBPATH=',
            'LAPACK=%s' % (spec['lapack'].libs + spec['blas'].libs).ld_flags,
            'COPENMP=%s' % self.compiler.openmp_flag,
            'FOPENMP=%s' % self.compiler.openmp_flag,
        ]

        # Build
        make(*makeflags)

        # Install
        make('install', *makeflags)
        fix_darwin_install_name(prefix.lib)
        dirs = ['plc_2.0']
        if '+lensing-ext' in spec:
            dirs.append('lensing_ext')
        if '+plik-DS' in spec:
            dirs.append('plik_DS')
        if '+plik-HM-ext' in spec:
            dirs.append('plik_HM_ext')
        if '+plik-unbinned' in spec:
            dirs.append('plik_unbinned')
        for dir in dirs:
            install_tree(dir, join_path(prefix, 'share', 'clik', dir))

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        prefix = self.prefix
        spack_env.set('CLIK_PATH', prefix)
        spack_env.set('CLIK_DATA', join_path(prefix, 'share', 'clik'))
        spack_env.set('CLIK_PLUGIN', 'rel2015')

    def setup_environment(self, spack_env, run_env):
        prefix = self.prefix
        run_env.set('CLIK_PATH', prefix)
        run_env.set('CLIK_DATA', join_path(prefix, 'share', 'clik'))
        run_env.set('CLIK_PLUGIN', 'rel2015')

    @on_package_attributes(run_tests=True)
    @run_after('install')
    def check_install(self):
        prefix = self.prefix
        clik_example_C = Executable(join_path(prefix.bin, 'clik_example_C'))
        with working_dir('spack-check', create=True):
            clik_example_C(join_path(prefix, 'share', 'clik',
                                     'plc_2.0', 'hi_l', 'plik',
                                     'plik_dx11dr2_HM_v18_TT.clik'))
