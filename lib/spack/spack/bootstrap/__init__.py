# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Function and classes needed to bootstrap Spack itself."""

from .config import (
    ensure_bootstrap_configuration,
    is_bootstrapping,
    spack_python_interpreter,
    store_path,
)
from .core import (
    all_binaries_root_specs,
    bootstrapping_sources,
    ensure_core_dependencies,
    ensure_executables_in_path_or_raise,
    ensure_module_importable_or_raise,
    ensure_patchelf_in_path_or_raise,
    source_is_enabled_or_raise,
)
from .environment import ensure_environment_dependencies
from .status import status_message

__all__ = [
    "is_bootstrapping",
    "ensure_bootstrap_configuration",
    "ensure_core_dependencies",
    "ensure_module_importable_or_raise",
    "ensure_executables_in_path_or_raise",
    "ensure_patchelf_in_path_or_raise",
    "all_binaries_root_specs",
    "source_is_enabled_or_raise",
    "ensure_environment_dependencies",
    "status_message",
    "spack_python_interpreter",
    "store_path",
    "bootstrapping_sources",
]
