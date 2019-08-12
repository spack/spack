# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class AllpathsLg(AutotoolsPackage):
    """ALLPATHS-LG is our original short read assembler and it works on both
       small and large (mammalian size) genomes."""

    homepage = "http://www.broadinstitute.org/software/allpaths-lg/blog/"
    url      = "ftp://ftp.broadinstitute.org/pub/crd/ALLPATHS/Release-LG/latest_source_code/LATEST_VERSION.tar.gz"

    version('52488', 'bde9008e236d87708a48eb83af6d6d5b')

    # compiles with gcc 4.7.0 to 4.9.4)
    conflicts('%gcc@:4.6.4,5.1.0:')
    conflicts('%cce')
    conflicts('%clang')
    conflicts('%intel')
    conflicts('%nag')
    conflicts('%pgi')
    conflicts('%xl')
    conflicts('%xl_r')
