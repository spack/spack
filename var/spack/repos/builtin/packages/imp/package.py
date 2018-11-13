# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Imp(CMakePackage):
    """IMP, the Integrative Modeling Platform."""

    homepage = "https://integrativemodeling.org"
    url      = "https://github.com/salilab/imp/archive/2.8.0.tar.gz"

    version('2.8.0', 'bc985d40dc63bb12e09d6d7403954645')

    depends_on('python@2.7:')
    depends_on('swig')
    depends_on('boost@1.40:')
    depends_on('hdf5')
    depends_on('eigen')
