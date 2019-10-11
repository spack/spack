# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Funhpc(CMakePackage):
    """FunHPC: Functional HPC Programming"""

    homepage = "https://github.com/eschnett/FunHPC.cxx"
    url      = "https://github.com/eschnett/FunHPC.cxx/archive/version/0.1.0.tar.gz"
    git      = "https://github.com/eschnett/FunHPC.cxx.git"

    version('develop', branch='master')
    version('1.3.0', sha256='140e60f55a307f21117bd43fa16db35d60c0df5ef37e17a4da1cb3f5da5e29c1')
    version('1.2.0', md5='ba2bbeea3091e999b6b85eaeb1b67a83')
    version('1.1.1', md5='7b9ef638b02fffe35b75517e8eeff580')
    version('1.1.0', md5='897bd968c42cd4f14f86fcf67da70444')
    version('1.0.0', md5='f34e71ccd5548b42672e692c913ba5ee')
    version('0.1.1', md5='f0248710f2de88ed2a595ad40d99997c')
    version('0.1.0', md5='00f7dabc08ed1ab77858785ce0809f50')

    variant('pic', default=True,
            description="Produce position-independent code")

    depends_on('cereal')
    depends_on('googletest')
    depends_on('hwloc')
    depends_on('jemalloc')
    depends_on('mpi')
    depends_on('qthreads')

    def cmake_args(self):
        spec = self.spec
        options = ["-DGTEST_ROOT=%s" % spec['googletest'].prefix]
        if '+pic' in spec:
            options += ["-DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=true"]
        return options

    def check(self):
        with working_dir(self.build_directory):
            make("test", "CTEST_OUTPUT_ON_FAILURE=1")
