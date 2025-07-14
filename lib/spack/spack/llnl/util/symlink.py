# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import warnings

import spack.error
import spack.llnl.util.filesystem

warnings.warn(
    "The `spack.llnl.util.symlink` module will be removed in Spack v1.1, "
    "use `spack.llnl.util.filesystem` instead",
    category=spack.error.SpackAPIWarning,
    stacklevel=2,
)

readlink = spack.llnl.util.filesystem.readlink
islink = spack.llnl.util.filesystem.islink
symlink = spack.llnl.util.filesystem.symlink
