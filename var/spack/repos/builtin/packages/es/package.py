# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Es(AutotoolsPackage):

    """Es is an extensible shell. The language was derived from the Plan 9
    shell, rc, and was influenced by functional programming languages,
    such as Scheme, and the Tcl embeddable programming language. This
    implementation is derived from Byron Rakitzis's public domain
    implementation of rc."""

    homepage = "http://wryun.github.io/es-shell/"
    url      = "https://github.com/wryun/es-shell/releases/download/v0.9.1/es-0.9.1.tar.gz"

    version('0.9.1', 'bf4db55b47bcc99892468b2e0aec0c9e')

    depends_on('readline')
