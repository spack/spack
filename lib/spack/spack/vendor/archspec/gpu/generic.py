# Copyright 2019-2026 Lawrence Livermore National Security, LLC and other
# Archspec Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Vendor-agnostic GPU enumeration based on sysfs PCI scanning."""

import os
import warnings
from typing import List

from . import schema
from .gpu_microarch import GPUMicroarch

#: Path to the sysfs PCI devices directory
SYSFS_PCI_DEVICES = "/sys/bus/pci/devices"


def _read_sysfs_file(path: str) -> str:
    """Read and strip the contents of a sysfs file."""
    with open(path) as f:  # pylint: disable=unspecified-encoding
        return f.read().strip()


def scan_sysfs_pci_for_gpus() -> List[GPUMicroarch]:
    """Enumerate GPUs by scanning sysfs PCI devices.

    Iterates over ``/sys/bus/pci/devices/`` and yields one entry per device whose
    PCI class indicates a GPU. Each entry carries only the identity available
    without a vendor tool: the vendor name and the PCI vendor and device codes.

    Returns:
        A list of GPUMicroarch, one per GPU-class PCI device on the system.
    """
    gpus: List[GPUMicroarch] = []

    if not os.path.isdir(SYSFS_PCI_DEVICES):
        return gpus

    gpu_pci_classes = schema.DETECTION_JSON["pci_classes"]
    gpu_vendors = schema.DETECTION_JSON["vendors"]

    for entry in os.listdir(SYSFS_PCI_DEVICES):
        device_dir = os.path.join(SYSFS_PCI_DEVICES, entry)
        if not os.path.isdir(device_dir):
            continue

        try:
            class_path = os.path.join(device_dir, "class")
            if not os.path.exists(class_path):
                continue
            if _read_sysfs_file(class_path) not in gpu_pci_classes:
                continue

            vendor_id = _read_sysfs_file(os.path.join(device_dir, "vendor"))
            vendor_name = gpu_vendors.get(vendor_id)
            if vendor_name is None:
                continue

            gpus.append(
                GPUMicroarch(
                    vendor=vendor_name,
                    vendor_pci_code=vendor_id,
                    component_pci_code=_read_sysfs_file(os.path.join(device_dir, "device")),
                )
            )
        except OSError as exc:
            warnings.warn(f"skipping PCI device {entry!r}: {exc}")

    return gpus
