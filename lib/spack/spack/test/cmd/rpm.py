import unittest
import itertools

from spack.cmd.rpm import *


class MockSpec(object):
    def __init__(self, name, deps=None):
        self.name = name
        self.deps = deps or {}

    def dependencies_dict(self):
        return self.deps

    def format(self):
        return self.__str__()

    def traverse(self, visited=None, cover=None, key=None):
        specs = set(dep.spec for dep in self.deps.values())
        return set(
            itertools.chain(
                [self],
                itertools.chain.from_iterable(y.traverse() for y in specs)))

    def __str__(self):
        return self.name + 'spec'

    @property
    def package(self):
        return type("Package", (), {
            '__doc__': 'Doc for ' + self.name,
            'license': None})


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


class MockSubspaceConfig(object):
    def get_namespace(self, pkgName, required=False):
        return MockNamespace()

    def get_extra_system_deps(self, pkg_name):
        return set(), set()


class MockDependencyConfig(object):
    def __init__(self, spec_to_norpm=None, spec_to_ignore=None,
                 spec_to_direct=None):
        self.spec_to_norpm = spec_to_norpm or {}
        self.spec_to_ignore = spec_to_ignore or {}
        self.spec_to_direct = spec_to_direct or {}

    def ignore_deps_for_pkg(self, pkg_spec):
        return self.spec_to_ignore.get(pkg_spec, set())

    def build_norpm_deps_for_pkg(self, pkg_spec):
        return self.spec_to_norpm.get(pkg_spec, set())

    def external_pkg_cfg(self, pkg_spec, ignore_deps):
        return {}, {}

    def split_by_rpm_deptype(self, pkg_spec, replace, spack_rpms):
        return set(), set()

    def direct_deps(self, pkg_spec):
        return self.spec_to_direct.get(pkg_spec, set())


subspaceCfg = MockSubspaceConfig()

# The following spec instantiations build a simple dependency dag:
#
#   X
#  / \ (build)
# Y   Z

specY1 = MockSpec('y')
specZ1 = MockSpec('z')
specX1 = MockSpec('x',
                  {'y': Dependency(specY1),
                   'z': Dependency(specZ1, ('build',))})

rpmY1 = Rpm(MockNamespace.name(specY1), specY1.name, str(specY1),
            MockNamespace.path(specY1), set())
rpmZ1 = Rpm(MockNamespace.name(specZ1), specZ1.name, str(specZ1),
            MockNamespace.path(specZ1), set())


class RpmTest(unittest.TestCase):
    def setUp(self):
        super(RpmTest, self).setUp()
        self.new = set()
        self.rpmDb1 = {
            rpmY1.name: RpmInfo(rpmY1, None),
            rpmZ1.name: RpmInfo(rpmZ1, None)}

    def test_leaf_pkg(self):
        rpmDb = self.rpmDb1
        resultRpm = resolve_autoname(specY1, subspaceCfg, rpmDb, self.new,
                                     MockDependencyConfig())

        self.assertEqual(rpmY1, resultRpm)

    def test_transitive(self):
        rpmX = Rpm(MockNamespace.name(specX1), specX1.name, str(specX1),
                   MockNamespace.path(specX1), set([rpmY1, rpmZ1]))
        rpmDb = self.rpmDb1

        resultRpm = resolve_autoname(specX1, subspaceCfg, rpmDb, self.new,
                                     MockDependencyConfig())

        self.assertEqual(rpmX, resultRpm)

    def test_rm_builddeps(self):
        rpmX = Rpm(MockNamespace.name(specX1), specX1.name, str(specX1),
                   MockNamespace.path(specX1), set([rpmY1]),
                   non_rpm_deps=set([specZ1.name]))
        rpmDb = self.rpmDb1
        rpmDb[rpmX.name] = RpmInfo(rpmX, None)

        resultRpm = resolve_autoname(specX1, subspaceCfg, rpmDb, self.new,
                                     MockDependencyConfig())

        expected = Rpm(MockNamespace.name(specX1), specX1.name, str(specX1),
                       MockNamespace.path(specX1), set([rpmY1, rpmZ1]))

        self.assertEqual(expected, resultRpm)

    def test_visited_dep(self):
        rpmDb = self.rpmDb1
        resultRpm = resolve_autoname(
            specX1, subspaceCfg, rpmDb, self.new, MockDependencyConfig(),
            visited=set([specY1]))

        expected = Rpm(MockNamespace.name(specX1), specX1.name, str(specX1),
                       MockNamespace.path(specX1), set([rpmZ1, rpmY1]))
        self.assertEqual(expected, resultRpm)

    def test_fill_spec(self):
        rpm_spec = RpmSpec(
            'foo-3.5',
            summary='example package summary',
            license='BSD',
            group='examples',
            extra_build_requires=['system_binutils'])

        requires = build_requires = ['spack_bar', 'spack_baz']
        spec_vars = rpm_spec.new_spec_variables(
            requires, build_requires,
            './bin/spack install foo@3.5',
            '/usr/spack/foo-3.5')

        fill_spec_template(spec_vars, default_spec())

    def test_parse_spec(self):
        rpm_spec = RpmSpec(
            'foo-3.5',
            summary='example package summary',
            license='BSD',
            group='examples',
            extra_build_requires=['system_binutils'])

        requires = build_requires = ['spack_bar', 'spack_baz']
        spec_vars = rpm_spec.new_spec_variables(
            requires, build_requires,
            './bin/spack install foo@3.5',
            '/usr/spack/foo-3.5')

        spec_contents = fill_spec_template(spec_vars, default_spec())

        spec_vars, rpm_props = RpmSpecParser().parse_to_properties(
            spec_contents, 'foo', '/usr/spack/')

        self.assertEqual('example package summary', spec_vars.SUMMARY)
        self.assertTrue(not spec_vars.PACKAGE_PATH)
        self.assertEqual('foo-3.5', rpm_props.name_spec)
        self.assertEqual('/usr/spack/', rpm_props.root)
