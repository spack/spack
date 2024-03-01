# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse

import spack.mirror
from spack.cmd import buildcache as bc


def post_install_in_db(spec):
    pkg = spec.package
    # Package was installed from source
    if not pkg.installed_from_binary_cache:
        hash = "/" + spec.dag_hash()
        # Iterate over all mirrors with autopush==True
        all_mirrors = spack.mirror.MirrorCollection(binary=True)
        autopush_mirrors = [mirror for mirror in all_mirrors.values() if mirror.get_autopush()]
        for mirror in autopush_mirrors:
            # Create and execute buildcache push command
            bc_parser = argparse.ArgumentParser()
            bc.setup_parser(bc_parser)
            bc_flags = []
            # The dependencies should already be in the buildcache
            # No need to add them again (especially with --force)
            bc_flags.append("--only=package")
            # We want the pushed packages to be available right away
            bc_flags.append("--update-index")
            # We always want to push the package to the buildcache
            # If it is already in the buildcache it must be corrupted,
            # otherwise it would not have been compiled from source
            bc_flags.append("--force")
            # TODO remove install_args?
            # if install_args["fail_fast"]:
            #    bc_flags.append("--fail-fast")
            bc_args = ["push"] + bc_flags + [mirror.name, hash]
            push_args = bc_parser.parse_args(bc_args)
            bc.push_fn(push_args)
