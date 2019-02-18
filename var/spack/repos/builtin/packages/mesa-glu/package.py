# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class MesaGlu(AutotoolsPackage):
    """This package provides the Mesa OpenGL Utility library."""

    homepage = "https://www.mesa3d.org"
    url      = "https://www.mesa3d.org/archive/glu/glu-9.0.0.tar.gz"

    version('9.0.0', 'bbc57d4fe3bd3fb095bdbef6fcb977c4')

    variant('mesa', default=True,
       description='Usually depends on mesa, disable for accelerated OpenGL')
    depends_on('mesa', when='+mesa')

    provides('glu@1.3')

    @property
    def libs(self):
        for dir in ['lib64', 'lib']:
            libs = find_libraries('libGLU', join_path(self.prefix, dir),
                                  shared=True, recursive=False)
            if libs:
                return libs
