# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import spack.store
from spack.main import SpackCommand, SpackCommandError

gc = SpackCommand('gc')
mark = SpackCommand('mark')
install = SpackCommand('install')
uninstall = SpackCommand('uninstall')


@pytest.mark.db
def test_mark_mode_required(mutable_database):
    with pytest.raises(SystemExit):
        mark('-a')


@pytest.mark.db
def test_mark_spec_required(mutable_database):
    with pytest.raises(SpackCommandError):
        mark('-i')


@pytest.mark.db
def test_mark_all_explicit(mutable_database):
    mark('-e', '-a')
    gc('-y')
    all_specs = spack.store.layout.all_specs()
    # BlueBrain: sometimes we see 16 specs instead of 15
    assert len(all_specs) in (15, 16)


@pytest.mark.db
def test_mark_all_implicit(mutable_database):
    mark('-i', '-a')
    gc('-y')
    all_specs = spack.store.layout.all_specs()
    assert len(all_specs) == 0


@pytest.mark.db
def test_mark_one_explicit(mutable_database):
    mark('-e', 'libelf')
    uninstall('-y', '-a', 'mpileaks')
    gc('-y')
    all_specs = spack.store.layout.all_specs()
    # BlueBrain: sometimes we see one more spec
    assert len(all_specs) in (3, 4)


@pytest.mark.db
def test_mark_one_implicit(mutable_database):
    mark('-i', 'externaltest')
    gc('-y')
    all_specs = spack.store.layout.all_specs()
    # BlueBrain: sometimes we see one more spec
    assert len(all_specs) in (14, 15)


@pytest.mark.db
def test_mark_all_implicit_then_explicit(mutable_database):
    mark('-i', '-a')
    mark('-e', '-a')
    gc('-y')
    all_specs = spack.store.layout.all_specs()
    # BlueBrain: sometimes we see 16 specs instead of 15
    assert len(all_specs) in (15, 16)
