# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import spack.concretize
from spack.main import SpackCommand, SpackCommandError

graph = SpackCommand("graph")


@pytest.mark.db
@pytest.mark.usefixtures("mock_packages", "database")
def test_graph_ascii():
    """Tests spack graph --ascii"""
    graph("--ascii", "dt-diamond")


@pytest.mark.db
@pytest.mark.usefixtures("mock_packages", "database")
def test_graph_dot():
    """Tests spack graph --dot"""
    graph("--dot", "dt-diamond")


@pytest.mark.db
@pytest.mark.usefixtures("mock_packages", "database")
def test_graph_dot_hashes():
    """Tests that --long/--very-long control the hash in --dot node labels"""
    spec = spack.concretize.concretize_one("dt-diamond")
    no_hash = f'label="{spec.format("{name}{@version}")}"'
    short_hash = f'label="{spec.format("{name}{@version}{/hash:7}")}"'
    full_hash = f'label="{spec.format("{name}{@version}{/hash}")}"'

    none = graph("--dot", "dt-diamond")
    assert no_hash in none and short_hash not in none

    short = graph("--dot", "--long", "dt-diamond")
    assert short_hash in short and full_hash not in short

    full = graph("--dot", "--very-long", "dt-diamond")
    assert full_hash in full


@pytest.mark.db
@pytest.mark.usefixtures("mock_packages", "database")
def test_graph_static():
    """Tests spack graph --static"""
    graph("--static", "dt-diamond")


@pytest.mark.db
@pytest.mark.usefixtures("mock_packages", "database")
def test_graph_installed():
    """Tests spack graph --installed"""

    graph("--installed")

    with pytest.raises(SpackCommandError):
        graph("--installed", "dt-diamond")


@pytest.mark.db
@pytest.mark.usefixtures("mock_packages", "database")
def test_graph_deptype():
    """Tests spack graph --deptype"""
    graph("--deptype", "all", "dt-diamond")


def test_graph_no_specs():
    """Tests spack graph with no arguments"""

    with pytest.raises(SpackCommandError):
        graph()
