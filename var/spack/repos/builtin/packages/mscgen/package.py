# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Mscgen(AutotoolsPackage):
    """Mscgen is a small program that parses Message Sequence Chart descriptions
    and produces PNG, SVG, EPS or server side image maps (ismaps) as the
    output."""

    homepage = "http://www.mcternan.me.uk/mscgen/"
    url      = "http://www.mcternan.me.uk/mscgen/software/mscgen-src-0.20.tar.gz"

    version('0.20', '65c90fb5150d7176b65b793f0faa7377')

    depends_on('flex')
    depends_on('bison')
    depends_on('pkgconf')
    depends_on('libgd')
