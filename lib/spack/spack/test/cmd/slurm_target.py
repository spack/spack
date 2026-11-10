# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.cmd import slurm_target as cmd
from spack.main import SpackCommand

slurm_target = SpackCommand("slurm-target")


def test_slurm_target_detect(monkeypatch):
    monkeypatch.setattr(cmd, "discover", lambda **kwargs: {"n1": "haswell", "n2": "skylake"})
    assert slurm_target("detect", "--target-only").strip() == "haswell"


def test_slurm_target_sync(monkeypatch, tmp_path):
    monkeypatch.setattr(cmd, "discover", lambda **kwargs: {"n1": "haswell", "n2": "skylake"})
    scope = tmp_path / "scope"
    output = slurm_target("sync", "--scope", str(scope))
    assert "Wrote config scope" in output
    assert (scope / "packages.yaml").exists()
    assert (scope / "concretizer.yaml").exists()


def test_slurm_target_spec_delegates(monkeypatch):
    from pathlib import Path
    from types import SimpleNamespace

    import spack.paths

    monkeypatch.setattr(cmd, "discover", lambda **kwargs: {"n1": "haswell", "n2": "skylake"})
    calls = []

    def fake_run(argv, check):
        assert check is False
        assert argv[0] == spack.paths.spack_script
        assert argv[1] == "-C"
        assert (Path(argv[2]) / "packages.yaml").exists()
        assert argv[3:] == ["spec", "zlib"]
        calls.append(argv)
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(cmd.subprocess, "run", fake_run)
    output = slurm_target("spec", "--", "zlib")
    assert "Slurm target: haswell" in output
    assert len(calls) == 1
