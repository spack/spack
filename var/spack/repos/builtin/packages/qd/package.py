# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Qd(AutotoolsPackage):
    """This package provides numeric types of twice the precision of IEEE double (106 mantissa bits, or approximately 32 decimal digits) and four times the precision of IEEE double (212 mantissa bits, or approximately 64 decimal digits).  Due to features such as operator and function overloading, these facilities can be utilized with only minor modifications to conventional C++ and Fortran-90 programs."""

    homepage = "https://github.com/scibuilder/QD"
    git      = "https://github.com/scibuilder/QD.git"

    version('develop', branch='master')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
