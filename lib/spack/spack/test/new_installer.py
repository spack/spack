# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Tests for the new_installer.py module"""

import pathlib as pathlb
import sys

import pytest

if sys.platform == "win32":
    pytest.skip("No Windows support", allow_module_level=True)

import spack.error
from spack.new_installer import OVERWRITE_GARBAGE_SUFFIX, PrefixPivoter


@pytest.fixture
def existing_prefix(tmp_path: pathlb.Path) -> pathlb.Path:
    """Creates a standard existing prefix with content."""
    prefix = tmp_path / "existing_prefix"
    prefix.mkdir()
    (prefix / "old_file").write_text("old content")
    return prefix


class TestPrefixPivoter:
    """Tests for the PrefixPivoter class."""

    def test_no_existing_prefix(self, tmp_path: pathlb.Path):
        """Test installation when prefix doesn't exist yet."""
        prefix = tmp_path / "new_prefix"

        with PrefixPivoter(str(prefix), overwrite=False):
            prefix.mkdir()
            (prefix / "installed_file").write_text("content")

        assert prefix.exists()
        assert (prefix / "installed_file").read_text() == "content"

    def test_existing_prefix_no_overwrite_raises(self, existing_prefix: pathlb.Path):
        """Test that existing prefix raises error when overwrite=False."""
        with pytest.raises(spack.error.InstallError, match="already exists"):
            with PrefixPivoter(str(existing_prefix), overwrite=False):
                pass

    def test_overwrite_success_cleans_up_old_prefix(
        self, tmp_path: pathlb.Path, existing_prefix: pathlb.Path
    ):
        """Test that overwrite=True moves old prefix and cleans it up on success."""
        with PrefixPivoter(str(existing_prefix), overwrite=True):
            assert not existing_prefix.exists()
            existing_prefix.mkdir()
            (existing_prefix / "new_file").write_text("new content")

        assert existing_prefix.exists()
        assert (existing_prefix / "new_file").exists()
        assert not (existing_prefix / "old_file").exists()
        # Only the existing_prefix directory should remain
        assert len(list(tmp_path.iterdir())) == 1

    def test_overwrite_failure_restores_original_prefix(
        self, tmp_path: pathlb.Path, existing_prefix: pathlb.Path
    ):
        """Test that original prefix is restored when installation fails.

        Note: keep_prefix=True is passed but should be ignored since overwrite=True
        takes precedence."""
        with pytest.raises(RuntimeError, match="simulated failure"):
            with PrefixPivoter(str(existing_prefix), overwrite=True, keep_prefix=True):
                existing_prefix.mkdir()
                (existing_prefix / "partial_file").write_text("partial")
                raise RuntimeError("simulated failure")

        assert existing_prefix.exists()
        assert (existing_prefix / "old_file").read_text() == "old content"
        assert not (existing_prefix / "partial_file").exists()
        # Only the existing_prefix directory should remain
        assert len(list(tmp_path.iterdir())) == 1

    def test_overwrite_failure_no_partial_prefix_created(self, existing_prefix: pathlb.Path):
        """Test restoration when failure occurs before any prefix is created."""
        with pytest.raises(RuntimeError, match="early failure"):
            with PrefixPivoter(str(existing_prefix), overwrite=True):
                raise RuntimeError("early failure")

        assert existing_prefix.exists()
        assert (existing_prefix / "old_file").read_text() == "old content"

    def test_overwrite_true_no_existing_prefix(self, tmp_path: pathlb.Path):
        """Test that overwrite=True works fine when prefix doesn't exist."""
        prefix = tmp_path / "new_prefix"
        with PrefixPivoter(str(prefix), overwrite=True):
            prefix.mkdir()
            (prefix / "installed_file").write_text("content")

        assert prefix.exists()
        # Only the new_prefix directory should remain
        assert len(list(tmp_path.iterdir())) == 1

    def test_keep_prefix_true_leaves_failed_install(self, tmp_path: pathlb.Path):
        """Test that keep_prefix=True preserves the failed installation."""
        prefix = tmp_path / "new_prefix"

        with pytest.raises(RuntimeError, match="simulated failure"):
            with PrefixPivoter(str(prefix), overwrite=False, keep_prefix=True):
                prefix.mkdir()
                (prefix / "partial_file").write_text("partial content")
                raise RuntimeError("simulated failure")

        # Failed prefix should still exist
        assert prefix.exists()
        assert (prefix / "partial_file").exists()
        assert (prefix / "partial_file").read_text() == "partial content"
        # Only the failed prefix should remain
        assert len(list(tmp_path.iterdir())) == 1

    def test_keep_prefix_false_removes_failed_install(self, tmp_path: pathlb.Path):
        """Test that keep_prefix=False removes the failed installation."""
        prefix = tmp_path / "new_prefix"

        with pytest.raises(RuntimeError, match="simulated failure"):
            with PrefixPivoter(str(prefix), overwrite=False, keep_prefix=False):
                prefix.mkdir()
                (prefix / "partial_file").write_text("partial content")
                raise RuntimeError("simulated failure")

        # Failed prefix should be removed
        assert not prefix.exists()
        # Nothing should remain
        assert len(list(tmp_path.iterdir())) == 0


