# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Notmuch(AutotoolsPackage):
    """Notmuch is a mail indexer.

    Essentially, is a very thin front end on top of xapian.
    """

    homepage = "https://notmuchmail.org/"
    url      = "https://notmuchmail.org/releases/notmuch-0.23.7.tar.gz"

    version('0.23.7', '1ad339b6d0c03548140434c7bcdf0624')

    depends_on('zlib')
    depends_on('talloc')
    depends_on('gmime@2.6:')
    depends_on('xapian-core')
