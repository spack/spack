import shutil
import tempfile

from llnl.util.filesystem import mkdirp, join_path, touchp, touch
import spack
import spack.architecture
from spack.environment import EnvironmentModifications
from spack.external_package import ExternalPackage, SpecVersionMisMatch
import spack.spec
from spack.test.mock_packages_test import *
from spack.util.spack_yaml import syaml_dict


def set_to_modulepath(path):
    env = EnvironmentModifications()
    env.append_path("MODULEPATH", path)
    env.apply_modifications()


def remove_from_modulepath(path):
    env = EnvironmentModifications()
    env.remove_path("MODULEPATH", path)
    env.apply_modifications()


class TestExternalPackage(MockPackagesTest):
    """Test ExternalPackage class."""

    def make_fake_install_path(self, path, exe_name):
        """Make a temporary path to a fake package """
        fake_root_path = join_path(self.external_package_path, path)
        exe_path = join_path(fake_root_path, "bin", exe_name)
        touchp(exe_path)
        for p in ["lib", "share", "include"]:
            package_path = join_path(fake_root_path, p)
            mkdirp(package_path)
        # Set the path we created to external_package_path directory
        self.external_package_path = fake_root_path

    def setUp(self):
        set_to_modulepath(spack.mock_modulefiles_path)
        # tmp directory set to attribute so tests can append to this path
        self.external_package_path = tempfile.mkdtemp() 
        super(TestExternalPackage, self).setUp()

    def tearDown(self):
        remove_from_modulepath(spack.mock_modulefiles_path)
        shutil.rmtree(self.external_package_path, ignore_errors=True)
        super(TestExternalPackage, self).tearDown()

    def test_package_detection_in_paths(self):
        spec = spack.spec.Spec("externalpackage@1.8.5%gcc@6.1.0")
        self.make_fake_install_path("external_package/1.8.5",
                                    "externalpackage")
        actual_package = ExternalPackage.create_external_package(
                                            spec, self.external_package_path)
        expected_package = ExternalPackage(spec,
                                           False,
                                           "paths",
                                           self.external_package_path)
        self.assertEquals(actual_package, expected_package)

    def test_package_detection_in_modules(self):
        if spack.architecture.sys_type() == "cray":
            spec = spack.spec.Spec("externalmodule@1.0%gcc@6.1.0")
            module_name = "externalmodule"
            actual_package = ExternalPackage.create_external_package(
                                                        spec, module_name)
            expected_package = ExternalPackage(spec, module_name, "modules")
            self.assertEquals(actual_package, expected_package)
        else:
            self.assertTrue(True)

    def test_when_external_type_not_detected(self):
        spec = spack.spec.Spec("externalpackage@1.8.5%gcc@6.1.0")
        non_existent_path = "path/to/externaltool"
        with self.assertRaises(SystemExit): # tty.die error
            ExternalPackage.create_external_package(spec, non_existent_path)

    def test_when_no_version_in_spec_and_no_version_detected(self):
        package_spec = spack.spec.Spec("externaltool%gcc@4.3")
        self.make_fake_install_path("path/to/externaltool",
                                                 "externaltool")
        with self.assertRaises(SystemExit): # tty.die error
            ExternalPackage.create_external_package(package_spec,
                                                    self.external_package_path)

        if spack.architecture.sys_type() == "cray":
            module_spec = spack.spec.Spec("externalmodule%gcc@4.3")
            no_version_module = "externalmodule"
            with self.assertRaises(SystemExit): # tty.die error
                ExternalPackage.create_external_package(module_spec,
                                                        no_version_module)
        else:
            self.assertTrue(True)

    def test_when_spec_version_and_found_version_dont_match(self):
        spec = spack.spec.Spec("externalpackage@1.7.0%gcc@6.1.0")
        self.make_fake_install_path("external_package/1.8.5",
                                    "externalpackage")
        with self.assertRaises(SpecVersionMisMatch):
            ExternalPackage.create_external_package(spec,
                                                    self.external_package_path)

    def test_proper_config_entry_creation(self):
        spec = spack.spec.Spec("externalpackage@1.8.5%gcc@6.1.0")
        path = "path/to/external_package"
        buildable = False
        external_type = "paths"
        external_package = ExternalPackage(spec, buildable, external_type,
                                           path)
        # subject to change once we move to json?
        specs_yaml = syaml_dict([(str(spec), "path/to/external_package")])
        complete_specs_yaml = syaml_dict([("buildable", False),
                                           ("paths", specs_yaml)])
        proper_yaml = syaml_dict([("externalpackage", complete_specs_yaml)])
        self.assertEquals(external_package.to_config_entry(), proper_yaml)
