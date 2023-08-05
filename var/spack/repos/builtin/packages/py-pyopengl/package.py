# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class PyPyopengl(PythonPackage):
    """PyOpenGL is the most common cross platform Python binding to OpenGL and related APIs."""

    homepage = "http://pyopengl.sourceforge.net"
    url = "https://files.pythonhosted.org/packages/py3/p/pyopengl/PyOpenGL-3.1.6-py3-none-any.whl"
    list_url = "https://pypi.org/simple/pyopengl/"

    version(
        "3.1.6",
        sha256="a7139bc3e15d656feae1f7e3ef68c799941ed43fadc78177a23db7e946c20738",
        expand=False,
    )

    variant(
        "gl",
        default="glx" if sys.platform.startswith("linux") else "other",
        values=("glx", "osmesa", "other"),
        multi=False,
        description="The OpenGL provider to use",
    )
    variant("glu", default=True)
    variant("glut", default=True)

    conflicts("osmesa", when="gl=glx")
    conflicts("osmesa", when="gl=other")
    conflicts("glx", when="gl=osmesa")
    conflicts("glx", when="gl=other")

    depends_on("python@3.6:", type=("build", "run"))
    # actually installing PyOpenGL itself just requires python
    # but tests (and possibly dependent packages) need OpenGL libraries
    depends_on("gl", type=("build", "run"))
    depends_on("glx", when="gl=glx", type=("build", "run"))
    depends_on("osmesa", when="gl=osmesa", type=("build", "run"))
    depends_on("glu", when="+glu", type=("build", "run"))
    depends_on("freeglut", when="+glut", type=("build", "run"))

    def setup_build_environment(self, env):
        # PyOpenGL uses ctypes.cdll (or similar), which searches LD_LIBRARY_PATH
        lib_dirs = self.spec["gl"].libs.directories
        if "gl=glx" in self.spec:
            lib_dirs.extend(self.spec["glx"].libs.directories)
            env.set("PYOPENGL_PLATFORM", "glx")
        if "gl=osmesa" in self.spec:
            lib_dirs.extend(self.spec["osmesa"].libs.directories)
            env.set("PYOPENGL_PLATFORM", "osmesa")
        if "+glu" in self.spec:
            lib_dirs.extend(self.spec["glu"].libs.directories)
        if "+glut" in self.spec:
            lib_dirs.append(self.spec["freeglut"].prefix.lib)
        libs = ":".join(lib_dirs)
        if sys.platform == "darwin":
            env.prepend_path("DYLD_FALLBACK_LIBRARY_PATH", libs)
        else:
            env.prepend_path("LD_LIBRARY_PATH", libs)

    def setup_run_environment(self, env):
        self.setup_build_environment(env)

    def setup_dependent_build_environment(self, env, dependent_spec):
        self.setup_build_environment(env)

    # only test import available module
    @property
    def import_modules(self):
        modules = ["OpenGL", "OpenGL.GL"]
        if "gl=glx" in self.spec:
            modules.append("OpenGL.GLX")
        if "gl=osmesa" in self.spec:
            modules.append("OpenGL.osmesa")
        if "+glu" in self.spec:
            modules.append("OpenGL.GLU")
        if "+glut" in self.spec:
            modules.append("OpenGL.GLUT")
        if "^python+tkinter" in self.spec:
            modules.append("OpenGL.Tk")

        return modules
