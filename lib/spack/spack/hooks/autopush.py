# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.tty as tty

import spack.binary_distribution as bindist
import spack.mirror


def post_install(spec, explicit):
    # Push package to all buildcaches with autopush==True

    # Do nothing if spec is an external package
    if spec.external:
        return

    # Do nothing if package was not installed from source
    pkg = spec.package
    if pkg.installed_from_binary_cache:
        return

    # Push the package to all autopush mirrors
    for mirror in spack.mirror.MirrorCollection(binary=True, autopush=True).values():
        bindist.push_or_raise(
            spec,
            mirror.push_url,
            bindist.PushOptions(force=True, regenerate_index=False, unsigned=not mirror.signed),
        )
        tty.msg(f"{spec.name}: Pushed to build cache: '{mirror.name}'")
