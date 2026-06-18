# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import warnings

import spack.error
import spack.llnl

warnings.warn(
    "The `llnl` module will be removed in Spack v1.1",
    category=spack.error.SpackAPIWarning,
    stacklevel=2,
)


__path__ = spack.llnl.__path__
