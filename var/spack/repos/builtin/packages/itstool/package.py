# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
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

    version('2.0.6', sha256='6233cc22726a9a5a83664bf67d1af79549a298c23185d926c3677afa917b92a9')
    version('2.0.5', sha256='100506f8df62cca6225ec3e631a8237e9c04650c77495af4919ac6a100d4b308')
    version('2.0.4', sha256='97c208b51da33e0b553e830b92655f8deb9132f8fbe9a646771f95c33226eb60')
    version('2.0.3', sha256='8c7a5c639eb4714a91ad829910fd06c1c677abcbbb60aee9211141faa7fb02c7')
    version('2.0.2', sha256='bf909fb59b11a646681a8534d5700fec99be83bb2c57badf8c1844512227033a')
    version('2.0.1', sha256='ec6b1b32403cbe338b6ac63c61ab1ecd361f539a6e41ef50eae56a4f577234d1')
    version('2.0.0', sha256='14708111b11b4a70e240e3b404d7a58941e61dbb5caf7e18833294d654c09169')
    version('1.2.0', sha256='46fed63fb89c72dbfc03097b4477084ff05ad6f171212d8f1f1546ea543978aa')

    depends_on('libxml2+python', type=('build', 'run'))
