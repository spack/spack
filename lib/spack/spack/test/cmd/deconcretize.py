# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import spack.environment as ev
from spack.main import SpackCommand, SpackCommandError

deconcretize = SpackCommand("deconcretize")


@pytest.fixture(scope="function")
def test_env(mutable_mock_env_path, config, mock_packages):
    ev.create("test")
    with ev.read("test") as e:
        e.add("a@2.0 foobar=bar ^b@1.0")
        e.add("a@1.0 foobar=bar ^b@0.9")
        e.concretize()
        e.write()


def test_deconcretize_dep(test_env):
    with ev.read("test") as e:
        deconcretize("-y", "b@1.0")
        specs = [s for s, _ in e.concretized_specs()]

    assert len(specs) == 1
    assert specs[0].satisfies("a@1.0")


def test_deconcretize_all_dep(test_env):
    with ev.read("test") as e:
        with pytest.raises(SpackCommandError):
            deconcretize("-y", "b")
        deconcretize("-y", "--all", "b")
        specs = [s for s, _ in e.concretized_specs()]

    assert len(specs) == 0


def test_deconcretize_root(test_env):
    with ev.read("test") as e:
        output = deconcretize("-y", "--root", "b@1.0")
        assert "No matching specs to deconcretize" in output
        assert len(e.concretized_order) == 2

        deconcretize("-y", "--root", "a@2.0")
        specs = [s for s, _ in e.concretized_specs()]

    assert len(specs) == 1
    assert specs[0].satisfies("a@1.0")


def test_deconcretize_all_root(test_env):
    with ev.read("test") as e:
        with pytest.raises(SpackCommandError):
            deconcretize("-y", "--root", "a")

        output = deconcretize("-y", "--root", "--all", "b")
        assert "No matching specs to deconcretize" in output
        assert len(e.concretized_order) == 2

        deconcretize("-y", "--root", "--all", "a")
        specs = [s for s, _ in e.concretized_specs()]

    assert len(specs) == 0


def test_deconcretize_all(test_env):
    with ev.read("test") as e:
        with pytest.raises(SpackCommandError):
            deconcretize()
        deconcretize("-y", "--all")
        specs = [s for s, _ in e.concretized_specs()]

    assert len(specs) == 0
