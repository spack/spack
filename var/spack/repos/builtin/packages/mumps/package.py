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
import subprocess


class Mumps(Package):
    """MUMPS: a MUltifrontal Massively Parallel sparse direct Solver"""

    homepage = "http://mumps.enseeiht.fr"
    url      = "http://mumps.enseeiht.fr/MUMPS_5.0.1.tar.gz"

    version('5.0.1', 'b477573fdcc87babe861f62316833db0')

    variant('mpi', default=True, description='Activate the compilation of MUMPS with the MPI support')
    variant('scotch', default=False, description='Activate Scotch as a possible ordering library')
    variant('ptscotch', default=False, description='Activate PT-Scotch as a possible ordering library')
    variant('metis', default=False, description='Activate Metis as a possible ordering library')
    variant('parmetis', default=False, description='Activate Parmetis as a possible ordering library')
    variant('double', default=True, description='Activate the compilation of dmumps')
    variant('float', default=True, description='Activate the compilation of smumps')
    variant('complex', default=True, description='Activate the compilation of cmumps and/or zmumps')
    variant('idx64', default=False, description='Use int64_t/integer*8 as default index type')
    variant('shared', default=True, description='Build shared libraries')

    depends_on('scotch + esmumps', when='~ptscotch+scotch')
    depends_on('scotch + esmumps + mpi', when='+ptscotch')
    depends_on('metis@5:', when='+metis')
    depends_on('parmetis', when="+parmetis")
    depends_on('blas')
    depends_on('lapack')
    depends_on('scalapack', when='+mpi')
    depends_on('mpi', when='+mpi')

    patch('mumps-shared.patch', when='+shared')

    # this function is not a patch function because in case scalapack
    # is needed it uses self.spec['scalapack'].fc_link set by the
    # setup_dependent_environment in scalapck. This happen after patch
    # end before install
    # def patch(self):
    def write_makefile_inc(self):
        if (('+parmetis' in self.spec or
             '+ptscotch' in self.spec)) and '+mpi' not in self.spec:
            raise RuntimeError('You cannot use the variants parmetis or ptscotch without mpi')  # NOQA: E501

        makefile_conf = [
            "LIBBLAS = -L%s -lblas" % self.spec['blas'].prefix.lib
        ]

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
                "LMETIS = -L%s -l%s" % (self.spec['metis'].prefix.lib,
                                        'metis')
            ])

            orderings.append('-Dmetis')

        makefile_conf.append("ORDERINGSF = %s" % (' '.join(orderings)))

        # when building shared libs need -fPIC, otherwise /usr/bin/ld:
        # graph.o: relocation R_X86_64_32 against `.rodata.str1.1' can
        # not be used when making a shared object; recompile with
        # -fPIC
        fpic = '-fPIC' if '+shared' in self.spec else ''

        # TODO: test this part, it needs a full blas, scalapack and
        # partitionning environment with 64bit integers
        if '+idx64' in self.spec:
            makefile_conf.extend(
                # the fortran compilation flags most probably are
                # working only for intel and gnu compilers this is
                # perhaps something the compiler should provide
                ['OPTF    = %s -O  -DALLOW_NON_INIT %s' % (fpic, '-fdefault-integer-8' if self.compiler.name == "gcc" else '-i8'),  # NOQA: E501
                 'OPTL    = %s -O ' % fpic,
                 'OPTC    = %s -O -DINTSIZE64' % fpic])
        else:
            makefile_conf.extend(
                ['OPTF    = %s -O  -DALLOW_NON_INIT' % fpic,
                 'OPTL    = %s -O ' % fpic,
                 'OPTC    = %s -O ' % fpic])

        if '+mpi' in self.spec:
            makefile_conf.extend(
                ["CC = %s" % self.spec['mpi'].mpicc,
                 "FC = %s" % self.spec['mpi'].mpif90,
                 "SCALAP = %s" % self.spec['scalapack'].fc_link,
                 "MUMPS_TYPE = par"])
        else:
            makefile_conf.extend(
                ["CC = cc",
                 "FC = fc",
                 "MUMPS_TYPE = seq"])

        # TODO: change the value to the correct one according to the
        # compiler possible values are -DAdd_, -DAdd__ and/or -DUPPER
        makefile_conf.extend([
            'CDEFS   = -DAdd_',
            'FL = $(FC)',
        ])

        if '+shared' in self.spec:
            makefile_conf.append('SHLIBEXT = .%s' % dso_suffix)
            if sys.platform == 'darwin':
                makefile_conf.append(
                    'LDFLAGS = -dynamiclib -Wl,-install_name -Wl,{0}/$(notdir $@) {1}{0} -undefined dynamic_lookup'.format(prefix.lib, self.compiler.fc_rpath_arg)  # NOQA: E501
                )
            else:
                makefile_conf.append(
                    'LDFLAGS = -shared {0}{1}'.format(
                        self.compiler.fc_rpath_arg,
                        prefix.lib)
                )

        makefile_conf.extend([
            'LIBEXT  = .a',
            'AR = ar vr ',
            'RANLIB = ranlib'
        ])

        makefile_inc_template = \
            join_path(os.path.dirname(self.module.__file__),
                      'Makefile.inc')
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
            make_libs.append('s')
            if '+complex' in spec:
                make_libs.append('c')

        if '+double' in spec:
            make_libs.append('d')
            if '+complex' in spec:
                make_libs.append('z')

        self.write_makefile_inc()

        make('mumps_lib', parallel=False)
        make(*make_libs)

        install_tree('lib', prefix.lib)
        install_tree('include', prefix.include)

        if '~mpi' in spec:
            install('libseq/libmpiseq.a', prefix.lib)
            if '+shared' in spec:
                install('libseq/libmpiseq.{0}'.format(dso_suffix), prefix.lib)
            install('libseq/mpi.h', prefix.include)
            install('libseq/mpif.h', prefix.include)

        # FIXME: extend the tests to mpirun -np 2 (or alike) when
        # build with MPI
        # FIXME: use something like numdiff to compare blessed output
        # with the current
        # TODO: test the installed mumps and not the one in stage
        for t in make_libs:
            make('{0}examples'.format(t))

        with working_dir('examples'):
            for t in make_libs:
                input_file = 'input_simpletest_{0}'.format(
                    'real' if t in ['s', 'd'] else 'cmplx')
                with open(input_file) as input:
                    test = './{0}simpletest'.format(t)
                    ret = subprocess.call(test,
                                          stdin=input)
                    if ret is not 0:
                        raise RuntimeError(
                            'The test {0} did not pass'.format(test))
