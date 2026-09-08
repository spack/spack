# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import spack.binary_distribution
import spack.debug_source
import spack.llnl.util.tty as tty
import spack.mirrors.mirror
import spack.oci.image
import spack.oci.oci


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
    for mirror in spack.mirrors.mirror.MirrorCollection(binary=True, autopush=True).values():
        if not mirror.matches_binary(spec, direction="push"):
            tty.debug(
                f"{spec.name}: Skipped push to '{mirror.name}' due to include/exclude filters"
            )
            continue

        signing_key = spack.binary_distribution.select_signing_key() if mirror.signed else None
        with spack.binary_distribution.make_uploader(
            mirror=mirror, force=True, signing_key=signing_key
        ) as uploader:
            uploader.push_or_raise([spec])
        tty.msg(f"{spec.name}: Pushed to build cache: '{mirror.name}'")

 
        # Also push debug-source/symbols, if this install captured any, keeping
        # this fully automatic and consistent with regular autopush behavior --
        # no separate manual push step is needed anywhere (e.g. in the Dockerfile).
        if spack.oci.image.is_oci_url(mirror.push_url):
            dest_root = spack.debug_source.debug_source_dir(spec)
            tty.debug(f"{spec.name}: checking for debug artifacts at {dest_root}")
            if os.path.isdir(dest_root):
                target_image = spack.oci.oci.image_from_mirror(mirror)
                tty.debug(f"{spec.name}: found debug-source cache, pushing to '{mirror.name}'")
                spack.debug_source.push_debug_artifacts(
                    pkg, target_image, push_source=True, push_symbols=True
                )
            else:
                tty.debug(f"{spec.name}: no debug-source cache found, skipping debug push")
