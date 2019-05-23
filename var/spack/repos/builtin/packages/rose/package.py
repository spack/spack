##############################################################################
# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
###############################################################################
# -----------------------------------------------------------------------------
# Author: Justin Too <too1@llnl.gov>
# -----------------------------------------------------------------------------
from spack import *


class Rose(AutotoolsPackage):
    """A compiler infrastructure to build source-to-source program
       transformation and analysis tools.
       (Developed at Lawrence Livermore National Lab)"""

    homepage = "http://rosecompiler.org/"
    url      = "https://github.com/rose-compiler/rose-develop/archive/v0.9.7.0.tar.gz"
    git      = "https://github.com/rose-compiler/rose-develop.git"

    version('master', branch='master')
    version('0.9.10.0', tag='v0.9.10.0')
    version('0.9.9.0',  tag='v0.9.9.0')
    version('0.9.7.0',  tag='v0.9.7.0')

    #patch('add_spack_compiler_recognition.patch')

    depends_on("autoconf@2.69:", type='build')
    depends_on("automake@1.14:", type='build')
    depends_on("libtool@2.4:", type='build')
    depends_on("bison", type='build')
    depends_on("flex", type='build')
    depends_on("boost@1.56.0:1.60.0", when="~cxx11")
    depends_on("boost@1.60.0",        when="+cxx11")
    

    variant('tests', default=False, description='Build the tests directory')

    variant('binanalysis', default=False, description='Enable binary analysis tooling')
    depends_on('libgcrypt', when='+binanalysis', type='build')
    depends_on('py-binwalk', when='+binanalysis', type='run')

    variant('c', default=True, description='Enable c language support')
    variant('cxx', default=True, description='Enable c++ language support')

    variant('fortran', default=False, description='Enable fortran language support')

    variant('java', default=False, description='Enable java language support')
    depends_on('java', when='+java')

    variant('z3', default=False, description='Enable z3 theorem prover')
    depends_on('z3', when='+z3')

    variant('cxx11', default=True)

    build_directory = 'spack-build'

    def autoreconf(self, spec, prefix):
        with working_dir(self.stage.source_path):
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
        cc = self.compiler.cc
        cxx = self.compiler.cxx
        
        if spec.satisfies('@0.9.8:'):
            edg = '4.12'
        else:
            edg = '4.9'
        
        args = [
            '--disable-boost-version-check',
            '--enable-edg_version={0}'.format(edg),
            "--with-alternate_backend_C_compiler={0}".format(cc),
            "--with-alternate_backend_Cxx_compiler={0}".format(cxx),
            "--with-boost={0}".format(spec['boost'].prefix),
            "--enable-languages={0}".format(",".join(self.languages)),
            "--with-z3={0}".format(spec['z3'].prefix) if '+z3' in spec else '',
            '--disable-tests-directory' if '+tests' not in spec else '',
            '--enable-tutorial-directory={0}'.format('no'),
            '--without-java',
        ]
        
        if '+cxx11' in spec:
            args.append("CXXFLAGS=-std=c++11")
        
        return args
        

    install_targets = ["install-core"]
