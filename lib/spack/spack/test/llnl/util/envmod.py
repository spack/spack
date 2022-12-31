# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Test Spack's environment utility functions."""
import os
import sys

import pytest

import llnl.util.envmod as envmod

is_windows = sys.platform == "win32"


def test_is_system_path():
    sys_path = "C:\\Users" if is_windows else "/usr/bin"
    assert envmod.is_system_path(sys_path)
    assert not envmod.is_system_path("/nonsense_path/bin")
    assert not envmod.is_system_path("")
    assert not envmod.is_system_path(None)


if is_windows:
    test_paths = [
        "C:\\Users",
        "C:\\",
        "C:\\ProgramData",
        "C:\\nonsense_path",
        "C:\\Program Files",
        "C:\\nonsense_path\\extra\\bin",
    ]
else:
    test_paths = [
        "/usr/bin",
        "/nonsense_path/lib",
        "/usr/local/lib",
        "/bin",
        "/nonsense_path/extra/bin",
        "/usr/lib64",
    ]


def test_filter_system_paths():
    nonsense_prefix = "C:\\nonsense_path" if is_windows else "/nonsense_path"
    expected = [p for p in test_paths if p.startswith(nonsense_prefix)]
    filtered = envmod.filter_system_paths(test_paths)
    assert expected == filtered


def deprioritize_system_paths():
    expected = [p for p in test_paths if p.startswith("/nonsense_path")]
    expected.extend([p for p in test_paths if not p.startswith("/nonsense_path")])
    filtered = envmod.deprioritize_system_paths(test_paths)
    assert expected == filtered


def test_prune_duplicate_paths():
    test_paths = ["/a/b", "/a/c", "/a/b", "/a/a", "/a/c", "/a/a/.."]
    expected = ["/a/b", "/a/c", "/a/a", "/a/a/.."]
    assert expected == envmod.prune_duplicate_paths(test_paths)


def test_get_path(working_env):
    os.environ["TEST_ENV_VAR"] = os.pathsep.join(["/a", "/b", "/c/d"])
    expected = ["/a", "/b", "/c/d"]
    assert envmod.get_path("TEST_ENV_VAR") == expected


def test_env_flag(working_env):
    assert not envmod.env_flag("TEST_NO_ENV_VAR")
    os.environ["TEST_ENV_VAR"] = "1"
    assert envmod.env_flag("TEST_ENV_VAR")
    os.environ["TEST_ENV_VAR"] = "TRUE"
    assert envmod.env_flag("TEST_ENV_VAR")
    os.environ["TEST_ENV_VAR"] = "True"
    assert envmod.env_flag("TEST_ENV_VAR")
    os.environ["TEST_ENV_VAR"] = "TRue"
    assert envmod.env_flag("TEST_ENV_VAR")
    os.environ["TEST_ENV_VAR"] = "true"
    assert envmod.env_flag("TEST_ENV_VAR")
    os.environ["TEST_ENV_VAR"] = "27"
    assert not envmod.env_flag("TEST_ENV_VAR")
    os.environ["TEST_ENV_VAR"] = "-2.3"
    assert not envmod.env_flag("TEST_ENV_VAR")
    os.environ["TEST_ENV_VAR"] = "0"
    assert not envmod.env_flag("TEST_ENV_VAR")
    os.environ["TEST_ENV_VAR"] = "False"
    assert not envmod.env_flag("TEST_ENV_VAR")
    os.environ["TEST_ENV_VAR"] = "false"
    assert not envmod.env_flag("TEST_ENV_VAR")
    os.environ["TEST_ENV_VAR"] = "garbage"
    assert not envmod.env_flag("TEST_ENV_VAR")


def test_path_set(working_env):
    envmod.path_set("TEST_ENV_VAR", ["/a", "/a/b", "/a/a"])
    assert os.environ["TEST_ENV_VAR"] == "/a" + os.pathsep + "/a/b" + os.pathsep + "/a/a"


def test_path_put_first(working_env):
    envmod.path_set("TEST_ENV_VAR", test_paths)
    expected = ["/usr/bin", "/new_nonsense_path/a/b"]
    expected.extend([p for p in test_paths if p != "/usr/bin"])
    envmod.path_put_first("TEST_ENV_VAR", expected)
    assert envmod.get_path("TEST_ENV_VAR") == expected


def test_reverse_environment_modifications(working_env):
    start_env = {
        "PREPEND_PATH": os.sep + os.path.join("path", "to", "prepend", "to"),
        "APPEND_PATH": os.sep + os.path.join("path", "to", "append", "to"),
        "UNSET": "var_to_unset",
        "APPEND_FLAGS": "flags to append to",
    }

    to_reverse = envmod.EnvironmentModifications()

    to_reverse.prepend_path("PREPEND_PATH", "/new/path/prepended")
    to_reverse.append_path("APPEND_PATH", "/new/path/appended")
    to_reverse.set_path("SET_PATH", ["/one/set/path", "/two/set/path"])
    to_reverse.set("SET", "a var")
    to_reverse.unset("UNSET")
    to_reverse.append_flags("APPEND_FLAGS", "more_flags")

    reversal = to_reverse.reversed()

    os.environ = start_env.copy()

    print(os.environ)
    to_reverse.apply_modifications()
    print(os.environ)
    reversal.apply_modifications()
    print(os.environ)

    start_env.pop("UNSET")
    assert os.environ == start_env
