# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""This package contains code for creating environment modules, which can
include TCL non-hierarchical modules, LUA hierarchical modules, and others.
"""

from __future__ import absolute_import

from .common import disable_modules
from .lmod import LmodConfiguration, LmodModulefileWriter
from .tcl import TclConfiguration, TclModulefileWriter

__all__ = ["TclModulefileWriter", "LmodModulefileWriter", "disable_modules"]

module_types = {"tcl": TclModulefileWriter, "lmod": LmodModulefileWriter}
module_config_types = {"tcl": TclConfiguration, "lmod": LmodConfiguration}
