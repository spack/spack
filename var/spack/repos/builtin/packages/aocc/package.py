# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
import subprocess
import platform

class Aocc(Package):
        """
        The AOCC compiler system is a high performance, production quality code generation tool. 
        The AOCC environment provides various options to developers when building and optimizing C, C++, and Fortran applications targeting 32-bit and 64-bit Linux® platforms. 
        The AOCC compiler system offers a high level of advanced optimizations, multi-threading and 
        processor support that includes global optimization, vectorization, inter-procedural analyses, loop transformations, and code generation.
        AMD also provides highly optimized libraries, which extract the optimal performance from each x86 processor core when utilized. 
        The AOCC Compiler Suite simplifies and accelerates development and tuning for x86 applications.
        Please install only if you agree to terms and conditions depicted under : http://developer.amd.com/wordpress/media/files/AOCC_EULA.pdf
          Example for installation: \'spack install aocc +license-agreed\'
        """
        family = 'compiler'
        AOCC_HOME = None
        homepage = "https://developer.amd.com/amd-aocc/"
        # manual_download = True
        version(ver="2.2.0", sha256='500940ce36c19297dfba3aa56dcef33b6145867a1f34890945172ac2be83b286', url='http://developer.amd.com/wordpress/media/files/aocc-compiler-2.2.0.tar')

        # Licensing
        license_required = True
        license_comment = '#'
        license_files = ['AOCC_EULA.pdf']
        license_url = 'http://developer.amd.com/wordpress/media/files/AOCC_EULA.pdf'

	# AOCC Requires : libxml2 zlib ncurses gcc libquadmath  libstdc++
        depends_on('libxml2')
        depends_on('zlib')
        depends_on('ncurses')
        depends_on('libtool')
        depends_on('texinfo')

        variant('license-agreed', default=False, description='Agree to terms and conditions depicted under : http://developer.amd.com/wordpress/media/files/AOCC_EULA.pdf')


        @run_before('install')
        def abort_without_license_agreed(self):
            if (not self.spec.variants['license-agreed'].value):
                raise InstallError('\n\n\nUse +license-agreed during installation to accept terms and conditions depicted under following link \nLink: http://developer.amd.com/wordpress/media/files/AOCC_EULA.pdf \nExample: \'spack install aocc +license-agreed\' \n ')

        def install(self, spec, prefix):
            status, output = subprocess.getstatusoutput("cp -r * " + prefix)
            Aocc.AOCC_HOME = prefix

        def setup_run_environment(self, env):
            if '+clang' in self.spec:
                env.set('CC', join_path(self.spec.prefix.bin, 'clang'))
                env.set('CXX', join_path(self.spec.prefix.bin, 'clang++'))
                env.set('FC',  join_path(self.spec.prefix.bin, 'flang'))
                env.set('F77', join_path(self.spec.prefix.bin, 'flang'))
                env.set('F95', join_path(self.spec.prefix.bin, 'flang'))

                env.set('AOCC_HOME', Aocc.AOCC_HOME)
                env.append_path('PATH', os.path.join (Aocc.AOCC_HOME, 'bin'))
                env.prepend_path('LIBRARY_PATH', self.spec.prefix.lib)
                env.prepend_path('LD_LIBRARY_PATH', self.spec.prefix.lib)
                env.prepend_path('C_INCLUDE_PATH', self.spec.prefix.include)
                env.prepend_path('CPLUS_INCLUDE_PATH', self.spec.prefix.include)
