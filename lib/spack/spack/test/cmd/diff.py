# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.config
import spack.store
import spack.cmd.diff


def test_diff(install_mockery, mock_fetch, mock_archive, mock_packages):
    """Test that we can install two packages and diff them"""

    specA = spack.spec.Spec('mpileaks').concretized()
    specB = spack.spec.Spec('mpileaks+debug').concretized()

    # Specs should be the same as themselves
    c = spack.cmd.diff.compare_specs(specA, specA, "A", "A", to_string=True)
    assert len(c['a_not_b']) == 0
    assert len(c['b_not_a']) == 0

    # Calculate the comparison (c)
    c = spack.cmd.diff.compare_specs(specA, specB, "A", "B", to_string=True)
    assert len(c['a_not_b']) == 1
    assert len(c['b_not_a']) == 1
    assert c['a_not_b'][0] == ['variant_set', 'mpileaks debug bool(False)']
    assert c['b_not_a'][0] == ['variant_set', 'mpileaks debug bool(True)']
