# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Function and classes needed to bootstrap Spack itself."""

from .config import ensure_bootstrap_configuration, is_bootstrapping, store_path
from .core import (
    all_core_root_specs,
    ensure_clingo_importable_or_raise,
    ensure_core_dependencies,
    ensure_gpg_in_path_or_raise,
    ensure_patchelf_in_path_or_raise,
    ensure_winsdk_external_or_raise,
)
from .environment import BootstrapEnvironment, ensure_environment_dependencies
from .status import status_message

__all__ = [
    "all_core_root_specs",
    "BootstrapEnvironment",
    "ensure_bootstrap_configuration",
    "ensure_clingo_importable_or_raise",
    "ensure_core_dependencies",
    "ensure_environment_dependencies",
    "ensure_gpg_in_path_or_raise",
    "ensure_patchelf_in_path_or_raise",
    "ensure_winsdk_external_or_raise",
    "is_bootstrapping",
    "status_message",
    "store_path",
]
