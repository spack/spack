# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import spack.concretize
import spack.environment as ev
import spack.spec
from spack import spec_diff
from spack.environment import diff


def test_input_spec_diff():
    """Tests basic construction of input diff"""
    mpileaks = ev.UserSpecId("default", spack.spec.Spec("mpileaks"))
    libelf = ev.UserSpecId("default", spack.spec.Spec("libelf"))
    zlib = ev.UserSpecId("default", spack.spec.Spec("zlib"))

    result = diff.input_spec_diff([mpileaks, libelf], [mpileaks, zlib])

    assert result.common == [mpileaks]
    assert result.only_in_a == [libelf]
    assert result.only_in_b == [zlib]


def test_input_spec_diff_distinguishes_groups():
    """The same abstract spec in two groups is two distinct input specs, not one."""
    in_default = ev.UserSpecId("default", spack.spec.Spec("mpileaks"))
    in_group = ev.UserSpecId("other", spack.spec.Spec("mpileaks"))

    result = diff.input_spec_diff([in_default, in_group], [in_default])

    assert result.common == [in_default]
    assert result.only_in_a == [in_group]
    assert result.only_in_b == []


def test_diff_environments_reports_an_input_it_cannot_explain(
    mutable_mock_env_path, mutable_config, mutable_mock_repo, tmp_path, monkeypatch
):
    """Tests that we have a catch-all reason for two roots that differ, but cannot be explained
    otherwise. In other words, we don't silently drop an unexpected case but we report it.
    """
    environments = []
    for name in ("a", "b"):
        (tmp_path / f"{name}.yaml").write_text("spack:\n  specs:\n  - mpileaks\n")
        environment = ev.create(name, str(tmp_path / f"{name}.yaml"))
        with environment:
            environment.concretize()
            environment.write()
        environments.append(environment)

    env_a, env_b = environments

    concrete = env_b.concrete_roots()[0]
    for node in concrete.traverse():
        node.clear_caches(ignore=("_package_hash",))
    concrete["callpath"]._package_hash = "0" * 32

    # Every difference a comparable environment can carry is accounted for by now, so this bucket
    # is reached only if that ever stops holding. Blind the comparison rather than leave the
    # promise that nothing is dropped silently untested.
    monkeypatch.setattr(spec_diff, "_compare_nodes", lambda a, b: [])

    result = diff.diff_environments(env_a, env_b)

    assert result.divergences == []
    assert [str(root.spec) for root in result.unresolved] == ["mpileaks"]


def test_environment_diff_as_dict_is_canonical_and_omits_environment_identity(
    mock_packages, config
):
    """Tests serializing and EnvironmentDiff."""
    a = spack.concretize.concretize_one("mpileaks ^mpich@3.0.4")
    b = spack.concretize.concretize_one("mpileaks ^mpich@1.0")
    nodes = spec_diff.diff_concrete_dags(a, b)

    root = ev.UserSpecId("default", spack.spec.Spec("mpileaks"))
    zlib = ev.UserSpecId("default", spack.spec.Spec("zlib"))
    libelf = ev.UserSpecId("default", spack.spec.Spec("libelf"))
    result = diff.EnvironmentDiff(
        # only_in_a is passed out of canonical order, to prove as_dict imposes one
        inputs=diff.InputDiff(only_in_a=[zlib, libelf], only_in_b=[], common=[root]),
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
        "unresolved",
        "divergences",
    }

    # Canonical order, regardless of the order the inputs arrived in
    assert [entry["spec"] for entry in payload["only_in_a"]] == ["libelf", "zlib"]

    # The one divergence transcribes to the node that actually differs, with both dag hashes
    node = payload["divergences"][0]["nodes"][0]
    assert node["name"] == "mpich"
    assert node["hash_a"] == a["mpich"].dag_hash()
    assert node["hash_b"] == b["mpich"].dag_hash()
    assert any(attribute["category"] == "version" for attribute in node["attributes"])


def test_environment_diff_as_dict_is_versioned():
    """Tests that the serialization carries its own format version."""
    result = diff.EnvironmentDiff(
        inputs=diff.InputDiff(only_in_a=[], only_in_b=[], common=[]), divergences=[], unresolved=[]
    )

    payload = result.as_dict()

    assert payload["_meta"] == {
        "file-type": "spack-environment-diff",
        "diff-version": diff.DIFF_FORMAT_VERSION,
    }
