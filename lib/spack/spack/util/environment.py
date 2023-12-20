# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import sys
import warnings

from llnl.util import lang

warnings.warn(
    f"{__name__} has been deprecated in favor of llnl.syscmd, "
    f"and will be removed from Spack v0.23",
    FutureWarning,
    stacklevel=2,
)
sys.modules[__name__] = lang.ModuleDelegate(deprecated=__name__, substitutes=["llnl.syscmd"])
