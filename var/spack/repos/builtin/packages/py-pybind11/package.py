# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

import spack.build_systems.cmake
import spack.build_systems.python
from spack.package import *


class PyPybind11(CMakePackage, PythonExtension):
    """pybind11 -- Seamless operability between C++11 and Python.

    pybind11 is a lightweight header-only library that exposes C++ types in
    Python and vice versa, mainly to create Python bindings of existing C++
    code. Its goals and syntax are similar to the excellent Boost.Python
    library by David Abrahams: to minimize boilerplate code in traditional
    extension modules by inferring type information using compile-time
    introspection.
    """

    homepage = "https://pybind11.readthedocs.io"
    url = "https://github.com/pybind/pybind11/archive/refs/tags/v2.10.1.tar.gz"
    git = "https://github.com/pybind/pybind11.git"

    maintainers("ax3l")

    version(
        "2.11.1",
        sha256="33cdd02a6453380dd71cc70357ce388ad1ee8d32bd0e38fc22b273d050aa29b3",
        url="https://pypi.org/packages/06/55/9f73c32dda93fa4f539fafa268f9504e83c489f460c380371d94296126cd/pybind11-2.11.1-py3-none-any.whl",
    )
    version(
        "2.11.0",
        sha256="307443ea89b73ce88f68fa48687d160c036622a54bc2a25aae9d5ea792bef268",
        url="https://pypi.org/packages/6d/88/37445fde2baddf06e13753b722c4d82b60a9844784567a80a04e9b6c6c74/pybind11-2.11.0-py3-none-any.whl",
    )
    version(
        "2.10.4",
        sha256="ec9be0c45061c829648d7e8c98a7d041768b768c934acd15196e0f1943d9a818",
        url="https://pypi.org/packages/52/ed/68e989fdac8f352cb6d506fac111ba1e1b74c0ef3660fadeeeeb765bc03c/pybind11-2.10.4-py3-none-any.whl",
    )
    version(
        "2.10.3",
        sha256="123e303f39ad5de97ddfa4f1f473cb85881a0a94ee5714eb3c37e2405371fc12",
        url="https://pypi.org/packages/17/4e/9b2f39b5d0ae5f81541e03a98379462871ccfbadfa315d24b3d8854c6a9f/pybind11-2.10.3-py3-none-any.whl",
    )
    version(
        "2.10.2",
        sha256="51507b4bcb2ce078fcc548e5ba46e9461f9706333fb75ad4ec6ee3ac375a6766",
        url="https://pypi.org/packages/fd/46/092d59dca8fb4a64592ba2752ae5688b9ea7591b924292d06db9cc5212a8/pybind11-2.10.2-py3-none-any.whl",
    )
    version(
        "2.10.1",
        sha256="ebf3eeac46859a2e10077ae45378ba3f33d999a9064697a3464fba1a4a04fc0a",
        url="https://pypi.org/packages/1d/53/e6b27f3596278f9dd1d28ef1ddb344fd0cd5db98ef2179d69a2044e11897/pybind11-2.10.1-py3-none-any.whl",
    )
    version(
        "2.10.0",
        sha256="6bbc7a2f79689307f0d8d240172851955fc214b33e4cbd7fdbc9cd7176a09260",
        url="https://pypi.org/packages/9a/7f/855560aa568e50bea6012ed535e6b8c436e99394f3e5a649d44d2e557242/pybind11-2.10.0-py3-none-any.whl",
    )
    version(
        "2.9.2",
        sha256="20f56674da31c96bca7569b91e60f2bd30d693f0728541412ec927574f7bc9df",
        url="https://pypi.org/packages/fd/24/efc9e62aa1baa48622028c59ae2c70fa134801e8acbdf30e5b594fe5a360/pybind11-2.9.2-py2.py3-none-any.whl",
    )
    version(
        "2.9.1",
        sha256="b570d17ed34b0f8ff43f5647833db87353be9afca0c7d1d69e92706b10a9c961",
        url="https://pypi.org/packages/11/88/98f65ae2e34cb52cda4ce16fd0839d482fbb5b690cb2f8b93d24aaa018fa/pybind11-2.9.1-py2.py3-none-any.whl",
    )
    version(
        "2.9.0",
        sha256="0c178c6e5806e8e58a7eec5a363d052bb9dac860a3ff64fbddb7226110644977",
        url="https://pypi.org/packages/70/1e/c7995fc7a0b0ec24bdb20b38f738e4f242250842717efa869e3fc4ce22fe/pybind11-2.9.0-py2.py3-none-any.whl",
    )

    extends("python")

    with when("build_system=cmake"):
        generator("ninja")

    # https://github.com/pybind/pybind11/#supported-compilers
    conflicts("%clang@:3.2")
    conflicts("%apple-clang@:4")
    conflicts("%gcc@:4.7")
    conflicts("%msvc@:16")
    conflicts("%intel@:17")

    # https://github.com/pybind/pybind11/pull/1995
    @when("@:2.4")
    def patch(self):
        """see https://github.com/spack/spack/issues/13559"""
        filter_file(
            "import sys",
            'import sys; return "{0}"'.format(self.prefix.include),
            "pybind11/__init__.py",
            string=True,
        )


class CMakeBuilder(spack.build_systems.cmake.CMakeBuilder):
    def cmake_args(self):
        return [self.define("PYBIND11_TEST", self.pkg.run_tests)]

    def install(self, pkg, spec, prefix):
        super().install(pkg, spec, prefix)
        python_builder = spack.build_systems.python.PythonPipBuilder(pkg)
        python_builder.install(pkg, spec, prefix)

    def setup_build_environment(self, env):
        env.set("PYBIND11_USE_CMAKE", 1)

    @run_after("install")
    def install_test(self):
        if not self.pkg.run_tests:
            return

        with working_dir("spack-test", create=True):
            # test include helper points to right location
            python = self.spec["python"].command
            py_inc = python(
                "-c", "import pybind11 as py; print(py.get_include())", output=str
            ).strip()
            for inc in [py_inc, self.prefix.include]:
                inc_file = join_path(inc, "pybind11", "pybind11.h")
                assert os.path.isfile(inc_file)
