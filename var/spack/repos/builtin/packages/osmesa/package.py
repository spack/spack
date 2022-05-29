# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import llnl.util.tty as tty
from spack import *

class Osmesa(BundlePackage):
    """Shim package for the OSMesa OpenGL library."""
    homepage = 'https://www.mesa3d.org'

    version('11.2.0')
    
    depends_on('libosmesa')
    provides('gl@4.5')

    @property
    def root(self):
        return self.spec['libosmesa'].root

    @property
    def headers(self):
        return self.spec['libosmesa'].headers

    @property
    def libs(self):
        return self.spec['libosmesa'].libs

    @property
    def gl_headers(self):
        return find_headers('GL/gl',
                            root=self.gl_root,
                            recursive=True)

    @property
    def gl_libs(self):
        return self.spec['libosmesa'].libs
