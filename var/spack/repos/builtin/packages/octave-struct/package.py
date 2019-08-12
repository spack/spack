# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class OctaveStruct(OctavePackage):
    """Additional structure manipulation functions for Octave."""

    homepage = "https://octave.sourceforge.io/struct/"
    url      = "https://downloads.sourceforge.net/octave/struct-1.0.14.tar.gz"

    version('1.0.14', '3589d5eb8000f18426e2178587eb82f4')
    extends('octave@2.9.7:')
