# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGevent(PythonPackage):
    """gevent is a coroutine-based Python networking library."""

    homepage = "https://www.gevent.org"
    pypi = "gevent/gevent-1.3a2.tar.gz"

    version("21.12.0", sha256="f48b64578c367b91fa793bf8eaaaf4995cb93c8bc45860e473bf868070ad094e")
    version("21.8.0", sha256="43e93e1a4738c922a2416baf33f0afb0a20b22d3dba886720bc037cd02a98575")
    version("1.5.0", sha256="b2814258e3b3fb32786bb73af271ad31f51e1ac01f33b37426b66cb8491b4c29")
    version("1.3a2", sha256="f7ab82697111ea233c7beeadf5240f669dfad9c4bbc89a3ec80a49e2c48a65bd")

    depends_on("python@2.7:2,3.6:", when="@21.8:", type=("build", "run"))
    depends_on("python@2.7:2,3.5:", when="@1.5:", type=("build", "run"))
    depends_on("python@2.7:2,3.4:", type=("build", "run"))
    depends_on("py-setuptools@40.8:", when="@20.5.1:", type=("build", "run"))
    depends_on("py-setuptools@40.8:", when="@1.5:", type="build")
    depends_on("py-setuptools@24.2:", when="@:1.4", type="build")
    depends_on("py-cython@3.0.0a9:", when="@20.5.1:", type="build")
    depends_on("py-cython@0.29.14:", when="@1.5:", type="build")
    depends_on("py-cython@0.27:", when="@:1.4", type="build")
    depends_on("py-cython@0.27:", when="@:1.4", type="build")
    depends_on("py-cffi@1.12.3:", when="@1.5:", type=("build", "run"))  # from pyproject.toml
    depends_on("py-cffi@1.4:", when="@:1.4", type=("build", "run"))
    depends_on("py-greenlet@1.1:1", when="@21.8:", type=("build", "run"))
    depends_on("py-greenlet@0.4.17:1", when="@20.12:", type=("build", "run"))
    depends_on("py-greenlet@0.4.14:", when="@1.5:", type=("build", "run"))
    depends_on("py-greenlet@0.4.13:", when="@:1.4", type=("build", "run"))
    depends_on("py-zope-event", when="@20.5.1:", type=("build", "run"))
    depends_on("py-zope-interface", when="@20.5.1:", type=("build", "run"))

    # Deprecated compiler options. upstream PR: https://github.com/gevent/gevent/pull/1896
    patch("icc.patch", when="%intel")

    def flag_handler(self, name, flags):
        if name == "cflags":
            if self.spec.satisfies("%oneapi@2023:"):
                flags.append("-Wno-error=incompatible-function-pointer-types")
        return (flags, None, None)
