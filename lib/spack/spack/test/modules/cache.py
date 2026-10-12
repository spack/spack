# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import pytest

import spack.modules.cache
import spack.util.module_cmd

pytestmark = pytest.mark.not_on_windows("does not run on windows")


@pytest.fixture(autouse=True)
def no_pending_dirs(monkeypatch):
    """Starts each test with an empty list of pending modulepath directories."""
    monkeypatch.setattr(spack.modules.cache, "_pending_dirs", set())


@pytest.fixture()
def module_cmd_calls(monkeypatch):
    """Intercepts module command runs, and returns the list of their arguments."""
    calls = []

    def fake_module(*args, environb=None, **kwargs):
        calls.append((args, environb))
        return ""

    monkeypatch.setattr(spack.util.module_cmd, "module", fake_module)
    return calls


def test_flush_without_registration(module_cmd_calls):
    """Tests that a flush with no pending directory does not run the module command."""
    spack.modules.cache.flush()
    assert not module_cmd_calls


def _make_modulepath_dir(root, name, empty=False):
    """Creates a modulepath directory, holding one module file unless empty."""
    dirname = root / name
    dirname.mkdir()
    if not empty:
        (dirname / "modulefile").write_text("#%Module")
    return str(dirname)


def test_flush_clears_then_builds_cache_once(tmp_path, module_cmd_calls):
    """Tests that a flush clears then builds the cache of the deduplicated list of
    pending directories, with one run of each module sub-command, then clears the
    pending list."""
    dir_a = _make_modulepath_dir(tmp_path, "a")
    dir_b = _make_modulepath_dir(tmp_path, "b")
    spack.modules.cache.register(dir_a)
    spack.modules.cache.register(dir_b)
    spack.modules.cache.register(dir_a)
    spack.modules.cache.flush()

    assert len(module_cmd_calls) == 2
    clear_args, clear_environb = module_cmd_calls[0]
    assert clear_args == ("cacheclear",)
    assert clear_environb[b"MODULEPATH"] == os.fsencode(os.pathsep.join([dir_a, dir_b]))
    assert module_cmd_calls[1] == (("cachebuild", dir_a, dir_b), None)

    # The pending list has been cleared: a second flush is a no-op
    spack.modules.cache.flush()
    assert len(module_cmd_calls) == 2


def test_flush_prunes_emptied_directories(tmp_path, module_cmd_calls):
    """Tests that directories left with no module file are pruned after the cache
    clear, and excluded from the cache build."""
    dir_a = _make_modulepath_dir(tmp_path, "a")
    dir_b = _make_modulepath_dir(tmp_path, "b", empty=True)
    spack.modules.cache.register(dir_a)
    spack.modules.cache.register(dir_b)
    spack.modules.cache.flush()

    assert not os.path.exists(dir_b)
    assert module_cmd_calls[0][0] == ("cacheclear",)
    assert module_cmd_calls[1] == (("cachebuild", dir_a), None)

    # No cache build at all if every pending directory has been pruned
    module_cmd_calls.clear()
    dir_c = _make_modulepath_dir(tmp_path, "c", empty=True)
    spack.modules.cache.register(dir_c)
    spack.modules.cache.flush()

    assert not os.path.exists(dir_c)
    assert [args for args, _ in module_cmd_calls] == [("cacheclear",)]


def test_flush_skips_vanished_directories(tmp_path, module_cmd_calls):
    """Tests that directories removed since their registration are not cachebuilt."""
    dir_a = _make_modulepath_dir(tmp_path, "a")
    dir_b = str(tmp_path / "b")
    spack.modules.cache.register(dir_a)
    spack.modules.cache.register(dir_b)
    spack.modules.cache.flush()
    assert [args for args, _ in module_cmd_calls] == [("cacheclear",), ("cachebuild", dir_a)]

    # No module command run at all if every pending directory vanished
    spack.modules.cache.register(dir_b)
    spack.modules.cache.flush()
    assert len(module_cmd_calls) == 2


def test_cacheclear_restricts_modulepath(tmp_path, module_cmd_calls, monkeypatch):
    """Tests that cacheclear runs with MODULEPATH set to the given directories only,
    ignoring the MODULEPATH value inherited by the Spack process."""
    monkeypatch.setenv("MODULEPATH", "/some/user/modulepath")
    dirs = [str(tmp_path / "a"), str(tmp_path / "b")]
    spack.modules.cache.cacheclear(dirs)

    (args, environb) = module_cmd_calls[0]
    assert args == ("cacheclear",)
    assert environb[b"MODULEPATH"] == os.fsencode(os.pathsep.join(dirs))


def test_module_cmd_error_reported(monkeypatch, capsys):
    """Tests that errors reported by the module command turn into a warning, while
    its regular output is kept for debug."""

    def fake_module(*args, environb=None, **kwargs):
        return "Creating /some/dir/.modulecache\n\nERROR: Invalid sub-command 'cachebuild'\n"

    monkeypatch.setattr(spack.util.module_cmd, "module", fake_module)
    spack.modules.cache.cachebuild(["/some/dir"])

    captured = capsys.readouterr()
    assert "Environment Modules >= 5.3" in captured.err
    assert "Invalid sub-command" in captured.err
    assert "Creating /some/dir/.modulecache" not in captured.err
