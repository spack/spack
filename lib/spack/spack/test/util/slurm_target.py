# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import json

import pytest

import spack.vendor.archspec.cpu as cpu

from spack.util import slurm_target as slurm


@pytest.mark.parametrize(
    "nodes, expected",
    [
        ({"n1": "haswell", "n2": "skylake", "n3": "skylake_avx512"}, "haswell"),
        ({"n1": "skylake_avx512", "n2": "cascadelake"}, "skylake_avx512"),
        ({"n1": "zen2", "n2": "zen3"}, "zen2"),
        ({"n1": "zen3", "n2": "sapphirerapids"}, "x86_64_v3"),
    ],
)
def test_resolve_common(nodes, expected):
    result = slurm.resolve(nodes)
    assert result.target == expected
    assert all(cpu.TARGETS[result.target] <= cpu.TARGETS[name] for name in nodes.values())


def test_resolve_generic():
    result = slurm.resolve({"a": "haswell", "b": "skylake"}, "generic")
    assert result.target == "x86_64_v3"


@pytest.mark.parametrize(
    "nodes", [{}, {"a": "not_a_real_archspec_target"}, {"a": "zen3", "b": "neoverse_v2"}]
)
def test_invalid_targets_fail_closed(nodes):
    with pytest.raises(slurm.SlurmTargetError):
        slurm.resolve(nodes)


def test_sinfo_deduplicates_partitions_and_keeps_down_nodes():
    def runner(cmd, timeout):
        assert cmd[0] == "sinfo"
        assert "-a" in cmd
        assert "-p" not in cmd
        assert "-N" in cmd
        return (
            "node01|archspec_haswell|archspec_haswell|cpu*\n"
            "node01|archspec_haswell|archspec_haswell|debug\n"
            "node02|archspec_zen3|archspec_zen3|cpu\n"
        )

    nodes = slurm.slurm_nodes(runner=runner)
    assert sorted(nodes) == ["node01", "node02"]
    assert nodes["node01"].partitions == {"cpu", "debug"}


def test_partition_and_prefixed_cluster_features():
    # Regression: these two sinfo flags are mutually exclusive on Slurm.
    def runner(cmd, timeout):
        assert cmd[0] == "sinfo"
        assert "-a" not in cmd
        assert cmd[-2:] == ["-p", "all_nodes"]
        return (
            "cmptpc|core_i5_10500,archspec_skylake,avx2|archspec_skylake|all_nodes\n"
            "cmptpvevm|core_i5_10500,archspec_skylake,avx2|archspec_skylake|all_nodes\n"
            "slurmcmpt1|xeon_gold_6136,archspec_haswell,avx2|archspec_haswell|all_nodes\n"
            "slurmcmpt2|xeon_e5_2630_v3,archspec_haswell,avx2|archspec_haswell|all_nodes\n"
        )

    targets = slurm.discover(partition="all_nodes", source="features", runner=runner)
    assert targets == {
        "cmptpc": "skylake",
        "cmptpvevm": "skylake",
        "slurmcmpt1": "haswell",
        "slurmcmpt2": "haswell",
    }
    assert slurm.resolve(targets).target == "haswell"


def test_missing_features_fail_closed():
    def runner(cmd, timeout):
        return "node01|archspec_haswell|archspec_haswell|cpu\nnode02|(null)|(null)|cpu\n"

    with pytest.raises(slurm.SlurmTargetError, match="node02"):
        slurm.discover(runner=runner)


def test_auto_probes_only_untagged_nodes():
    commands = []

    def runner(cmd, timeout):
        commands.append(cmd)
        if cmd[0] == "sinfo":
            return "node01|archspec_haswell|archspec_haswell|cpu\nnode02|none|none|cpu\n"
        assert cmd[0] == "srun" and "--nodelist=node02" in cmd
        return "skylake\n"

    data = slurm.discover(source="auto", spack_executable="/spack/bin/spack", runner=runner)
    assert data == {"node01": "haswell", "node02": "skylake"}
    assert len(commands) == 2


def test_probe_limit_prevents_allocations():
    calls = []

    def runner(cmd, timeout):
        calls.append(cmd)
        return "n1|none|none|cpu\nn2|none|none|cpu\n"

    with pytest.raises(slurm.SlurmTargetError, match="exceed"):
        slurm.discover(
            source="auto", spack_executable="/spack/bin/spack", runner=runner, max_probes=1
        )
    assert len(calls) == 1


def test_file_source_without_slurm(tmp_path):
    p = tmp_path / "nodes.json"
    p.write_text('{"n1":"zen2","n2":"zen3"}')
    assert slurm.discover(source="file", inventory=str(p)) == {"n1": "zen2", "n2": "zen3"}


def test_write_scope_strict_and_protect_unmanaged(tmp_path):
    output = tmp_path / "generated"
    nodes = {"n1": "haswell", "n2": "skylake"}
    result = slurm.resolve(nodes)
    slurm.write_scope(
        str(output), result, nodes, partition="cpu", source="features", mode="common"
    )
    config = (output / "packages.yaml").read_text()
    assert "require:" in config and "target=haswell" in config
    assert "host_compatible: false" in (output / "concretizer.yaml").read_text()
    assert json.loads((output / "slurm-target.json").read_text())["node_targets"] == nodes
    (output / "packages.yaml").write_text("packages:\n")
    with pytest.raises(slurm.SlurmTargetError, match="unmanaged"):
        slurm.write_scope(
            str(output), result, nodes, partition="cpu", source="features", mode="common"
        )


def test_mismatched_active_archspec_features_are_rejected():
    def runner(cmd, timeout):
        assert "%b" in cmd[cmd.index("-o") + 1]
        return "node01|archspec_skylake|archspec_haswell|cpu\n"

    with pytest.raises(slurm.SlurmTargetError, match="ActiveFeatures"):
        slurm.discover(source="features", runner=runner)


def test_invalid_active_archspec_features_are_rejected():
    def runner(cmd, timeout):
        return "node01|archspec_haswell|archspec_zen3,archspec_skylake|cpu\n"

    with pytest.raises(slurm.SlurmTargetError, match="ActiveFeatures"):
        slurm.discover(source="features", runner=runner)


def test_file_inventory_does_not_silently_ignore_partition(tmp_path):
    p = tmp_path / "inventory.json"
    p.write_text('{"node01":"haswell"}')
    with pytest.raises(slurm.SlurmTargetError, match="--partition"):
        slurm.discover(source="file", inventory=str(p), partition="cpu")


def test_scope_json_must_be_owned_by_slurm_target(tmp_path):
    nodes = {"node01": "haswell"}
    target = slurm.resolve(nodes)
    scope = tmp_path / "scope"
    scope.mkdir()
    other_data = '{"selected_target":"other","node_targets":{"n":"skylake"}}'
    (scope / "slurm-target.json").write_text(other_data)
    with pytest.raises(slurm.SlurmTargetError, match="unmanaged"):
        slurm.write_scope(
            str(scope), target, nodes, partition=None, source="features", mode="common"
        )
    assert (scope / "slurm-target.json").read_text() == other_data
    assert not (scope / "packages.yaml").exists()
