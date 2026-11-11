# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.binary_distribution
import spack.config
import spack.mirrors.mirror
from spack.util import tty


def post_install(spec, explicit):
    # Push package to all buildcaches with autopush==True

    # Do nothing if spec is an external package
    if spec.external:
        return

    # Do nothing if package was not installed from source
    pkg = spec.package
    if pkg.installed_from_binary_cache:
        return

    fail_on_error = spack.config.CONFIG.get("config:autopush_fail_on_error", True)

    # Push the package to all autopush mirrors
    for mirror in spack.mirrors.mirror.MirrorCollection(binary=True, autopush=True).values():
        if not mirror.matches_binary(spec, direction="push"):
            tty.debug(
                f"{spec.name}: Skipped push to '{mirror.name}' due to include/exclude filters"
            )
            continue

        try:
            _push(spec, mirror)
        except Exception as e:
            if fail_on_error:
                raise
            tty.warn(f"{spec.name}: Failed to push to build cache '{mirror.name}': {e}")
            continue
        tty.msg(f"{spec.name}: Pushed to build cache: '{mirror.name}'")


def _push(spec, mirror):
    signing_key = spack.binary_distribution.select_signing_key() if mirror.signed else None
    with spack.binary_distribution.make_uploader(
        mirror=mirror, force=True, signing_key=signing_key
    ) as uploader:
        uploader.push_or_raise([spec], config=spack.config.CONFIG)
