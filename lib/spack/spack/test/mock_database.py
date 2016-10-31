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
##############################################################################
import shutil
import tempfile

import spack
import spack.store
from spack.spec import Spec
from spack.database import Database
from spack.directory_layout import YamlDirectoryLayout
from spack.test.mock_packages_test import MockPackagesTest


class MockDatabase(MockPackagesTest):

    def _mock_install(self, spec):
        s = Spec(spec)
        s.concretize()
        pkg = spack.repo.get(s)
        pkg.do_install(fake=True)

    def _mock_remove(self, spec):
        specs = spack.store.db.query(spec)
        assert len(specs) == 1
        spec = specs[0]
        spec.package.do_uninstall(spec)

    def setUp(self):
        super(MockDatabase, self).setUp()
        #
        # TODO: make the mockup below easier.
        #

        # Make a fake install directory
        self.install_path = tempfile.mkdtemp()
        self.spack_install_path = spack.store.root
        spack.store.root = self.install_path

        self.install_layout = YamlDirectoryLayout(self.install_path)
        self.spack_install_layout = spack.store.layout
        spack.store.layout = self.install_layout

        # Make fake database and fake install directory.
        self.install_db = Database(self.install_path)
        self.spack_install_db = spack.store.db
        spack.store.db = self.install_db

        # make a mock database with some packages installed note that
        # the ref count for dyninst here will be 3, as it's recycled
        # across each install.
        #
        # Here is what the mock DB looks like:
        #
        # o  mpileaks     o  mpileaks'    o  mpileaks''
        # |\              |\              |\
        # | o  callpath   | o  callpath'  | o  callpath''
        # |/|             |/|             |/|
        # o |  mpich      o |  mpich2     o |  zmpi
        #   |               |             o |  fake
        #   |               |               |
        #   |               |______________/
        #   | .____________/
        #   |/
        #   o  dyninst
        #   |\
        #   | o  libdwarf
        #   |/
        #   o  libelf
        #

        # Transaction used to avoid repeated writes.
        with spack.store.db.write_transaction():
            self._mock_install('mpileaks ^mpich')
            self._mock_install('mpileaks ^mpich2')
            self._mock_install('mpileaks ^zmpi')

    def tearDown(self):
        with spack.store.db.write_transaction():
            for spec in spack.store.db.query():
                spec.package.do_uninstall(spec)

        super(MockDatabase, self).tearDown()
        shutil.rmtree(self.install_path)
        spack.store.root = self.spack_install_path
        spack.store.layout = self.spack_install_layout
        spack.store.db = self.spack_install_db
