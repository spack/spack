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


class Rose(AutotoolsPackage):
    """A compiler infrastructure to build source-to-source program
       transformation and analysis tools.
       (Developed at Lawrence Livermore National Lab)"""

    homepage = "http://rosecompiler.org/"
    url = "https://github.com/rose-compiler/rose/archive/v0.9.7.0.tar.gz"

    version('0.9.9.0', '131356e5f12ddc232ad90cfc25f8bfb7')
    version('0.9.7.0', 'be0d0941ba4c0349a20d6394c20d16d7')
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

    build_directory = 'rose-build'

    def patch(self):
        spec = self.spec

        # ROSE needs its <VERSION> <TIMESTAMP> to compute its EDG
        # binary compatibility signature for C/C++ and for its
        # --version information.
        with open('VERSION', 'w') as f:
            if '@0.9.9.0:' in spec:
                # EDG: 46306e9f73d3ccd690be300aefdaf766a9ba3f70
                f.write('14d3ebdd7f83cbcc295e6ed45b45d2e9ed32b5ff 1492716108')
            elif '@0.9.7.0:' in spec:
                # EDG: 8e63f421f9107ef6c7882b57f9c83e3878623ffa
                f.write('992c21ad06893bc1e9e7688afe0562eee0fda021 1460595442')

    def autoreconf(self, spec, prefix):
        bash = which('bash')
        #bash('build')

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

    def build(self, spec, prefix):
        # Spack will automatically pass ncpus as the number of make jobs.
        #
        # If you really want to srun this on a separate node, you can do this:
        #
        #   $ srun -n1 spack install -j16 rose
        #
        with working_dir(self.build_directory):
            # ROSE needs the EDG version for C/C++
            with open('src/frontend/CxxFrontend/EDG-submodule-sha1', 'w') as f:
                if '@0.9.9.0' in spec:
                    f.write('46306e9f73d3ccd690be300aefdaf766a9ba3f70')
                elif '@0.9.7.0' in spec:
                    f.write('8e63f421f9107ef6c7882b57f9c83e3878623ffa')
                else:
                    raise InstallError('Unknown ROSE version for EDG!')

            # Install librose and identityTranslator
            make('install-core')

            # Install "official" ROSE-based tools
            with working_dir('tools'):
                make('install')
