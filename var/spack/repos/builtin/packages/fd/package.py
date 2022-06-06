# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fd(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://github.com/sharkdp/fd"
    url      = "https://github.com/sharkdp/fd/archive/refs/tags/v8.4.0.tar.gz"

    version('8.4.0', sha256='d0c2fc7ddbe74e3fd88bf5bb02e0f69078ee6d2aeea3d8df42f508543c9db05d')

    depends_on('rust')

    def install(self, spec, prefix):
        cargo = which('cargo')
        cargo('install', '--root', prefix, '--path', '.')
