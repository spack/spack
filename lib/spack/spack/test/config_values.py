# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.spec


def test_set_install_hash_length(mock_packages, mutable_config, monkeypatch):
    # spack.store.layout caches initial config values, so we monkeypatch
    mutable_config.set('config:install_hash_length', 5)
    monkeypatch.setattr(spack.store, 'store', spack.store._store())

    spec = spack.spec.Spec('libelf').concretized()
    prefix = spec.prefix
    hash = prefix.rsplit('-')[-1]

    assert len(hash) == 5

    mutable_config.set('config:install_hash_length', 9)
    monkeypatch.setattr(spack.store, 'store', spack.store._store())

    spec = spack.spec.Spec('libelf').concretized()
    prefix = spec.prefix
    hash = prefix.rsplit('-')[-1]

    assert len(hash) == 9


def test_set_install_hash_length_upper_case(mock_packages, mutable_config,
                                            monkeypatch):
    # spack.store.layout caches initial config values, so we monkeypatch
    mutable_config.set('config:install_path_scheme', '{name}-{HASH}')
    mutable_config.set('config:install_hash_length', 5)
    monkeypatch.setattr(spack.store, 'store', spack.store._store())

    spec = spack.spec.Spec('libelf').concretized()
    prefix = spec.prefix
    hash = prefix.rsplit('-')[-1]

    assert len(hash) == 5
