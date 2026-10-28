# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

import pytest

from spack.main import SpackCommand
from spack.util.tty.color import color_when

dependents = SpackCommand("dependents")


def test_immediate_dependents(mock_packages):
    out = dependents("libelf")
    actual = set(re.split(r"\s+", out.strip()))
    assert actual == set(
        [
            "dyninst",
            "libdwarf",
            "patch-a-dependency",
            "patch-several-dependencies",
            "quantum-espresso",
            "conditionally-patch-dependency",
        ]
    )


def test_transitive_dependents(mock_packages):
    out = dependents("--transitive", "libelf")
    actual = set(re.split(r"\s+", out.strip()))
    assert actual == {
        "callpath",
        "dyninst",
        "libdwarf",
        "mixing-parent",
        "mpileaks",
        "multivalue-variant",
        "singlevalue-variant-dependent",
        "trilinos",
        "patch-a-dependency",
        "patch-several-dependencies",
        "quantum-espresso",
        "conditionally-patch-dependency",
    }


def test_format_requires_installed(mock_packages):
    dependents("--format", "{name}", "libelf", fail_on_error=False)
    assert dependents.returncode == 2
    assert "--format requires --installed" in dependents.output


@pytest.mark.db
def test_immediate_installed_dependents(mock_packages, database):
    with color_when(False):
        out = dependents("--installed", "libelf")

    lines = [li for li in out.strip().split("\n") if not li.startswith("--")]
    hashes = set([re.split(r"\s+", li)[0] for li in lines if li])

    expected = set([database.query_one(s).dag_hash(7) for s in ["dyninst", "libdwarf"]])

    libelf = database.query_one("libelf")
    expected = set([d.dag_hash(7) for d in libelf.dependents()])

    assert expected == hashes


@pytest.mark.db
def test_transitive_installed_dependents(mock_packages, database):
    with color_when(False):
        out = dependents("--installed", "--transitive", "fake")

    lines = [li for li in out.strip().split("\n") if li and not li.startswith("--")]
    hashes = set([re.split(r"\s+", li)[0] for li in lines])

    expected = set(
        [database.query_one(s).dag_hash(7) for s in ["zmpi", "callpath^zmpi", "mpileaks^zmpi"]]
    )

    assert expected == hashes


@pytest.mark.db
def test_format_installed_dependents(mock_packages, database):
    libelf = database.query_one("libelf")
    out = dependents("--installed", "--format", "{name}", "libelf")
    assert set(out.splitlines()) == {d.name for d in libelf.dependents()}
    assert "Dependents of" not in out

    out = dependents("--installed", "--format", "/{hash}", "libelf")
    assert set(out.splitlines()) == {"/" + d.dag_hash() for d in libelf.dependents()}
    assert all(line.startswith("/") for line in out.splitlines())


@pytest.mark.db
def test_format_installed_dependents_tty(mock_packages, database, mock_tty_stdout):
    libelf = database.query_one("libelf")
    out = dependents("--installed", "--format", "{name}", "libelf")
    assert set(out.splitlines()) == {d.name for d in libelf.dependents()}
    assert "Dependents of" not in out


@pytest.mark.db
def test_format_empty_installed_dependents(mock_packages, database):
    leaf = next(s for s in database.query() if not database.installed_relatives(s, "parents"))
    out = dependents("--installed", "--format", "{name}", leaf.format("{name}{/hash}"))
    assert out.strip() == "No dependents"


@pytest.mark.db
def test_empty_format_installed_dependents(mock_packages, database):
    # An empty format string is valid and produces one blank line per result.
    libelf = database.query_one("libelf")
    out = dependents("--installed", "--format=", "libelf")
    assert out.splitlines() == [""] * len(libelf.dependents())
