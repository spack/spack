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
    # Get initial STORE
    initial_store = spack.store.STORE

    # Reinitialize
    spack.config.reinitialize_global_state()

    # STORE should be a different object
    assert spack.store.STORE is not initial_store


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

    # Call reinitialize_global_state
    spack.config.reinitialize_global_state()

    # Cache should now use config_2 path
    assert str(spack.caches.MISC_CACHE.root) == str(cache_dir_2)
