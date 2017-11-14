##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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
# -----------------------------------------------------------------------------
# Author: Justin Too <too1@llnl.gov>
# -----------------------------------------------------------------------------

from spack import *
import spack.build_environment

class Rose(AutotoolsPackage):
    """A compiler infrastructure to build source-to-source program
       transformation and analysis tools.
       (Developed at Lawrence Livermore National Lab)"""

    homepage = "http://rosecompiler.org/"
    #url = "https://github.com/rose-compiler/rose-develop/archive/v0.9.7.0.tar.gz"
    url = "https://github.com/justintoo/rose-develop/archive/v0.9.9.104.zip"

    version('0.9.9.104', 'b01cf9d2fd440fc0fe77a713c5f7831e')
    version('0.9.9.0', '8f47fb8aa803d019657bd42c8b892cce')
    version('0.9.7.0', 'be0d0941ba4c0349a20d6394c20d16d7')
    version('0.9.9.52', commit='bd4fc0cc332ce62d9fa54db19879507d9e4f239b',
            git='https://github.com/rose-compiler/rose-develop.git')
    version('develop', branch='master',
            git='https://github.com/rose-compiler/rose-develop.git')

    depends_on("autoconf@2.69", type='build')
    depends_on("automake@1.14", type='build')
    depends_on("libtool@2.4", type='build')
    depends_on("boost@1.56.0")

    variant('debug', default=False,
            description='Enable compiler debugging symbols')
    variant('optimized', default=False,
            description='Enable compiler optimizations')

    variant('tests', default=False, description='Build the tests directory')
    variant('tutorial', default=False, description='Build the tutorial directory')

    variant('mvapich2_backend', default=False, description='Enable mvapich2 backend compiler')
    depends_on("mvapich2", when='+mvapich2_backend')

    variant('binanalysis', default=False,
            description='Enable binary analysis tooling')
    depends_on('libgcrypt', when='+binanalysis', type='build')
    depends_on('py-binwalk', when='+binanalysis', type='run')

    variant('c', default=True, description='Enable c language support')
    variant('cxx', default=True, description='Enable c++ language support')

    variant('fortran', default=False,
            description='Enable fortran language support')

    variant('java', default=False, description='Enable java language support')
    depends_on('jdk', when='+java')

    variant('z3', default=False, description='Enable z3 theorem prover')
    depends_on('z3', when='+z3')

    variant('edg_source', default=False, description='Use the EDG C/C++ frontend source code')
    depends_on('git', when='+edg_source')

    #------------------------------------------------------------------------
    # ROSE-based Projects
    #------------------------------------------------------------------------
    variant('codethorn', default=False, description='Enable the CodeThorn project')
    variant('polyopt', default=False, description='Enable the PolyOpt project')

    build_directory = 'rose-build'

    def patch(self):
        spec = self.spec

        # ROSE needs its <VERSION> <TIMESTAMP> to compute its EDG
        # binary compatibility signature for C/C++ and for its
        # --version information.
        #
        # <VERSION>      git rev-parse HEAD
        # <TIMESTAMP>    git log -1 --format="%at"
        #
        with open('VERSION', 'w') as f:
            if '@0.9.9.104:' in spec:
                # EDG: 27acd506c6b0e4b1c5f7573c642e3e407237eddd
                f.write('66c87e9395126a7ab8663d81f0e0b99d6e09131e 1504924600')
            elif '@0.9.9.0:' in spec:
                # EDG: 46306e9f73d3ccd690be300aefdaf766a9ba3f70
                f.write('14d3ebdd7f83cbcc295e6ed45b45d2e9ed32b5ff 1492716108')
            elif '@0.9.7.0:' in spec:
                # EDG: 8e63f421f9107ef6c7882b57f9c83e3878623ffa
                f.write('992c21ad06893bc1e9e7688afe0562eee0fda021 1460595442')
            else:
                raise InstallError('Unknown ROSE version!')

    def autoreconf(self, spec, prefix):
