# Copyright 2019-2026 Lawrence Livermore National Security, LLC and other
# Archspec Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Defines the GPU class to represent detected GPUs."""

import re
import string
from enum import Enum
from typing import Dict, Optional


class VendorPciCode(str, Enum):
    """PCI vendor IDs for supported GPU manufacturers."""

    NVIDIA = "0x10de"
    AMD = "0x1002"
    INTEL = "0x8086"


class PciClass(str, Enum):
    """PCI class codes for display controllers and process accelerators."""

    VGA = "0x030000"
    XGA = "0x030100"
    CONTROLLER_3D = "0x030200"
    DISPLAY_OTHER = "0x038000"
    PROCESS_ACCELERATOR = "0x120000"


class ComputeCapability:
    """Represents the compute capability of an NVIDIA GPU (e.g. ``90``).

    The canonical name is the decimal-free ``XYs`` form used by nvcc and the
    archspec JSON: major version, single-digit minor version, and an optional
    feature suffix (e.g. ``90``, ``90a``, ``100f``).
    """

    def __init__(self, major: int, minor: int, suffix: str = ""):
        self.major = major
        self.minor = minor
        self.suffix = suffix

    @property
    def name(self) -> str:
        """The ``XYs`` string form (e.g. ``90``, ``90a``)."""
        return f"{self.major}{self.minor}{self.suffix}"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(major={self.major!r}, minor={self.minor!r}, "
            f"suffix={self.suffix!r})"
        )

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other):
        if not isinstance(other, ComputeCapability):
            return NotImplemented
        return (self.major, self.minor, self.suffix) == (other.major, other.minor, other.suffix)

    def __hash__(self) -> int:
        return hash((self.major, self.minor, self.suffix))

    @classmethod
    def from_str(cls, compute_capability: str) -> "ComputeCapability":
        """Parse a compute capability from either its dotted ``X.Y`` form, as reported by
        nvidia-smi (e.g. ``9.0``), or its ``XYs`` form (e.g. ``90``, ``90a``, ``100f``).

        The minor version is always a single digit; the suffix is optional and made of
        letters only.

        Raises:
            ValueError: if *compute_capability* is not in ``X.Y[s]`` or ``XY[s]`` form.
        """
        text = compute_capability.strip()
        match = re.fullmatch(r"(\d+)\.?(\d)([A-Za-z]*)", text)
        if not match:
            raise ValueError(
                f"Invalid compute capability format: expected `X.Y[s]` or `XY[s]`,"
                f" got {compute_capability!r}"
            )

        major, minor, suffix = match.groups()
        return cls(major=int(major), minor=int(minor), suffix=suffix)


class GFXTarget:
    """Represents the gfx target of an AMD GPU (e.g. ``gfx90a``)."""

    def __init__(self, major: int, minor: int, stepping: int, xnack: str = ""):
        self.major = major
        self.minor = minor
        self.stepping = stepping
        #: ``"+"`` or ``"-"`` when the device reports an xnack mode, ``""`` otherwise
        self.xnack = xnack

    @property
    def name(self) -> str:
        """The target ID string form (e.g. ``gfx90a`` or ``gfx90a:xnack-``)."""
        processor = f"gfx{self.major}{self.minor:x}{self.stepping:x}"
        return f"{processor}:xnack{self.xnack}" if self.xnack else processor

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(major={self.major!r}, minor={self.minor!r}, "
            f"stepping={self.stepping!r}, xnack={self.xnack!r})"
        )

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other):
        if not isinstance(other, GFXTarget):
            return NotImplemented
        return (self.major, self.minor, self.stepping, self.xnack) == (
            other.major,
            other.minor,
            other.stepping,
            other.xnack,
        )

    def __hash__(self) -> int:
        return hash((self.major, self.minor, self.stepping, self.xnack))

    @classmethod
    def from_str(cls, gfx_target: str) -> "GFXTarget":
        """Parse a gfx target from its target ID string form (e.g. ``gfx90a:sramecc+:xnack-``).

        The ``xnack`` target feature is kept, since code objects built for one xnack mode do
        not run in the other. Any other feature (e.g. ``sramecc``) is dropped.

        Raises:
            ValueError: if *gfx_target* is not ``gfx`` followed by a decimal major version and
                single hex digits for the minor version and stepping.
        """
        processor, _, features = gfx_target.strip().lower().partition(":")
        xnack = ""
        for feature in features.split(":"):
            if feature in ("xnack+", "xnack-"):
                xnack = feature[-1]
        major, minor, stepping = processor[3:-2], processor[-2:-1], processor[-1:]
        if not (
            processor.startswith("gfx")
            and major.isdigit()
            and minor in string.hexdigits
            and stepping in string.hexdigits
        ):
            raise ValueError(f"Invalid gfx target format: expected `gfxXYZ`, got {gfx_target!r}")

        return cls(major=int(major), minor=int(minor, 16), stepping=int(stepping, 16), xnack=xnack)


