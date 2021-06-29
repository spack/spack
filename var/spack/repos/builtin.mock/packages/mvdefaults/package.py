# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
class Mvdefaults(Package):

    version('1.0', 'abcdef')

    variant('foo', values=('a', 'b', 'c'), default=('a', 'b', 'c'),
            multi=True, description='')
