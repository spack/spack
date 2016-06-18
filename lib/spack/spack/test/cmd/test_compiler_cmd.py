import spack.spec
import spack.cmd.compiler
import spack.compilers
from spack.test.mock_packages_test import *


class MockArgs(object):
    def __init__(self, add_paths=[], scope=None, compiler_spec=None, all=None):
        self.add_paths = add_paths
        self.scope = scope
        self.compiler_spec = compiler_spec
        self.all = all


class CompilerCmdTest(MockPackagesTest):
    """ Test compiler commands for add and remove """

    def test_compiler_remove(self):
        args = MockArgs(all=True, compiler_spec='gcc@4.5.0')
        spack.cmd.compiler.compiler_remove(args)
        compilers = spack.compilers.all_compilers()
        self.assertTrue(spack.spec.CompilerSpec("gcc@4.5.0") not in compilers)

    def test_compiler_add(self):
        # Probably not a good a assumption but might try finding local
        # compilers
        # installed in /usr
        compilers = spack.compilers.all_compilers()
        s = set(compilers)
        args = MockArgs(add_paths=["/usr"])
        spack.cmd.compiler.compiler_find(args)
        new_compilers = spack.compilers.all_compilers()
        new_compiler = [x for x in new_compilers if x not in s]
        self.assertTrue(new_compiler)
