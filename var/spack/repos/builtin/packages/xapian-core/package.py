# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class XapianCore(AutotoolsPackage):
    """Xapian is a highly adaptable toolkit which allows developers to easily
    add advanced indexing and search facilities to their own applications.
    It supports the Probabilistic Information Retrieval model and also
    supports a rich set of boolean query operators."""

    homepage = "https://xapian.org"
    url      = "http://oligarchy.co.uk/xapian/1.4.3/xapian-core-1.4.3.tar.xz"

    version('1.4.3', '143f72693219f7fc5913815ed858f295')

    depends_on('zlib')
