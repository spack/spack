# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

import pytest

from spack.main import SpackCommand
from spack.util.tty.color import color_when

dependencies = SpackCommand("dependencies")

MPIS = [
    "intel-parallel-studio",
    "low-priority-provider",
    "mpich",
    "mpich2",
    "multi-provider-mpi",
    "zmpi",
]
COMPILERS = ["gcc", "llvm", "compiler-with-deps"]
MPI_DEPS = ["fake"]
COMPILER_DEPS = ["binutils-for-test", "zlib"]


@pytest.mark.parametrize(
    "cli_args,expected",
    [
        (["mpileaks"], set(["callpath"] + MPIS + COMPILERS)),
        (
            ["--transitive", "mpileaks"],
            set(
                ["callpath", "dyninst", "libdwarf", "libelf"]
                + MPIS
                + MPI_DEPS
                + COMPILERS
                + COMPILER_DEPS
            ),
        ),
        (["--transitive", "--deptype=link,run", "dtbuild1"], {"dtlink2", "dtrun2"}),
        (["--transitive", "--deptype=build", "dtbuild1"], {"dtbuild2", "dtlink2"}),
        (["--transitive", "--deptype=link", "dtbuild1"], {"dtlink2"}),
    ],
)
def test_direct_dependencies(cli_args, expected, mock_packages):
    out = dependencies(*cli_args)
    result = set(re.split(r"\s+", out.strip()))
    assert expected == result


def test_format_requires_installed(mock_packages):
    dependencies("--format", "{name}", "mpileaks", fail_on_error=False)
    assert dependencies.returncode == 2
    assert "--format requires --installed" in dependencies.output


@pytest.mark.db
def test_direct_installed_dependencies(mock_packages, database):
    with color_when(False):
        out = dependencies("--installed", "mpileaks^mpich")

    root = database.query_one("mpileaks ^mpich")

    lines = [line for line in out.strip().split("\n") if line and not line.startswith("--")]
    hashes = {re.split(r"\s+", line)[0] for line in lines}
    expected = {s.dag_hash(7) for s in root.dependencies()}

    assert expected == hashes


@pytest.mark.db
def test_transitive_installed_dependencies(mock_packages, database):
    with color_when(False):
        out = dependencies("--installed", "--transitive", "mpileaks^zmpi")

    root = database.query_one("mpileaks ^zmpi")

    lines = [line for line in out.strip().split("\n") if line and not line.startswith("--")]
    hashes = {re.split(r"\s+", line)[0] for line in lines}
    expected = {s.dag_hash(7) for s in root.traverse(root=False)}

    assert expected == hashes


@pytest.mark.db
def test_format_installed_dependencies(mock_packages, database):
    root = database.query_one("mpileaks ^mpich")
    out = dependencies("--installed", "--format", "{name}", "mpileaks^mpich")
    assert set(out.splitlines()) == {s.name for s in root.dependencies()}
    assert "Dependencies of" not in out

    out = dependencies("--installed", "--format", "/{hash}", "mpileaks^mpich")
    assert set(out.splitlines()) == {"/" + s.dag_hash() for s in root.dependencies()}

    out = dependencies("--installed", "--transitive", "--format", "/{hash}", "mpileaks^mpich")
    assert set(out.splitlines()) == {"/" + s.dag_hash() for s in root.traverse(root=False)}
    assert all(line.startswith("/") for line in out.splitlines())


@pytest.mark.db
def test_format_installed_dependencies_tty(mock_packages, database, mock_tty_stdout):
    root = database.query_one("mpileaks ^mpich")
    out = dependencies("--installed", "--format", "{name}", "mpileaks^mpich")
    assert set(out.splitlines()) == {s.name for s in root.dependencies()}
    assert "Dependencies of" not in out


@pytest.mark.db
def test_format_empty_installed_dependencies(mock_packages, database):
    leaf = next(s for s in database.query() if not database.installed_relatives(s, "children"))
    out = dependencies("--installed", "--format", "{name}", leaf.format("{name}{/hash}"))
    assert out.strip() == "No dependencies"


@pytest.mark.db
def test_empty_format_installed_dependencies(mock_packages, database):
    # An empty format string is valid and produces one blank line per result.
    root = database.query_one("mpileaks ^mpich")
    out = dependencies("--installed", "--format=", "mpileaks^mpich")
    assert out.splitlines() == [""] * len(root.dependencies())
