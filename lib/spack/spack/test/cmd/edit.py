# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pathlib

import spack.paths
import spack.repo
import spack.util.editor
from spack.main import SpackCommand

edit = SpackCommand("edit")


def test_edit_packages(monkeypatch, mock_packages: spack.repo.RepoPath):
    """Test spack edit pkg-a pkg-b"""
    path_a = mock_packages.filename_for_package_name("pkg-a")
    path_b = mock_packages.filename_for_package_name("pkg-b")
    called = False

    def editor(*args: str, **kwargs):
        nonlocal called
        called = True
        assert args[0] == path_a
        assert args[1] == path_b

    monkeypatch.setattr(spack.util.editor, "editor", editor)
    edit("pkg-a", "pkg-b")
    assert called


def test_edit_files(monkeypatch, mock_packages):
    """Test spack edit --build-system autotools cmake"""
    called = False

    def editor(*args: str, **kwargs):
        nonlocal called
        called = True
        from spack_repo.builtin_mock.build_systems import autotools, cmake  # type: ignore

        assert os.path.samefile(args[0], autotools.__file__)
        assert os.path.samefile(args[1], cmake.__file__)

    monkeypatch.setattr(spack.util.editor, "editor", editor)
    edit("--build-system", "autotools", "cmake")
    assert called


def test_edit_non_default_build_system(monkeypatch, mock_packages, mutable_config):
    called = False

    def editor(*args: str, **kwargs):
        nonlocal called
        called = True
        from spack_repo.builtin_mock.build_systems import autotools, cmake  # type: ignore

        assert os.path.samefile(args[0], autotools.__file__)
        assert os.path.samefile(args[1], cmake.__file__)

    monkeypatch.setattr(spack.util.editor, "editor", editor)

    # set up an additional repo
    extra_repo_dir = pathlib.Path(spack.paths.test_repos_path) / "spack_repo" / "requirements_test"
    with spack.repo.use_repositories(str(extra_repo_dir), override=False):
        edit("--build-system", "builtin_mock.autotools", "builtin_mock.cmake")
        assert called
