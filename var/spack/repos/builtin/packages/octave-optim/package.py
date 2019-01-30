# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class OctaveOptim(OctavePackage):
    """Non-linear optimization toolkit for Octave."""

    homepage = "https://octave.sourceforge.io/optim/"
    url      = "https://downloads.sourceforge.net/octave/optim-1.5.2.tar.gz"

    version('1.5.2', 'd3d77982869ea7c1807b13b24e044d44')

    depends_on('octave-struct@1.0.12:')
    extends('octave@3.6.0:')
