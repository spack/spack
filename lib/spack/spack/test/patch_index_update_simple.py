# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Simple test for patch index auto-update that avoids Python module caching issues."""

import os
import sys

import pytest

import spack.error
import spack.patch
import spack.repo
import spack.util.file_cache


def _cleanup_modules(namespace):
    """Remove all modules for the given repo namespace from sys.modules."""
    to_remove = [k for k in sys.modules if k.startswith(f"spack_repo.{namespace}")]
    for k in to_remove:
        del sys.modules[k]


def _get_patch_by_name(pkg_cls, patch_filename):
    """Helper to get a patch object by its filename from a package class."""
    return next(p for patches in pkg_cls.patches.values() for p in patches if isinstance(p, spack.patch.FilePatch) and p.relative_path == patch_filename)


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

        # Get the original patch hash for fix.patch
        original_hash = _get_patch_by_name(pkg_cls, "fix.patch").sha256

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
        # Remove all package modules from sys.modules so they get reloaded
        _cleanup_modules(namespace)

        # Create a new Repo with a new FileCache pointing to the same cache directory
        # This simulates a fresh Spack session that loads the stale index from disk
        # Because package.py didn't change, FastPackageChecker marks the index as fresh
        # and loads it without rebuilding - even though the patch file changed
        repo_cache2 = spack.util.file_cache.FileCache(str(cache_dir))
        repo2 = spack.repo.Repo(repo_root, cache=repo_cache2)
        repo_path2 = spack.repo.RepoPath(repo2)

        # Load the package - it should create NEW patch objects from the modified file
        pkg_cls2 = repo2.get_pkg_class("test_pkg")

        # Get the new hash (should be computed from modified file by fresh patch object)
        new_hash = _get_patch_by_name(pkg_cls2, "fix.patch").sha256
        assert new_hash != original_hash, "Patch hash should have changed after file modification"

        # Try to get patches using the NEW hash (from modified file)
        # The stale index (loaded from cache) only has the OLD hash
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
        _cleanup_modules(namespace)
