# Copyright 2019-2026 Lawrence Livermore National Security, LLC and other
# Archspec Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Vendor-agnostic GPU enumeration based on sysfs PCI scanning."""

import os
import warnings
from typing import List

from .gpu import GPU, PciClass, VendorPciCode

#: Path to the sysfs PCI devices directory
SYSFS_PCI_DEVICES = "/sys/bus/pci/devices"


def _read_sysfs_file(path: str) -> str:
    """Read and strip the contents of a sysfs file."""
    with open(path) as f:  # pylint: disable=unspecified-encoding
        return f.read().strip()


def scan_sysfs_pci_for_gpus() -> List[GPU]:
    """Enumerate GPUs by scanning sysfs PCI devices.

    Iterates over ``/sys/bus/pci/devices/`` and yields one entry per device whose
    PCI class is in ``PciClass`` and whose vendor is in ``VendorPciCode``. Each entry
    carries only the identity available without a vendor tool: the vendor, the PCI
    vendor and device codes, and the PCI class.

    Returns:
        A list of GPU, one per GPU-class PCI device from a supported vendor.
    """
    gpus: List[GPU] = []

    if not os.path.isdir(SYSFS_PCI_DEVICES):
        return gpus

    for entry in os.listdir(SYSFS_PCI_DEVICES):
        device_dir = os.path.join(SYSFS_PCI_DEVICES, entry)
        if not os.path.isdir(device_dir):
            continue

        try:
            class_path = os.path.join(device_dir, "class")
            if not os.path.exists(class_path):
                continue

            # Skip devices that aren't GPUs, or aren't from a supported vendor
            try:
                pci_class = PciClass(_read_sysfs_file(class_path))
                vendor_pci_code = VendorPciCode(
                    _read_sysfs_file(os.path.join(device_dir, "vendor"))
                )
            except ValueError:
                continue

            gpus.append(
                GPU(
                    vendor=vendor_pci_code.name.lower(),
                    vendor_pci_code=vendor_pci_code,
                    component_pci_code=_read_sysfs_file(os.path.join(device_dir, "device")),
                    pci_class=pci_class,
                )
            )
        except OSError as exc:
            warnings.warn(f"skipping PCI device {entry!r}: {exc}")

    return gpus
