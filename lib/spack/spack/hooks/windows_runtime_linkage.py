# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import sys

import spack.relocate_windows


def post_install(spec, explicit=None):
    # If spec is an external, we should not be modifying its bin directory.
    # Spack should in general not modify things it has not installed.
    if sys.platform != "win32" or spec.external or spec.package.installed_from_binary_cache:
        return
    if not spec.satisfies("%compiler-wrapper"):
        return
    # The Windows compiler-wrapper package only carries code once the real MSVC wrapper is
    # available; otherwise it installs a placeholder and we fall back to the symlink-based
    # simulated rpath.
    if spec["compiler-wrapper"].package.has_code:
        spack.relocate_windows.relocate_win_rpath(spec)
    else:
        spec.package.windows_establish_runtime_linkage()
