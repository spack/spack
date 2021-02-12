# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
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

    version('0.16.0', sha256='80d6444d92f999787e4470b2c1c4dae5a81db1058e72b292ebfe662ee56471cd')
    version('0.15.1', sha256='9ae303b43f8771693342d41099d1884c572580fa4a022c7618b4adaf420bf7b4')
    version('0.15.0', sha256='f682ac91fcff5610d4d92669881bd5baf3d7b71ab8c5713f3f1fadbdf336a9d4')
    version('0.14.1', sha256='084d7cdef59205e1a048e5c142be1ffeaacedc42965824b642e8302ef30ebb13')

    depends_on('ufo-core')
