##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

import collections

import hypothesis
import spack
import spack.spec

from hypothesis.strategies import one_of, sampled_from, none, composite


@composite
def spec(draw):
    names = list(spack.repo.all_package_names())

    # Draw the name
    spec_str = draw(sampled_from(names))
    pkg = spack.repo.get(spec_str)

    hypothesis.note('Chosen package: {0}'.format(spec_str))
    # Draw the version
    versions = ['@' + str(v) for v in pkg.versions]
    spec_version = draw(one_of(sampled_from(versions), none()))
    if spec_version:
        spec_str += spec_version

    # Draw variants
    for pkg_variant in pkg.variants.values():

        if not isinstance(pkg_variant.values, collections.Sequence):
            continue

        value = draw(one_of(sampled_from(pkg_variant.values), none()))
        if value:
            spec_str += ' ' + str(pkg_variant.make_variant(value))

    return spack.spec.Spec(spec_str)


@hypothesis.settings(deadline=None, timeout=None, max_examples=500)
@hypothesis.given(spec())
def test_spec_can_be_concretized(spec):
    hypothesis.event(spec.name)

    try:
        s = spec.concretized()
    except spack.spec.ConflictsInSpecError:
        msg = 'Conflict with spec: {0}'
        hypothesis.note(msg.format(str(spec)))
        return

    spec.concretize()
    assert s.satisfies(spec, strict=True)
    assert spec.satisfies(s, strict=True)
