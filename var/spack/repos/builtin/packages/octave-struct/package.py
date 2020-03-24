# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class OctaveStruct(OctavePackage):
    """Additional structure manipulation functions for Octave."""

    homepage = "https://octave.sourceforge.io/struct/"
    url      = "https://downloads.sourceforge.net/octave/struct-1.0.14.tar.gz"

    version('1.0.14', sha256='ad4e17687bc24650f032757271b20b70fe32c35513d4dd9ab1e549919df36b47')
    extends('octave@2.9.7:')
