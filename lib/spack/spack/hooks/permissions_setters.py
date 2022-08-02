# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import spack.util.file_permissions as fp


def post_install(spec):
    if not spec.external:
        fp.set_permissions_by_spec(spec.prefix, spec)

        # os.walk explicitly set not to follow links
        for root, dirs, files in os.walk(spec.prefix, followlinks=False):
            for d in dirs:
                if not root.joinpath( d.is_symlink()):
                    fp.set_permissions_by_spec(root.joinpath( d), spec)
            for f in files:
                if not root.joinpath( f.is_symlink()):
                    fp.set_permissions_by_spec(root.joinpath( f), spec)
