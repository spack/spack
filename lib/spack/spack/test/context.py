# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.binary_distribution
import spack.caches
import spack.config
import spack.context
import spack.repo
import spack.store


def test_default_context():
    """Test that the default() function returns a SpackContext wrapping globals."""
    ctx = spack.context.default()
    
    assert ctx.config is spack.config.CONFIG
    assert ctx.store is spack.store.STORE
    assert ctx.repo is spack.repo.PATH
    assert ctx.binary_index is spack.binary_distribution.BINARY_INDEX
    assert ctx.misc_cache is spack.caches.MISC_CACHE


def test_from_config(mutable_config):
    """Test that from_config() correctly derives context fields from a configuration."""
    ctx = spack.context.from_config(mutable_config)
    
    # Assert it derived from the provided config
    assert ctx.config is mutable_config
    
    # It should construct distinct new objects for store, repo, etc.
    assert ctx.store is not spack.store.STORE
    assert ctx.repo is not spack.repo.PATH
    assert ctx.binary_index is not spack.binary_distribution.BINARY_INDEX
    assert ctx.misc_cache is not spack.caches.MISC_CACHE
