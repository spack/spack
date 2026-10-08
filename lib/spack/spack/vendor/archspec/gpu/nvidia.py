# Copyright 2019-2026 Lawrence Livermore National Security, LLC and other
# Archspec Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Detection of NVIDIA GPUs through the nvidia-smi toolchain."""

import string
import subprocess
import warnings
from typing import List, Tuple

from .gpu_microarch import GPUMicroarch

#: Fields queried from nvidia-smi, in output-column order. ``compute_cap`` is
#: only recognized on newer drivers (~R495+); on older drivers it is dropped
#: (see ``smi_info``), so it is kept last to keep the leading columns
#: at stable indices regardless of whether it is present.
_SMI_BASE_FIELDS = ["gpu_name", "driver_version", "pci.device_id"]


def _parse_pci_device_id(combined_id: str) -> Tuple[str, str]:
    """Parse a combined PCI device ID into (device, vendor) codes.

    Args:
        combined_id: 10-character hex string from nvidia-smi ``pci.device_id``
            (e.g. ``0x2C0210DE``).

    Returns:
        A tuple of ``(component_pci_code, vendor_pci_code)`` in lowercase
        (e.g. ``("0x2c02", "0x10de")``).

    Raises:
        ValueError: if *combined_id* is not a valid 10-character hex string
            with a ``0x`` prefix.
    """
    if len(combined_id) != 10 or combined_id[:2] != "0x":
        raise ValueError(
            "invalid PCI device ID: expected 10-character '0x'-prefixed hex"
            f" string, got {combined_id!r}"
        )

    hex_digits = combined_id[2:]
    if not all(c in string.hexdigits for c in hex_digits):
        raise ValueError(
            "invalid PCI device ID: expected 10-character '0x'-prefixed hex"
            f" string, got {combined_id!r}"
        )

    return (f"0x{hex_digits[:4]}".lower(), f"0x{hex_digits[4:]}".lower())


def _compute_capability_to_compiler_flag(name: str) -> str:
    """Transform decimal format compute capability to format expected by compiler flags.

    e.g. 9.0 -> 90
    """
    # validation
    if not name:
        return ""

    if not name[0].isdigit() or "." not in name:
        return ""

    # parsing
    parsed_name = name.replace(".", "")

    return parsed_name


def _run_smi(fields: List[str]) -> subprocess.CompletedProcess:
    """Run nvidia-smi querying the given GPU fields, in CSV format."""
    return subprocess.run(
        [
            "nvidia-smi",
            f"--query-gpu={','.join(fields)}",
            "--format=csv,noheader",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        check=True,
    )


def smi_info() -> List[GPUMicroarch]:
    """Retrieve info for all NVIDIA GPUs using nvidia-smi."""

    # Try query with compute_cap first, then fall back without it.
    fields = _SMI_BASE_FIELDS + ["compute_cap"]
    try:
        result = _run_smi(fields)
    except FileNotFoundError:
        warnings.warn("nvidia-smi is not installed; skipping NVIDIA GPU detection")
        return []
    except subprocess.CalledProcessError:
        # An unrecognized query field (compute_cap on older drivers, ~pre-R495)
        # fails the whole query, so retry with just the base fields rather than
        # losing detection entirely.
        fields = _SMI_BASE_FIELDS
        try:
            result = _run_smi(fields)
        except subprocess.CalledProcessError:
            return []

    gpus: List[GPUMicroarch] = []
    for line in result.stdout.strip().splitlines():
        parts = [p.strip() for p in line.split(",")]
        # parts align positionally with `fields`:
        # [brand_string, driver_version, combined vendor+device pci code(, compute_cap)]
        if len(parts) < len(_SMI_BASE_FIELDS):
            continue

        # Skip this gpu if id parsing is malformed
        try:
            pci_codes = _parse_pci_device_id(parts[2])
        except ValueError as e:
            warnings.warn(f"skipping NVIDIA GPU: {e}")
            continue

        compute_capability = (
            _compute_capability_to_compiler_flag(parts[3]) if len(parts) > 3 else ""
        )
        gpus.append(
            GPUMicroarch(
                name=compute_capability,
                vendor="nvidia",
                brand_string=parts[0],
                driver_version=parts[1],
                component_pci_code=pci_codes[0],
                vendor_pci_code=pci_codes[1],
                compute_capability=compute_capability,
            )
        )
    return gpus
