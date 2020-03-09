# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack import *


class Opengl(Package):
    """Placeholder for external OpenGL libraries from hardware vendors"""

    homepage = "https://www.opengl.org/"

    provides('gl')
    provides('gl@:4.5', when='@4.5:')
    provides('gl@:4.4', when='@4.4:')
    provides('gl@:4.3', when='@4.3:')
    provides('gl@:4.2', when='@4.2:')
    provides('gl@:4.1', when='@4.1:')
    provides('gl@:3.3', when='@3.3:')

    if sys.platform != 'darwin':
        provides('glx@1.4')

    # Override the fetcher method to throw a useful error message;
    # fixes GitHub issue (#7061) in which this package threw a
    # generic, uninformative error during the `fetch` step,
    @property
    def fetcher(self):
        msg = """This package is intended to be a placeholder for
        system-provided OpenGL libraries from hardware vendors.  Please
        download and install OpenGL drivers/libraries for your graphics
        hardware separately, and then set that up as an external package.
        An example of a working packages.yaml:

        packages:
          opengl:
            paths:
              opengl@4.5.0: /opt/opengl
            buildable: False

        In that case, /opt/opengl/ should contain these two folders:

        include/GL/       (opengl headers, including "gl.h")
        lib               (opengl libraries, including "libGL.so")

        On Apple Darwin (e.g., OS X, macOS) systems, this package is
        normally installed as part of the XCode Command Line Tools in
        /usr/X11R6, so a working packages.yaml would be

        packages:
          opengl:
            paths:
              opengl@4.1: /usr/X11R6
            buildable: False

        In that case, /usr/X11R6 should contain

        include/GL/      (OpenGL headers, including "gl.h")
        lib              (OpenGL libraries, including "libGL.dylib")

        On OS X/macOS, note that the version of OpenGL provided
        depends on your hardware. Look at
        https://support.apple.com/en-us/HT202823 to see what version
        of OpenGL your Mac uses."""
        raise InstallError(msg)

    @property
    def libs(self):
        for dir in ['lib64', 'lib']:
            libs = find_libraries('libGL', join_path(self.prefix, dir),
                                  shared=True, recursive=False)
            if libs:
                return libs
