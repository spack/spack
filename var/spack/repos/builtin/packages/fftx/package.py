# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import subprocess

from spack import *


class Fftx(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://spiral.net"
    url      = "https://github.com/spiral-software/fftx/archive/0.9.0.tar.gz"
    git      = "https://github.com/spiral-software/fftx.git"

    maintainers = ['spiralgen']

    version('develop', branch='develop')
    version('main',  branch='main')
    version('0.9.0', sha256='d4930e9b959fd56bb63543b359ca09a7ae2c56db3ffc28d7d3628d92fc79ce12')

    variant('build_type', default='Release',
            values=('Debug', 'Release', 'RelWithDebInfo', 'MinSizeRel'),
            description='The build type to build')

    depends_on('spiral-software')
    #  depends_on('spiral-package-fftx')
    #  depends_on('spiral-package-simt')
    #  depends_on('spiral-package-mpi')

    @run_before('cmake')
    def create_lib_source_code(self):
        #  From directory examples/library run the build-lib-code.sh script
        with working_dir(join_path(self.stage.source_path, 'examples/library')):
            bld_script = join_path(self.stage.source_path,
                                   'examples/library/build-lib-code.sh')
            result = subprocess.run(bld_script, shell=True, check=False)
            res = result.returncode
            print(result)
            #  Use the script result to set the build parameter for use with cmake
            if res == 0:
                self.build_config = '-D_codegen=CPU'
            elif res == 1:
                self.build_config = '-D_codegen=CUDA'
            elif res == 2:
                self.build_config = '-D_codegen=HIP'

    def cmake_args(self):
        spec = self.spec
        args = [
            '-DSPIRAL_HOME:STRING={0}'.format(spec['spiral-software'].prefix)
        ]
        args.append('-DCMAKE_INSTALL_PREFIX:PATH={0}'.format(self.stage.source_path))
        args.append(self.build_config)
        print('Args = ' + str(args))
        return args

    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            make('install')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.CMakeIncludes)
        mkdirp(prefix.examples)
        mkdirp(prefix.include)
        mkdirp(prefix.lib)

        with working_dir(self.stage.source_path):
            files = ('License.txt', 'README.md', 'ReleaseNotes.md')
            for fil in files:
                install(fil, prefix)

        with working_dir(self.stage.source_path):
            install_tree('bin', prefix.bin)
            install_tree('CMakeIncludes', prefix.CMakeIncludes)
            install_tree('examples', prefix.examples)
            install_tree('include', prefix.include)
            install_tree('lib', prefix.lib)

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set('FFTX_HOME', self.prefix)

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.set('FFTX_HOME', self.prefix)

    def setup_run_environment(self, env):
        env.set('FFTX_HOME', self.prefix)
