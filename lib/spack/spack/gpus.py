# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Detection of GPUs on the host, and their translation into Spack variant defaults.

This module is the glue between archspec's GPU detection and the concretizer. It knows
which Spack variant receives the identifier detected for each GPU vendor, and exposes the
result in a form the solver can turn into ``variant_default_value_from_host`` facts.
"""

from typing import Dict, List

import spack.vendor.archspec.gpu

import spack.util.lang
from spack.util import tty

#: Maps the vendor name reported by archspec to the Spack variant that receives the
#: detected architecture identifier.
VARIANT_BY_VENDOR: Dict[str, str] = {"nvidia": "cuda_arch", "amd": "amdgpu_target"}


@spack.util.lang.memoized
def host() -> List[spack.vendor.archspec.gpu.GPUMicroarch]:
    """Returns the GPUs detected on the host, as archspec ``GPUMicroarch`` objects.

    The list is empty when detection finds nothing.
    """
    return list(spack.vendor.archspec.gpu.host())


@spack.util.lang.memoized
def host_variants() -> Dict[str, List[str]]:
    """Returns the variant defaults implied by the GPUs detected on the host.

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
