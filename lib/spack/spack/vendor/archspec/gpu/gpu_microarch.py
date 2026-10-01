# Copyright 2019-2026 Lawrence Livermore National Security, LLC and other
# Archspec Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Defines the GPUMicroarch class, describing a detected GPU microarchitecture."""

from typing import Dict


class GPUMicroarch:
    """Specific GPU Microarchitecture"""

    # pylint: disable=too-many-arguments,too-many-positional-arguments,too-many-instance-attributes

    def __init__(
        self,
        name: str = "",
        brand_string: str = "",
        vendor: str = "",
        driver_version: str = "",
        vendor_pci_code: str = "",
        component_pci_code: str = "",
        # Only relevant for NVIDIA
        compute_capability: str = "",
        # Only relevant for AMD
        gfx_target: str = "",
    ):
        """
        Args:
            name: compatability identifier name (e.g. ``sm_90`` for NVIDIA, ``gfx902`` for AMD)
            brand_string: marketing name of specific device (e.g. ``NVIDIA GeForce RTX 5080``)
            vendor: name of chip manufacturer (e.g. ``nvidia``)
            driver_version: version number of currently installed driver (e.g. ``595.58.03``)
            vendor_pci_code: 4-digit hex string used to identify vendor (e.g. ``0x8086`` for intel)
            component_pci_code: 4-digit hex string used to identify GPU (e.g. ``0x2c02``)
            compute_capability: NVIDIA-specific compatability identifier (e.g. ``sm_90``)
            gfx_target: AMD-specific compatability identifier (e.g. ``gfx902``)
        """
        self.name = name
        self.brand_string = brand_string
        self.vendor = vendor
        self.driver_version = driver_version
        self.vendor_pci_code = vendor_pci_code
        self.component_pci_code = component_pci_code
        # Only relevant for NVIDIA
        self.compute_capability = compute_capability
        # Only relevant for AMD
        self.gfx_target = gfx_target

    def __eq__(self, other):
        if not isinstance(other, GPUMicroarch):
            return NotImplemented
        return vars(self) == vars(other)

    def __hash__(self) -> int:
        return hash((self.vendor, self.vendor_pci_code, self.component_pci_code, self.name))

    def __repr__(self) -> str:
        fields = ", ".join(
            f"{field}={value!r}" for field, value in vars(self).items() if value != ""
        )
        return f"{self.__class__.__name__}({fields})"

    def __str__(self) -> str:
        if self.name and self.vendor:
            return f"{self.name} ({self.vendor})"
        if self.vendor and self.component_pci_code:
            return f"unresolved {self.vendor} gpu (PCI ID: {self.component_pci_code})"
        return "unknown gpu"

    def detailed_string(self) -> str:
        """Returns detailed information about what the Microarch detected"""
        detail = ""

        for field, value in vars(self).items():
            if value != "":
                detail += f"{field}: {value}\n"

        return detail.strip()

    def to_dict(self) -> Dict[str, str]:
        """Returns a dictionary representation of this object."""
        return {
            "name": self.name,
            "brand_string": self.brand_string,
            "vendor": self.vendor,
            "driver_version": self.driver_version,
            "vendor_pci_code": self.vendor_pci_code,
            "component_pci_code": self.component_pci_code,
            "compute_capability": self.compute_capability,
            "gfx_target": self.gfx_target,
        }

    @staticmethod
    def from_dict(data) -> "GPUMicroarch":
        """Construct a GPU microarchitecture from a dictionary representation."""
        return GPUMicroarch(
            name=data.get("name", ""),
            brand_string=data.get("brand_string", ""),
            vendor=data.get("vendor", ""),
            driver_version=data.get("driver_version", ""),
            vendor_pci_code=data.get("vendor_pci_code", ""),
            component_pci_code=data.get("component_pci_code", ""),
            compute_capability=data.get("compute_capability", ""),
            gfx_target=data.get("gfx_target", ""),
        )
