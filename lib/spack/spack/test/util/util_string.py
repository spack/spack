# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.string import plural


def test_plural():
    assert plural(0, 'thing') == '0 things'
    assert plural(1, 'thing') == '1 thing'
    assert plural(2, 'thing') == '2 things'
    assert plural(1, 'thing', 'wombats') == '1 thing'
    assert plural(2, 'thing', 'wombats') == '2 wombats'
