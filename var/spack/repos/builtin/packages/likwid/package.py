# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import glob
import os


class Likwid(Package):
    """Likwid is a simple to install and use toolsuite of command line
    applications for performance oriented programmers. It works for Intel and
    AMD processors on the Linux operating system. This version uses the
    perf_event backend which reduces the feature set but allows user installs.
    See https://github.com/RRZE-HPC/likwid/wiki/TutorialLikwidPerf#feature-limitations
    for information."""

    homepage = "https://github.com/RRZE-HPC/likwid"
    url      = "https://github.com/RRZE-HPC/likwid/archive/4.1.2.tar.gz"

    version('4.3.4', '37bdcd20630ef3694435065a6c8a14fa')
    version('4.3.3', '70ff0d1238989010842644db792f4910')
    version('4.3.2', '2cf00e220dfe22c8d9b6e44f7534e11d')
    version('4.3.1', 'ff28250f622185688bf5e2e0975368ea')
    version('4.3.0', '7f8f6981d7d341fce2621554323f8c8b')

    patch('https://github.com/RRZE-HPC/likwid/commit/d2d0ef333b5e0997d7c80fc6ac1a473b5e47d084.patch', sha256='636cbf40669261fdb36379d67253be2b731cfa7b6d610d232767d72fbdf08bc0', when='@4.3.4')

    # NOTE: There is no way to use an externally provided hwloc with Likwid.
    # The reason is that the internal hwloc is patched to contain extra
    # functionality and functions are prefixed with "likwid_".

    depends_on('lua', when='@4.2.0:')

    # TODO: check
    # depends_on('gnuplot', type='run')

    depends_on('perl', type=('build', 'run'))

    supported_compilers = {'clang': 'CLANG', 'gcc': 'GCC', 'intel': 'ICC'}

    def patch(self):
        files = glob.glob('perl/*.*') + glob.glob('bench/perl/*.*')

        # Allow the scripts to find Spack's perl
        filter_file('^#!/usr/bin/perl -w', '#!/usr/bin/env perl', *files)
        filter_file('^#!/usr/bin/perl', '#!/usr/bin/env perl', *files)

    @run_before('install')
    def filter_sbang(self):
        # Filter sbang before install so Spack's sbang hook can fix it up
        files = ['perl/feedGnuplot'] + glob.glob('filters/*')

        filter_file('^#!/usr/bin/perl',
                    '#!{0}'.format(self.spec['perl'].command.path),
                    *files)

    def install(self, spec, prefix):
        if self.compiler.name not in self.supported_compilers:
            raise RuntimeError('{0} is not a supported compiler \
            to compile Likwid'.format(self.compiler.name))

        filter_file('^COMPILER .*',
                    'COMPILER = ' +
                    self.supported_compilers[self.compiler.name],
                    'config.mk')
        filter_file('^PREFIX .*',
                    'PREFIX = ' +
                    prefix,
                    'config.mk')

        # FIXME: once https://github.com/spack/spack/issues/4432 is
        # resolved, install as root by default and remove this
        filter_file('^ACCESSMODE .*',
                    'ACCESSMODE = perf_event',
                    'config.mk')
        filter_file('^BUILDFREQ .*',
                    'BUILDFREQ = false',
                    'config.mk')
        filter_file('^BUILDDAEMON .*',
                    'BUILDDAEMON = false',
                    'config.mk')

        if spec.satisfies('^lua'):
            filter_file('^#LUA_INCLUDE_DIR.*',
                        'LUA_INCLUDE_DIR = {0}'.format(
                            spec['lua'].prefix.include),
                        'config.mk')
            filter_file('^#LUA_LIB_DIR.*',
                        'LUA_LIB_DIR = {0}'.format(
                            spec['lua'].prefix.lib),
                        'config.mk')
            filter_file('^#LUA_LIB_NAME.*',
                        'LUA_LIB_NAME = lua',
                        'config.mk')
            filter_file('^#LUA_BIN.*',
                        'LUA_BIN = {0}'.format(
                            spec['lua'].prefix.bin),
                        'config.mk')

        env['PWD'] = os.getcwd()
        make()
        make('install')
