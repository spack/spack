# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Idba(AutotoolsPackage):
    """IDBA is a practical iterative De Bruijn Graph De Novo Assembler for
       sequence assembly in bioinfomatics."""

    homepage = "http://i.cs.hku.hk/~alse/hkubrg/projects/idba/"
    url      = "https://github.com/loneknightpy/idba/archive/1.1.3.tar.gz"

    version('1.1.3', '303d9b4af7a7498b56ac9698028b4e15')

    depends_on('m4', type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
