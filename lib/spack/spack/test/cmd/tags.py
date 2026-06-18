# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.concretize
import spack.main
import spack.repo
from spack.installer import PackageInstaller

tags = spack.main.SpackCommand("tags")


def test_tags_bad_options(mock_packages):
    out = tags("-a", "tag1", fail_on_error=False)
    assert "option OR provide" in out


def test_tags_no_installed(install_mockery, mock_fetch):
    out = tags("-i")
    assert "No installed" in out


def test_tags_invalid_tag(mock_packages):
    out = tags("nosuchtag")
    assert "None" in out


def test_tags_all_mock_tags(mock_packages):
    out = tags()
    for tag in ["tag1", "tag2", "tag3"]:
        assert tag in out


def test_tags_all_mock_tag_packages(mock_packages):
    out = tags("-a")
    for pkg in ["mpich\n", "mpich2\n"]:
        assert pkg in out


def test_tags_no_tags(repo_builder):
    repo_builder.add_package("pkg-a")
    with spack.repo.use_repositories(repo_builder.root):
        out = tags()
    assert "No tagged" in out


def test_tags_installed(install_mockery, mock_fetch):
    s = spack.concretize.concretize_one("mpich")
    PackageInstaller([s.package], explicit=True, fake=True).install()

    out = tags("-i")
    for tag in ["tag1", "tag2"]:
        assert tag in out

    out = tags("-i", "tag1")
    assert "mpich" in out

    out = tags("-i", "tag3")
    assert "No installed" in out
