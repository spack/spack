# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import pytest

import spack.cmd.diff
import spack.concretize
import spack.main
import spack.paths
import spack.repo
import spack.util.spack_json as sjson

install_cmd = spack.main.SpackCommand("install")
diff_cmd = spack.main.SpackCommand("diff")
find_cmd = spack.main.SpackCommand("find")

# Note that the hash of p1 will differ depending on the variant chosen
# we probably always want to omit that from diffs
# p1____
# |     \
# p2     v1
# | ____/ |
# p3      p4

# i1 and i2 provide v1 (and both have the same dependencies)

# All packages have an associated variant


@pytest.fixture
def test_repo(config):
    builder_test_path = os.path.join(spack.paths.test_repos_path, "spack_repo", "diff")
    with spack.repo.use_repositories(builder_test_path) as mock_repo:
        yield mock_repo


def test_diff_ignore(test_repo):
    specA = spack.concretize.concretize_one("p1+usev1")
    specB = spack.concretize.concretize_one("p1~usev1")

    c1 = spack.cmd.diff.compare_specs(specA, specB, to_string=False)

    def match(function, name, args):
        limit = len(args)
        return function.name == name and list(args[:limit]) == list(function.args[:limit])

    def find(function_list, name, args):
        return any(match(f, name, args) for f in function_list)

    assert find(c1["a_not_b"], "node_os", ["p4"])

    c2 = spack.cmd.diff.compare_specs(specA, specB, ignore_packages=["v1"], to_string=False)

    assert not find(c2["a_not_b"], "node_os", ["p4"])
    assert find(c2["intersect"], "node_os", ["p3"])

    # Check ignoring changes on multiple packages

    specA = spack.concretize.concretize_one("p1+usev1 ^p3+p3var")
    specA = spack.concretize.concretize_one("p1~usev1 ^p3~p3var")

    c3 = spack.cmd.diff.compare_specs(specA, specB, to_string=False)
    assert find(c3["a_not_b"], "variant_value", ["p3", "p3var"])

    c4 = spack.cmd.diff.compare_specs(specA, specB, ignore_packages=["v1", "p3"], to_string=False)
    assert not find(c4["a_not_b"], "node_os", ["p4"])
    assert not find(c4["a_not_b"], "variant_value", ["p3"])


def test_diff_cmd(install_mockery, mock_fetch, mock_archive, mock_packages):
    """Test that we can install two packages and diff them"""

    specA = spack.concretize.concretize_one("mpileaks")
    specB = spack.concretize.concretize_one("mpileaks+debug")

    # Specs should be the same as themselves
    c = spack.cmd.diff.compare_specs(specA, specA, to_string=True)
    assert len(c["a_not_b"]) == 0
    assert len(c["b_not_a"]) == 0

    # Calculate the comparison (c)
    c = spack.cmd.diff.compare_specs(specA, specB, to_string=True)

    # these particular diffs should have the same length b/c thre aren't
    # any node differences -- just value differences.
    assert len(c["a_not_b"]) == len(c["b_not_a"])

    # ensure that variant diffs are in here the result
    assert ["variant_value", "mpileaks debug False"] in c["a_not_b"]
    assert ["variant_value", "mpileaks debug True"] in c["b_not_a"]

    # ensure that hash diffs are in here the result
    assert ["hash", "mpileaks %s" % specA.dag_hash()] in c["a_not_b"]
    assert ["hash", "mpileaks %s" % specB.dag_hash()] in c["b_not_a"]


def test_load_first(install_mockery, mock_fetch, mock_archive, mock_packages):
    """Test with and without the --first option"""
    install_cmd("--fake", "mpileaks")

    # Only one version of mpileaks will work
    diff_cmd("mpileaks", "mpileaks")

    # 2 specs are required for a diff
    with pytest.raises(spack.main.SpackCommandError):
        diff_cmd("mpileaks")
    with pytest.raises(spack.main.SpackCommandError):
        diff_cmd("mpileaks", "mpileaks", "mpileaks")

    # Ensure they are the same
    assert "No differences" in diff_cmd("mpileaks", "mpileaks")
    output = diff_cmd("--json", "mpileaks", "mpileaks")
    result = sjson.load(output)

    assert not result["a_not_b"]
    assert not result["b_not_a"]

    assert "mpileaks" in result["a_name"]
    assert "mpileaks" in result["b_name"]

    # spot check attributes in the intersection to ensure they describe the spec
    assert "intersect" in result
    assert all(
        ["node", dep] in result["intersect"]
        for dep in ("mpileaks", "callpath", "dyninst", "libelf", "libdwarf", "mpich")
    )
    assert all(
        len([diff for diff in result["intersect"] if diff[0] == attr]) == 8
        for attr in (
            "version",
            "node_target",
            "node_platform",
            "node_os",
            "node",
            "package_hash",
            "hash",
        )
    )

    # After we install another version, it should ask us to disambiguate
    install_cmd("mpileaks+debug")

    # There are two versions of mpileaks
    with pytest.raises(spack.main.SpackCommandError):
        diff_cmd("mpileaks", "mpileaks+debug")

    # But if we tell it to use the first, it won't try to disambiguate
    assert "variant" in diff_cmd("--first", "mpileaks", "mpileaks+debug")

    # This matches them exactly
    debug_hash = find_cmd("--format", "{hash}", "mpileaks+debug").strip()
    no_debug_hashes = find_cmd("--format", "{hash}", "mpileaks~debug")
    no_debug_hash = no_debug_hashes.split()[0]
    output = diff_cmd(
        "--json", "mpileaks/{0}".format(debug_hash), "mpileaks/{0}".format(no_debug_hash)
    )
    result = sjson.load(output)

    assert ["hash", "mpileaks %s" % debug_hash] in result["a_not_b"]
    assert ["variant_value", "mpileaks debug True"] in result["a_not_b"]

    assert ["hash", "mpileaks %s" % no_debug_hash] in result["b_not_a"]
    assert ["variant_value", "mpileaks debug False"] in result["b_not_a"]
