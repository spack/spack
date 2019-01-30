# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class UfoFilters(CMakePackage):
    """The UFO data processing framework is a C library suited to build general
    purpose streams data processing on heterogeneous architectures such as
    CPUs, GPUs or clusters. This package contains filter plugins."""

    homepage = "https://ufo.kit.edu"
    url      = "https://github.com/ufo-kit/ufo-filters/archive/v0.14.1.tar.gz"

    version('0.14.1', 'f2a81f5d38cfa71de58cbb5279782297')

    depends_on('ufo-core')
