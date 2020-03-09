# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Neovim(CMakePackage):
    """NeoVim: the future of vim"""

    homepage = "http://neovim.io"
    url      = "https://github.com/neovim/neovim/archive/v0.3.4.tar.gz"

    version('0.3.4', sha256='a641108bdebfaf319844ed46b1bf35d6f7c30ef5aeadeb29ba06e19c3274bc0e')
    version('0.3.1', sha256='bc5e392d4c076407906ccecbc283e1a44b7832c2f486cad81aa04cc29973ad22')
    version('0.3.0', sha256='f7acb61b16d3f521907d99c486b7a9f1e505e8b2a18c9ef69a6d7f18f29f74b8')
    version('0.2.2', sha256='a838ee07cc9a2ef8ade1b31a2a4f2d5e9339e244ade68e64556c1f4b40ccc5ed')
    version('0.2.1', sha256='9e2c068a8994c9023a5f84cde9eb7188d3c85996a7e42e611e3cd0996e345dd3')
    version('0.2.0', sha256='72e263f9d23fe60403d53a52d4c95026b0be428c1b9c02b80ab55166ea3f62b5')

    depends_on('lua@5.1:5.2')
    depends_on('lua-lpeg')
    depends_on('lua-mpack')
    depends_on('lua-bitlib')
    depends_on('libuv')
    depends_on('jemalloc')
    depends_on('libtermkey')
    depends_on('libvterm')
    depends_on('unibilium')
    depends_on('msgpack-c')
    depends_on('gperf')

    def cmake_args(self):
        args = []
        if self.version >= Version('0.2.1'):
            args = ['-DPREFER_LUA=ON']

        return args
