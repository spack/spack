# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#: (major, minor, micro, dev release) tuple
spack_version_info = (0, 18, 0, 'dev0')

#: PEP440 canonical <major>.<minor>.<micro>.<devN> string
spack_version = '.'.join(str(s) for s in spack_version_info)

__all__ = ['spack_version_info', 'spack_version']
__version__ = spack_version
