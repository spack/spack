# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Discovardenovo(AutotoolsPackage):
    """DISCOVAR de novo is a large (and small) de novo genome assembler.
       It quickly generates highly accurate and complete assemblies using the
       same single library data as used by DISCOVAR. It currently doesn't
       support variant calling, for that, please use DISCOVAR instead."""

    homepage = "https://software.broadinstitute.org/software/discovar/blog/"
    url      = "ftp://ftp.broadinstitute.org/pub/crd/DiscovarDeNovo/latest_source_code/discovardenovo-52488.tar.gz"

    version('52488', '2b08c77b1b998d85be8048e5efb10358')

    # lots of compiler errors with GCC7, works with 4.8.5
    # and devs claim it works with 4.7 so I'm assuming 4.7-4.8'll work
    conflicts('%gcc@5:')
    conflicts('%gcc@:4.7.0')

    depends_on('samtools')
    depends_on('jemalloc')
