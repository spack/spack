# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import spack.modules.common
import spack.modules.tcl
import spack.spec

mpich_spec_string = "mpich@3.0.4"
mpileaks_spec_string = "mpileaks"
libdwarf_spec_string = "libdwarf arch=x64-linux"

#: Class of the writer tested in this module
writer_cls = spack.modules.ups_version.UpsVersionModulefileWriter


@pytest.mark.usefixtures("config", "mock_packages")
class TestTcl(object):
    def test_simple_case(self, modulefile_content, module_configuration):
        """Tests the generation of a simple TCL module file."""

        module_configuration("autoload_direct")
        content = modulefile_content(mpich_spec_string)

        assert "PRODUCT = mpich" in content

    def test_autoload_direct(self, modulefile_content, module_configuration):
        """Tests the automatic loading of direct dependencies."""

        module_configuration("autoload_direct")
        content = modulefile_content(mpileaks_spec_string)

        assert len([x for x in content if "FILE = version" in x]) == 1

        # dtbuild1 has
        # - 1 ('run',) dependency
        # - 1 ('build','link') dependency
        # - 1 ('build',) dependency
        # Just make sure the 'build' dependency is not there
        content = modulefile_content("dtbuild1")

        assert len([x for x in content if "FILE = version" in x]) == 1

        # The configuration file sets the verbose keyword to False
        messages = [x for x in content if 'puts stderr "Autoloading' in x]
        assert len(messages) == 0

    def test_autoload_all(self, modulefile_content, module_configuration):
        """Tests the automatic loading of all dependencies."""

        module_configuration("autoload_all")
        content = modulefile_content(mpileaks_spec_string)

        assert len([x for x in content if "FILE = version" in x]) == 1

        # dtbuild1 has
        # - 1 ('run',) dependency
        # - 1 ('build','link') dependency
        # - 1 ('build',) dependency
        # Just make sure the 'build' dependency is not there
        content = modulefile_content("dtbuild1")

        assert len([x for x in content if "FILE = version" in x]) == 1

    def test_prerequisites_direct(self, modulefile_content, module_configuration):
        """Tests asking direct dependencies as prerequisites."""

        module_configuration("prerequisites_direct")
        content = modulefile_content("mpileaks arch=x86-linux")

        assert len([x for x in content if "FILE = version" in x]) == 1

    def test_prerequisites_all(self, modulefile_content, module_configuration):
        """Tests asking all dependencies as prerequisites."""

        module_configuration("prerequisites_all")
        content = modulefile_content("mpileaks arch=x86-linux")

        assert len([x for x in content if "FILE = version" in x]) == 1

    def test_alter_environment(self, modulefile_content, module_configuration):
        """Tests modifications to run-time environment."""

        module_configuration("alter_environment")
        content = modulefile_content("mpileaks platform=test target=x86_64")
        assert len([x for x in content if "FILE = version" in x]) == 1

        content = modulefile_content("libdwarf %clang platform=test target=x86_32")
        assert len([x for x in content if "FILE = version" in x]) == 1

    def test_blacklist(self, modulefile_content, module_configuration):
        """Tests blacklisting the generation of selected modules."""

        module_configuration("blacklist")
        content = modulefile_content("mpileaks ^zmpi")

        assert len([x for x in content if "FILE = version" in x]) == 1

        # Returns a StringIO instead of a string as no module file was written
        with pytest.raises(AttributeError):
            modulefile_content("callpath arch=x86-linux")

        content = modulefile_content("zmpi arch=x86-linux")

        assert len([x for x in content if "FILE = version" in x]) == 1

    def test_naming_scheme(self, factory, module_configuration):
        """Tests reading the correct naming scheme."""

        # This configuration has no error, so check the conflicts directives
        # are there
        module_configuration("conflicts")

        # Test we read the expected configuration for the naming scheme
        writer, _ = factory("mpileaks")
        expected = "{name}/{version}-{compiler.name}"

        assert writer.conf.naming_scheme == expected

    def test_invalid_naming_scheme(self, factory, module_configuration):
        """Tests the evaluation of an invalid naming scheme."""

        module_configuration("invalid_naming_scheme")

        # Test that having invalid tokens in the naming scheme raises
        # a RuntimeError
        writer, _ = factory("mpileaks")
        with pytest.raises(RuntimeError):
            writer.layout.use_name

    def test_invalid_token_in_env_name(self, factory, module_configuration):
        """Tests setting environment variables with an invalid name."""

        module_configuration("invalid_token_in_env_var_name")

        writer, _ = factory("mpileaks")
        with pytest.raises(RuntimeError):
            writer.write()

    def test_module_index(self, module_configuration, factory, tmpdir_factory):

        module_configuration("suffix")

        w1, s1 = factory("mpileaks")
        w2, s2 = factory("callpath")

        test_root = str(tmpdir_factory.mktemp("module-root"))

        spack.modules.common.generate_module_index(test_root, [w1, w2])

        index = spack.modules.common.read_module_index(test_root)

        assert index[s1.dag_hash()].use_name == w1.layout.use_name
        assert index[s2.dag_hash()].path == w2.layout.filename

    def test_suffixes(self, module_configuration, factory):
        """Tests adding suffixes to module file name."""
        module_configuration("suffix")

        writer, spec = factory("mpileaks+debug arch=x86-linux")
        assert "foo" in writer.layout.use_name

        writer, spec = factory("mpileaks~debug arch=x86-linux")
        assert "bar" in writer.layout.use_name

    def test_setup_environment(self, modulefile_content, module_configuration):
        """Tests the internal set-up of run-time environment."""

        module_configuration("suffix")
        spec = spack.spec.Spec("mpileaks")
        spec.concretize()

    def test_override_template_in_modules_yaml(self, modulefile_content, module_configuration):
        """Tests overriding a template from `modules.yaml`"""
        module_configuration("override_template")

        content = modulefile_content("override-module-templates")
        assert "Override even better!" in content

        content = modulefile_content("mpileaks arch=x86-linux")
        assert "Override even better!" in content

    def test_extend_context(self, modulefile_content, module_configuration):
        """Tests using a package defined context"""
        module_configuration("autoload_direct")
        content = modulefile_content("override-context-templates")

        assert "PRODUCT = override-context-templates" in content

    @pytest.mark.regression("9624")
    @pytest.mark.db
    def test_autoload_with_constraints(self, modulefile_content, module_configuration, database):
        """Tests the automatic loading of direct dependencies."""

        module_configuration("autoload_with_constraints")

        # Test the mpileaks that should have the autoloaded dependencies
        content = modulefile_content("mpileaks ^mpich2")
        assert len([x for x in content if "FILE = version" in x]) == 1

        # Test the mpileaks that should NOT have the autoloaded dependencies
        content = modulefile_content("mpileaks ^mpich")
        assert len([x for x in content if "FILE = version" in x]) == 1
