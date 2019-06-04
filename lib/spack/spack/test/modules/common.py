# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest
import os
import stat
import spack.spec
import spack.modules.common
import spack.modules.tcl


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


@pytest.fixture()
def mock_module_filename(monkeypatch, tmpdir):
    filename = str(tmpdir.join('module'))
    monkeypatch.setattr(spack.modules.common.BaseFileLayout,
                        'filename',
                        filename)

    yield filename


@pytest.fixture()
def mock_package_perms(monkeypatch):
    perms = stat.S_IRGRP | stat.S_IWGRP
    monkeypatch.setattr(spack.package_prefs,
                        'get_package_permissions',
                        lambda spec: perms)

    yield perms


def test_modules_written_with_proper_permissions(mock_module_filename,
                                                 mock_package_perms,
                                                 mock_packages, config):
    spec = spack.spec.Spec('mpileaks').concretized()

    # The code tested is common to all module types, but has to be tested from
    # one. TCL picked at random
    generator = spack.modules.tcl.TclModulefileWriter(spec)
    generator.write()

    assert mock_package_perms & os.stat(
        mock_module_filename).st_mode == mock_package_perms
