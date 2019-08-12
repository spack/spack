# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Squid(AutotoolsPackage):
    """C function library for sequence analysis."""

    homepage = "http://eddylab.org/software.html"

    version('1.9g', 'b9bf480c65d01417b7894c82d094ce07', url='http://eddylab.org/software/squid/squid.tar.gz')
