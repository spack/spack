# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Detection of GPUs on the host, and their translation into Spack variant values.

This module is the glue between archspec's GPU detection and the rest of Spack. It knows
which Spack variant receives the identifier detected for each GPU vendor, and resolves the
reserved variant value :data:`HOST_DEFAULT` into the identifiers of the GPUs on the host.
"""

from typing import Dict, List

import spack.vendor.archspec.gpu

import spack.error
import spack.util.lang
from spack.util import tty

#: Maps the vendor name reported by archspec to the Spack variant that receives the
#: detected architecture identifier.
VARIANT_BY_VENDOR: Dict[str, str] = {"nvidia": "cuda_arch", "amd": "amdgpu_target"}

#: Inverse of :data:`VARIANT_BY_VENDOR`
VENDOR_BY_VARIANT: Dict[str, str] = {v: k for k, v in VARIANT_BY_VENDOR.items()}

#: Reserved value of the variants above, asking for the GPUs detected on the host
HOST_DEFAULT: str = "host_default"


@spack.util.lang.memoized
def host() -> List[spack.vendor.archspec.gpu.GPUMicroarch]:
    """Returns the GPUs detected on the host, as archspec ``GPUMicroarch`` objects.

    The list is empty when detection finds nothing, which is always the case outside Linux.
    """
    return list(spack.vendor.archspec.gpu.host())


@spack.util.lang.memoized
def host_variants() -> Dict[str, List[str]]:
    """Returns the variant values implied by the GPUs detected on the host.

    The result maps a variant name to the ordered, de-duplicated list of values detected
    for it, e.g. ``{"cuda_arch": ["90"]}``. GPUs from vendors without a mapped variant, or
    whose architecture could not be resolved, are skipped.
    """
    result: Dict[str, List[str]] = {}
    for gpu in host():
        variant_name = VARIANT_BY_VENDOR.get(gpu.vendor)
        if variant_name is None or not gpu.name:
            tty.debug(f"[GPU] skipping {gpu}: no variant mapping or unresolved architecture")
            continue
        values = result.setdefault(variant_name, [])
        if gpu.name not in values:
            values.append(gpu.name)
    return result


def resolve_host_default(variant_name: str) -> List[str]:
    """Returns the values to use for a GPU variant set to :data:`HOST_DEFAULT`.

    These are the identifiers of the detected GPUs from the vendor the variant belongs to, in
    order of detection and without duplicates, e.g. ``["86"]`` for ``cuda_arch`` on a host with
    an RTX 3090.

    Args:
        variant_name: one of the variants in :data:`VARIANT_BY_VENDOR`

    Raises:
        ValueError: if the variant is not a GPU variant
        NoHostGPUError: if no GPU from the matching vendor was detected
    """
    vendor = VENDOR_BY_VARIANT.get(variant_name)
    if vendor is None:
        raise ValueError(f"'{variant_name}' is not a GPU architecture variant")

    values = host_variants().get(variant_name, [])
    if not values:
        raise NoHostGPUError(
            f"{variant_name}={HOST_DEFAULT} requires a {vendor} GPU, but none was detected on "
            "this host"
        )
    return values


class NoHostGPUError(spack.error.SpecError):
    """Raised when a variant asks for the host GPUs and none of the right vendor is present."""
