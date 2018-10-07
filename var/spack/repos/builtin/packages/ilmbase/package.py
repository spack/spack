# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ilmbase(AutotoolsPackage):
    """OpenEXR ILM Base libraries (high dynamic-range image file format)"""

    homepage = "http://www.openexr.com/"
    url      = "http://download.savannah.nongnu.org/releases/openexr/ilmbase-2.2.0.tar.gz"

    version('2.2.0', 'b540db502c5fa42078249f43d18a4652')
    version('2.1.0', 'af1115f4d759c574ce84efcde9845d29')
    version('2.0.1', '74c0d0d2873960bd0dc1993f8e03f0ae')
    version('1.0.2', '26c133ee8ca48e1196fbfb3ffe292ab4')
    version('0.9.0', '4df45f8116cb7a013b286caf6da30a2e')
