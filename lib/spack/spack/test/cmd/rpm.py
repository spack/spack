import unittest
import itertools

import spack.cmd.rpm as rpm
from spack.cmd.rpm import resolve_autoname, Rpm, RpmSpec, RpmInfo

class MockSpec(object):
    def __init__(self, name, deps=None):
        self.name = name
        self.deps = deps or {}

    def dependencies_dict(self):
        return self.deps

    def format(self):
        return self.__str__()

    def traverse(self):
        specs = set(dep.spec for dep in self.deps.itervalues())
        return set(itertools.chain([self], 
            itertools.chain.from_iterable(
                y.traverse() for y in specs)))

    def __str__(self):
        return self.name + 'spec'

    @property
    def package(self):
        return type("Package", (), {
            '__doc__':'Doc for ' + self.name,
            'license':None})

class Dependency(object):
    def __init__(self, spec, deptypes=None):
        self.deptypes = deptypes or ('build', 'link')
        self.spec = spec

class MockNamespace(object):
    ROOT = '/path/to/'

    @staticmethod
    def name(spec):
        return spec.name + 'rpm'
    
    @staticmethod
    def provides_name(spec):
        return MockNamespace.name(spec)
    
    @staticmethod
    def path(spec):
        return MockNamespace.ROOT + spec.name

    @property
    def root(self):
        return MockNamespace.ROOT
    
    @property
    def name_spec(self):
        return "MockNamespace.nameSpec"
    
    @property
    def provides_spec(self):
        return "MockNamespace.providesSpec"

class MockNamespaceStore(object):
    def get_namespace(self, pkgName, required=False):
        return MockNamespace()

namespaceStore = MockNamespaceStore()

"""
  X
 / \ (build)
Y   Z
"""

specY1 = MockSpec('y')
specZ1 = MockSpec('z')
specX1 = MockSpec('x', {'y':Dependency(specY1), 
    'z':Dependency(specZ1, ('build',))})

rpmY1 = Rpm(MockNamespace.name(specY1), specY1.name, str(specY1), 
    MockNamespace.path(specY1), set())
rpmZ1 = Rpm(MockNamespace.name(specZ1), specZ1.name, str(specZ1), 
    MockNamespace.path(specZ1), set())

class RpmTest(unittest.TestCase):
    def setUp(self):
        super(RpmTest, self).setUp()
        self.new = set()
        self.pkgToRpmProps = {}
        self.rpmDb1 = {
            rpmY1.name: RpmInfo(rpmY1, None), 
            rpmZ1.name: RpmInfo(rpmZ1, None)}

    def test_leaf_pkg(self):
        buildDeps = None
        ignoreDeps = None
        rpmDb = self.rpmDb1
        resultRpm = resolve_autoname(specY1, namespaceStore, rpmDb, self.new, 
            buildDeps, ignoreDeps, self.pkgToRpmProps)

        self.assertEqual(rpmY1, resultRpm)   

    def test_transitive(self):
        rpmX = Rpm(MockNamespace.name(specX1), specX1.name, str(specX1), 
            MockNamespace.path(specX1), set([rpmY1, rpmZ1]))
        rpmDb = self.rpmDb1
        rpmDb[rpmX.name] = RpmInfo(rpmX, None)

        buildDeps = None
        ignoreDeps = None
        resultRpm = resolve_autoname(specX1, namespaceStore, rpmDb, self.new, 
            buildDeps, ignoreDeps, self.pkgToRpmProps)

        self.assertEqual(rpmX, resultRpm)

    def test_rm_builddeps(self):
        rpmX = Rpm(MockNamespace.name(specX1), specX1.name, str(specX1), 
            MockNamespace.path(specX1), set([rpmY1]), 
            non_rpm_deps=set([specZ1.name]))
        rpmDb = self.rpmDb1
        rpmDb[rpmX.name] = RpmInfo(rpmX, None)

        buildDeps = set()
        ignoreDeps = None
        resultRpm = resolve_autoname(specX1, namespaceStore, rpmDb, self.new, 
            buildDeps, ignoreDeps, self.pkgToRpmProps)

        expected = Rpm(MockNamespace.name(specX1), specX1.name, str(specX1), 
            MockNamespace.path(specX1), set([rpmY1, rpmZ1]))

        self.assertEqual(expected, resultRpm)

    def test_visited_dep(self):
        rpmDb = self.rpmDb1
        buildDeps = None
        ignoreDeps = None
        resultRpm = resolve_autoname(specX1, namespaceStore, rpmDb, self.new, 
            buildDeps, ignoreDeps, self.pkgToRpmProps, 
            visited=set([specY1]))
            
        expected = Rpm(MockNamespace.name(specX1), specX1.name, str(specX1), 
            MockNamespace.path(specX1), set([rpmZ1, rpmY1]))
        self.assertEqual(expected, resultRpm)
