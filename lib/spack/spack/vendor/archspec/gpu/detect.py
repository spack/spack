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
_SMI_SOURCES: List[Tuple[str, Callable[[], List[GPUMicroarch]]]] = [
    ("nvidia-smi", nvidia.smi_info),
    ("rocm-smi", amd.smi_info),
]


@detection(operating_system="Linux")
def _detect_gpus_linux() -> List[GPUMicroarch]:
    """Enumerate all GPUs present on Linux: vendor SMI tools plus a sysfs PCI scan fallback."""
    results: List[GPUMicroarch] = []

    for executable, info_fn in _SMI_SOURCES:
        if shutil.which(executable) is not None:
            results.extend(info_fn())

    described = {(gpu.vendor_pci_code, gpu.component_pci_code) for gpu in results}

    for gpu in generic.scan_sysfs_pci_for_gpus():
        if (gpu.vendor_pci_code, gpu.component_pci_code) not in described:
            results.append(gpu)

    return results


@functools.lru_cache(maxsize=None)
def host() -> List[GPUMicroarch]:
    """Detects the GPUs on the host system and returns information about them.

    Returns:
        A list of GPUMicroarch objects, one per detected GPU.
    """
    results: List[GPUMicroarch] = []

    for factory in INFO_FACTORY[platform.system()]:
        try:
            results = factory()
            break
        except Exception as e:  # pylint: disable=broad-except
            warnings.warn(str(e))

    return results
