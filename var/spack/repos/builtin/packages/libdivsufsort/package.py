# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libdivsufsort(CMakePackage):
    """libdivsufsort is a software library that implements a
     lightweight suffix array construction algorithm."""

    homepage = "https://github.com/y-256/libdivsufsort"
    url      = "https://github.com/y-256/libdivsufsort/archive/2.0.1.tar.gz"

    version('2.0.1', 'a75c6be4715d3d659936f3a1ab8cb5c0')
