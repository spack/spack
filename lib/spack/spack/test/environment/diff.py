# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from typing import Dict, Tuple

import spack.concretize
import spack.environment as ev
import spack.spec
from spack import spec_diff
from spack.environment import diff


def _roots(*pairs: Tuple[ev.UserSpecId, str]) -> Dict[ev.UserSpecId, spack.spec.Spec]:
    """Map input specs to the concrete specs of the given strings."""
    return {root: spack.concretize.concretize_one(concrete) for root, concrete in pairs}


def test_input_spec_diff(mock_packages, config):
    """Tests that input specs are split into common ones and ones in only one environment."""
    mpileaks = ev.UserSpecId("default", spack.spec.Spec("mpileaks"))
    libelf = ev.UserSpecId("default", spack.spec.Spec("libelf"))
    zlib = ev.UserSpecId("default", spack.spec.Spec("zlib"))

    result = diff.input_spec_diff(
        _roots((mpileaks, "mpileaks"), (libelf, "libelf")),
        _roots((mpileaks, "mpileaks"), (zlib, "zlib")),
    )

    assert result.common == [mpileaks]
    assert result.only_in_a == [libelf]
    assert result.only_in_b == [zlib]


def test_input_spec_diff_distinguishes_groups(mock_packages, config):
    """Tests that the same abstract spec in two groups gives two input specs."""
    in_default = ev.UserSpecId("default", spack.spec.Spec("mpileaks"))
    in_group = ev.UserSpecId("other", spack.spec.Spec("mpileaks"))

    result = diff.input_spec_diff(
        _roots((in_default, "mpileaks"), (in_group, "mpileaks")), _roots((in_default, "mpileaks"))
    )

    assert result.common == [in_default]
    assert result.only_in_a == [in_group]
    assert result.only_in_b == []


def test_environment_diff_as_dict_is_canonical_and_omits_environment_identity(
    mock_packages, config
):
    """Tests that the serialization has a fixed schema and order, and no environment identity."""
    a = spack.concretize.concretize_one("mpileaks ^mpich@3.0.4")
    b = spack.concretize.concretize_one("mpileaks ^mpich@1.0")
    nodes = spec_diff.diff_concrete_dags(a, b)

    root = ev.UserSpecId("default", spack.spec.Spec("mpileaks"))
    zlib = ev.UserSpecId("default", spack.spec.Spec("zlib"))
    libelf = ev.UserSpecId("default", spack.spec.Spec("libelf"))
    result = diff.EnvironmentDiff(
        # only_in_a is passed out of canonical order, to prove as_dict imposes one
        inputs=diff.InputDiff(only_in_a=[zlib, libelf], only_in_b=[], common=[root]),
        providers=[],
        divergences=[diff.UserSpecDivergence(root, nodes)],
        unresolved=[],
    )

    payload = result.as_dict()

    # The whole schema, and nothing about which two environments were compared
    assert set(payload) == {
        "_meta",
        "only_in_a",
        "only_in_b",
        "common",
        "providers",
        "unresolved",
        "divergences",
    }

    assert payload["_meta"] == {
        "file-type": "spack-environment-diff",
        "diff-version": spec_diff.DIFF_FORMAT_VERSION,
    }

    # Canonical order, regardless of the order the inputs arrived in
    assert [entry["spec"] for entry in payload["only_in_a"]] == ["libelf", "zlib"]

    # The divergence is serialized at the node that differs, with both dag hashes
    node = payload["divergences"][0]["nodes"][0]
    assert node["name"] == "mpich"
    assert node["hash_a"] == a["mpich"].dag_hash()
    assert node["hash_b"] == b["mpich"].dag_hash()
    assert any(attribute["category"] == "version" for attribute in node["attributes"])
