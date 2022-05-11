# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class Utf8proc(CMakePackage):
    """A clean C library for processing UTF-8 Unicode data:
    normalization, case-folding, graphemes, and more"""

    homepage = "https://juliastrings.github.io/utf8proc/"
    url      = "https://github.com/JuliaStrings/utf8proc/archive/v2.4.0.tar.gz"

    version('2.6.1', sha256='4c06a9dc4017e8a2438ef80ee371d45868bda2237a98b26554de7a95406b283b')
    version('2.6.0', sha256='b36ce1534b8035e7febd95c031215ed279ee9d31cf9b464e28b4c688133b22c5')
    version('2.5.0', sha256='d4e8dfc898cfd062493cb7f42d95d70ccdd3a4cd4d90bec0c71b47cca688f1be')
    version('2.4.0', sha256='b2e5d547c1d94762a6d03a7e05cea46092aab68636460ff8648f1295e2cdfbd7')

    depends_on('cmake@2.8.12:', type='build')
