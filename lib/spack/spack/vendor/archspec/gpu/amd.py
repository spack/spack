# Copyright 2019-2026 Lawrence Livermore National Security, LLC and other
# Archspec Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Detection of AMD GPUs through the rocm-smi toolchain."""

import json
import subprocess
import warnings
from typing import List

from . import schema
from .gpu_microarch import GPUMicroarch


def smi_info() -> List[GPUMicroarch]:
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

    # AMD's PCI vendor code is not reported by rocm-smi, so derive it from the
    # known vendor mapping the same way the ``vendor`` field is hardcoded.
    vendor_pci_code = next(
        code for code, name in schema.DETECTION_JSON["vendors"].items() if name == "amd"
    )

    # The driver version is reported once for the whole system rather than
    # per-card, under a top-level "system" entry.
    system_info = data.get("system", {})
    driver_version = system_info.get("Driver version", "")

    gpus: List[GPUMicroarch] = []
    for key, info in data.items():
        if not key.startswith("card"):
            continue

        # Key names vary across rocm-smi versions, so fall back across the
        # known aliases for the marketing name and the PCI device ID.
        brand_string = info.get("Card Series") or info.get("Market Name") or ""
        component_pci_code = info.get("Device ID") or info.get("GPU ID") or ""
        gfx_version = info.get("GFX Version") or ""

        gpus.append(
            GPUMicroarch(
                name=gfx_version,
                vendor="amd",
                brand_string=brand_string,
                driver_version=driver_version,
                component_pci_code=component_pci_code.lower(),
                vendor_pci_code=vendor_pci_code,
                gfx_target=gfx_version,
            )
        )
    return gpus
