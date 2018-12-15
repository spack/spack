# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ilmbase(AutotoolsPackage):
    """OpenEXR ILM Base libraries (high dynamic-range image file format)"""

    homepage = "http://www.openexr.com/"
    url      = "https://github.com/openexr/openexr/releases/download/v2.3.0/ilmbase-2.3.0.tar.gz"

    version('2.3.0', sha256='456978d1a978a5f823c7c675f3f36b0ae14dba36638aeaa3c4b0e784f12a3862')

    version('2.2.0', 'b540db502c5fa42078249f43d18a4652',
            url='http://download.savannah.nongnu.org/releases/openexr/ilmbase-2.2.0.tar.gz')
    version('2.1.0', 'af1115f4d759c574ce84efcde9845d29',
            url='http://download.savannah.nongnu.org/releases/openexr/ilmbase-2.1.0.tar.gz')
    version('2.0.1', '74c0d0d2873960bd0dc1993f8e03f0ae',
            url='http://download.savannah.nongnu.org/releases/openexr/ilmbase-2.0.1.tar.gz')
    version('1.0.2', '26c133ee8ca48e1196fbfb3ffe292ab4',
            url='http://download.savannah.nongnu.org/releases/openexr/ilmbase-1.0.2.tar.gz')
    version('0.9.0', '4df45f8116cb7a013b286caf6da30a2e',
            url='http://download.savannah.nongnu.org/releases/openexr/ilmbase-0.9.0.tar.gz')
