# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ragel(AutotoolsPackage):
    """Ragel State Machine Compiler
    Ragel compiles executable finite state machines from regular
    languages. Ragel targets C, C++ and ASM. Ragel state machines can
    not only recognize byte sequences as regular expression machines
    do, but can also execute code at arbitrary points in the
    recognition of a regular language. Code embedding is done using
    inline operators that do not disrupt the regular language syntax.
    """
    homepage = "http://www.colm.net/open-source/ragel"
    git      = "git://colm.net/ragel.git"
    url      = "http://www.colm.net/files/ragel/ragel-6.10.tar.gz"

    version('20080319', sha256='82742f49da1327d134de3b81f11489cc070fb87723b602b7f1947bb391b4d3fe')
    version('20070429', sha256='bf05d4914f066602716417fffbd1c9c27185a29da823a3bd2803c52d9e4d6e25')
    version('20070122', sha256='c891bb5571d1e9de8e81c9d035e717bb85d715c14f648d61c862f58707b2aac7')
    version('7.0.3',    sha256='49982728635d44ca1d81b060395d0b2ac106058d88a5e49b15b74d5514660a3a')
    version('7.0.2',    sha256='741b042aa27402746d95b173cbd337f19cfa41db8f483db8925f50f03ca48048')
    version('7.0.1',    sha256='4375d666806619fffc19cbc4f7a833a9146aeadb86ad404f1ac142887c37b78a')
    version('7.0.0.12', sha256='3999ef97fb108b39d11d9b96986f5e05c74bd95de8dd474301d86c5aca887a74')
    version('7.0.0.11', sha256='08bac6ff8ea9ee7bdd703373fe4d39274c87fecf7ae594774dfdc4f4dd4a5340')
    version('7.0.0.10', sha256='40562bcac66a22dbea8357a35745bbcb1ab596c262d8691145ee11aafa6f8dec')
    version('7.0.0.9',  sha256='b9e6cac5d388398ac05d8ef15a07628f5e6de292e39f5ad92b8176379e8352f0')
    version('7.0.0.8',  sha256='fbbf0974c5dfecca9a9374d907a5bbb370caac5dcba463972e3835130f89ef24')
    version('7.0.0.7',  sha256='97e46b50c2b8d5dac5c918d3caa2f084c2cae0f4790519ff332e8bce997d2d86')
    version('7.0.0.6',  sha256='7a1f50f8cf1168ced7cb834edd697448d1d012795291527926d646b8d99a43db')
    version('7.0.0.5',  sha256='4485621ab545cb5ff16846d14648be0249f37e436e6dfa72635b6f569b104dd1')
    version('6.10', sha256='5f156edb65d20b856d638dd9ee2dfb43285914d9aa2b6ec779dac0270cd56c3f')

    depends_on('colm', type='build')
