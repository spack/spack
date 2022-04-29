# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class SpiralSoftware(CMakePackage):
    """SPIRAL is a program generation system for linear transforms and other
    mathematical functions that produces very high performance code for a wide
    spectrum of hardware platforms."""

    homepage = "https://spiral.net"
    url      = "https://github.com/spiral-software/spiral-software/archive/refs/tags/8.4.0.tar.gz"
    git      = "https://github.com/spiral-software/spiral-software.git"

    maintainers = ['spiralgen']

    version('develop', branch='develop')
    version('master',  branch='master')
    version('8.4.0',   sha256='d0c58de65c678130eeee6b8b8b48061bbe463468990f66d9b452225ce46dee19')
    version('8.3.0',   sha256='41cf0e7f14f9497e98353baa1ef4ca6204ce5ca525db8093f5bb44e89992abdf')
    version('8.2.1',   sha256='78d7bb1c22a5b2d216eac7b6ddedd20b601ba40227e64f743cbb54d4e5a7794d')
    version('8.2.0',   sha256='983f38d270ae2cb753c88cbce3f412e307c773807ad381acedeb9275afc0be32')

    variant('build_type', default='Release',
            values=('Debug', 'Release', 'RelWithDebInfo', 'MinSizeRel'),
            description='Build the Release version by default')

    extendable = True

    # No dependencies.

    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            make('all')
            make('install')

    def install(self, spec, prefix):
        with working_dir(self.stage.source_path):
            files = ('LICENSE', 'README.md', 'ReleaseNotes.md')
            for fil in files:
                install(fil, prefix)

        mkdirp(prefix.gap.bin)
        mkdirp(prefix.gap.lib)
        mkdirp(prefix.gap.grp)
        mkdirp(prefix.namespaces)
        mkdirp(prefix.profiler)
        mkdirp(prefix.tests)
        mkdirp(prefix.bin)
        mkdirp(prefix.config)

        print("self.stage.source_path = " + self.stage.source_path)
        with working_dir(self.stage.source_path):
            install_tree('namespaces', prefix.namespaces)
            install_tree('profiler', prefix.profiler)
            install_tree('tests', prefix.tests)
            install_tree('bin', prefix.bin)
            install_tree('config', prefix.config)

        with working_dir(join_path(self.stage.source_path, 'gap')):
            install_tree('lib', prefix.gap.lib)
            install_tree('grp', prefix.gap.grp)
            install_tree('bin', prefix.gap.bin)

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set('SPIRAL_HOME', self.prefix)

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.set('SPIRAL_HOME', self.prefix)

    def setup_run_environment(self, env):
        env.set('SPIRAL_HOME', self.prefix)
