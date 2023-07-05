# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""This package contains code for creating environment modules, which can
include Tcl non-hierarchical modules, Lua hierarchical modules, and others.
"""

from .common import disable_modules, ensure_modules_are_enabled_or_warn
from .lmod import LmodModulefileWriter
from .tcl import TclModulefileWriter

__all__ = [
    "TclModulefileWriter",
    "LmodModulefileWriter",
    "disable_modules",
    "ensure_modules_are_enabled_or_warn",
]

module_types = {"tcl": TclModulefileWriter, "lmod": LmodModulefileWriter}
