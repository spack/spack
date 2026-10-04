# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.spec
from spack.spec_filter import SpecFilter


def test_spec_filter_is_selected():
    """Test various include and exclude criteria on SpecFilter.is_selected"""
    s = spack.spec.Spec("zlib@1.2.11")

    # 1. By default, a usable spec is selected
    f = SpecFilter(lambda: [s], lambda x: True)
    assert f.is_selected(s)

    # 2. Not usable spec is not selected
    f = SpecFilter(lambda: [s], lambda x: False)
    assert not f.is_selected(s)

    # 3. Include match
    f = SpecFilter(lambda: [s], lambda x: True, include=["zlib@1.0:1.3"])
    assert f.is_selected(s)

    # 4. Include mismatch
    f = SpecFilter(lambda: [s], lambda x: True, include=["zlib@1.2.12:"])
    assert not f.is_selected(s)

    # 5. Exclude match (should reject)
    f = SpecFilter(lambda: [s], lambda x: True, exclude=["zlib@1.2.11"])
    assert not f.is_selected(s)

    # 6. Exclude mismatch (should accept)
    f = SpecFilter(lambda: [s], lambda x: True, exclude=["hdf5"])
    assert f.is_selected(s)

    # 7. Include and exclude combined
    f = SpecFilter(
        lambda: [s], lambda x: True, include=["zlib"], exclude=["zlib@1.2.11"]
    )
    assert not f.is_selected(s)

    f = SpecFilter(
        lambda: [s], lambda x: True, include=["zlib"], exclude=["zlib@1.3.0"]
    )
    assert f.is_selected(s)


def test_spec_filter_selected_specs():
    """Test that selected_specs properly builds the filtered list"""
    s1 = spack.spec.Spec("zlib@1.2.11")
    s2 = spack.spec.Spec("hdf5@1.10.7")
    s3 = spack.spec.Spec("hdf5@1.10.8")

    def factory():
        return [s1, s2, s3]

    # Usability filter
    f1 = SpecFilter(factory, lambda s: s.name == "hdf5")
    assert f1.selected_specs() == [s2, s3]

    # Include filter
    f2 = SpecFilter(factory, lambda s: True, include=["hdf5@1.10.8"])
    assert f2.selected_specs() == [s3]

    # Exclude filter
    f3 = SpecFilter(factory, lambda s: True, exclude=["hdf5"])
    assert f3.selected_specs() == [s1]

    # Complex combination
    f4 = SpecFilter(factory, lambda s: True, include=["hdf5"], exclude=["@1.10.8"])
    assert f4.selected_specs() == [s2]
