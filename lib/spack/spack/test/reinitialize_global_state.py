# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Tests for reinitialize_global_state() to verify global singletons update after CONFIG swap."""


import spack.binary_distribution
import spack.caches
import spack.config
import spack.repo
import spack.store


def test_reinitialize_replaces_store_singleton(tmp_path, monkeypatch):
    """Test that reinitialize_global_state() creates a new STORE singleton."""
    # Create two install directories
    install_root_1 = tmp_path / "opt" / "spack1"
    install_root_2 = tmp_path / "opt" / "spack2"
    install_root_1.mkdir(parents=True)
    install_root_2.mkdir(parents=True)

    # Set up config_1 and initialize
    config_1 = spack.config.create()
    config_1.set("config:install_tree:root", str(install_root_1))
    monkeypatch.setattr(spack.config, "CONFIG", config_1)
    spack.store.reinitialize()

    initial_store = spack.store.STORE
    assert initial_store.root == str(install_root_1)

    # Swap to config_2
    config_2 = spack.config.create()
    config_2.set("config:install_tree:root", str(install_root_2))
    monkeypatch.setattr(spack.config, "CONFIG", config_2)

    # BEFORE reinitialize: STORE should still be same object with old path
    assert spack.store.STORE is initial_store
    assert spack.store.STORE.root == str(install_root_1)

    # Reinitialize
    spack.config.reinitialize_global_state()

    # AFTER reinitialize: STORE should be different object with new path
    assert spack.store.STORE is not initial_store
    assert spack.store.STORE.root == str(install_root_2)


def test_reinitialize_replaces_cache_singleton(tmp_path, monkeypatch):
    """Test that reinitialize_global_state() creates a new MISC_CACHE singleton."""
    # Get initial cache
    initial_cache = spack.caches.MISC_CACHE

    # Reinitialize
    spack.config.reinitialize_global_state()

    # Cache should be a different object
    assert spack.caches.MISC_CACHE is not initial_cache


def test_reinitialize_replaces_all_singletons(tmp_path, monkeypatch):
    """Test that reinitialize_global_state() replaces all documented singletons."""
    # Capture initial singletons
    initial_store = spack.store.STORE
    initial_misc_cache = spack.caches.MISC_CACHE
    initial_repo_path = spack.repo.PATH
    initial_binary_index = spack.binary_distribution.BINARY_INDEX

    # Reinitialize
    spack.config.reinitialize_global_state()

    # All singletons should be new objects
    assert spack.store.STORE is not initial_store
    assert spack.caches.MISC_CACHE is not initial_misc_cache
    assert spack.repo.PATH is not initial_repo_path
    assert spack.binary_distribution.BINARY_INDEX is not initial_binary_index


def test_reinitialize_after_config_swap_uses_new_paths(tmp_path, monkeypatch):
    """Test that after swapping CONFIG and reinitializing, new paths are used."""
    # Create two cache directories
    cache_dir_1 = tmp_path / "cache1"
    cache_dir_2 = tmp_path / "cache2"
    cache_dir_1.mkdir()
    cache_dir_2.mkdir()

    # Create config_1 and install it
    config_1 = spack.config.create()
    config_1.set("config:misc_cache", str(cache_dir_1))
    monkeypatch.setattr(spack.config, "CONFIG", config_1)
    spack.caches.reinitialize()

    # Verify cache uses config_1
    assert str(spack.caches.MISC_CACHE.root) == str(cache_dir_1)

    # Create config_2 and swap
    config_2 = spack.config.create()
    config_2.set("config:misc_cache", str(cache_dir_2))
    monkeypatch.setattr(spack.config, "CONFIG", config_2)

    # BEFORE reinitialize: cache should still use old path
    assert str(spack.caches.MISC_CACHE.root) == str(cache_dir_1)

    # Call reinitialize_global_state
    spack.config.reinitialize_global_state()

    # AFTER reinitialize: cache should now use config_2 path
    assert str(spack.caches.MISC_CACHE.root) == str(cache_dir_2)


def test_config_swap_without_reinitialize_keeps_old_values(tmp_path, monkeypatch):
    """Test that swapping CONFIG alone doesn't update singletons until reinitialize."""
    cache_dir_1 = tmp_path / "cache1"
    cache_dir_2 = tmp_path / "cache2"
    cache_dir_1.mkdir()
    cache_dir_2.mkdir()

    # Set up config_1 and initialize
    config_1 = spack.config.create()
    config_1.set("config:misc_cache", str(cache_dir_1))
    monkeypatch.setattr(spack.config, "CONFIG", config_1)
    spack.caches.reinitialize()

    cache_after_init = spack.caches.MISC_CACHE
    assert str(cache_after_init.root) == str(cache_dir_1)

    # Swap to config_2 but DON'T reinitialize
    config_2 = spack.config.create()
    config_2.set("config:misc_cache", str(cache_dir_2))
    monkeypatch.setattr(spack.config, "CONFIG", config_2)

    # Singleton should be the same object with old path
    assert spack.caches.MISC_CACHE is cache_after_init
    assert str(spack.caches.MISC_CACHE.root) == str(cache_dir_1)

    # Only after reinitialize_global_state should it update
    spack.config.reinitialize_global_state()
    assert spack.caches.MISC_CACHE is not cache_after_init
    assert str(spack.caches.MISC_CACHE.root) == str(cache_dir_2)


def test_multiple_reinitialization_cycles(tmp_path, monkeypatch):
    """Test that reinitialize can be called multiple times with different configs."""
    cache_dir_1 = tmp_path / "cache1"
    cache_dir_2 = tmp_path / "cache2"
    cache_dir_3 = tmp_path / "cache3"
    cache_dir_1.mkdir()
    cache_dir_2.mkdir()
    cache_dir_3.mkdir()

    # Config 1
    config_1 = spack.config.create()
    config_1.set("config:misc_cache", str(cache_dir_1))
    monkeypatch.setattr(spack.config, "CONFIG", config_1)
    spack.config.reinitialize_global_state()
    assert str(spack.caches.MISC_CACHE.root) == str(cache_dir_1)

    # Config 2
    config_2 = spack.config.create()
    config_2.set("config:misc_cache", str(cache_dir_2))
    monkeypatch.setattr(spack.config, "CONFIG", config_2)
    spack.config.reinitialize_global_state()
    assert str(spack.caches.MISC_CACHE.root) == str(cache_dir_2)

    # Config 3
    config_3 = spack.config.create()
    config_3.set("config:misc_cache", str(cache_dir_3))
    monkeypatch.setattr(spack.config, "CONFIG", config_3)
    spack.config.reinitialize_global_state()
    assert str(spack.caches.MISC_CACHE.root) == str(cache_dir_3)
