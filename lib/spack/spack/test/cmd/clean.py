# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pathlib

import pytest

import spack.caches
import spack.cmd.clean
import spack.concretize
import spack.main
import spack.stage
import spack.store
import spack.util.file_cache
import spack.util.filesystem as fs

clean = spack.main.SpackCommand("clean")

#: The autouse mock_fetch_cache fixture replaces this with a stub that has no destroy()
_fetch_cache = spack.caches.fetch_cache

all_effects = ["stages", "downloads", "caches", "failures", "python_cache", "bootstrap"]


@pytest.fixture
def cleanable(install_mockery, mutable_config, mock_stage, tmp_path: pathlib.Path, monkeypatch):
    """Creates one item for each thing ``spack clean`` can remove, and returns a function that
    maps each of them to whether it is still present.
    """
    # The global MISC_CACHE is shared by every test in the process
    misc_cache = spack.util.file_cache.FileCache(tmp_path / "misc_cache")
    monkeypatch.setattr(spack.caches, "MISC_CACHE", misc_cache)
    monkeypatch.setattr(spack.caches, "fetch_cache", _fetch_cache)
    monkeypatch.setattr(spack.cmd.clean, "lib_path", str(tmp_path / "lib"))
    monkeypatch.setattr(spack.cmd.clean, "var_path", str(tmp_path / "var"))
    mutable_config.set("bootstrap:root", str(tmp_path / "bootstrap"))

    source_cache = pathlib.Path(spack.caches.fetch_cache_location(config=mutable_config))
    paths = {
        "stages": pathlib.Path(mock_stage) / f"{spack.stage.stage_prefix}x",
        "downloads": source_cache / "archive",
        "caches": misc_cache.root / "index",
        "python_cache": tmp_path / "lib" / "__pycache__",
        "bootstrap": tmp_path / "bootstrap" / "store",
    }
    for path in paths.values():
        path.mkdir(parents=True)
    failed = spack.concretize.concretize_one("pkg-a")
    spack.store.STORE.failure_tracker.mark(failed)

    def present():
        result = {name: path.exists() for name, path in paths.items()}
        result["failures"] = spack.store.STORE.failure_tracker.has_failed(failed)
        return result

    return present


@pytest.mark.disable_clean_stage_check
@pytest.mark.parametrize(
    "command_line,removed",
    [
        ([], ["stages"]),
        (["-s"], ["stages"]),
        (["-sd"], ["stages", "downloads"]),
        (["-m"], ["caches"]),
        (["-f"], ["failures"]),
        (["-p"], ["python_cache"]),
        (["-b"], ["bootstrap"]),
        (["-a"], all_effects),
    ],
)
def test_clean_removes(command_line, removed, cleanable):
    clean(*command_line)
    assert cleanable() == {name: name not in removed for name in all_effects}


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


@pytest.mark.disable_clean_stage_check
def test_clean_spec_removes_only_its_stage(cleanable):
    stage = pathlib.Path(spack.concretize.concretize_one("mpileaks").package.stage.path)
    stage.mkdir(parents=True)
    clean("mpileaks")
    assert not stage.exists()
    assert all(cleanable().values())
