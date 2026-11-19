# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import sys
from typing import Dict

import pytest

from spack.util.environment import EnvironmentModifications
from spack.util.undo_record import (
    EnvironmentTooLargeError,
    UndoRecord,
    Unit,
    apply_changes,
    check_environment_size,
    ops_from_modifications,
    unit_key,
)

pytestmark = pytest.mark.not_on_windows("paths and separators are POSIX")


def _without_environment(environ: Dict[str, str]) -> UndoRecord:
    """Returns the record of ``environ`` with the unit of the active environment removed."""
    record = UndoRecord.from_environ(environ)
    active = record.find("env")
    if active is not None:
        record.remove(active.key)
    return record


def activate(environ: Dict[str, str], path: str, mods: EnvironmentModifications):
    """Returns the environment after activating the environment at ``path``, which applies
    ``mods``, replacing the active one."""
    record = _without_environment(environ)
    record.push(Unit(unit_key("env", path), ops_from_modifications(mods)))
    return apply_changes(environ, record.environment_changes())


def deactivate(environ: Dict[str, str]):
    """Returns the environment after deactivating the active environment."""
    return apply_changes(environ, _without_environment(environ).environment_changes())


def view_mods(view: str = "/env/view", *extra_bin: str) -> EnvironmentModifications:
    mods = EnvironmentModifications()
    for path in extra_bin:
        mods.prepend_path("PATH", path)
    mods.prepend_path("PATH", f"{view}/bin")
    mods.prepend_path("MANPATH", f"{view}/share/man")
    mods.prepend_path("CMAKE_PREFIX_PATH", view)
    mods.prepend_path("LUA_PATH", f"{view}/share/?.lua", separator=";")
    return mods


def test_deactivate_restores_the_environment_exactly():
    """Entries already on PATH, unset variables and MANPATH come back as they were."""
    before = {"PATH": "/env/view/bin:/usr/bin:/opt/ext/bin:/bin", "MANPATH": "/usr/share/man"}
    during = activate(before, "/env", view_mods("/env/view", "/opt/ext/bin"))

    assert during["PATH"] == "/env/view/bin:/opt/ext/bin:/usr/bin:/bin"
    assert during["MANPATH"] == "/env/view/share/man:/usr/share/man:"
    assert during["LUA_PATH"] == "/env/view/share/?.lua"

    assert deactivate(during) == before


def test_activation_keeps_values_as_written():
    """A trailing slash in a value that is set, and empty path entries, are not rewritten."""
    mods = view_mods()
    mods.set("NWCHEM_BASIS_LIBRARY", "/env/view/share/libraries/")
    before = {"PATH": "/usr/bin::/bin/"}
    during = activate(before, "/env", mods)

    assert during["NWCHEM_BASIS_LIBRARY"] == "/env/view/share/libraries/"
    assert during["PATH"] == "/env/view/bin:/usr/bin::/bin/"
    assert deactivate(during) == before


def test_changes_made_after_activation_are_kept():
    before = {"PATH": "/usr/bin:/bin", "FOO": "user"}
    mods = view_mods()
    mods.set("FOO", "env")
    during = activate(before, "/env", mods)
    assert during["FOO"] == "env"

    during["PATH"] = (
        "/first:" + during["PATH"].replace("/usr/bin:", "/usr/bin:/middle:") + ":/last"
    )
    during["PATH"] = during["PATH"].replace(":/bin:", ":")
    during["MANPATH"] += "/my/man"

    after = deactivate(during)
    assert after["PATH"] == "/first:/usr/bin:/middle:/last"
    assert after["MANPATH"] == "/my/man"
    assert after["FOO"] == "user"
    assert not any(name.startswith("SPACK_UNDO") for name in after)


def test_variable_overwritten_after_activation_keeps_the_new_value():
    before = {"PATH": "/usr/bin", "FOO": "user"}
    mods = EnvironmentModifications()
    mods.set("FOO", "env")
    mods.unset("BAR")
    during = activate({**before, "BAR": "bar"}, "/env", mods)
    assert "BAR" not in during

    during["FOO"] = "mine"
    after = deactivate(during)
    assert after["FOO"] == "mine"
    assert after["BAR"] == "bar"


def test_entries_shared_by_two_environments():
    """Replacing an environment leaves the entries the new one also inserts in place, and
    deactivating the second one gives back the shell from before the first."""
    before = {"PATH": "/usr/bin:/bin"}
    first = activate(before, "/env1", view_mods("/env1/view", "/opt/shared/bin"))
    second = activate(first, "/env2", view_mods("/env2/view", "/opt/shared/bin"))

    assert second["PATH"] == "/env2/view/bin:/opt/shared/bin:/usr/bin:/bin"
    assert second["SPACK_UNDO_STACK"].count("env:") == 1
    assert deactivate(second) == before


def test_activating_twice_does_not_duplicate_entries():
    before = {"PATH": "/usr/bin"}
    once = activate(before, "/env", view_mods())
    twice = activate(once, "/env", view_mods())
    assert twice["PATH"] == once["PATH"]
    assert deactivate(twice) == before


def test_forgetting_a_unit_leaves_the_shell_as_it_is():
    """A unit undone outside the record, for instance by a Spack that does not record its
    changes, is forgotten without changing any variable."""
    during = activate({"PATH": "/usr/bin:/bin"}, "/env", view_mods())

    elsewhere = dict(during)
    elsewhere["PATH"] = "/usr/bin:/bin:/new"
    del elsewhere["LUA_PATH"]

    record = UndoRecord.from_environ(elsewhere)
    record.forget(unit_key("env", "/env"))
    changes = record.environment_changes()
    assert all(name.startswith("SPACK_UNDO_") for name in changes)
    assert all(value is None for value in changes.values())


@pytest.mark.parametrize(
    "variable,value",
    [
        ("SPACK_UNDO_STACK", "env:abc load;rm"),
        (None, "not base64!"),
        ("SPACK_UNDO_BASE", "eJwrSS0uAQAEXQHB"),
        ("SPACK_UNDO_SEEN", "PATH;x"),
    ],
)
def test_unreadable_record_is_ignored(variable, value):
    """A corrupted record variable (None for the variable of the unit) is ignored."""
    during = activate({"PATH": "/usr/bin"}, "/env", view_mods())
    if variable is None:
        (variable,) = (name for name in during if name.startswith("SPACK_UNDO_U_"))
    during[variable] = value

    with pytest.warns(UserWarning, match="ignoring the undo record"):
        record = UndoRecord.from_environ(during)
    assert record.find("env") is None


@pytest.mark.skipif(not sys.platform.startswith("linux"), reason="Linux exec limits")
def test_environment_too_large_for_exec():
    with pytest.raises(EnvironmentTooLargeError, match="BIG"):
        check_environment_size({"PATH": "/usr/bin"}, {"BIG": "x" * 200_000})
    check_environment_size({"PATH": "/usr/bin"}, {"BIG": "x" * 100_000})


def test_repeated_modifications_are_all_applied():
    """Two packages in a view appending the same flag, or each removing the first copy of the
    same path, change the variable twice."""
    mods = EnvironmentModifications()
    for _ in range(2):
        mods.append_flags("FFLAGS", "-x")
        mods.remove_first_path("PATH", "/opt/old/bin")
    before = {"PATH": "/opt/old/bin:/usr/bin:/opt/old/bin:/bin"}
    during = activate(before, "/env", mods)

    assert during["FFLAGS"] == "-x -x"
    assert during["PATH"] == "/usr/bin:/bin"
    assert deactivate(during) == before
