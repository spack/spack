# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import tarfile

from spack import *


class Cernlib(Package):
    """The CERN Program Library is a large collection ofi
    general purpose libraries and modules."""

    homepage = "https://www.zeuthen.desy.de/linear_collider/cernlib/new/cernlib_2005.html"
    url      = "https://www-zeuthen.desy.de/linear_collider/cernlib/new/cernlib-2005-all-new.tgz"

    maintainers = ['DraTeots', 'wdconinc']

    tags = ['hep']

    versions = {
        '2020.12.11': (
            '99486b6dbfb3a93803420719e0ea74a15735ee817277b0be0695b075ea136714',
            '991cc960bf90f1a8f7d61279554bedaae9c17737d5862607414f193953db6384'
        )
    }

    for v in versions:
        version(
            v,
            sha256='25bda7271dce6e7d199039e46bd044e7eb97fd9c1287ccbf6d7b5772749e78a9',
            url='http://www-zeuthen.desy.de/linear_collider/cernlib/new/cernlib-2005-all-new.tgz'
        )
        resource(
            name='cernlib.2005.corr.{}.tgz'.format(v),
            url='http://www-zeuthen.desy.de/linear_collider/cernlib/new/cernlib.2005.corr.{}.tgz'.format(v),
            sha256=versions[v][0],
            destination='resources',
            placement='corr',
            expand=False,
            when='@{}'.format(v)
        )
        resource(
            name='cernlib.2005.install.{}.tgz'.format(v),
            url='http://www-zeuthen.desy.de/linear_collider/cernlib/new/cernlib.2005.install.{}.tgz'.format(v),
            sha256=versions[v][1],
            destination='resources',
            placement='install',
            expand=False,
            when='@{}'.format(v)
        )

    depends_on('makedepend', type='build')
    depends_on('imake', type='build')
    depends_on('gmake', type='build')
    depends_on('netlib-lapack')
    depends_on('libxmu')
    depends_on('libxt')
    depends_on('motif')

    phases = ['unpack', 'build', 'install']

    def setup_build_environment(self, env):
        env.set('CERN', self.stage.source_path)
        env.set('CERN_LEVEL', '2005')
        env.set('FORTRANOPTIONS', '')

    def unpack(self, spec, prefix):
        # Untar inner tar files
        install_tar = tarfile.open(
            'resources/install/cernlib.2005.install.2020.12.11.tgz')
        install_tar.extractall()

        # Update corr tar file
        copy('resources/corr/cernlib.2005.corr.2020.12.11.tgz',
             'cernlib.2005.corr.tgz')

        # Unpack cernlib src
        filter_file(
            r'#!/bin/bash',
            '#!/bin/bash -ue',
            './Install_cernlib_src')
        filter_file(
            r'./Install_cernlib_src',
            '#./Install_cernlib_src',
            './Install_cernlib')
        filter_file(
            r'./Install_old_patchy4',
            '#./Install_old_patchy4',
            './Install_cernlib')
        filter_file(
            r'./Install_cernlib_patchy',
            '#./Install_cernlib_patchy',
            './Install_cernlib')
        install_cernlib_src = Executable('./Install_cernlib_src')
        install_cernlib_src()

        def patch(target_file, patch_file):
            which('patch')('-N', '-l', '-p1', target_file,
                           '-i', join_path(patches, patch_file))

        # Apply patches
        src = self.stage.source_path
        patches = self.package_dir
        with working_dir(join_path(src, '2005/src/config')):
            patch('Imake.tmpl', 'Imake.tmpl.patch')
            patch('linux-lp64.cf', 'linux-lp64.cf.patch')
        with working_dir(join_path(src, '2005/src/packlib/cspack/sysreq')):
            patch('serror.c', 'serror.c.patch')
            patch('socket.c', 'socket.c.patch')
        with working_dir(join_path(src, '2005/src/packlib/kernlib/kernbit/z268')):
            patch('systems.c', 'systems.c.patch')
        with working_dir(join_path(src, '2005/src/geant321/miface')):
            patch('gmicap.F', 'gmicap.F.patch')

        # Scripts should exit on error
        files = glob.glob('Install_*')
        filter_file(r'#!/bin/bash', '#!/bin/bash -ue', *files)
        filter_file(r'#!/bin/sh', '#!/bin/sh -ue', *files)
        filter_file(r'> log', '| tee log', *files)
        filter_file(r'>> ../log', '| tee -a ../log', *files)

    def build(self, spec, prefix):
        # Link lapack and blas to their cernlib locations
        cernlib_dirs = ['2005/src/lib', '2005/lib']
        lapack_libs = find_libraries(['liblapack.a', 'libblas.a'],
                                     spec['netlib-lapack'].prefix,
                                     recursive=True,
                                     shared=False)
        for cernlib_dir in cernlib_dirs:
            mkdirp(cernlib_dir)
            for lapack_lib in lapack_libs:
                symlink(lapack_lib, cernlib_dir)

        # Install (i.e. build) cernlib
        filter_file(
            r'./Install_cernlib_test',
            '#./Install_cernlib_test',
            './Install_cernlib')
        install_cernlib = Executable('./Install_cernlib')
        install_cernlib()

    def install(self, spec, prefix):
        # Install tree to final location
        level = '2005'
        for dir in ['bin', 'lib', 'include']:
            install_tree(join_path(level, dir),
                         join_path(prefix, dir))
        # Link level to prefix
        symlink('.', join_path(prefix, level))

    def setup_run_environment(self, env):
        env.set('CERN', self.prefix)
        env.set('CERN_LEVEL', '2005')
