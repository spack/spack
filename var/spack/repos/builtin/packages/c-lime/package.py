# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class CLime(AutotoolsPackage):
    """LIME (which can stand for Lattice QCD Interchange Message Encapsulation
       or more generally, Large Internet Message Encapsulation) is a simple
       packaging scheme for combining records containing ASCII and/or binary
       data."""

    homepage = "https://usqcd-software.github.io/c-lime/"
    url      = "https://github.com/usqcd-software/c-lime/archive/qio2-3-9.tar.gz"

    version('2-3-9', '28257e7ae75dc68c7c920e3e16db0ec9')
