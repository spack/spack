# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Squid(AutotoolsPackage):
    """C function library for sequence analysis."""

    homepage = "http://eddylab.org/software.html"

    version('1.9g', sha256='302f42e8794aa4dbcfa0996c14fb7a70a7c4397fc45c2bbd2748055460d8dca7', url='http://eddylab.org/software/squid/squid.tar.gz')
