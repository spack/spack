# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import spack.package_prefs as pp


def post_install(spec, explicit=None):
    if not spec.external:
        pp.set_permissions_by_spec(spec.prefix, spec)

        # os.walk explicitly set not to follow links
        for root, dirs, files in os.walk(spec.prefix, followlinks=False):
            for d in dirs:
                if not os.path.islink(os.path.join(root, d)):
                    pp.set_permissions_by_spec(os.path.join(root, d), spec)
            for f in files:
                if not os.path.islink(os.path.join(root, f)):
                    pp.set_permissions_by_spec(os.path.join(root, f), spec)
