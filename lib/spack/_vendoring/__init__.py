# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import warnings

import spack.vendor

import spack.error

warnings.warn(
    "The `_vendoring` module will be removed in Spack v1.1",
    category=spack.error.SpackAPIWarning,
    stacklevel=2,
)

__path__ = spack.vendor.__path__
