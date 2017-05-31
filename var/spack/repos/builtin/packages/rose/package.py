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
# -----------------------------------------------------------------------------
# Author: Justin Too <too1@llnl.gov>
# -----------------------------------------------------------------------------

from spack import *


class Rose(Package):
    """A compiler infrastructure to build source-to-source program
       transformation and analysis tools.
       (Developed at Lawrence Livermore National Lab)"""

    homepage = "http://rosecompiler.org/"
    url      = "https://github.com/rose-compiler/rose/archive/v0.9.7.tar.gz"

    version('0.9.7', 'e14ce5250078df4b09f4f40559d46c75')
    version('master', branch='master',
            git='https://github.com/rose-compiler/rose.git')

    patch('add_spack_compiler_recognition.patch')

    depends_on("autoconf@2.69", type='build')
    depends_on("automake@1.14", type='build')
    depends_on("libtool@2.4", type='build')
    depends_on("boost@1.47.0:")

    variant('tests', default=False, description='enable the tests directory')

    variant('binanalysis', default=False, description='enable binary analysis tooling')
    depends_on('libgcrypt', when='+binanalysis')
    depends_on('py-binwalk', when='+binanalysis')

    variant('c', default=True)
    variant('cxx', default=True)

    variant('fortran', default=False, description='enable fortran')

    variant('java', default=False, description='enable java')
    depends_on('jdk', when='+java')

    variant('z3', default=False, description='enable z3')
    depends_on('z3', when='+z3')

    @property
    def build_directory(self):
        return join_path(self.stage.source_path, 'build_tree')

    def autoreconf(self, spec, prefix):
        bash = which('bash')
        bash('build')

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
        return [
            '--disable-boost-version-check',
            "--with-alternate_backend_C_compiler={}".format(self.compiler.cc),
            "--with-alternate_backend_Cxx_compiler={}".format(self.compiler.cxx),
            "--with-boost={}".format(spec['boost'].prefix),
            "--enable-languages={}".format(",".join(self.languages)),
            "--with-z3={}".format(spec['z3'].prefix) if '+z3' in spec else '',
            '--enable-tests-directory' if '+tests' in spec else '--disable-tests-directory',
            '--enable-tutorial-directory={}'.format('no'),
        ]

    install_targets = [ "install-core" ]
