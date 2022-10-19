# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.spec import Spec
from spack.traverse import traverse_breadth_first_nodes


def test_bf_traversal_is_breadth_first(config, mock_packages):
    # That that depth of discovery is non-decreasing
    s = Spec("dttop").concretized()
    depths = [depth for (depth, _) in traverse_breadth_first_nodes([s], depth=True)]
    assert depths == sorted(depths)


def test_bf_deptype_traversal(config, mock_packages):
    s = Spec("dtuse").concretized()

    names = [
        "dtuse",
        "dttop",
        "dtbuild1",
        "dtlink1",
        "dtbuild2",
        "dtlink2",
        "dtlink3",
        "dtlink4",
    ]

    traversal = traverse_breadth_first_nodes([s], deptype=("build", "link"))
    assert [x.name for x in traversal] == names


def test_bf_deptype_traversal_with_builddeps(config, mock_packages):
    s = Spec("dttop").concretized()

    names = ["dttop", "dtbuild1", "dtlink1", "dtbuild2", "dtlink2", "dtlink3", "dtlink4"]

    traversal = traverse_breadth_first_nodes([s], deptype=("build", "link"))
    assert [x.name for x in traversal] == names


def test_bf_deptype_traversal_full(config, mock_packages):
    s = Spec("dttop").concretized()

    names = [
        "dttop",
        "dtbuild1",
        "dtlink1",
        "dtrun1",
        "dtbuild2",
        "dtlink2",
        "dtrun2",
        "dtlink3",
        "dtlink5",
        "dtrun3",
        "dtlink4",
        "dtbuild3",
    ]

    traversal = traverse_breadth_first_nodes([s], deptype="all")
    assert [x.name for x in traversal] == names


def test_deptype_traversal_run(config, mock_packages):
    s = Spec("dttop").concretized()
    names = ["dttop", "dtrun1", "dtrun3"]
    traversal = traverse_breadth_first_nodes([s], deptype="run")
    assert [x.name for x in traversal] == names
