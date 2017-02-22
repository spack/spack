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
import os
from spack import *


class Scotch(Package):
    """Scotch is a software package for graph and mesh/hypergraph
       partitioning, graph clustering, and sparse matrix ordering."""

    homepage = "http://www.labri.fr/perso/pelegrin/scotch/"
    url = "http://gforge.inria.fr/frs/download.php/latestfile/298/scotch_6.0.3.tar.gz"
    base_url = "http://gforge.inria.fr/frs/download.php/latestfile/298"
    list_url = "http://gforge.inria.fr/frs/?group_id=248"

    version('6.0.4', 'd58b825eb95e1db77efe8c6ff42d329f')
    version('6.0.3', '10b0cc0f184de2de99859eafaca83cfc')
    version('6.0.0', 'c50d6187462ba801f9a82133ee666e8e')
    version('5.1.10b', 'f587201d6cf5cf63527182fbfba70753')

    variant('mpi', default=True,
            description='Activate the compilation of parallel libraries')
    variant('compression', default=True,
            description='Activate the posibility to use compressed files')
    variant('esmumps', default=False,
            description='Activate the compilation of esmumps needed by mumps')
    variant('shared', default=True,
            description='Build a shared version of the library')
    variant('metis', default=True,
            description='Build metis and parmetis wrapper libraries')

    depends_on('flex@:2.6.1', type='build')
    depends_on('bison', type='build')
    depends_on('mpi', when='+mpi')
    depends_on('zlib', when='+compression')

    # NOTE: In cross-compiling environment parallel build
    # produces weird linker errors.
    parallel = False

    # NOTE: Versions of Scotch up to version 6.0.0 don't include support for
    # building with 'esmumps' in their default packages.  In order to enable
    # support for this feature, we must grab the 'esmumps' enabled archives
    # from the Scotch hosting site.  These alternative archives include a
    # superset of the behavior in their default counterparts, so we choose to
    # always grab these versions for older Scotch versions for simplicity.
    def url_for_version(self, version):
        return super(Scotch, self).url_for_version(version)

    @when('@:6.0.0')
    def url_for_version(self, version):
        return '%s/scotch_%s_esmumps.tar.gz' % (Scotch.base_url, version)

    def patch(self):
        self.configure()

    # NOTE: Configuration of Scotch is achieved by writing a 'Makefile.inc'
    # file that contains all of the configuration variables and their desired
    # values for the installation.  This function writes this file based on
    # the given installation variants.
    def configure(self):
        makefile_inc = []
        cflags = [
            '-O3',
            '-DCOMMON_RANDOM_FIXED_SEED',
            '-DSCOTCH_DETERMINISTIC',
            '-DSCOTCH_RENAME',
            '-DIDXSIZE64'
        ]

        if self.spec.satisfies('platform=darwin'):
            cflags.extend([
                '-Drestrict=__restrict'
            ])

        # Library Build Type #
        if '+shared' in self.spec:
            if self.spec.satisfies('platform=darwin'):
                makefile_inc.extend([
                    'LIB       = .dylib',
                    'CLIBFLAGS = -dynamiclib -fPIC',
                    'RANLIB    = echo',
                    'AR        = $(CC)',
                    'ARFLAGS   = -dynamiclib $(LDFLAGS) -Wl,-install_name -Wl,%s/$(notdir $@) -undefined dynamic_lookup -o ' % prefix.lib  # noqa
                ])
            else:
                makefile_inc.extend([
                    'LIB       = .so',
                    'CLIBFLAGS = -shared -fPIC',
                    'RANLIB    = echo',
                    'AR        = $(CC)',
                    'ARFLAGS   = -shared $(LDFLAGS) -o'
                ])
            cflags.append('-fPIC')
        else:
            makefile_inc.extend([
                'LIB       = .a',
                'CLIBFLAGS = ',
                'RANLIB    = ranlib',
                'AR        = ar',
                'ARFLAGS   = -ruv '
            ])

        # Compiler-Specific Options #

        if self.compiler.name == 'gcc':
            cflags.append('-Drestrict=__restrict')
        elif self.compiler.name == 'intel':
            cflags.append('-restrict')

        mpicc_path = self.spec['mpi'].mpicc if '+mpi' in self.spec else 'mpicc'
        makefile_inc.append('CCS       = $(CC)')
        makefile_inc.append('CCP       = %s' % mpicc_path)
        makefile_inc.append('CCD       = $(CCS)')

        # Extra Features #

        ldflags = []

        if '+compression' in self.spec:
            cflags.append('-DCOMMON_FILE_COMPRESS_GZ')
            ldflags.append('-L%s -lz' % (self.spec['zlib'].prefix.lib))

        cflags.append('-DCOMMON_PTHREAD')

        # NOTE: bg-q platform needs -lpthread (and not -pthread)
        # otherwise we get illegal instruction error during runtime
        if self.spec.satisfies('platform=darwin'):
            cflags.append('-DCOMMON_PTHREAD_BARRIER')
            ldflags.append('-lm -pthread')
        elif self.spec.satisfies('platform=bgq'):
            ldflags.append('-lm -lrt -lpthread')
        else:
            ldflags.append('-lm -lrt -pthread')

        makefile_inc.append('LDFLAGS   = %s' % ' '.join(ldflags))

        # General Features #

        flex_path = os.path.join(self.spec['flex'].prefix.bin, 'flex')
        bison_path = os.path.join(self.spec['bison'].prefix.bin, 'bison')
        makefile_inc.extend([
            'EXE       =',
            'OBJ       = .o',
            'MAKE      = make',
            'CAT       = cat',
            'LN        = ln',
            'MKDIR     = mkdir',
            'MV        = mv',
            'CP        = cp',
            'CFLAGS    = %s' % ' '.join(cflags),
            'LEX       = %s -Pscotchyy -olex.yy.c' % flex_path,
            'YACC      = %s -pscotchyy -y -b y' % bison_path,
            'prefix    = %s' % self.prefix
        ])

        with working_dir('src'):
            with open('Makefile.inc', 'w') as fh:
                fh.write('\n'.join(makefile_inc))

    def install(self, spec, prefix):
        targets = ['scotch']
        if '+mpi' in self.spec:
            targets.append('ptscotch')

        if self.spec.version >= Version('6.0.0'):
            if '+esmumps' in self.spec:
                targets.append('esmumps')
                if '+mpi' in self.spec:
                    targets.append('ptesmumps')

        with working_dir('src'):
            for target in targets:
                # It seams that building ptesmumps in parallel fails, for
                # version prior to 6.0.0 there is no separated targets force
                # ptesmumps, this library is built by the ptscotch target. This
                # should explain the test for the can_make_parallel variable
                can_make_parallel = \
                    not (target == 'ptesmumps' or
                         (self.spec.version < Version('6.0.0') and
                          target == 'ptscotch'))
                make(target, parallel=can_make_parallel)

        lib_ext = dso_suffix if '+shared' in self.spec else 'a'
        # It seams easier to remove metis wrappers from the folder that will be
        # installed than to tweak the Makefiles
        if '+metis' not in self.spec:
            with working_dir('lib'):
                force_remove('libscotchmetis.{0}'.format(lib_ext))
                force_remove('libptscotchparmetis.{0}'.format(lib_ext))

            with working_dir('include'):
                force_remove('metis.h')
                force_remove('parmetis.h')

        if '~esmumps' in self.spec and self.spec.version < Version('6.0.0'):
            with working_dir('lib'):
                force_remove('libesmumps.{0}'.format(lib_ext))
                force_remove('libptesmumps.{0}'.format(lib_ext))

            with working_dir('include'):
                force_remove('esmumps.h')

        install_tree('bin', prefix.bin)
        install_tree('lib', prefix.lib)
        install_tree('include', prefix.include)
        install_tree('man/man1', prefix.share_man1)
