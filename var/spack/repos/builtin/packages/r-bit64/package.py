# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RBit64(RPackage):
    """Package 'bit64' provides serializable S3 atomic 64bit (signed)
    integers. These are useful for handling database keys and exact
    counting in +-2^63. WARNING: do not use them as replacement for 32bit
    integers, integer64 are not supported for subscripting by R-core and
    they have different semantics when combined with double, e.g.
    integer64 + double => integer64. Class integer64 can be used in vectors,
    matrices, arrays and data.frames. Methods are available for coercion
    from and to logicals, integers, doubles, characters and factors
    as well as many elementwise and summary functions. Many fast
    algorithmic operations such as 'match' and 'order' support
    inter- active data exploration
    and manipulation and optionally leverage caching."""

    homepage = "https://cloud.r-project.org/package=bit64"
    url      = "https://cloud.r-project.org/src/contrib/bit64_0.9-7.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/bit64"

    version('0.9-7', 'ac4bc39827338c552d329d3d4d2339c2')

    depends_on('r@3.0.1:', type=('build', 'run'))
    depends_on('r-bit@1.1-12:', type=('build', 'run'))
