# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Neovim(CMakePackage):
    """NeoVim: the future of vim"""

    homepage = "http://neovim.io"
    url      = "https://github.com/neovim/neovim/archive/v0.2.0.tar.gz"

    version('0.3.1', '5405bced1c929ebc245c75409cd6c7ef')
    version('0.3.0', 'e5fdb2025757c337c17449c296eddf5b')
    version('0.2.2', '44b69f8ace88b646ec890670f1e462c4')
    version('0.2.1', 'f4271f22d2a46fa18dace42849c56a98')
    version('0.2.0', '9af7f61f9f0b1a2891147a479d185aa2')

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
