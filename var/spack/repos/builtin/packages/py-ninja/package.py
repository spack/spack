# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyNinja(PythonPackage):
    """Ninja is a small build system with a focus on speed."""

    homepage = "https://ninja-build.org"
    pypi = "ninja/ninja-1.10.2.2.tar.gz"

    version('1.10.2.2', sha256='3f8a75acd929abb9f003d3aa5bc299cea30b9db0dfa18669877e9c02ddcf530d')

    depends_on('py-scikit-build', type='build')
