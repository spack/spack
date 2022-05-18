# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re
import sys


class Opengl(BundlePackage):
    """Placeholder for external OpenGL libraries from hardware vendors"""

    homepage = "https://www.opengl.org/"

    # Supported OpenGL versions:
    # 1.0 1.1 1.2 1.3 1.4 1.5
    # 2.0 2.1
    # 3.0 3.1 3.2 3.3
    # 4.0 4.1 4.2 4.3 4.4 4.5 4.6
    for ver_major in [
        (1, [0, 1, 2, 3, 4, 5]),
        (2, [0, 1]),
        (3, [0, 1, 2, 3]),
        (4, [0, 1, 2, 3, 4, 5]),
    ]:
        for ver_minor in ver_major[1]:
            ver = "{0}.{1}".format(ver_major[0], ver_minor)
            version(ver)
            provides("gl@:{0}".format(ver), when="@{0}".format(ver))

    # The last version needs to be open-ended
    version('4.6')
    provides("gl@:4.6", when="@4.6:")

    # This should really be when='platform=linux' but can't because of a
    # current bug in when and how ArchSpecs are constructed
    if sys.platform == "linux":
        provides("glx@1.4")

    executables = ["^glxinfo$"]

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)(output=str, error=str)
        match = re.search(r"OpenGL version string: (\S+)", output)
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
        if "platform=windows" in self.spec:
            return find_libraries("opengl32", self.prefix, shared=True, recursive=True)
        else:
            return find_libraries("libGL", self.prefix, shared=True, recursive=True)

    @property
    def glx_libs(self):
        return find_libraries("libGL",
                              root=self.spec.prefix,
                              recursive=True)

    @property
    def gl_libs(self):
        if "platform=windows" in self.spec:
            return find_libraries("opengl32", self.prefix, shared=True, recursive=True)
        else:
            return find_libraries("libGL", self.prefix, shared=True, recursive=True)
