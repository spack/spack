# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import sys

import pytest

import llnl.syscmd.environment as envutil


@pytest.fixture()
def prepare_environment_for_tests():
    if "TEST_ENV_VAR" in os.environ:
        del os.environ["TEST_ENV_VAR"]
    yield
    del os.environ["TEST_ENV_VAR"]


@pytest.mark.parametrize(
    "tested_path,expected",
    [
        ("C:\\Users" if sys.platform == "win32" else "/usr/bin", True),
        ("/nonsense_path/bin", False),
        ("", False),
        (None, False),
    ],
)
def test_is_system_path(tested_path, expected):
    assert envutil.is_system_path(tested_path) is expected


if sys.platform == "win32":
    TEST_PATHS = [
        "C:\\Users",
        "C:\\",
        "C:\\ProgramData",
        "C:\\nonsense_path",
        "C:\\Program Files",
        "C:\\nonsense_path\\extra\\bin",
    ]
    NON_SYSTEM_PREFIX = "C:\\nonsense_path"
else:
    TEST_PATHS = [
        "/usr/bin",
        "/nonsense_path/lib",
        "/usr/local/lib",
        "/bin",
        "/nonsense_path/extra/bin",
        "/usr/lib64",
    ]
    NON_SYSTEM_PREFIX = "/nonsense_path"


def test_filter_system_paths():
    expected = [p for p in TEST_PATHS if p.startswith(NON_SYSTEM_PREFIX)]
    filtered = envutil.filter_system_paths(TEST_PATHS)
    assert expected == filtered


def deprioritize_system_paths():
    expected = [p for p in TEST_PATHS if p.startswith(NON_SYSTEM_PREFIX)]
    expected.extend([p for p in TEST_PATHS if not p.startswith(NON_SYSTEM_PREFIX)])
    filtered = envutil.deprioritize_system_paths(TEST_PATHS)
    assert expected == filtered


def test_prune_duplicate_paths():
    test_paths = ["/a/b", "/a/c", "/a/b", "/a/a", "/a/c", "/a/a/.."]
    expected = ["/a/b", "/a/c", "/a/a", "/a/a/.."]
    assert expected == envutil.prune_duplicate_paths(test_paths)


def test_get_path(prepare_environment_for_tests):
    os.environ["TEST_ENV_VAR"] = os.pathsep.join(["/a", "/b", "/c/d"])
    expected = ["/a", "/b", "/c/d"]
    assert envutil.get_path("TEST_ENV_VAR") == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        # Flag is set
        ("1", True),
        ("TRUE", True),
        ("True", True),
        ("TRue", True),
        ("true", True),
        # Flag is not set
        ("27", False),
        ("-2.3", False),
        ("0", False),
        ("False", False),
        ("false", False),
        ("garbage", False),
    ],
)
def test_env_flag(prepare_environment_for_tests, value, expected):
    assert not envutil.env_flag("TEST_NO_ENV_VAR")
    os.environ["TEST_ENV_VAR"] = value
    assert envutil.env_flag("TEST_ENV_VAR") is expected


def test_path_set(prepare_environment_for_tests):
    envutil.path_set("TEST_ENV_VAR", ["/a", "/a/b", "/a/a"])
    assert os.environ["TEST_ENV_VAR"] == "/a" + os.pathsep + "/a/b" + os.pathsep + "/a/a"


def test_path_put_first(prepare_environment_for_tests):
    envutil.path_set("TEST_ENV_VAR", TEST_PATHS)
    expected = ["/usr/bin", "/new_nonsense_path/a/b"]
    expected.extend([p for p in TEST_PATHS if p != "/usr/bin"])
    envutil.path_put_first("TEST_ENV_VAR", expected)
    assert envutil.get_path("TEST_ENV_VAR") == expected


@pytest.mark.parametrize("shell", ["pwsh", "bat"] if sys.platform == "win32" else ["bash"])
def test_dump_environment(prepare_environment_for_tests, shell_as, shell, tmp_path):
    test_paths = "/a:/b/x:/b/c"
    os.environ["TEST_ENV_VAR"] = test_paths
    envdump_txt = tmp_path / "envdump.txt"
    envutil.dump_environment(str(envdump_txt))
    content = envdump_txt.read_text()
    if shell == "pwsh":
        assert f"$Env:TEST_ENV_VAR={test_paths}\n" in content
    elif shell == "bat":
        assert f'set "TEST_ENV_VAR={test_paths}"\n' in content
    else:
        assert f"TEST_ENV_VAR={test_paths}; export TEST_ENV_VAR\n" in content


def test_reverse_environment_modifications(working_env):
    start_env = {
        "PREPEND_PATH": os.sep + os.path.join("path", "to", "prepend", "to"),
        "APPEND_PATH": os.sep + os.path.join("path", "to", "append", "to"),
        "UNSET": "var_to_unset",
        "APPEND_FLAGS": "flags to append to",
    }

    to_reverse = envutil.EnvironmentModifications()

    to_reverse.prepend_path("PREPEND_PATH", "/new/path/prepended")
    to_reverse.append_path("APPEND_PATH", "/new/path/appended")
    to_reverse.set_path("SET_PATH", ["/one/set/path", "/two/set/path"])
    to_reverse.set("SET", "a var")
    to_reverse.unset("UNSET")
    to_reverse.append_flags("APPEND_FLAGS", "more_flags")

    reversal = to_reverse.reversed()

    os.environ.clear()
    os.environ.update(start_env)

    to_reverse.apply_modifications()
    reversal.apply_modifications()

    start_env.pop("UNSET")
    assert os.environ == start_env


def test_escape_double_quotes_in_shell_modifications():
    to_validate = envutil.EnvironmentModifications()

    to_validate.set("VAR", "$PATH")
    to_validate.append_path("VAR", "$ANOTHER_PATH")

    to_validate.set("QUOTED_VAR", '"MY_VAL"')

    if sys.platform == "win32":
        cmds = to_validate.shell_modifications(shell="bat")
        assert r'set "VAR=$PATH;$ANOTHER_PATH"' in cmds
        assert r'set "QUOTED_VAR="MY_VAL"' in cmds
        cmds = to_validate.shell_modifications(shell="pwsh")
        assert "$Env:VAR='$PATH;$ANOTHER_PATH'" in cmds
        assert "$Env:QUOTED_VAR='\"MY_VAL\"'" in cmds
    else:
        cmds = to_validate.shell_modifications()
        assert 'export VAR="$PATH:$ANOTHER_PATH"' in cmds
        assert r'export QUOTED_VAR="\"MY_VAL\""' in cmds
