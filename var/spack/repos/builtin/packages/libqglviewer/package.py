# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class Libqglviewer(QMakePackage):
    """libQGLViewer is a C++ library based on Qt that eases the creation of
    OpenGL 3D viewers."""

    homepage = "http://libqglviewer.com/"
    url      = "http://libqglviewer.com/src/libQGLViewer-2.7.2.tar.gz"
    git      = "https://github.com/GillesDebunne/libQGLViewer.git"

    version('2.7.2', sha256='e2d2799dec5cff74548e951556a1fa06a11d9bcde2ce6593f9c27a17543b7c08')

    # http://libqglviewer.com/installUnix.html

    depends_on('qt+opengl')
    depends_on('freeglut', when='^qt@:3.0')

    build_directory = 'QGLViewer'

    def qmake_args(self):
        return ['PREFIX=' + self.prefix]