class GPU:
    "Hardware-specific attributes for a given card detected on the host."

    # pylint: disable=too-many-arguments,too-many-positional-arguments,too-many-instance-attributes

    def __init__(
        self,
        name: str = "",
        vendor: str = "",
        vendor_pci_code: Optional[VendorPciCode] = None,
        component_pci_code: str = "",
        pci_class: Optional[PciClass] = None,
        driver_version: str = "",
        # Only relevant for NVIDIA
        compute_capability: Optional[ComputeCapability] = None,
        # Only relevant for AMD
        gfx_target: Optional[GFXTarget] = None,
    ):
        """
        Args:
            name: human-readable name of card (e.g. ``RTX 5080``)
            vendor: name of chip manufacturer (e.g. ``nvidia``)
            vendor_pci_code: PCI vendor ID (e.g. ``VendorPciCode.INTEL`` for ``0x8086``)
            component_pci_code: 4-digit hex PCI device ID of the GPU (e.g. ``0x2c02``)
            pci_class: PCI class code of the device (e.g. ``PciClass.VGA`` for ``0x030000``)
            driver_version: version number of currently installed driver (e.g. ``595.58.03``)
            compute_capability: NVIDIA-specific compatibility identifier (e.g. ``90``)
            gfx_target: AMD-specific compatibility identifier (e.g. ``gfx90a``)
        """
        self.name = name
        self.vendor = vendor
        self.vendor_pci_code = vendor_pci_code
        self.component_pci_code = component_pci_code
        self.pci_class = pci_class
        self.driver_version = driver_version
        self.compute_capability = compute_capability
        self.gfx_target = gfx_target

    def __eq__(self, other):
        if not isinstance(other, GPU):
            return NotImplemented
        return vars(self) == vars(other)

    def __hash__(self) -> int:
        return hash(
            (
                self.vendor,
                self.vendor_pci_code,
                self.component_pci_code,
                self.pci_class,
                self.name,
            )
        )

    def __repr__(self) -> str:
        fields = ", ".join(f"{field}={value!r}" for field, value in vars(self).items() if value)
        return f"{self.__class__.__name__}({fields})"

    def __str__(self) -> str:
        if self.name and self.vendor:
            return f"{self.vendor} {self.name}"
        if self.vendor and self.component_pci_code:
            return f"unresolved {self.vendor} gpu (PCI ID: {self.component_pci_code})"
        return "unknown gpu"

    def detailed_string(self) -> str:
        """Returns detailed information about the detected GPU."""
        detail = ""

        for field, value in vars(self).items():
            if value:
                if isinstance(value, Enum):
                    value = value.value
                detail += f"{field}: {value}\n"

        return detail.strip()

    def to_dict(self) -> Dict[str, str]:
        """Returns a dictionary representation of this object."""
        return {
            "name": self.name,
            "vendor": self.vendor,
            "vendor_pci_code": self.vendor_pci_code.value if self.vendor_pci_code else "",
            "component_pci_code": self.component_pci_code,
            "pci_class": self.pci_class.value if self.pci_class else "",
            "driver_version": self.driver_version,
            "compute_capability": self.compute_capability.name if self.compute_capability else "",
            "gfx_target": self.gfx_target.name if self.gfx_target else "",
        }

    @classmethod
    def from_dict(cls, data) -> "GPU":
        """Construct a GPU from a dictionary representation."""
        vendor_pci_code = data.get("vendor_pci_code")
        pci_class = data.get("pci_class")
        compute_capability = data.get("compute_capability")
        gfx_target = data.get("gfx_target")
        return cls(
            name=data.get("name", ""),
            vendor=data.get("vendor", ""),
            vendor_pci_code=VendorPciCode(vendor_pci_code) if vendor_pci_code else None,
            component_pci_code=data.get("component_pci_code", ""),
            pci_class=PciClass(pci_class) if pci_class else None,
            driver_version=data.get("driver_version", ""),
            compute_capability=(
                ComputeCapability.from_str(compute_capability) if compute_capability else None
            ),
            gfx_target=GFXTarget.from_str(gfx_target) if gfx_target else None,
        )