class FailingPrefixPivoter(PrefixPivoter):
    """Test subclass that can simulate filesystem failures."""

    def __init__(
        self,
        prefix: str,
        overwrite: bool,
        keep_prefix: bool = False,
        fail_on_restore: bool = False,
        fail_on_move_garbage: bool = False,
    ):
        super().__init__(prefix, overwrite, keep_prefix)
        self.fail_on_restore = fail_on_restore
        self.fail_on_move_garbage = fail_on_move_garbage
        self.restore_rename_count = 0

    def _rename(self, src: str, dst: str) -> None:
        if (
            self.fail_on_restore
            and self.tmp_prefix
            and src == self.tmp_prefix
            and dst == self.prefix
        ):
            self.restore_rename_count += 1
            raise OSError("Simulated rename failure during restore")

        if self.fail_on_move_garbage and dst.endswith(OVERWRITE_GARBAGE_SUFFIX):
            raise OSError("Simulated rename failure moving to garbage")

        super()._rename(src, dst)


class TestPrefixPivoterFailureRecovery:
    """Tests for edge cases and failure recovery in PrefixPivoter."""

    def test_restore_failure_leaves_backup(
        self, tmp_path: pathlb.Path, existing_prefix: pathlb.Path
    ):
        """Test that if restoration fails, the backup is not deleted."""
        pivoter = FailingPrefixPivoter(str(existing_prefix), overwrite=True, fail_on_restore=True)

        with pytest.raises(OSError, match="Simulated rename failure during restore"):
            with pivoter:
                existing_prefix.mkdir()
                (existing_prefix / "partial_file").write_text("partial")
                raise RuntimeError("simulated failure")

        assert pivoter.restore_rename_count > 0
        # Backup directory should still exist (plus the failed prefix)
        assert len(list(tmp_path.iterdir())) == 2

    def test_garbage_move_failure_leaves_backup(
        self, tmp_path: pathlb.Path, existing_prefix: pathlb.Path
    ):
        """Test that if moving the failed install to garbage fails, the backup is preserved."""
        pivoter = FailingPrefixPivoter(
            str(existing_prefix), overwrite=True, fail_on_move_garbage=True
        )

        with pytest.raises(OSError, match="Simulated rename failure moving to garbage"):
            with pivoter:
                existing_prefix.mkdir()
                (existing_prefix / "partial_file").write_text("partial")
                raise RuntimeError("simulated failure")

        assert (existing_prefix / "partial_file").exists()
        # Backup directory, failed prefix, and empty garbage directory should exist
        assert len(list(tmp_path.iterdir())) == 3
