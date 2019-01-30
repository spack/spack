# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class UfoCore(CMakePackage):
    """The UFO data processing framework is a C library suited to build general
    purpose streams data processing on heterogeneous architectures such as
    CPUs, GPUs or clusters. This package contains the run-time system and
    development files."""

    homepage = "https://ufo.kit.edu"
    url      = "https://github.com/ufo-kit/ufo-core/archive/v0.14.0.tar.gz"

    version('0.14.0', '3bd94d10d0f589953aba11821a8295f3')

    depends_on('glib')
    depends_on('json-glib')
