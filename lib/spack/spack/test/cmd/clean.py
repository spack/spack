# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pathlib
import types

import pytest

import spack.caches
import spack.cmd.clean
import spack.main
import spack.package_base
import spack.stage
import spack.store
import spack.util.filesystem as fs

clean = spack.main.SpackCommand("clean")


@pytest.fixture()
def mock_calls_for_clean(monkeypatch):
    counts = {}

    class Counter:
        def __init__(self, name):
            self.name = name
            counts[name] = 0

        def __call__(self, *args, **kwargs):
            counts[self.name] += 1

    monkeypatch.setattr(spack.package_base.PackageBase, "do_clean", Counter("package"))
    monkeypatch.setattr(spack.stage, "purge", Counter("stages"))
    downloads = types.SimpleNamespace(destroy=Counter("downloads"))
    monkeypatch.setattr(spack.caches, "fetch_cache", lambda config: downloads)
    monkeypatch.setattr(spack.caches.MISC_CACHE, "destroy", Counter("caches"))
    monkeypatch.setattr(spack.store.STORE.failure_tracker, "clear_all", Counter("failures"))
    monkeypatch.setattr(spack.cmd.clean, "remove_python_cache", Counter("python_cache"))
    monkeypatch.setattr(spack.cmd.clean, "remove_python_cache", Counter("python_cache"))
    monkeypatch.setattr(fs, "remove_directory_contents", Counter("bootstrap"))

    yield counts


all_effects = ["stages", "downloads", "caches", "failures", "python_cache", "bootstrap"]


@pytest.mark.usefixtures("mock_packages")
@pytest.mark.parametrize(
    "command_line,effects",
    [
        ("mpileaks", ["package"]),
        ("-s", ["stages"]),
        ("-sd", ["stages", "downloads"]),
        ("-m", ["caches"]),
        ("-f", ["failures"]),
        ("-p", ["python_cache"]),
        ("-a", all_effects),
        ("", []),
    ],
)
def test_function_calls(
    command_line, effects, mock_calls_for_clean, mutable_config, tmp_path: pathlib.Path
):
    # Redirect only where it is read, so the other cases keep the store clingo is bootstrapped in
    if "bootstrap" in effects:
        mutable_config.set("bootstrap:root", str(tmp_path / "bootstrap"))

    # Call the command with the supplied command line
    clean(command_line)

    # Assert that we called the expected functions the correct
    # number of times
    for name in ["package"] + all_effects:
        assert mock_calls_for_clean[name] == (1 if name in effects else 0)


def test_remove_python_cache(tmp_path: pathlib.Path, monkeypatch):
    cache_files = ["file1.pyo", "file2.pyc"]
    source_file = "file1.py"

    def _setup_files(directory):
        # Create a python cache and source file.
        cache_dir = fs.join_path(directory, "__pycache__")
        fs.mkdirp(cache_dir)
        fs.touch(fs.join_path(directory, source_file))
        fs.touch(fs.join_path(directory, cache_files[0]))
        for filename in cache_files:
            # Ensure byte code files in python cache directory
            fs.touch(fs.join_path(cache_dir, filename))

    def _check_files(directory):
        # Ensure the python cache created by _setup_files is removed
        # and the source file is not.
        assert os.path.exists(fs.join_path(directory, source_file))
        assert not os.path.exists(fs.join_path(directory, cache_files[0]))
        assert not os.path.exists(fs.join_path(directory, "__pycache__"))

    source_dir = fs.join_path(str(tmp_path), "lib", "spack", "spack")
    var_dir = fs.join_path(str(tmp_path), "var", "spack", "stuff")

    for d in [source_dir, var_dir]:
        _setup_files(d)

    # Patching the path variables from-import'd by spack.cmd.clean is needed
    # to ensure the paths used by the command for this test reflect the
    # temporary directory locations and not those from spack.paths when
    # the clean command's module was imported.
    monkeypatch.setattr(spack.cmd.clean, "lib_path", source_dir)
    monkeypatch.setattr(spack.cmd.clean, "var_path", var_dir)

    spack.cmd.clean.remove_python_cache()

    for d in [source_dir, var_dir]:
        _check_files(d)


@pytest.mark.not_on_windows("Creating symlinks requires extra privileges on Windows")
def test_remove_python_cache_skips_symlinked_pycache(tmp_path: pathlib.Path, monkeypatch):
    """A __pycache__ that is a symlink (as in an environment view) must not make
    `spack clean --python-cache` fail, and what it points to is left alone."""
    target = tmp_path / "opt" / "prefix" / "lib" / "__pycache__"
    target.mkdir(parents=True)
    (target / "module.cpython-312.pyc").touch()

    view_dir = tmp_path / "var" / "spack" / "environments" / "env" / "view" / "lib"
    view_dir.mkdir(parents=True)
    (view_dir / "__pycache__").symlink_to(target, target_is_directory=True)
    real_cache = tmp_path / "var" / "spack" / "stuff" / "__pycache__"
    real_cache.mkdir(parents=True)

    monkeypatch.setattr(spack.cmd.clean, "lib_path", str(tmp_path / "lib"))
    monkeypatch.setattr(spack.cmd.clean, "var_path", str(tmp_path / "var"))

    spack.cmd.clean.remove_python_cache()

    assert (view_dir / "__pycache__").is_symlink()
    assert (target / "module.cpython-312.pyc").exists()
    assert not real_cache.exists()


def test_remove_python_cache_tolerates_concurrent_removal(tmp_path: pathlib.Path, monkeypatch):
    """Files and directories removed by another process while walking are not an error."""
    cache = tmp_path / "var" / "__pycache__"
    cache.mkdir(parents=True)
    (tmp_path / "var" / "stale.pyc").touch()

    real_remove = os.remove

    def remove_twice(path, *args, **kwargs):
        real_remove(path)
        real_remove(path)  # raises FileNotFoundError, as if another process got there first

    monkeypatch.setattr(spack.cmd.clean.os, "remove", remove_twice)
    monkeypatch.setattr(spack.cmd.clean, "lib_path", str(tmp_path / "lib"))
    monkeypatch.setattr(spack.cmd.clean, "var_path", str(tmp_path / "var"))

    spack.cmd.clean.remove_python_cache()

    assert not (tmp_path / "var" / "stale.pyc").exists()
    assert not cache.exists()
