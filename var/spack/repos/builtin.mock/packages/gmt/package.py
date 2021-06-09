# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
class Gmt(Package):

    version('2.0', 'abcdef')
    version('1.0', 'abcdef')

    depends_on('mvdefaults', when='@1.0')
