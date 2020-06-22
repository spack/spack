# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import collections


ExternalPackageEntry = collections.namedtuple(
    'ExternalPackageEntry', ['spec', 'base_dir', 'modules']
)
