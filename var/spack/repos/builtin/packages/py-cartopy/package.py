# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCartopy(PythonPackage):
    """Cartopy - a cartographic python library with matplotlib support."""

    homepage = "https://scitools.org.uk/cartopy/docs/latest/"
    pypi = "Cartopy/Cartopy-0.20.2.tar.gz"

    maintainers("adamjstewart")
    skip_modules = ["cartopy.tests"]

    version("0.21.1", sha256="89d5649712c8582231c6e11825a04c85f6f0cee94dbb89e4db23eabca1cc250a")
    version("0.21.0", sha256="ce1d3a28a132e94c89ac33769a50f81f65634ab2bd40556317e15bd6cad1ce42")
    version("0.20.3", sha256="0d60fa2e2fbd77c4d1f6b1f9d3b588966147f07c1b179d2d34570ac1e1b49006")
    version("0.20.2", sha256="4d08c198ecaa50a6a6b109d0f14c070e813defc046a83ac5d7ab494f85599e35")
    version("0.20.1", sha256="91f87b130e2574547a20cd634498df97d797abd12dcfd0235bc0cdbcec8b05e3")
    version("0.20.0", sha256="eae58aff26806e63cf115b2bce9477cedc4aa9f578c5e477b2c25cfa404f2b7a")
    version(
        "0.19.0.post1", sha256="4b8b4773a98ed7009fe17d9b6ec87ac3ac62b7d14634d7768c190eadc647d576"
    )
    version("0.18.0", sha256="7ffa317e8f8011e0d965a3ef1179e57a049f77019867ed677d49dcc5c0744434")
    version("0.17.0", sha256="424bd9e9ddef6e48cbdee694ce589ec431be8591f15b6cb93cb2b333a29b2c61")
    version("0.16.0", sha256="f23dffa101f43dd91e866a49ebb5f5048be2a24ab8a921a5c07edabde746d9a4")

    variant("epsg", default=False, when="@:0.19", description="Add support for epsg.io")
    variant(
        "ows",
        default=False,
        description="Add support for Open Geospatial Consortium (OGC) web service",
    )
    variant("plotting", default=False, description="Add plotting functionality")

    # pyproject.toml
    depends_on("py-setuptools@40.6:", when="@0.19:", type="build")
    depends_on("py-setuptools@0.7.2:", type="build")
    depends_on("py-cython@0.29.13:", when="@0.20:", type="build")
    depends_on("py-cython@0.29.2:", when="@0.19:", type="build")
    depends_on("py-cython@0.28:", when="@0.18:", type="build")
    depends_on("py-cython@0.15.1:", when="@0.17:", type="build")
    depends_on("py-cython", type="build")
    depends_on("py-setuptools-scm@7:", when="@0.20.3:", type="build")
    depends_on("py-setuptools-scm", when="@0.19:", type="build")
    depends_on("py-setuptools-scm-git-archive", when="@0.19:0.20.2", type="build")

    # setup.py
    depends_on("python@3.8:", when="@0.21:", type=("build", "run"))
    depends_on("python@:3.9", when="@:0.18", type=("build", "run"))
    depends_on("geos@3.7.2:", when="@0.20:")
    depends_on("geos@3.3.3:")
    depends_on("proj@8:", when="@0.20")
    depends_on("proj@4.9:7", when="@0.17:0.19")
    depends_on("proj@4.9:5", when="@:0.16")

    # requirements/default.txt
    depends_on("py-numpy@1.18:", when="@0.20:", type=("build", "run"))
    depends_on("py-numpy@1.13.3:", when="@0.19:", type=("build", "run"))
    depends_on("py-numpy@1.10:", when="@0.17:", type=("build", "run"))
    depends_on("py-numpy@1.6:", type=("build", "run"))
    depends_on("py-matplotlib@3.1:", when="@0.21:", type=("build", "run"))
    # https://github.com/SciTools/cartopy/issues/2086
    depends_on("py-matplotlib@3.1:3.5", when="@0.20", type=("build", "run"))
    depends_on("py-shapely@1.6.4:", when="@0.21.1:", type=("build", "run"))
    depends_on("py-shapely@1.6.4:1", when="@0.20:0.21.0", type=("build", "run"))
    depends_on("py-shapely@1.5.6:1", when="@:0.19", type=("build", "run"))
    depends_on("py-pyshp@2.1:", when="@0.20:", type=("build", "run"))
    depends_on("py-pyshp@2:", when="@0.19:", type=("build", "run"))
    depends_on("py-pyshp@1.1.4:", type=("build", "run"))
    depends_on("py-pyproj@3:", when="@0.20:", type=("build", "run"))
    depends_on("py-six@1.3:", when="@:0.18", type=("build", "run"))

    # requirements/epsg.txt
    with when("+epsg"):
        depends_on("py-pyepsg@0.2:", type="run")
        depends_on("py-pyepsg@0.4:", when="@0.18:", type="run")

    # requirements/ows.txt
    with when("+ows"):
        depends_on("py-owslib@0.18:", when="@0.20:", type="run")
        depends_on("py-owslib@0.8.11:", type="run")
        depends_on("pil@6.1:", when="@0.20:", type="run")
        depends_on("pil@1.7.8:", type="run")

    # requirements/plotting.txt
    with when("+plotting"):
        depends_on("gdal@2.3.2:+python", when="@0.20:", type="run")
        depends_on("gdal@1.10:+python", type="run")
        depends_on("pil@6.1:", when="@0.20:", type="run")
        depends_on("pil@1.7.8:", type="run")
        depends_on("py-scipy@1.3.1:", when="@0.20:", type="run")
        depends_on("py-scipy@0.10:", type="run")
        depends_on("py-matplotlib@1.5.1:3.5", when="@0.17:0.19", type="run")
        depends_on("py-matplotlib@1.3:3.5", when="@0.16", type="run")

    patch("proj6.patch", when="@0.17.0")

    def setup_build_environment(self, env):
        # Needed for `spack install --test=root py-cartopy`
        library_dirs = []
        for dep in self.spec.dependencies(deptype="link"):
            query = self.spec[dep.name]
            library_dirs.extend(query.libs.directories)

        # Cartopy uses ctypes.util.find_library, which searches LD_LIBRARY_PATH
        # Our RPATH logic works fine, but the unit tests fail without this
        libs = ":".join(library_dirs)
        if self.spec.satisfies("platform=darwin"):
            env.prepend_path("DYLD_FALLBACK_LIBRARY_PATH", libs)
        else:
            env.prepend_path("LD_LIBRARY_PATH", libs)

    # Needed for `spack test run py-cartopy`
    setup_run_environment = setup_build_environment

    # Needed for `spack test run py-foo` where `py-foo` depends on `py-cartopy`
    def setup_dependent_run_environment(self, env, dependent_spec):
        self.setup_build_environment(env)
