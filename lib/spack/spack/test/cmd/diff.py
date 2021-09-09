# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import spack.cmd.diff
import spack.config
import spack.main
import spack.store
import spack.util.spack_json as sjson

install_cmd = spack.main.SpackCommand('install')
diff_cmd = spack.main.SpackCommand('diff')
find_cmd = spack.main.SpackCommand('find')


def test_diff_cmd(install_mockery, mock_fetch, mock_archive, mock_packages):
    """Test that we can install two packages and diff them"""

    specA = spack.spec.Spec('mpileaks').concretized()
    specB = spack.spec.Spec('mpileaks+debug').concretized()

    # Specs should be the same as themselves
    c = spack.cmd.diff.compare_specs(specA, specA, to_string=True)
    assert len(c['a_not_b']) == 0
    assert len(c['b_not_a']) == 0

    # Calculate the comparison (c)
    c = spack.cmd.diff.compare_specs(specA, specB, to_string=True)
    assert len(c['a_not_b']) == 1
    assert len(c['b_not_a']) == 1
    assert c['a_not_b'][0] == ['variant_value', 'mpileaks debug False']
    assert c['b_not_a'][0] == ['variant_value', 'mpileaks debug True']


def test_load_first(install_mockery, mock_fetch, mock_archive, mock_packages):
    """Test with and without the --first option"""
    install_cmd('mpileaks')

    # Only one version of mpileaks will work
    diff_cmd('mpileaks', 'mpileaks')

    # 2 specs are required for a diff
    with pytest.raises(spack.main.SpackCommandError):
        diff_cmd('mpileaks')
    with pytest.raises(spack.main.SpackCommandError):
        diff_cmd('mpileaks', 'mpileaks', 'mpileaks')

    # Ensure they are the same
    assert "No differences" in diff_cmd('mpileaks', 'mpileaks')
    output = diff_cmd('--json', 'mpileaks', 'mpileaks')
    result = sjson.load(output)

    assert len(result['a_not_b']) == 0
    assert len(result['b_not_a']) == 0

    assert 'mpileaks' in result['a_name']
    assert 'mpileaks' in result['b_name']
    assert "intersect" in result and len(result['intersect']) > 50

    # After we install another version, it should ask us to disambiguate
    install_cmd('mpileaks+debug')

    # There are two versions of mpileaks
    with pytest.raises(spack.main.SpackCommandError):
        diff_cmd('mpileaks', 'mpileaks+debug')

    # But if we tell it to use the first, it won't try to disambiguate
    assert "variant" in diff_cmd('--first', 'mpileaks', 'mpileaks+debug')

    # This matches them exactly
    debug_hash = find_cmd('--format', '{hash}', 'mpileaks+debug').strip()
    no_debug_hashes = find_cmd('--format', '{hash}', 'mpileaks~debug')
    no_debug_hash = no_debug_hashes.split()[0]
    output = diff_cmd("--json",
                      "mpileaks/{0}".format(debug_hash),
                      "mpileaks/{0}".format(no_debug_hash))
    result = sjson.load(output)

    assert len(result['a_not_b']) == 1
    assert len(result['b_not_a']) == 1
    assert result['a_not_b'][0] == ['variant_value', 'mpileaks debug True']
    assert result['b_not_a'][0] == ['variant_value', 'mpileaks debug False']
