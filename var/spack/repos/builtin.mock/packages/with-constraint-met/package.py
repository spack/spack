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

    # By default constraints from the context manager are appended
    # to each when= argument in the directive, so the following are
    # equivalent to:
    # depends_on('b', when='@1.0')
    # conflicts('%gcc', when='+foo @1.0')
    with when('@1.0'):
        depends_on('b')
        conflicts('%gcc', when='+foo')

    # In certain contexts it is necessary to prepend the constraint
    # that is grouped together among different directives. The following
    # is equivalent to:
    # depends_on('c', when='@0.14: ^b@3.8:')
    with when('@0.14:', prepend=True):
        depends_on('c', when='^b@3.8:')
