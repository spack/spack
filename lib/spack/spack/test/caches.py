# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.caches
import spack.config
import spack.paths


def test_misc_cache_location_custom(mutable_config, tmp_path):
    """Test that misc_cache_location respects the config setting."""
    custom_path = str(tmp_path / "custom_misc_cache")
    mutable_config.set("config:misc_cache", custom_path)
    
    expected = spack.config.canonicalize_path(custom_path, config=mutable_config)
    assert spack.caches.misc_cache_location(config=mutable_config) == expected


def test_misc_cache(mutable_config, tmp_path):
    """Test that misc_cache returns a FileCache with the correct properties."""
    custom_path = str(tmp_path / "custom_misc_cache")
    mutable_config.set("config:misc_cache", custom_path)
    mutable_config.set("config:locks", False)

    cache = spack.caches.misc_cache(config=mutable_config)
    
    assert str(cache.root) == spack.config.canonicalize_path(custom_path, config=mutable_config)


def test_fetch_cache_location_custom(mutable_config, tmp_path):
    """Test that fetch_cache_location respects the config setting."""
    custom_path = str(tmp_path / "custom_source_cache")
    mutable_config.set("config:source_cache", custom_path)
    
    expected = spack.config.canonicalize_path(custom_path)
    assert spack.caches.fetch_cache_location() == expected


def test_mirror_cache_init(tmp_path):
    """Test that MirrorCache initializes correctly."""
    root_path = str(tmp_path / "mirror_root")
    mc = spack.caches.MirrorCache(root_path, skip_unstable_versions=True)
    
    assert str(mc.root) == root_path
    assert mc.skip_unstable_versions is True
