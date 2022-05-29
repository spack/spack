# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *

class Glx(BundlePackage):
    """Shim package for the GLX library."""
    homepage = 'https://www.khronos.org/registry/OpenGL/index_gl.php'
    
    version('1.4')

    depends_on('libglx')
    provides('gl@4.5')

    @property
    def root(self):
        return self.spec['libglx'].root

    @property
    def headers(self):
        return self.spec['libglx'].headers

    @property
    def libs(self):
        return self.spec['libglx'].libs

    @property
    def gl_headers(self):
        return find_headers('GL/gl',
                            root=self.gl_root,
                            recursive=True)

    @property
    def gl_libs(self):
        return self.spec['libglx'].libs
