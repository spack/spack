# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlTextSimpletable(PerlPackage):
    """Simple Eyecandy ASCII Tables"""

    homepage = "http://search.cpan.org/~mramberg/Text-SimpleTable/lib/Text/SimpleTable.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/M/MR/MRAMBERG/Text-SimpleTable-2.04.tar.gz"

    version('2.07', sha256='256d3f38764e96333158b14ab18257b92f3155c60d658cafb80389f72f4619ed')
    version('2.06', sha256='17172edac7cb666f0d9be84dc7767f1154e8fcb761e30f3eb364dacbbb826132')
    version('2.05', sha256='a5aab24fd4a55bae75b5fd6f9b9865e58167f6f649828b1093d57882e3d86caa')
    version('2.04', sha256='8d82f3140b1453b962956b7855ba288d435e7f656c3c40ced4e3e8e359ab5293')
