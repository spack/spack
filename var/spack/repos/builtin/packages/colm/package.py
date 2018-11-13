# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Colm(AutotoolsPackage):
    """Colm Programming Language
    Colm is a programming language designed for the analysis and
    transformation of computer languages. Colm is influenced primarily
    by TXL. It is in the family of program transformation languages.
    """

    homepage = "http://www.colm.net/open-source/colm"
    url      = "http://www.colm.net/files/colm/colm-0.12.0.tar.gz"

    version('0.12.0', '079a1ed44f71d48a349d954096c8e411')
