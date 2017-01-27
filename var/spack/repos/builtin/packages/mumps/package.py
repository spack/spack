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
import os
import sys
import glob


class Mumps(Package):
    """MUMPS: a MUltifrontal Massively Parallel sparse direct Solver"""

    homepage = "http://mumps.enseeiht.fr"
    url      = "http://mumps.enseeiht.fr/MUMPS_5.0.1.tar.gz"

    version('5.0.2', '591bcb2c205dcb0283872608cdf04927')
    # Alternate location if main server is down.
    # version('5.0.1', 'b477573fdcc87babe861f62316833db0', url='http://pkgs.fedoraproject.org/repo/pkgs/MUMPS/MUMPS_5.0.1.tar.gz/md5/b477573fdcc87babe861f62316833db0/MUMPS_5.0.1.tar.gz')
    version('5.0.1', 'b477573fdcc87babe861f62316833db0')

    variant('mpi', default=True,
            description='Compile MUMPS with MPI support')
    variant('scotch', default=False,
            description='Activate Scotch as a possible ordering library')
    variant('ptscotch', default=False,
            description='Activate PT-Scotch as a possible ordering library')
    variant('metis', default=False,
            description='Activate Metis as a possible ordering library')
    variant('parmetis', default=False,
            description='Activate Parmetis as a possible ordering library')
    variant('double', default=True,
            description='Activate the compilation of dmumps')
    variant('float', default=True,
            description='Activate the compilation of smumps')
    variant('complex', default=True,
            description='Activate the compilation of cmumps and/or zmumps')
    variant('int64', default=False,
            description='Use int64_t/integer*8 as default index type')
    variant('shared', default=True, description='Build shared libraries')

    depends_on('scotch + esmumps', when='~ptscotch+scotch')
    depends_on('scotch + esmumps + mpi', when='+ptscotch')
    depends_on('metis@5:', when='+metis')
    depends_on('parmetis', when="+parmetis")
    depends_on('blas')
    depends_on('lapack')
    depends_on('scalapack', when='+mpi')
    depends_on('mpi', when='+mpi')

    # this function is not a patch function because in case scalapack
    # is needed it uses self.spec['scalapack'].fc_link set by the
    # setup_dependent_environment in scalapck. This happen after patch
    # end before install
    # def patch(self):
    def write_makefile_inc(self):
        if ('+parmetis' in self.spec or '+ptscotch' in self.spec) and (
                '+mpi' not in self.spec):
            raise RuntimeError(
                'You cannot use the variants parmetis or ptscotch without mpi')

        lapack_blas = (self.spec['lapack'].lapack_libs +
                       self.spec['blas'].blas_libs)
        makefile_conf = ["LIBBLAS = %s" % lapack_blas.ld_flags]

        orderings = ['-Dpord']

        if '+ptscotch' in self.spec or '+scotch' in self.spec:
            join_lib = ' -l%s' % ('pt' if '+ptscotch' in self.spec else '')
            makefile_conf.extend([
                "ISCOTCH = -I%s" % self.spec['scotch'].prefix.include,
                "LSCOTCH = -L%s %s%s" % (self.spec['scotch'].prefix.lib,
                                         join_lib,
                                         join_lib.join(['esmumps',
                                                        'scotch',
                                                        'scotcherr']))
            ])

            orderings.append('-Dscotch')
            if '+ptscotch' in self.spec:
                orderings.append('-Dptscotch')

        if '+parmetis' in self.spec and '+metis' in self.spec:
            makefile_conf.extend([
                "IMETIS = -I%s" % self.spec['parmetis'].prefix.include,
                "LMETIS = -L%s -l%s -L%s -l%s" % (
                    self.spec['parmetis'].prefix.lib, 'parmetis',
                    self.spec['metis'].prefix.lib, 'metis')
            ])

            orderings.append('-Dparmetis')
        elif '+metis' in self.spec:
            makefile_conf.extend([
                "IMETIS = -I%s" % self.spec['metis'].prefix.include,
                "LMETIS = -L%s -l%s" % (self.spec['metis'].prefix.lib, 'metis')
            ])

            orderings.append('-Dmetis')

        makefile_conf.append("ORDERINGSF = %s" % (' '.join(orderings)))

        # when building shared libs need -fPIC, otherwise
        # /usr/bin/ld: graph.o: relocation R_X86_64_32 against `.rodata.str1.1'
        # can not be used when making a shared object; recompile with -fPIC
        fpic = '-fPIC' if '+shared' in self.spec else ''
        # TODO: test this part, it needs a full blas, scalapack and
        # partitionning environment with 64bit integers
        if '+int64' in self.spec:
            makefile_conf.extend(
                # the fortran compilation flags most probably are
                # working only for intel and gnu compilers this is
                # perhaps something the compiler should provide
                ['OPTF    = %s -O  -DALLOW_NON_INIT %s' % (fpic, '-fdefault-integer-8' if self.compiler.name == "gcc" else '-i8'),  # noqa
                 'OPTL    = %s -O ' % fpic,
                 'OPTC    = %s -O -DINTSIZE64' % fpic])
        else:
            makefile_conf.extend(
                ['OPTF    = %s -O  -DALLOW_NON_INIT' % fpic,
                 'OPTL    = %s -O ' % fpic,
                 'OPTC    = %s -O ' % fpic])

        if '+mpi' in self.spec:
            scalapack = self.spec['scalapack'].scalapack_libs
            makefile_conf.extend(
                ["CC = %s" % join_path(self.spec['mpi'].prefix.bin, 'mpicc'),
                 "FC = %s" % join_path(self.spec['mpi'].prefix.bin, 'mpif90'),
                 "FL = %s" % join_path(self.spec['mpi'].prefix.bin, 'mpif90'),
                 "SCALAP = %s" % scalapack.ld_flags,
                 "MUMPS_TYPE = par"])
        else:
            makefile_conf.extend(
                ["CC = cc",
                 "FC = fc",
                 "FL = fc",
                 "MUMPS_TYPE = seq"])

        # TODO: change the value to the correct one according to the
        # compiler possible values are -DAdd_, -DAdd__ and/or -DUPPER
        if self.compiler.name == 'intel':
            # Intel Fortran compiler provides the main() function so
            # C examples linked with the Fortran compiler require a
            # hack defined by _DMAIN_COMP (see examples/c_example.c)
            makefile_conf.append("CDEFS   = -DAdd_ -DMAIN_COMP")
        else:
            makefile_conf.append("CDEFS   = -DAdd_")

        if '+shared' in self.spec:
            if sys.platform == 'darwin':
                # Building dylibs with mpif90 causes segfaults on 10.8 and
                # 10.10. Use gfortran. (Homebrew)
                makefile_conf.extend([
                    'LIBEXT=.dylib',
                    'AR=%s -dynamiclib -Wl,-install_name -Wl,%s/$(notdir $@) -undefined dynamic_lookup -o ' % (os.environ['FC'], prefix.lib),  # noqa
                    'RANLIB=echo'
                ])
            else:
                makefile_conf.extend([
                    'LIBEXT=.so',
                    'AR=$(FL) -shared -Wl,-soname -Wl,%s/$(notdir $@) -o' % prefix.lib,  # noqa
                    'RANLIB=echo'
                ])
        else:
            makefile_conf.extend([
                'LIBEXT  = .a',
                'AR = ar vr',
                'RANLIB = ranlib'
            ])

        makefile_inc_template = join_path(
            os.path.dirname(self.module.__file__), 'Makefile.inc')
        with open(makefile_inc_template, "r") as fh:
            makefile_conf.extend(fh.read().split('\n'))

        with working_dir('.'):
            with open("Makefile.inc", "w") as fh:
                makefile_inc = '\n'.join(makefile_conf)
                fh.write(makefile_inc)

    def install(self, spec, prefix):
        make_libs = []

        # the choice to compile ?examples is to have kind of a sanity
        # check on the libraries generated.
        if '+float' in spec:
            make_libs.append('sexamples')
            if '+complex' in spec:
                make_libs.append('cexamples')

        if '+double' in spec:
            make_libs.append('dexamples')
            if '+complex' in spec:
                make_libs.append('zexamples')

        self.write_makefile_inc()

        # Build fails in parallel
        make(*make_libs, parallel=False)

        install_tree('lib', prefix.lib)
        install_tree('include', prefix.include)

        if '~mpi' in spec:
            lib_dsuffix = '.dylib' if sys.platform == 'darwin' else '.so'
            lib_suffix = lib_dsuffix if '+shared' in spec else '.a'
            install('libseq/libmpiseq%s' % lib_suffix, prefix.lib)
            for f in glob.glob(join_path('libseq', '*.h')):
                install(f, prefix.include)

        # FIXME: extend the tests to mpirun -np 2 when build with MPI
        # FIXME: use something like numdiff to compare output files
        with working_dir('examples'):
            if '+float' in spec:
                os.system('./ssimpletest < input_simpletest_real')
                if '+complex' in spec:
                    os.system('./csimpletest < input_simpletest_real')
            if '+double' in spec:
                os.system('./dsimpletest < input_simpletest_real')
                if '+complex' in spec:
                    os.system('./zsimpletest < input_simpletest_cmplx')
