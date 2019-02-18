# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fmt(CMakePackage):
    """fmt (formerly cppformat) is an open-source formatting library.
    It can be used as a safe alternative to printf or as a fast alternative
    to C++ IOStreams."""

    homepage = "http://fmtlib.net/latest/index.html"
    url      = "https://github.com/fmtlib/fmt/releases/download/5.2.1/fmt-5.2.1.zip"

    version('5.2.1', sha256='43894ab8fe561fc9e523a8024efc23018431fa86b95d45b06dbe6ddb29ffb6cd')
    version('5.2.0', sha256='c016db7f825bce487a7929e1edb747b9902a2935057af6512cad3df3a080a027')
    version('5.1.0', sha256='77ef9fea638dc846e484409fbc1ea710bb9bcea042e7b35b8805041bf7655ad5')
    version('5.0.0', sha256='8dd58daf13e7e8adca99f8725ef3ae598f9c97efda7d6d8d4c49db5047879097')
    version('4.1.0', sha256='9d49bf02ceb9d0eec51144b203b63b77e69d3798bb402fb82e7d0bdb06c79eeb')
    version('4.0.0', sha256='10a9f184d4d66f135093a08396d3b0a0ebe8d97b79f8b3ddb8559f75fe4fcbc3')
    version('3.0.2', sha256='51407b62a202b29d1a9c0eb5ecd4095d30031aea65407c42c25cb10cb5c59ad4')
    version('3.0.1', sha256='4c9af0dc919a8ae7022b44e1a03c435e42d65c866f44667d8d920d342b098550')
    version('3.0.0', sha256='1b050b66fa31b74f1d75a14f15e99e728ab79572f176a53b2f8ad7c201c30ceb')

    depends_on('cmake@3.1.0:', type='build')

    # Supported compilers are detailed here:
    # http://fmtlib.net/latest/index.html#portability
    conflicts('%gcc@:4.3.999', when='@5:')
    conflicts('%llvm@:2.8.999', when='@5:')

    variant('pic', default=True, description='Enable generation of position-independent code')

    def cmake_args(self):
        spec = self.spec
        args = []
        if '+pic' in spec:
            args.extend([
                '-DCMAKE_C_FLAGS={0}'.format(self.compiler.pic_flag),
                '-DCMAKE_CXX_FLAGS={0}'.format(self.compiler.pic_flag)
            ])
        return args
