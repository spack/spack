# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RDeriv(RPackage):
    """R-based solution for symbolic differentiation. It admits user-defined
    function as well as function substitution in arguments of functions to be
    differentiated. Some symbolic simplification is part of the work."""

    homepage = "https://cloud.r-project.org/package=Deriv"
    url      = "https://cloud.r-project.org/src/contrib/Deriv_4.1.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/Deriv"

    version('4.1.2', sha256='c4b0c3f351f6df53778d48033460cf8674e7a7878fbc542085d66a9a78803ac9')

    extends('r')
    depends_on('r', type=('build', 'run'))
