# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""This package contains code for creating environment modules, which can
include Tcl non-hierarchical modules, Lua hierarchical modules, and others.
"""

from typing import Dict, Type

from .common import BaseModuleFileWriter, disable_modules
from .lmod import LmodModulefileWriter
from .tcl import TclModulefileWriter

__all__ = ["TclModulefileWriter", "LmodModulefileWriter", "disable_modules"]

module_types: Dict[str, Type[BaseModuleFileWriter]] = {
    "tcl": TclModulefileWriter,
    "lmod": LmodModulefileWriter,
}
