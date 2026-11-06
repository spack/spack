# Copyright 2019-2026 Lawrence Livermore National Security, LLC and other
# Archspec Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Detection of GPU microarchitectures"""

import collections
import functools
import platform
import shutil
import warnings
from typing import Callable, Dict, List, Tuple

from . import amd, generic, nvidia
from .gpu import GPU
from .gpu_microarch import GPUMicroarch

#: Mapping from operating systems to chain of commands
#: to obtain a list of raw info on the current gpus
INFO_FACTORY: Dict[str, List[Callable]] = collections.defaultdict(list)


def detection(operating_system: str):
    """Decorator to mark functions that are meant to return raw information on detected GPUs.

    Args:
        operating_system: operating system where this function can be used.
    """

    def decorator(factory):
        INFO_FACTORY[operating_system].append(factory)
        return factory

    return decorator


#: Vendor SMI tools used to enrich detection: (executable, info function).
_SMI_SOURCES: List[Tuple[str, Callable[[], List[GPU]]]] = [
    ("nvidia-smi", nvidia.smi_info),
    ("rocm-smi", amd.smi_info),
]


@detection(operating_system="Linux")
def _detect_gpus_linux() -> List[GPU]:
    """Enumerate all GPUs present on Linux: vendor SMI tools plus a sysfs PCI scan fallback."""
    results: List[GPU] = []

    for executable, info_fn in _SMI_SOURCES:
        if shutil.which(executable) is not None:
            results.extend(info_fn())

    described = {(gpu.vendor_pci_code, gpu.component_pci_code) for gpu in results}

    for gpu in generic.scan_sysfs_pci_for_gpus():
        if (gpu.vendor_pci_code, gpu.component_pci_code) not in described:
            results.append(gpu)

    return results


def detected_info() -> List[GPU]:
    """Returns a GPU object for each GPU detected on the current host.

    This function calls all the viable factories one after the other until there's one that is
    able to produce the requested information. Returns an empty list if none of the calls succeed.
    """
    # Mirrors archspec.cpu.detect.detected_info
    # pylint: disable=broad-except,duplicate-code
    for factory in INFO_FACTORY[platform.system()]:
        try:
            return factory()
        except Exception as exc:
            warnings.warn(str(exc))

    return []


@functools.lru_cache(maxsize=None)
def host() -> List[GPUMicroarch]:
    """Detects the GPU microarchitectures on the host system.

    GPUs that can't be mapped to a microarchitecture (e.g. from an unsupported vendor, or missing
    the vendor-specific identifier) are skipped with a warning.

    Returns:
        A list of GPUMicroarch objects, one per successfully mapped GPU.
    """
    microarchs: List[GPUMicroarch] = []

    for gpu in detected_info():
        try:
            microarchs.append(GPUMicroarch.from_gpu(gpu))
        except ValueError as exc:
            warnings.warn(f"skipping GPU: {exc}")

    return microarchs
