# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fermisciencetools(Package):
    """The Fermi Science Tools consists of the basic tools necessary to
    analyze Fermi data.

    This is the binary version for Linux x86_64 with libc-2.17."""

    homepage = "https://fermi.gsfc.nasa.gov/ssc/data/analysis/software/"
    url      = "https://fermi.gsfc.nasa.gov/ssc/data/analysis/software/v11r5p3/ScienceTools-v11r5p3-fssc-20180124-x86_64-unknown-linux-gnu-libc2.17.tar.gz"

    # Now we are using the binary distribution. The source distribution is also
    # available, but there might be some logical errors in the configure codes,
    # which leads to failing in building it from source. Hopefully someone else
    # can figure it out and we can use the source distribution instead.
    version('11r5p3', 'cf050ddddfe9251b6ebe8d3fd7de3c3f')

    def install(self, spec, prefix):
        install_tree('x86_64-unknown-linux-gnu-libc2.17', prefix)
