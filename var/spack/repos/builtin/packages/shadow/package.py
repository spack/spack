# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Shadow(AutotoolsPackage):
    """Tools to help unprivileged users create uid and gid mappings in
    user namespaces."""

    homepage = "https://github.com/shadow-maint/shadow"
    url = "https://github.com/shadow-maint/shadow/releases/download/4.7/shadow-4.7.tar.gz"
    git = "https://github.com/shadow-maint/shadow.git"

    version("4.13", sha256="813057047499c7fe81108adcf0cffa3ad4ec75e19a80151f9cbaa458ff2e86cd")
    version("4.8.1", sha256="3ee3081fbbcbcfea5c8916419e46bc724807bab271072104f23e7a29e9668f3a")
    version("4.7", sha256="5135b0ca2a361a218fab59e63d9c1720d2a8fc1faa520c819a654b638017286f")
    version("4.6", sha256="4668f99bd087399c4a586084dc3b046b75f560720d83e92fd23bf7a89dda4d31")
