# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import spack.modules.common


def test_update_dictionary_extending_list():
    target = {
        'foo': {
            'a': 1,
            'b': 2,
            'd': 4
        },
        'bar': [1, 2, 4],
        'baz': 'foobar'
    }
    update = {
        'foo': {
            'c': 3,
        },
        'bar': [3],
        'baz': 'foobaz',
        'newkey': {
            'd': 4
        }
    }
    spack.modules.common.update_dictionary_extending_lists(target, update)
    assert len(target) == 4
    assert len(target['foo']) == 4
    assert len(target['bar']) == 4
    assert target['baz'] == 'foobaz'
