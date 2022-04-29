# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re
import sys

import llnl.util.tty as tty


class Opengl(Package):
    """Placeholder for external OpenGL libraries from hardware vendors"""

    has_code = False

    homepage = "https://www.opengl.org/"

    version('4.5')

    is_linux = sys.platform.startswith('linux')
    variant('glx', default=is_linux, description="Enable GLX API.")
    variant('egl', default=False, description="Enable EGL API.")
    variant('glvnd', default=is_linux,
            description="Expose Graphics APIs through libglvnd")

    provides('gl', when='~glvnd')

    provides('glx@1.4', when='~glvnd +glx')
    provides('egl@1.5', when='~glvnd +egl')

    # NOTE: This package should have a dependency on libglvnd, but because it
    # is exclusively provided externally the dependency is never traversed.
    # depends_on('libglvnd', when='+glvnd')  # don't uncomment this

    provides('libglvnd-be-gl', when='+glvnd')
    provides('libglvnd-be-glx', when='+glvnd +glx')
    provides('libglvnd-be-egl', when='+glvnd +egl')

    executables = ['^glxinfo$']

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)(output=str, error=str)
        match = re.search(r'OpenGL version string: (\S+)', output)
        return match.group(1) if match else None

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
            buildable: False
            externals:
            - spec: opengl@4.5.0
              prefix: /opt/opengl

        In that case, /opt/opengl/ should contain these two folders:

        include/GL/       (opengl headers, including "gl.h")
        lib               (opengl libraries, including "libGL.so")

        On Apple Darwin (e.g., OS X, macOS) systems, this package is
        normally installed as part of the XCode Command Line Tools in
        /usr/X11R6, so a working packages.yaml would be

        packages:
          opengl:
            buildable: False
            externals:
            - spec: opengl@4.1
              prefix: /usr/X11R6

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
        spec = self.spec
        libs_to_seek = set()

        tty.debug("Previously found libraries may no longer be found." +
                  " Refer to OpenGL section of documentation for more information")

        if '~glvnd' in spec:
            if '+glx' in spec:
                libs_to_seek.add('libGL')

            if '+egl' in spec:
                libs_to_seek.add('libEGL')

            if '+opengl' in spec:
                libs_to_seek.add('libGL')

        if libs_to_seek:
            return find_libraries(list(libs_to_seek),
                                  root=self.spec.prefix,
                                  recursive=True)
        return LibraryList(())

    @property
    def glx_libs(self):
        return find_libraries('libGL',
                              root=self.spec.prefix,
                              recursive=True)

    @property
    def egl_libs(self):
        return find_libraries('libEGL',
                              root=self.spec.prefix,
                              recursive=True)

    @property
    def gl_libs(self):
        return find_libraries('libGL',
                              root=self.spec.prefix,
                              recursive=True)

    def setup_run_environment(self, env):
        if '+glx +glvnd' in self.spec:
            env.set('__GLX_VENDOR_LIBRARY_NAME',
                    self.spec.extra_attributes['glvnd']['glx'])

        if '+egl +glvnd' in self.spec:
            env.set('__EGL_VENDOR_LIBRARY_FILENAMES',
                    self.spec.extra_attributes['glvnd']['egl'])
