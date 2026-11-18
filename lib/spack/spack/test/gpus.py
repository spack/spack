# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Tests for the translation of detected GPUs into Spack variant values."""

import pytest

import spack.vendor.archspec.gpu as archspec_gpu

import spack.gpus


def _gpu(name: str, vendor: str = "") -> archspec_gpu.GPUMicroarch:
    """A detected GPU: the archspec node for a known name, a bare node otherwise."""
    return archspec_gpu.TARGETS.get(name) or archspec_gpu.GPUMicroarch(name=name, vendor=vendor)


@pytest.fixture(autouse=True)
def clear_caches():
    """Clear memoized detection results before each test, so patched inputs are seen."""
    spack.gpus.host.cache_clear()
    spack.gpus.host_variants.cache_clear()


def test_host_variants_maps_vendors_to_variants(monkeypatch):
    monkeypatch.setattr(spack.gpus, "host", lambda: [_gpu("90"), _gpu("gfx942")])
    assert spack.gpus.host_variants() == {"cuda_arch": ["90"], "amdgpu_target": ["gfx942"]}


def test_host_variants_deduplicates_and_keeps_order(monkeypatch):
    monkeypatch.setattr(spack.gpus, "host", lambda: [_gpu("80"), _gpu("90"), _gpu("80")])
    assert spack.gpus.host_variants() == {"cuda_arch": ["80", "90"]}


def test_host_variants_skips_unmapped_and_unresolved(monkeypatch):
    monkeypatch.setattr(
        spack.gpus,
        "host",
        lambda: [_gpu("xe", vendor="intel"), _gpu("", vendor="nvidia"), _gpu("gfx90a")],
    )
    assert spack.gpus.host_variants() == {"amdgpu_target": ["gfx90a"]}


def test_host_variants_empty_without_gpus(monkeypatch):
    monkeypatch.setattr(spack.gpus, "host", lambda: [])
    assert spack.gpus.host_variants() == {}


@pytest.mark.parametrize(
    "detected,variant,expected",
    [
        # only the GPUs of the variant's vendor are used
        (["86", "gfx942"], "cuda_arch", ["86"]),
        (["86", "gfx942"], "amdgpu_target", ["gfx942"]),
        # every GPU of that vendor, in detection order, once
        (["80", "90", "80"], "cuda_arch", ["80", "90"]),
        # a GPU newer than the archspec data is still reported by name
        (["999", "80"], "cuda_arch", ["999", "80"]),
    ],
)
def test_resolve_host_default(monkeypatch, detected, variant, expected):
    monkeypatch.setattr(spack.gpus, "host", lambda: [_gpu(n, vendor="nvidia") for n in detected])
    assert spack.gpus.resolve_host_default(variant) == expected


@pytest.mark.parametrize("detected", [[], ["gfx942"]])
def test_resolve_host_default_without_matching_gpu_is_an_error(monkeypatch, detected):
    monkeypatch.setattr(spack.gpus, "host", lambda: [_gpu(n) for n in detected])
    with pytest.raises(spack.gpus.NoHostGPUError, match="requires a nvidia GPU"):
        spack.gpus.resolve_host_default("cuda_arch")


def test_resolve_host_default_rejects_non_gpu_variants():
    with pytest.raises(ValueError, match="not a GPU architecture variant"):
        spack.gpus.resolve_host_default("shared")
