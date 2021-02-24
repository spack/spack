# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
class DepWithVariantsDisjoint(Package):
    """Package that has a variant that is a disjoint set
    with a default value
    """
    homepage = "https://dev.null"

    version('1.0')

    variant('foo', description='nope',
            values=disjoint_sets(('bar',), ('baz',)).with_default('bar'))
