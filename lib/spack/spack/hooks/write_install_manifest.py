# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.verify


def post_install(spec, timer=None):
    if not spec.external:
        spack.verify.write_manifest(spec)
