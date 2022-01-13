# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCmakeFormat(PythonPackage):
    """cmake-format project provides Quality Assurance (QA) tools for
    cmake. Tools include cmake-annotate, cmake-format, cmake-lint,
    and ctest-to."""

    homepage = "https://pypi.python.org/pypi/cmake-format"
    url      = "https://github.com/cheshirekow/cmake_format/archive/v0.6.13.tar.gz"

    version('0.6.13', sha256='b67dd150380d9223036a12f82126a7a9b18e77db4a8d7240f993ee090884e4bf')
    version('0.6.10', sha256='82f0ef16236225cb43f45bfb6983ef7f6f72634727a1a6c26290402527bdd793')
    version('0.6.9', sha256='b2f8bf2e9c6651126f2f2954b7803222b0faf6b8649eabc4d965ea97483a4d20')
    version('0.6.0', sha256='fc9795907c508b4a1f851eba311bd7478b374a4ba4430cdda976ebbec440376a')
    version('0.4.5', sha256='16602408c774cd989ecfa25883de4c2dbac937e3890b735be4aab76f9647875a')

    depends_on('py-setuptools',  type=('build', 'run'))
    depends_on('py-six@1.13.0:', type=('build', 'run'))
    depends_on('py-pyyaml', type=('run'))
