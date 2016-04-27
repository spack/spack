import spack.test.mock_database

from spack.cmd.uninstall import uninstall


class MockArgs(object):
    def __init__(self, packages, all=False, force=False, dependents=False):
        self.packages = packages
        self.all = all
        self.force = force
        self.dependents = dependents
        self.yes_to_all = True


class TestUninstall(spack.test.mock_database.MockDatabase):
    def test_uninstall(self):
        parser = None
        # Multiple matches
        args = MockArgs(['mpileaks'])
        self.assertRaises(SystemExit, uninstall, parser, args)
        # Installed dependents
        args = MockArgs(['libelf'])
        self.assertRaises(SystemExit, uninstall, parser, args)
        # Recursive uninstall
        args = MockArgs(['callpath'], all=True, dependents=True)
        uninstall(parser, args)

        all_specs = spack.install_layout.all_specs()
        self.assertEqual(len(all_specs), 7)
        # query specs with multiple configurations
        mpileaks_specs = [s for s in all_specs if s.satisfies('mpileaks')]
        callpath_specs = [s for s in all_specs if s.satisfies('callpath')]
        mpi_specs = [s for s in all_specs if s.satisfies('mpi')]

        self.assertEqual(len(mpileaks_specs), 0)
        self.assertEqual(len(callpath_specs), 0)
        self.assertEqual(len(mpi_specs),      3)
