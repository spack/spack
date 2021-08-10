# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#: (major, minor, patch, pre-release) semantic version for Spack
spack_version_info = ('0', '18', '0', 'dev')

#: Semantic version string <major>.<minor>.<path>-<pre-release>
spack_version = '.'.join(spack_version_info[:3])
if len(spack_version_info) >= 4:
    spack_version += '-' + spack_version_info[3]

__all__ = ['spack_version_info', 'spack_version']
__version__ = spack_version
