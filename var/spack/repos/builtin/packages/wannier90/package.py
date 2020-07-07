# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import inspect
import os.path
from llnl.util.filesystem import find

from spack import *


class Wannier90(MakefilePackage):
    """Wannier90 calculates maximally-localised Wannier functions (MLWFs).

    Wannier90 is released under the GNU General Public License.
    """
    homepage = 'http://wannier.org'
    url = 'http://wannier.org/code/wannier90-2.0.1.tar.gz'
    # Newer versions are here
    new_url = 'https://github.com/wannier-developers/wannier90/archive/v3.1.0.tar.gz'

    version('3.1.0', sha256='40651a9832eb93dec20a8360dd535262c261c34e13c41b6755fa6915c936b254')
    version('3.0.0', sha256='f196e441dcd7b67159a1d09d2d7de2893b011a9f03aab6b30c4703ecbf20fe5b')
    version('2.1.0', sha256='ee90108d4bc4aa6a1cf16d72abebcb3087cf6c1007d22dda269eb7e7076bddca')
    version('2.0.1', sha256='05ea7cd421a219ce19d379ad6ae3d9b1a84be4ffb367506ffdfab1e729309e94')

    depends_on('mpi')
    depends_on('lapack')
    depends_on('blas')

    parallel = False

    variant(
        'shared',
        default=True,
        description='Builds a shared version of the library'
    )

    @property
    def build_targets(self):
        targets = []
        if '@:3.0.0' in self.spec:
            targets = [
                'wannier', 'post', 'lib', 'w90chk2chk', 'w90vdw', 'w90pov'
            ]
        if '@2.999.999:' in self.spec:
            # 'wannier', 'post', 'lib', 'w90chk2chk', 'w90vdw', 'dynlib'
            targets = ['wannier', 'post', 'lib', 'w90chk2chk', 'w90vdw']
            if '+shared' in self.spec:
                targets.append('dynlib')

        return targets

    def url_for_version(self, version):
        maj_ver = version.up_to(1)
        if (maj_ver > Version('2')):
            url = 'https://github.com/wannier-developers/wannier90/archive/v{0}.tar.gz'
        else:
            url = 'http://wannier.org/code/wannier90-{0}.tar.gz'
        return url.format(version)

    @property
    def makefile_name(self):
        # Older versions use 'make.sys'
        filename = 'make.sys'

        # While newer search for 'make.inc'
        if self.spec.satisfies('@2.1.0:'):
            filename = 'make.inc'

        abspath = join_path(self.stage.source_path, filename)
        return abspath

    def edit(self, spec, prefix):

        lapack = self.spec['lapack'].libs
        blas = self.spec['blas'].libs
        mpi = self.spec['mpi'].libs

        substitutions = {
            '@F90': spack_fc,
            '@MPIF90': self.spec['mpi'].mpifc,
            '@LIBS': (lapack + blas + mpi).joined()
        }

        template = join_path(
            os.path.dirname(inspect.getmodule(self).__file__),
            'make.sys'
        )

        copy(template, self.makefile_name)
        for key, value in substitutions.items():
            filter_file(key, value, self.makefile_name)

        if '+shared' in self.spec:
            if self.spec.satisfies('@2.0.0:2.999.999'):
                # this is to build a .so wannier90 library
                filter_file('LIBRARY = ../../libwannier.a',
                            'LIBRARY = ../../libwannier.so',
                            join_path(self.stage.source_path,
                                      'src/Makefile.2'))
                objs_post = ['parameters.o', 'kmesh.o', 'io.o', 'comms.o',
                             'utility.o', 'get_oper.o', 'constants.o',
                             'postw90_common.o', 'wan_ham.o', 'spin.o',
                             'dos.o', 'berry.o', 'kpath.o', 'kslice.o',
                             'boltzwann.o', 'geninterp.o']
                new_objs_post = ['comms.o', 'get_oper.o', 'postw90_common.o',
                                 'wan_ham.o', 'spin.o', 'dos.o', 'berry.o',
                                 'kpath.o', 'kslice.o', 'boltzwann.o',
                                 'geninterp.o']
                filter_file(''.join(['OBJS_POST  = ', ' '.join(objs_post)]),
                            ''.join(['OBJS_POST  = ',
                                     ' '.join(new_objs_post)]),
                            join_path(self.stage.source_path,
                                      'src/Makefile.2'))
                filter_file('../../wannier90.x: .*',
                            ' '.join(['../../wannier90.x: $(OBJS)',
                                      '../wannier_prog.F90 $(LIBRARY)']),
                            join_path(self.stage.source_path,
                                      'src/Makefile.2'))
                filter_file(' '.join(['../../postw90.x: \\$\\(OBJS_POST\\)',
                                      '\\$\\(POSTDIR\\)postw90.F90']),
                            ' '.join(['../../postw90.x: $(OBJS_POST)',
                                     '$(POSTDIR)postw90.F90 $(LIBRARY)']),
                            join_path(self.stage.source_path,
                                      'src/Makefile.2'))
                filter_file(
                    ' '.join([
                        '\\$\\(COMPILER\\) ../wannier_prog.F90',
                        '\\$\\(LDOPTS\\) \\$\\(OBJS\\) \\$\\(LIBS\\)',
                        '-o ../../wannier90.x']),
                    ' '.join(['$(COMPILER) -I../obj ../wannier_prog.F90',
                              '$(LDOPTS) -L../.. -lwannier',
                              '-o ../../wannier90.x']),
                    join_path(self.stage.source_path,
                              'src/Makefile.2'))
                filter_file(
                    ' '.join(['\\$\\(COMPILER\\) \\$\\(POSTDIR\\)postw90.F90',
                              '\\$\\(POSTOPTS\\) \\$\\(LDOPTS\\)',
                              '\\$\\(OBJS_POST\\)',
                              '\\$\\(LIBS\\) -o ../../postw90.x']),
                    ' '.join(['$(COMPILER) -I../obj $(POSTDIR)postw90.F90',
                              '$(POSTOPTS) $(LDOPTS) $(OBJS_POST)',
                              '-L../.. -lwannier $(LIBS) -o ../../postw90.x']),
                    join_path(self.stage.source_path,
                              'src/Makefile.2'))

                filter_file(
                    ' '.join(['\\$\\(AR\\) \\$\\(ARFLAGS\\)',
                              '\\$\\(LIBRARY\\)',
                              '\\$\\(OBJS2\\) \\$\\(OBJS\\)']),
                    ' '.join(['$(MPIF90) $(FCOPTS) -shared -o '
                              '$(LIBRARY) $(OBJS2) $(OBJS) $(LIBS)']),
                    join_path(self.stage.source_path,
                              'src/Makefile.2'))

    def setup_build_environment(self, env):
        env.set('MPIFC', self.prefix.bin.mpifc)

    def install(self, spec, prefix):
        mkdirp(self.prefix.bin)
        mkdirp(self.prefix.lib)
        if '+shared' in spec:
            mkdirp(self.prefix.modules)

        install(
            join_path(self.stage.source_path, 'wannier90.x'),
            join_path(self.prefix.bin, 'wannier90.x')
        )

        install(
            join_path(self.stage.source_path, 'postw90.x'),
            join_path(self.prefix.bin, 'postw90.x')
        )

        if '+shared' in spec:
            if '@3:' in spec:
                inst = ['libwannier.a', 'libwannier.so']
            else:
                inst = ['libwannier.so']
        else:
            inst = ['libwannier.a']

        for file in inst:
            install(join_path(self.stage.source_path, file),
                    join_path(self.prefix.lib, file))

        install(
            join_path(self.stage.source_path, 'w90chk2chk.x'),
            join_path(self.prefix.bin, 'w90chk2chk.x')
        )

        install(
            join_path(self.stage.source_path, 'utility', 'w90vdw', 'w90vdw.x'),
            join_path(self.prefix.bin, 'w90vdw.x')
        )

        if spec.satisfies('@:2.99')
            install(
                join_path(self.stage.source_path,
                          'utility', 'w90pov', 'w90pov'),
                join_path(self.prefix.bin, 'w90pov')
            )

        install_tree(
            join_path(self.stage.source_path, 'pseudo'),
            join_path(self.prefix.bin, 'pseudo')
        )

        for file in find(join_path(self.stage.source_path, 'src/obj'),
                         '*.mod'):
            install(file, self.prefix.modules)
