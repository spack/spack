# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import ast

import spack.paths
import spack.util.package_hash as ph
from spack.spec import Spec
from spack.util.unparse import unparse


def test_hash(tmpdir, mock_packages, config):
    ph.package_hash("hash-test1@1.2")


def test_different_variants(tmpdir, mock_packages, config):
    spec1 = Spec("hash-test1@1.2 +variantx")
    spec2 = Spec("hash-test1@1.2 +varianty")
    assert ph.package_hash(spec1) == ph.package_hash(spec2)


def test_all_same_but_name(tmpdir, mock_packages, config):
    spec1 = Spec("hash-test1@1.2")
    spec2 = Spec("hash-test2@1.2")
    compare_sans_name(True, spec1, spec2)

    spec1 = Spec("hash-test1@1.2 +varianty")
    spec2 = Spec("hash-test2@1.2 +varianty")
    compare_sans_name(True, spec1, spec2)


def test_all_same_but_archive_hash(tmpdir, mock_packages, config):
    """
    Archive hash is not intended to be reflected in Package hash.
    """
    spec1 = Spec("hash-test1@1.3")
    spec2 = Spec("hash-test2@1.3")
    compare_sans_name(True, spec1, spec2)


def test_all_same_but_patch_contents(tmpdir, mock_packages, config):
    spec1 = Spec("hash-test1@1.1")
    spec2 = Spec("hash-test2@1.1")
    compare_sans_name(True, spec1, spec2)


def test_all_same_but_patches_to_apply(tmpdir, mock_packages, config):
    spec1 = Spec("hash-test1@1.4")
    spec2 = Spec("hash-test2@1.4")
    compare_sans_name(True, spec1, spec2)


def test_all_same_but_install(tmpdir, mock_packages, config):
    spec1 = Spec("hash-test1@1.5")
    spec2 = Spec("hash-test2@1.5")
    compare_sans_name(False, spec1, spec2)


def compare_sans_name(eq, spec1, spec2):
    content1 = ph.package_content(spec1)
    content1 = content1.replace(spec1.package.__class__.__name__, '')
    content2 = ph.package_content(spec2)
    content2 = content2.replace(spec2.package.__class__.__name__, '')
    if eq:
        assert content1 == content2
    else:
        assert content1 != content2


many_strings = '''\
"""ONE"""
"""TWO"""

var = "THREE"  # make sure this is not removed

"FOUR"

class ManyDocstrings:
    """FIVE"""
    """SIX"""

    x = "SEVEN"

    def method1():
        """EIGHT"""

        print("NINE")

        "TEN"
        for i in range(10):
            print(i)

    def method2():
        """ELEVEN"""
        return "TWELVE"
'''


def test_remove_docstrings():
    tree = ast.parse(many_strings)
    tree = ph.RemoveDocstrings().visit(tree)

    unparsed = unparse(tree)

    # make sure the methods are preserved
    assert "method1" in unparsed
    assert "method2" in unparsed

    # all of these are unassigned and should be removed
    assert "ONE" not in unparsed
    assert "TWO" not in unparsed
    assert "FOUR" not in unparsed
    assert "FIVE" not in unparsed
    assert "SIX" not in unparsed
    assert "EIGHT" not in unparsed
    assert "TEN" not in unparsed
    assert "ELEVEN" not in unparsed

    # these are used in legitimate expressions
    assert "THREE" in unparsed
    assert "SEVEN" in unparsed
    assert "NINE" in unparsed
    assert "TWELVE" in unparsed
