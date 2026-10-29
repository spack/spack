# Copyright 2019-2026 Lawrence Livermore National Security, LLC and other
# Archspec Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Detection of AMD GPUs through the rocm-smi toolchain."""

import json
import subprocess
import warnings
from typing import List

from .gpu import GPU, GFXTarget, VendorPciCode


def smi_info() -> List[GPU]:
    """Retrieve info for all AMD GPUs using rocm-smi."""

    try:
        result = subprocess.run(
            [
                "rocm-smi",
                "--showproductname",
                "--showdriverversion",
                "--showid",
                "--json",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            check=True,
        )
    except FileNotFoundError:
        warnings.warn("rocm-smi is not installed; skipping AMD GPU detection")
        return []
    except subprocess.CalledProcessError:
        return []

    try:
        data = json.loads(result.stdout)
    except ValueError:
        return []

    # The driver version is reported once for the whole system rather than
    # per-card, under a top-level "system" entry.
    system_info = data.get("system", {})
    driver_version = system_info.get("Driver version", "")

    gpus: List[GPU] = []
    for key, info in data.items():
        if not key.startswith("card"):
            continue

        # Key names vary across rocm-smi versions, so fall back across the
        # known aliases for the marketing name and the PCI device ID.
        name = info.get("Card Series") or info.get("Market Name") or ""
        component_pci_code = info.get("Device ID") or info.get("GPU ID") or ""
        gfx_version = info.get("GFX Version")

        gfx_target = None
        if gfx_version:
            try:
                gfx_target = GFXTarget.from_str(gfx_version)
            except ValueError as e:
                warnings.warn(f"AMD GPU {name!r}: {e}")

        gpus.append(
            GPU(
                name=name,
                vendor="amd",
                # rocm-smi doesn't report the PCI vendor ID, but it's always AMD's
                vendor_pci_code=VendorPciCode.AMD,
                component_pci_code=component_pci_code.lower(),
                driver_version=driver_version,
                gfx_target=gfx_target,
            )
        )
    return gpus
