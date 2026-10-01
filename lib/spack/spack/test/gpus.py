# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Tests for the translation of detected GPUs into Spack variant defaults."""

from types import SimpleNamespace

import pytest

import spack.gpus


def _gpu(vendor: str, name: str, brand_string: str = "") -> SimpleNamespace:
    return SimpleNamespace(vendor=vendor, name=name, brand_string=brand_string)


@pytest.fixture(autouse=True)
def clear_caches():
    """Clear memoized detection results before each test, so patched inputs are seen."""
    spack.gpus.host.cache_clear()
    spack.gpus.host_variants.cache_clear()


def test_host_variants_maps_vendors_to_variants(monkeypatch):
    monkeypatch.setattr(
        spack.gpus, "host", lambda: [_gpu("nvidia", "90", "NVIDIA H100"), _gpu("amd", "gfx942")]
    )
    assert spack.gpus.host_variants() == {"cuda_arch": ["90"], "amdgpu_target": ["gfx942"]}


def test_host_variants_deduplicates_and_keeps_order(monkeypatch):
    monkeypatch.setattr(
        spack.gpus,
        "host",
        lambda: [_gpu("nvidia", "80"), _gpu("nvidia", "90"), _gpu("nvidia", "80")],
    )
    assert spack.gpus.host_variants() == {"cuda_arch": ["80", "90"]}


def test_host_variants_skips_unmapped_and_unresolved(monkeypatch):
    monkeypatch.setattr(
        spack.gpus,
        "host",
        lambda: [_gpu("intel", "xe"), _gpu("nvidia", ""), _gpu("amd", "gfx90a")],
    )
    assert spack.gpus.host_variants() == {"amdgpu_target": ["gfx90a"]}


def test_host_variants_empty_without_gpus(monkeypatch):
    monkeypatch.setattr(spack.gpus, "host", lambda: [])
    assert spack.gpus.host_variants() == {}
