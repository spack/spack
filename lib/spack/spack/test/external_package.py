import pytest
import shutil

from llnl.util.filesystem import mkdirp, join_path, touchp
import spack
import spack.architecture
from spack.environment import EnvironmentModifications
from spack.external_package import ExternalPackage, SpecVersionMisMatch
import spack.spec
from spack.util.spack_yaml import syaml_dict


@pytest.mark.usefixtures("modulepath", "fake_external_package")
class TestExternalPackage(object):
    """Test ExternalPackage class."""

    @pytest.mark.skipif("cray" in spack.architecture.sys_type(),
                        reason="Requires cray packages to test")
    def test_find_cray_packages(self):
        cray_packages = ExternalPackage.find_external_packages()
        correct_packages = True
        assert cray_packages


    def make_fake_install_path(self, path, exe_name, fake_external_package):
        """Make a temporary path to a fake package """
        temp_path = fake_external_package
        fake_root_path = join_path(temp_path, path)
        exe_path = join_path(fake_root_path, "bin", exe_name)
        touchp(exe_path)
        # Mimics common case for standard install directory
        for p in ["lib", "share", "include"]:
            package_path = join_path(fake_root_path, p)
            mkdirp(package_path)
        # Set the path we created to external_package_path directory
        self.external_package_path = fake_root_path


    def test_package_detection_in_paths(self, fake_external_package):
        spec = spack.spec.Spec("externalpackage@1.8.5%gcc@6.1.0")
        self.make_fake_install_path("external_package/1.8.5",
                                    "externalpackage",
                                    fake_external_package)
        path = self.external_package_path
        actual_package = ExternalPackage.create_external_package(spec, path)
        expected_package = ExternalPackage(spec, False, "paths",
                                           self.external_package_path)
        assert actual_package == expected_package

    @pytest.mark.skipif("cray" in spack.architecture.sys_type(),
                        reason="Requires cray modules to test")
    def test_package_detection_in_modules(self):
        spec = spack.spec.Spec("externalmodule@1.0%gcc@6.1.0")
        mod_name = "externalmodule"
        actual_package = ExternalPackage.create_external_package(spec,
                                                                 mod_name)
        expected_package = ExternalPackage(spec, False, "modules", mod_name)
        assert actual_package == expected_package

    def test_when_external_type_not_detected(self):
        spec = spack.spec.Spec("externalpackage@1.8.5%gcc@6.1.0")
        non_existent_path = "path/to/externaltool"
        # tty.die error
        with pytest.raises(SystemExit):
            ExternalPackage.create_external_package(spec, non_existent_path)

    def test_when_no_version_in_spec_and_no_version_detected(self,
                                                        fake_external_package):
        package_spec = spack.spec.Spec("externaltool%gcc@4.3")
        self.make_fake_install_path("path/to/externaltool",
                                    "externaltool",
                                    fake_external_package)
        # tty.die error
        with pytest.raises(SystemExit):
            ExternalPackage.create_external_package(package_spec,
                                                    self.external_package_path)

        if spack.architecture.sys_type() == "cray":
            module_spec = spack.spec.Spec("externalmodule%gcc@4.3")
            no_version_module = "externalmodule"
            with pytest.raises(SystemExit):
                ExternalPackage.create_external_package(module_spec,
                                                        no_version_module)

    def test_when_spec_version_and_found_version_dont_match(self,
                                                        fake_external_package):
        spec = spack.spec.Spec("externalpackage@1.7.0%gcc@6.1.0")
        self.make_fake_install_path("external_package/1.8.5",
                                    "externalpackage",
                                    fake_external_package)
        with pytest.raises(SpecVersionMisMatch):
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
        assert external_package.to_config_entry() == proper_yaml
