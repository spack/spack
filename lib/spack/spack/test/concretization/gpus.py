# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Tests for variant defaults derived from GPUs detected on the host."""

import pytest

import spack.concretize
import spack.gpus
from spack.spec import Spec

pytestmark = pytest.mark.usefixtures("concretize_scope", "mock_packages")


def _concretize(abstract_spec: str) -> Spec:
    return spack.concretize.concretize_one(abstract_spec)


@pytest.fixture()
def host_gpus(monkeypatch, mutable_config):
    """Enable host GPU detection and pretend an NVIDIA and an AMD GPU are present."""
    mutable_config.set("concretizer:gpus:detect", True)
    monkeypatch.setattr(
        spack.gpus, "host_variants", lambda: {"cuda_arch": ["70"], "amdgpu_target": ["gfx900"]}
    )


@pytest.mark.parametrize(
    "spec_str,variant,expected",
    [("vtk-m +cuda", "cuda_arch", "70"), ("vtk-m +rocm", "amdgpu_target", "gfx900")],
)
def test_host_gpu_sets_default(host_gpus, spec_str, variant, expected):
    """A detected GPU provides the default for the matching sticky variant."""
    spec = _concretize(spec_str)
    assert spec.variants[variant].value == expected


def test_host_gpu_ignored_when_variant_is_inactive(host_gpus):
    """The conditional variant does not appear at all without +cuda."""
    spec = _concretize("vtk-m ~cuda")
    assert "cuda_arch" not in spec.variants


def test_packages_yaml_overrides_host_gpu(host_gpus, mutable_config):
    """A packages.yaml preference takes precedence over the host default."""
    mutable_config.set("packages", {"vtk-m": {"variants": "cuda_arch=none"}}, scope="concretize")
    spec = _concretize("vtk-m +cuda")
    assert spec.variants["cuda_arch"].value == "none"


def test_cli_overrides_host_gpu(host_gpus):
    """A value on the command line takes precedence over the host default."""
    spec = _concretize("vtk-m +cuda cuda_arch=none")
    assert spec.variants["cuda_arch"].value == "none"


def test_detection_disabled_keeps_package_default(host_gpus, mutable_config):
    """With detection off the recipe default is used, even if GPUs are present."""
    mutable_config.set("concretizer:gpus:detect", False)
    spec = _concretize("vtk-m +cuda")
    assert spec.variants["cuda_arch"].value == "none"


def test_unknown_host_value_is_rejected(host_gpus, monkeypatch):
    """A detected value the package does not accept is skipped, not an error."""
    monkeypatch.setattr(spack.gpus, "host_variants", lambda: {"cuda_arch": ["99"]})
    spec = _concretize("vtk-m +cuda")
    assert spec.variants["cuda_arch"].value == "none"
