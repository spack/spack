# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class WithConstraintMet(Package):
    """Package that tests True when specs on directives."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/example-1.0.tar.gz"

    version('2.0', '0123456789abcdef0123456789abcdef')
    version('1.0', '0123456789abcdef0123456789abcdef')

    with when('@1.0'):
        depends_on('b')
        conflicts('%gcc')
