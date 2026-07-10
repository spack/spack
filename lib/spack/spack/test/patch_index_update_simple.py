# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Simple test for patch index auto-update that avoids Python module caching issues."""

import hashlib
import os

import pytest

import spack.error
import spack.patch
import spack.paths
import spack.repo
import spack.util.crypto
import spack.util.file_cache


def test_patch_index_update_packages_works(tmp_path, config):
    """Test that patch index automatically updates when a patch file changes.

    This simulates the real scenario: a patch file is modified (e.g., during repo update),
    but package.py is not modified, so FastPackageChecker doesn't detect the change.
    The patch index becomes stale, and get_patches_for_package() should automatically
    update it when a patch hash is not found.
    """
    # Create a test repository
    repo_root, namespace = spack.repo.create_repo(str(tmp_path / "test_repo"), "test_patch_repo")
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()
    repo_cache = spack.util.file_cache.FileCache(str(cache_dir))

    # Create a simple package with one patch
    pkg_dir = os.path.join(repo_root, "packages", "test_pkg")
    os.makedirs(pkg_dir, exist_ok=True)

    # Write initial patch file
    patch_content_v1 = """--- a/file.txt
+++ b/file.txt
@@ -1 +1 @@
-old content
+new content
"""
    patch_path = os.path.join(pkg_dir, "fix.patch")
    with open(patch_path, "w") as f:
        f.write(patch_content_v1)

    # Write package.py
    package_py = os.path.join(pkg_dir, "package.py")
    with open(package_py, "w") as f:
        f.write("""
from spack.package import *

class TestPkg(Package):
    version("1.0", md5="0123456789abcdef0123456789abcdef")
    patch("fix.patch", when="@1.0")
""")

    try:
        # Create repo and load package with original patch
        repo = spack.repo.Repo(repo_root, cache=repo_cache)
        repo_path = spack.repo.RepoPath(repo)
        pkg_cls = repo.get_pkg_class("test_pkg")

        # Get the original patch hash
        original_hash = None
        for cond, patch_list in pkg_cls.patches.items():
            for p in patch_list:
                original_hash = p.sha256
                break

        # Build the patch index with the original hash
        patch_index = repo_path.get_patch_index(allow_stale=False)
        assert original_hash in patch_index.index, "Original patch should be in index"

        # Now modify the patch file on disk (simulating repo update)
        patch_content_v2 = """--- a/file.txt
+++ b/file.txt
@@ -1 +1 @@
-old content
+modified content
"""
        with open(patch_path, "w") as f:
            f.write(patch_content_v2)

        # Create a fresh Repo and RepoPath to simulate a new Spack session
        # In a real scenario, this would be a completely fresh Python process
        import sys

        # Remove the package module from sys.modules so it gets reloaded
        module_name = f"spack_repo.{namespace}.packages.test_pkg"
        if module_name in sys.modules:
            del sys.modules[module_name]

        # Also clear the parent package modules
        parent_modules = [k for k in sys.modules.keys() if k.startswith(f"spack_repo.{namespace}.packages")]
        for mod in parent_modules:
            del sys.modules[mod]

        # Create a new Repo with fresh cache to ensure clean state
        cache_dir2 = tmp_path / "cache2"
        cache_dir2.mkdir()
        repo_cache2 = spack.util.file_cache.FileCache(str(cache_dir2))
        repo2 = spack.repo.Repo(repo_root, cache=repo_cache2)
        repo_path2 = spack.repo.RepoPath(repo2)

        # Load the package - it should create NEW patch objects from the modified file
        pkg_cls2 = repo2.get_pkg_class("test_pkg")

        # Get the new hash (should be computed from modified file by fresh patch object)
        new_hash = None
        for cond, patch_list in pkg_cls2.patches.items():
            for p in patch_list:
                new_hash = p.sha256
                break

        # Verify the hash actually changed
        assert new_hash != original_hash, "Patch hash should have changed after file modification"

        # Simulate the stale index scenario by installing the stale index (with only the old hash)
        # on the new repo_path. This simulates what happens when FastPackageChecker doesn't
        # detect the change because package.py didn't change (only the patch file changed)
        repo_path2._patch_index = patch_index
        repo_path2._index_is_fresh = True  # Mark as fresh so get_patch_index won't rebuild

        # Try to get patches using the NEW hash (from modified file)
        # The stale index only has the OLD hash
        # WITHOUT the fix: This raises PatchLookupError
        # WITH the fix: update_packages() is called automatically and succeeds
        try:
            result_patches = repo_path2.get_patches_for_package([new_hash], pkg_cls2)
            assert len(result_patches) == 1
            assert result_patches[0].sha256 == new_hash
        except spack.error.PatchLookupError:
            pytest.fail(
                f"PatchLookupError raised for hash {new_hash} - "
                "automatic patch index update in get_patches_for_package() failed"
            )

    finally:
        # Clean up modules
        import sys
        to_remove = [k for k in sys.modules if k.startswith(f"spack_repo.{namespace}")]
        for k in to_remove:
            del sys.modules[k]
