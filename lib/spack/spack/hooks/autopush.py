# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.tty as tty

import spack.binary_distribution as bindist
import spack.mirror


def post_install(spec, explicit):
    # Push package to all buildcaches with autopush==True

    # Do nothing if package was not installed from source
    pkg = spec.package
    if pkg.installed_from_binary_cache:
        return

    # Iterate over all mirrors with autopush==True
    all_mirrors = spack.mirror.MirrorCollection(binary=True)
    autopush_mirrors = [mirror for mirror in all_mirrors.values() if mirror.get_autopush()]
    for mirror in autopush_mirrors:
        # Push the package to a mirror
        bindist.push_or_raise(
            spec,
            mirror.push_url,
            bindist.PushOptions(force=True, regenerate_index=False, unsigned=False, key=None),
        )
        tty.msg(f"Pushed to mirror {mirror.name}")
