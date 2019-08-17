# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Talloc(AutotoolsPackage):
    """Talloc provides a hierarchical, reference counted memory pool system
    with destructors. It is the core memory allocator used in Samba."""

    homepage = "https://talloc.samba.org"
    url      = "https://www.samba.org/ftp/talloc/talloc-2.1.9.tar.gz"

    version('2.1.9', '19ba14eba97d79a169fa92ea824d2b9e')
