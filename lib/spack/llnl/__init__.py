# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import warnings

import spack.error
import spack.llnl

warnings.warn(
    "The top-level `llnl` module is removed in Spack v1.0",
    category=spack.error.SpackAPIWarning,
    stacklevel=2,
)


__path__ = spack.llnl.__path__
