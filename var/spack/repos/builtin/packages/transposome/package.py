# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Transposome(PerlPackage):
    """A toolkit for annotation of transposable element families from
       unassembled sequence reads."""

    homepage = "https://sestaton.github.io/Transposome/"
    url      = "https://github.com/sestaton/Transposome/archive/v0.11.2.tar.gz"

    version('0.11.2', '157c1fc090b0aa30050d03df885dcde0')

    depends_on('blast-plus')
