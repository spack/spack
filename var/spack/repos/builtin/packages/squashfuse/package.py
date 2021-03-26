# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Squashfuse(AutotoolsPackage):
    """squashfuse - Mount SquashFS archives using FUSE"""

    homepage = "https://github.com/vasi/squashfuse"
    url      = "https://github.com/vasi/squashfuse/releases/download/0.1.103/squashfuse-0.1.103.tar.gz"
    git      = "https://github.com/vasi/squashfuse.git"

    maintainers = ['haampie']

    # there hasn't been a release for a while, and the master branch introduces
    # support for fuse@3:, so we have our own spack version here (46 commits
    # after 0.1.103)
    version('master', branch='master')
    version('0.1.103-46', commit='e5dddbfc6e402c82f5fbba115b0eb3476684f50d', preferred=True)

    # official releases
    version('0.1.103', sha256='42d4dfd17ed186745117cfd427023eb81effff3832bab09067823492b6b982e7')

    depends_on('libfuse@2.5:')
    depends_on('libfuse@:2.99', when='@0.1.103')

    # Note: typically libfuse is external, but this implies that you have to make
    # pkg-config external too, because spack's pkg-config doesn't know how to
    # locate system pkg-config's fuse.pc/fuse3.pc
    depends_on('pkg-config', type='build')

    # compression libs
    depends_on('zlib')
    depends_on('lz4')
    depends_on('lzo')
    depends_on('xz')
    depends_on('zstd')

    # build deps for non-tarball versions
    depends_on('m4',       type='build', when='@master,0.1.103-46')
    depends_on('autoconf', type='build', when='@master,0.1.103-46')
    depends_on('automake', type='build', when='@master,0.1.103-46')
    depends_on('libtool',  type='build', when='@master,0.1.103-46')

    def configure_args(self):
        return ['--disable-demo']
