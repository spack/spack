import shutil
import tempfile

import spack
import spack.install_area
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
        specs = spack.install_area.db.query(spec)
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
        self.spack_install_path = spack.install_area.path
        spack.install_area.path = self.install_path

        self.install_layout = YamlDirectoryLayout(self.install_path)
        self.spack_install_layout = spack.install_area.layout
        spack.install_area.layout = self.install_layout

        # Make fake database and fake install directory.
        self.installed_db = Database(self.install_path)
        self.spack_installed_db = spack.install_area.db
        spack.install_area.db = self.installed_db

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
        with spack.install_area.db.write_transaction():
            self._mock_install('mpileaks ^mpich')
            self._mock_install('mpileaks ^mpich2')
            self._mock_install('mpileaks ^zmpi')

    def tearDown(self):
        for spec in spack.install_area.db.query():
            spec.package.do_uninstall(spec)
        super(MockDatabase, self).tearDown()
        shutil.rmtree(self.install_path)
        spack.install_area.path = self.spack_install_path
        spack.install_area.layout = self.spack_install_layout
        spack.install_area.db = self.spack_installed_db
