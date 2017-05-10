# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Xkbcomp(AutotoolsPackage):
    """The X Keyboard (XKB) Extension essentially replaces the core protocol
    definition of a keyboard. The extension makes it possible to specify
    clearly and explicitly most aspects of keyboard behaviour on a per-key
    basis, and to track more closely the logical and physical state of a
    keyboard. It also includes a number of keyboard controls designed to
    make keyboards more accessible to people with physical impairments."""

    homepage = "https://www.x.org/wiki/XKB/"
    url      = "https://www.x.org/archive/individual/app/xkbcomp-1.3.1.tar.gz"

    version('1.3.1', '9e8ca110ed40d4703f8f73d99bc81576')

    depends_on('libx11')
    depends_on('libxkbfile')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('bison', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
    depends_on('xkeyboard-config', type='build')

    def configure_args(self):
        datadir = os.path.join(self.spec['xkeyboard-config'].prefix, 'share')
        return [
            '--datadir={0}'.format(datadir)]
