# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.tty as tty

import spack.binary_distribution as bindist
import spack.mirror
from spack.cmd import buildcache as bc

updated_mirrors = set()


def post_install_in_db(spec):
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
        # TODO: Why mirror.push_url does not work, but mirror.name does?
        #       It fails in the update below, even though lookup() should accept both name and url
        #       Does every mirror have a name?
        # updated_mirrors.add(mirror.push_url)
        updated_mirrors.add(mirror.name)
        tty.msg(f"Pushed to mirror {mirror.name}")


def on_install_done():
    # Exit right away if there are no mirrors to update
    if not updated_mirrors:
        return

    # Update index of all mirrors where a package was pushed
    all_mirrors = spack.mirror.MirrorCollection(binary=True)
    update_index_mirrors = [all_mirrors.lookup(mirror) for mirror in updated_mirrors]
    for mirror in update_index_mirrors:
        # Sanity check
        if mirror.get_autopush():
            bc.update_index(mirror)
            tty.msg(f"Updated index of mirror {mirror.name}")
