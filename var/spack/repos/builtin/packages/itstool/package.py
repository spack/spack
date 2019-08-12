# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Itstool(AutotoolsPackage):
    """ITS Tool allows you to translate your XML documents with PO files, using
       rules from the W3C Internationalization Tag Set (ITS) to determine what
       to translate and how to separate it into PO file messages."""

    homepage = "http://itstool.org/"
    url      = "http://files.itstool.org/itstool/itstool-2.0.2.tar.bz2"

    version('2.0.2', 'd472d877a7bc49899a73d442085b2f93')
    version('2.0.1', '40935cfb08228488bd45575e5f001a34')
    version('2.0.0', 'd8c702c3e8961db83d04182c2aa4730b')
    version('1.2.0', 'c0925f6869e33af8e7fe56848c129152')
