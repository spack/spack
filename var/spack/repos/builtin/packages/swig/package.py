# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os


from spack import *


class Swig(AutotoolsPackage):
    """SWIG is an interface compiler that connects programs written in
       C and C++ with scripting languages such as Perl, Python, Ruby,
       and Tcl. It works by taking the declarations found in C/C++
       header files and using them to generate the wrapper code that
       scripting languages need to access the underlying C/C++
       code. In addition, SWIG provides a variety of customization
       features that let you tailor the wrapping process to suit your
       application."""

    homepage = "http://www.swig.org"
    url      = "http://prdownloads.sourceforge.net/swig/swig-3.0.12.tar.gz"

    version('master', git='https://github.com/swig/swig.git')
    version('4.0.0', 'e8a39cd6437e342cdcbd5af27a9bf11b62dc9efec9248065debcb8276fcbb925')
    version('3.0.12', '82133dfa7bba75ff9ad98a7046be687c')
    version('3.0.11', '13732eb0f1ab2123d180db8425c1edea')
    version('3.0.10', 'bb4ab8047159469add7d00910e203124')
    version('3.0.8',  'c96a1d5ecb13d38604d7e92148c73c97')
    version('3.0.2',  '62f9b0d010cef36a13a010dc530d0d41')
    version('2.0.12', 'c3fb0b2d710cc82ed0154b91e43085a4')
    version('2.0.2',  'eaf619a4169886923e5f828349504a29')
    version('1.3.40', '2df766c9e03e02811b1ab4bba1c7b9cc')
    version('fortran', branch='master',
            git='https://github.com/swig-fortran/swig.git')

    depends_on('pcre')

    # Git repository does *not* include configure script
    for _version in ['@fortran', '@master']:
        depends_on('autoconf', type='build', when=_version)
        depends_on('automake', type='build', when=_version)
        depends_on('libtool', type='build', when=_version)
    depends_on('pkgconfig', type='build')

    build_directory = 'spack-build'

    @run_after('install')
    def create_symlink(self):
        # CMake compatibility: see https://github.com/spack/spack/pull/6240
        with working_dir(self.prefix.bin):
            os.symlink('swig', 'swig{0}'.format(self.spec.version.up_to(2)))

    for _version in ['@fortran', '@master']:
        @when(_version)
        def autoreconf(self, spec, prefix):
            which('sh')('./autogen.sh')