#        if not spec.satisfies('@develop'):
        with working_dir(self.stage.source_path):
            bash = which('bash')
            bash('build')

        if '+edg_source' in spec:
            git = which('git')
            git('clone',
                'rose-dev@rosecompiler1.llnl.gov:rose/edg4x/edg.git',
                'src/frontend/CxxFrontend/EDG')

    @property
    def languages(self):
        spec = self.spec
        langs = [
            'binaries' if '+binanalysis' in spec else '',
            'c' if '+c' in spec else '',
            'c++' if '+cxx' in spec else '',
            'java' if '+java' in spec else '',
            'fortran' if '+fortran' in spec else ''
        ]
        return list(filter(None, langs))

    def configure_args(self):
        spec = self.spec

        if '+mvapich2_backend' in spec:
            cc = spec['mvapich2'].mpicc
            cxx = spec['mvapich2'].mpicxx
        else:
            cc = spack_cc
            cxx = spack_cxx

        if spec.satisfies('@0.9.8:'):
            edg = "4.12"
        else:
            edg = "4.9"

        args = [
            '--disable-boost-version-check',
            '--enable-edg_version={0}'.format(edg),
            "--with-alternate_backend_C_compiler={0}".format(cc),
            "--with-alternate_backend_Cxx_compiler={0}".format(cxx),
            "--with-boost={0}".format(spec['boost'].prefix),
            "--enable-languages={0}".format(",".join(self.languages)),
        ]

        if '+z3' in spec:
            args.append("--with-z3={0}".format(spec['z3'].prefix))
        else:
            args.append("--without-z3")

        if '+tests' in spec:
            args.append("--enable-tests-directory")
        else:
            args.append("--disable-tests-directory")

        if '+tutorial' in spec:
            args.append("--enable-tutorial-directory")
        else:
            args.append("--disable-tutorial-directory")

        if '+java' in spec:
            args.append("--with-java={0}".format(spec['java'].prefix))
        else:
            args.append("--without-java")

        if '+debug' in spec:
            args.append("--with-CXX_DEBUG=-g")
        else:
            args.append("--without-CXX_DEBUG")

        if '+optimized' in spec:
            args.append("--with-C_OPTIMIZE=-O0")
            args.append("--with-CXX_OPTIMIZE=-O0")
        else:
            args.append("--without-C_OPTIMIZE")
            args.append("--without-CXX_OPTIMIZE")

        return args

    def setup_environment(self, spack_env, run_env):
        if '+codethorn' in self.spec:
            spack_env.set('CXXFLAGS', '-std=c++11')

    def build(self, spec, prefix):
        # Spack will automatically pass ncpus as the number of make jobs.
        #
        # If you really want to srun this on a separate node, you can do this:
        #
        #   $ srun -n1 spack install rose
        #
        with working_dir(self.build_directory):
            # ROSE needs the EDG version for C/C++
            with open('src/frontend/CxxFrontend/EDG-submodule-sha1', 'w') as f:
                if '@0.9.9.104' in spec:
                    f.write('27acd506c6b0e4b1c5f7573c642e3e407237eddd')
                elif '@0.9.9.52' in spec:
                    f.write('56a826126289414db5436e6c49879b99d046d26d')
                elif '@0.9.9.0' in spec:
                    f.write('46306e9f73d3ccd690be300aefdaf766a9ba3f70')
                elif '@0.9.7.0' in spec:
                    f.write('8e63f421f9107ef6c7882b57f9c83e3878623ffa')
                else:
                    raise InstallError('Unknown ROSE version for EDG!')

            # Compile librose
            with working_dir('src'):
                make()

            # Install librose
            with working_dir('src'):
                make('install')

            # Install "official" ROSE-based tools
            make('install-core')

            with working_dir('tools'):
                make('install')

            #-----------------------------------------------------------------
            # ROSE-based Projects
            #-----------------------------------------------------------------
            if '+codethorn' in spec:
                with working_dir('projects/CodeThorn'):
                    make('install')

            if '+polyopt' in spec:
                mkdir = which('mkdir')
                mkdir('-p', 'projects/PolyOpt2')
                with working_dir('projects/PolyOpt2'):
                    env['ROSE_SRC'] = self.stage.source_path
                    env['ROSE_ROOT'] = self.prefix

                    bash = which('bash')
                    bash(join_path(self.stage.source_path, 'projects/PolyOpt2/install.sh'))
