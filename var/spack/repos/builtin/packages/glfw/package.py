# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install glfw
#
# You can edit this file again by typing:
#
#     spack edit glfw
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Glfw(CMakePackage):
    """GLFW is an Open Source, multi-platform library for
    OpenGL, OpenGL ES and Vulkan development on the desktop. It
    provides a simple API for creating windows, contexts and
    surfaces, receiving input and events."""

    homepage = "https://www.glfw.org/"
    url      = "https://github.com/glfw/glfw/archive/3.3.2.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version('3.3.2', sha256='98768e12e615fbe9f3386f5bbfeb91b5a3b45a8c4c77159cef06b1f6ff749537')
    version('3.3.1', sha256='6bca16e69361798817a4b62a5239a77253c29577fcd5d52ae8b85096e514177f')
    version('3.3',   sha256='81bf5fde487676a8af55cb317830703086bb534c53968d71936e7b48ee5a0f3e')
    version('3.2.1', sha256='e10f0de1384d75e6fc210c53e91843f6110d6c4f3afbfb588130713c2f9d8fe8')
    version('3.2',   sha256='cb3aab46757981a39ae108e5207a1ecc4378e68949433a2b040ce2e17d8f6aa6')
    version('3.1.2', sha256='6ac642087682aaf7f8397761a41a99042b2c656498217a1c63ba9706d1eef122')
    version('3.1.1', sha256='4de311ec9bf43bfdc8423ddf93b91dc54dc73dcfbedfb0991b6fbb3a9baf245f')
    version('3.1',   sha256='2140f4c532e7ce4c84cb7e4c419d0979d5954fa1ce204b7646491bd2cc5bf308')
    version('3.0.4', sha256='a4e7c57db2086803de4fc853bd472ff8b6d2639b9aa16e6ac6b19ffb53958caf')
    version('3.0.3', sha256='7a182047ba6b1fdcda778b79aac249bb2328b6d141188cb5df29560715d01693')

    # FIXME: Add dependencies if required.
    # depends_on('foo')

    def cmake_args(self):
        # FIXME: Add arguments other than
        # FIXME: CMAKE_INSTALL_PREFIX and CMAKE_BUILD_TYPE
        # FIXME: If not needed delete this function
        args = []
        return args
