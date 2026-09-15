# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pathlib

import pytest

import spack.concretize
import spack.config
import spack.store


@pytest.mark.parametrize("hash_length", [1, 2, 3, 4, 5, 9])
@pytest.mark.usefixtures("mock_packages")
def test_set_install_hash_length(hash_length, mutable_config, tmp_path: pathlib.Path):
    mutable_config.set("config:install_hash_length", hash_length)
    with spack.store.use_store(str(tmp_path)):
        spec = spack.concretize.concretize_one("libelf")
        prefix = spec.prefix
        hash_str = prefix.rsplit("-")[-1]
        assert len(hash_str) == hash_length


@pytest.mark.usefixtures("mock_packages")
def test_set_install_hash_length_upper_case(mutable_config, tmp_path: pathlib.Path):
    mutable_config.set("config:install_hash_length", 5)
    with spack.store.use_store(
        str(tmp_path), extra_data={"projections": {"all": "{name}-{HASH}"}}
    ):
        spec = spack.concretize.concretize_one("libelf")
        prefix = spec.prefix
        hash_str = prefix.rsplit("-")[-1]
        assert len(hash_str) == 5


@pytest.mark.regression("45247")
def test_use_store_does_not_try_writing_outside_root(
    tmp_path: pathlib.Path, monkeypatch, mutable_config
):
    """Tests that when we use the 'use_store' context manager, there is no attempt at creating
    a Store outside the given root.
    """
    initial_store = mutable_config.get("config:install_tree:root")
    user_store = tmp_path / "store"

    fn = spack.store.Store.__init__

    def _checked_init(self, root, *args, **kwargs):
        fn(self, root, *args, **kwargs)
        assert self.root == str(user_store)

    monkeypatch.setattr(spack.store.Store, "__init__", _checked_init)

    spack.store.reinitialize()
    with spack.store.use_store(user_store):
        assert spack.config.CONFIG.get("config:install_tree:root") == str(user_store)
    assert spack.config.CONFIG.get("config:install_tree:root") == initial_store
