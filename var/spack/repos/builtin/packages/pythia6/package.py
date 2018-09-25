##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
from spack import *
import os
from six import iteritems
from six.moves.urllib.parse import urlparse


class Pythia6(CMakePackage):
    """PYTHIA is a program for the generation of high-energy physics events,
    i.e. for the description of collisions at high energies between elementary
    particles such as e+, e-, p and pbar in various combinations.

    PYTHIA6 is a Fortran package which is no longer maintained: new
    prospective users should use Pythia8 instead.

    This recipe includes patches required to interoperate with Root.
    """

    homepage = 'https://pythiasix.hepforge.org/'
    url = 'http://www.hepforge.org/archive/pythiasix/pythia-6.4.28.tgz'

    version('6.4.28',
            sha256='01cbff47e99365b5e46f6d62c1735d3cae1932c4710604850d59f538cb758020')

    variant('root', default=False,
            description='Build extra (non OEM) code to allow use by Root.')

    # In the unlikely event of new versions >6.4.28,
    # pythia6_common_address.c should be checked for accuracy against
    # the definitions of the relevant COMMON blocks in the Pythia6
    # Fortran source, and patched if necessaary.
    resource(
        name='root-pythia6-shim',
        url='https://root.cern.ch/download/pythia6.tar.gz',
        sha256='d613dcb27c905710e2f13a934913cc5545e3e5d0e477e580107385d9ef260056',
        when='+root',
        destination='.',
        placement={'pythia6_common_address.c': 'pythia6_common_address.c',
                   'tpythia6_called_from_cc.F': 'tpythia6_called_from_cc.F'}
    )

    # Download examples separately.
    examples \
        = {'main60.f':
           'd713b8b267c4405cc9d31c58bba267ae3378902a26fa52393003bf35fd56902c',
           'main61.f':
           'e2a3d5524e43d16f60d9edc6e7198d41006d1ba127fb7b0e265aa509e13128b4',
           'main62.f':
           'dce822a72fe2d6cfb6d43c479ba98928fb0a39290a6ee26fdcacc66229313045',
           'main63.f':
           'b2dd343b3cd7969979b80c564d82b92e0d776d66bb19d346b52f2af27adeb62d',
           'main64.f':
           'a35f2f232e6e0d68d67fd350d4d46b0a353f5c7811de0c2db47ae16d17ed1843',
           'main65.f':
           '03c81e0bbd77710b0461e18265e80e3bd51360b9f416c86013401f882ac39a5e',
           'main66.f':
           '50dd9221a7e84ee7c5005db6758e5880d190eab8cce8a52e7c7b29e9fee8d3da',
           'main67.f':
           '1984aa90fe4e3d628c3bcceaa6fca1b08231d835158d975fa171337d55ca4a2f',
           'main68.f':
           'c8d6def1298477ffec6a1d98c7e02dcee0debe6badc7c63f752f9194b82f212d',
           'main69.f':
           'd14399d43f8c4b670907558849d3e5a4d7625d027de3c10002185c58b20b061a',
           'main71.f':
           '2e47af778003b0596e8999f0914033c6eda7335211b9e96ac3075d45a3cde12e',
           'main72.f':
           'e27ce2af68b40436c51c65767ebb5ff0955ab8dfdfc5fc5c217ae73cd53070da',
           'main73.f':
           '567db2d1a66896ce5103ffa7e10742442b0e934088883e91339536e0249772c4',
           'main75.f':
           'b850986c43a5af1e7d13b66d22b01584e3c68bb338be32eac39e31f971b80be4',
           'main77.f':
           '0679852c4f35719531ad38dc1dbb374b884181eb5e483c36d8867ccb449177a4',
           'main78.f':
           '5babc59fe6a0bd57d97ec398cf01745bc9b72ce6ce0711e934d53c7821e21912',
           'main79.f':
           '27ca84d6d0877f3605cbc1b865c3e1f571e7d2c9301094a4122e726a903dbead',
           'main81.f':
           'b02fecd1cd0f9ba16eaae53e9da0ba602569fdf0e46856cccdfb4c5b7ba33e8b',
           'ttbar.lhe':
           'fb0d43175cc392b19c2b6633dcf673d0b56229b60bec92df4aa782c7196b149c'}

    for example, checksum in iteritems(examples):
        resource(name=example,
                 url='http://pythiasix.hepforge.org/examples/{0}'.
                 format(example),
                 sha256=checksum,
                 expand=False,
                 destination='example',
                 placement={example: example}
             )

    # Docs.
    docs \
        = {'http://www.hepforge.org/archive/pythiasix/update_notes-6.4.28.txt':
            'a229be4ba9a4eb65a9d53600a5f388b620038d56694c6cb4671c2be224b67751',
           'http://home.thep.lu.se/~torbjorn/pythia6/lutp0613man2.pdf':
           '03d637310ea80f0d7aea761492bd38452c602890d8cf913a1ec9edacd79fa43d',
           'https://pythiasix.hepforge.org/pythia6-announcement.txt':
           '2a52def41f0c93e32e0db58dbcf072b987ebfbd32e42ccfc1f9382fcf65f1271'}

    for docurl, checksum in iteritems(docs):
        doc = os.path.basename(urlparse(docurl).path)
        resource(name=doc,
                 url=docurl,
                 sha256=checksum,
                 expand=False,
                 destination='doc',
                 placement={doc: doc}
             )

    patch('pythia6.patch', level=0)

    def patch(self):
        # Use our provided CMakeLists.txt
        llnl.util.filesystem.copy(os.path.join(os.path.dirname(__file__),
                                               'CMakeLists.txt'),
                                  self.stage.source_path)

    def cmake_args(self):
        args = ['-DPYTHIA6_VERSION={0}'.format(self.version.dotted)]
        return args
