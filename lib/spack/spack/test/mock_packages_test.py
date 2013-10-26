import unittest

import spack
import spack.packages as packages
from spack.spec import Spec
from spack.util.lang import new_path, list_modules

mock_packages_path = new_path(spack.module_path, 'test', 'mock_packages')
original_deps = None


def set_pkg_dep(pkg, spec):
    """Alters dependence information for a pacakge.
       Use this to mock up constraints.
    """
    spec = Spec(spec)
    packages.get(pkg).dependencies[spec.name] = spec


def restore_dependencies():
    # each time through restore original dependencies & constraints
    global original_deps
    for pkg_name, deps in original_deps.iteritems():
        packages.get(pkg_name).dependencies.clear()
        for dep in deps:
            set_pkg_dep(pkg_name, dep)


class MockPackagesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Use a different packages directory for these tests.  We want to use
        # mocked up packages that don't interfere with the real ones.
        cls.real_packages_path = spack.packages_path
        spack.packages_path = mock_packages_path

        # First time through, record original relationships bt/w packages
        global original_deps
        original_deps = {}
        for name in list_modules(mock_packages_path):
            pkg = packages.get(name)
            original_deps[name] = [
                spec for spec in pkg.dependencies.values()]


    @classmethod
    def tearDownClass(cls):
        """Restore the real packages path after any test."""
        restore_dependencies()
        spack.packages_path = cls.real_packages_path


    def setUp(self):
        """Before each test, restore deps between packages to original state."""
        restore_dependencies()
