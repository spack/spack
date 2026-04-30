# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

import pytest

import spack.vendor.archspec.cpu

import spack.concretize
import spack.config
import spack.main
import spack.modules.common
import spack.modules.error
import spack.modules.tcl
import spack.spec
import spack.util.environment
from spack.config import Configuration

mpich_spec_string = "mpich@3.0.4"
mpileaks_spec_string = "mpileaks"
libdwarf_spec_string = "libdwarf target=x86_64"

install = spack.main.SpackCommand("install")
mark = spack.main.SpackCommand("mark")
uninstall = spack.main.SpackCommand("uninstall")

#: Class of the writer tested in this module
writer_cls = spack.modules.tcl.TclModulefileWriter

pytestmark = [
    pytest.mark.not_on_windows("does not run on windows"),
    pytest.mark.usefixtures("mock_modules_root"),
]


@pytest.fixture(params=["clang@=15.0.0", "gcc@=10.2.1"])
def compiler(request):
    return request.param


@pytest.fixture(
    params=[
        ("mpich@3.0.4", ("mpi",), True, False),
        ("mpich@3.0.1", [], True, True),
        ("openblas@0.2.15", ("blas",), True, False),
        ("openblas-with-lapack@0.2.15", ("blas", "lapack"), True, False),
        ("mpileaks@2.3", ("mpi",), True, False),
        ("mpileaks@2.1", [], True, False),
        ("py-extension1@2.0", ("python",), False, True),
        ("python@3.8.0", ("python",), False, True),
    ]
)
def provider(request):
    return request.param


@pytest.mark.usefixtures("mutable_config", "mock_packages")
class TestTcl:
    def test_simple_case(self, modulefile_content, module_configuration):
        """Tests the generation of a simple Tcl module file."""

        module_configuration("autoload_direct")
        content = modulefile_content(mpich_spec_string)

        assert "module-whatis {mpich @3.0.4}" in content

    def test_autoload_direct(self, modulefile_content, module_configuration):
        """Tests the automatic loading of direct dependencies."""

        module_configuration("autoload_direct")
        content = modulefile_content(mpileaks_spec_string)

        assert (
            len([x for x in content if "if {![info exists ::env(LMOD_VERSION_MAJOR)]} {" in x])
            == 1
        )
        assert len([x for x in content if "    proc depends-on {args} {" in x]) == 1
        assert len([x for x in content if "        module load {*}$args" in x]) == 1
        # depends-on command defined once and used 3 times
        assert len([x for x in content if "depends-on " in x]) == 4

        # dtbuild1 has
        # - 1 ('run',) dependency
        # - 1 ('build','link') dependency
        # - 1 ('build',) dependency
        # Just make sure the 'build' dependency is not there
        content = modulefile_content("dtbuild1")

        assert (
            len([x for x in content if "if {![info exists ::env(LMOD_VERSION_MAJOR)]} {" in x])
            == 1
        )
        assert len([x for x in content if "    proc depends-on {args} {" in x]) == 1
        assert len([x for x in content if "        module load {*}$args" in x]) == 1
        # depends-on command defined once and used twice
        assert len([x for x in content if "depends-on " in x]) == 3

        # The configuration file sets the verbose keyword to False
        messages = [x for x in content if 'puts stderr "Autoloading' in x]
        assert len(messages) == 0

    def test_autoload_all(self, modulefile_content, module_configuration):
        """Tests the automatic loading of all dependencies."""

        module_configuration("autoload_all")
        content = modulefile_content(mpileaks_spec_string)

        assert (
            len([x for x in content if "if {![info exists ::env(LMOD_VERSION_MAJOR)]} {" in x])
            == 1
        )
        assert len([x for x in content if "    proc depends-on {args} {" in x]) == 1
        assert len([x for x in content if "        module load {*}$args" in x]) == 1
        # depends-on command defined once and used 6 times
        assert len([x for x in content if "depends-on " in x]) == 7

        # dtbuild1 has
        # - 1 ('run',) dependency
        # - 1 ('build','link') dependency
        # - 1 ('build',) dependency
        # Just make sure the 'build' dependency is not there
        content = modulefile_content("dtbuild1")

        assert (
            len([x for x in content if "if {![info exists ::env(LMOD_VERSION_MAJOR)]} {" in x])
            == 1
        )
        assert len([x for x in content if "    proc depends-on {args} {" in x]) == 1
        assert len([x for x in content if "        module load {*}$args" in x]) == 1
        # depends-on command defined once and used twice
        assert len([x for x in content if "depends-on " in x]) == 3

    def test_prerequisites_direct(
        self, modulefile_content, module_configuration, host_architecture_str
    ):
        """Tests asking direct dependencies as prerequisites."""

        module_configuration("prerequisites_direct")
        content = modulefile_content(f"mpileaks target={host_architecture_str}")

        assert len([x for x in content if "prereq" in x]) == 3

    def test_prerequisites_all(
        self, modulefile_content, module_configuration, host_architecture_str
    ):
        """Tests asking all dependencies as prerequisites."""

        module_configuration("prerequisites_all")
        content = modulefile_content(f"mpileaks target={host_architecture_str}")

        assert len([x for x in content if "prereq" in x]) == 6

    def test_alter_environment(self, modulefile_content, module_configuration):
        """Tests modifications to run-time environment."""

        module_configuration("alter_environment")
        content = modulefile_content("mpileaks platform=test target=x86_64")

        assert len([x for x in content if x.startswith("    prepend-path CMAKE_PREFIX_PATH")]) == 0
        assert len([x for x in content if "setenv FOO {foo}" in x]) == 1
        assert len([x for x in content if "setenv OMPI_MCA_mpi_leave_pinned {1}" in x]) == 1
        assert len([x for x in content if "setenv OMPI_MCA_MPI_LEAVE_PINNED {1}" in x]) == 0
        assert len([x for x in content if "unsetenv BAR" in x]) == 1
        assert len([x for x in content if "setenv MPILEAKS_ROOT" in x]) == 1

        content = modulefile_content("libdwarf platform=test target=core2")

        assert len([x for x in content if x.startswith("    prepend-path CMAKE_PREFIX_PATH")]) == 0
        assert len([x for x in content if "setenv FOO {foo}" in x]) == 0
        assert len([x for x in content if "unsetenv BAR" in x]) == 0
        assert len([x for x in content if "depends-on foo/bar" in x]) == 1
        assert len([x for x in content if "setenv LIBDWARF_ROOT" in x]) == 1

    def test_prepend_path_separator(self, modulefile_content, module_configuration):
        """Tests that we can use custom delimiters to manipulate path lists."""

        module_configuration("module_path_separator")
        content = modulefile_content("module-path-separator")

        assert len([x for x in content if "append-path -d {:} COLON {foo}" in x]) == 1
        assert len([x for x in content if "prepend-path -d {:} COLON {foo}" in x]) == 1
        assert len([x for x in content if "remove-path -d {:} COLON {foo}" in x]) == 1
        assert len([x for x in content if "append-path -d {;} SEMICOLON {bar}" in x]) == 1
        assert len([x for x in content if "prepend-path -d {;} SEMICOLON {bar}" in x]) == 1
        assert len([x for x in content if "remove-path -d {;} SEMICOLON {bar}" in x]) == 1
        assert len([x for x in content if "append-path -d { } SPACE {qux}" in x]) == 1
        assert len([x for x in content if "remove-path -d { } SPACE {qux}" in x]) == 1

    @pytest.mark.regression("11355")
    def test_manpath_setup(self, modulefile_content, module_configuration):
        """Tests specific setup of MANPATH environment variable."""

        module_configuration("autoload_direct")

        # no manpath set by module
        content = modulefile_content("mpileaks")
        assert len([x for x in content if "append-path MANPATH {}" in x]) == 0

        # manpath set by module with prepend-path
        content = modulefile_content("module-manpath-prepend")
        assert len([x for x in content if "prepend-path -d {:} MANPATH {/path/to/man}" in x]) == 1
        assert (
            len([x for x in content if "prepend-path -d {:} MANPATH {/path/to/share/man}" in x])
            == 1
        )
        assert len([x for x in content if "append-path MANPATH {}" in x]) == 1

        # manpath set by module with append-path
        content = modulefile_content("module-manpath-append")
        assert len([x for x in content if "append-path -d {:} MANPATH {/path/to/man}" in x]) == 1
        assert len([x for x in content if "append-path MANPATH {}" in x]) == 1

        # manpath set by module with setenv
        content = modulefile_content("module-manpath-setenv")
        assert len([x for x in content if "setenv MANPATH {/path/to/man}" in x]) == 1
        assert len([x for x in content if "append-path MANPATH {}" in x]) == 0

    @pytest.mark.regression("29578")
    def test_setenv_raw_value(self, modulefile_content, module_configuration):
        """Tests that we can set environment variable value without formatting it."""

        module_configuration("autoload_direct")
        content = modulefile_content("module-setenv-raw")

        assert len([x for x in content if "setenv FOO {{{name}}, {name}, {{}}, {}}" in x]) == 1

    @pytest.mark.skipif(
        str(spack.vendor.archspec.cpu.host().family) != "x86_64",
        reason="test data is specific for x86_64",
    )
    def test_help_message(self, modulefile_content, module_configuration):
        """Tests the generation of module help message."""

        module_configuration("autoload_direct")
        content = modulefile_content("mpileaks target=core2")

        help_msg = (
            "proc ModulesHelp { } {"
            "    puts stderr {Name   : mpileaks}"
            "    puts stderr {Version: 2.3}"
            "    puts stderr {Target : core2}"
            "    puts stderr {}"
            "    puts stderr {Mpileaks is a mock package that passes audits}"
            "}"
        )
        assert help_msg in "".join(content)

        content = modulefile_content("libdwarf target=core2")

        help_msg = (
            "proc ModulesHelp { } {"
            "    puts stderr {Name   : libdwarf}"
            "    puts stderr {Version: 20130729}"
            "    puts stderr {Target : core2}"
            "}"
        )
        assert help_msg in "".join(content)

        content = modulefile_content("module-long-help target=core2")

        help_msg = (
            "proc ModulesHelp { } {"
            "    puts stderr {Name   : module-long-help}"
            "    puts stderr {Version: 1.0}"
            "    puts stderr {Target : core2}"
            "    puts stderr {}"
            "    puts stderr {Package to test long description message generated in modulefile.}"
            "    puts stderr {Message too long is wrapped over multiple lines.}"
            "}"
        )
        assert help_msg in "".join(content)

    def test_exclude(self, modulefile_content, module_configuration, host_architecture_str):
        """Tests excluding the generation of selected modules."""

        module_configuration("exclude")
        content = modulefile_content("mpileaks ^zmpi")

        # depends-on command defined once and used twice
        assert len([x for x in content if "depends-on " in x]) == 3

        with pytest.raises(FileNotFoundError):
            modulefile_content(f"callpath target={host_architecture_str}")

        content = modulefile_content(f"zmpi target={host_architecture_str}")

        # depends-on command defined once and used twice
        assert len([x for x in content if "depends-on " in x]) == 3

    def test_naming_scheme_compat(self, factory, module_configuration):
        """Tests backwards compatibility for naming_scheme key"""
        module_configuration("naming_scheme")

        # Test we read the expected configuration for the naming scheme
        writer, _ = factory("mpileaks")
        expected = {"all": "{name}/{version}-{compiler.name}"}

        assert writer.conf.projections == expected
        projection = writer.spec.format(writer.conf.projections["all"])
        assert projection in writer.layout.use_name

    def test_projections_specific_non_hierarchical(self, factory, module_configuration):
        """Tests reading the correct naming scheme."""

        # This configuration has no error, so check the conflicts directives
        # are there
        module_configuration("projections_non_hierarchical")

        # Test we read the expected configuration for the naming scheme
        writer, _ = factory("mpileaks")
        expected = {"all": "{name}/{version}-{compiler.name}", "mpileaks": "{name}-mpiprojection"}

        assert writer.conf.projections == expected
        projection = writer.spec.format(writer.conf.projections["mpileaks"])
        assert projection in writer.layout.use_name

    def test_projections_all_non_hierarchical(self, factory, module_configuration):
        """Tests reading the correct naming scheme."""

        # This configuration has no error, so check the conflicts directives
        # are there
        module_configuration("projections_non_hierarchical")

        # Test we read the expected configuration for the naming scheme
        writer, _ = factory("libelf")
        expected = {"all": "{name}/{version}-{compiler.name}", "mpileaks": "{name}-mpiprojection"}

        assert writer.conf.projections == expected
        projection = writer.spec.format(writer.conf.projections["all"])
        assert projection in writer.layout.use_name

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

    def test_conflicts(self, modulefile_content, module_configuration):
        """Tests adding conflicts to the module."""

        # This configuration has no error, so check the conflicts directives
        # are there
        module_configuration("conflicts")
        content = modulefile_content("mpileaks")

        assert len([x for x in content if x.startswith("    conflict")]) == 2
        assert len([x for x in content if x == "    conflict mpileaks"]) == 1
        assert len([x for x in content if x == "    conflict intel/14.0.1"]) == 1

    def test_inconsistent_conflict_in_modules_yaml(self, modulefile_content, module_configuration):
        """Tests inconsistent conflict definition in `modules.yaml`."""

        # This configuration is inconsistent, check an error is raised
        module_configuration("wrong_conflicts")
        with pytest.raises(spack.modules.error.ModulesError):
            modulefile_content("mpileaks")

    def test_module_index(
        self, module_configuration, factory, tmp_path_factory: pytest.TempPathFactory
    ):
        module_configuration("suffix")

        w1, s1 = factory("mpileaks")
        w2, s2 = factory("callpath")
        w3, s3 = factory("openblas")

        test_root = str(tmp_path_factory.mktemp("module-root"))

        spack.modules.common.generate_module_index(test_root, [w1, w2])

        index = spack.modules.common.read_module_index(test_root)

        assert index[s1.dag_hash()].use_name == w1.layout.use_name
        assert index[s2.dag_hash()].path == w2.layout.filename

        spack.modules.common.generate_module_index(test_root, [w3])

        index = spack.modules.common.read_module_index(test_root)

        assert len(index) == 3
        assert index[s1.dag_hash()].use_name == w1.layout.use_name
        assert index[s2.dag_hash()].path == w2.layout.filename

        spack.modules.common.generate_module_index(test_root, [w3], overwrite=True)

        index = spack.modules.common.read_module_index(test_root)

        assert len(index) == 1
        assert index[s3.dag_hash()].use_name == w3.layout.use_name

    def test_suffixes(self, module_configuration, factory):
        """Tests adding suffixes to module file name."""
        module_configuration("suffix")

        writer, spec = factory("mpileaks+debug target=x86_64")
        assert "foo" in writer.layout.use_name
        assert "foo-foo" not in writer.layout.use_name

        writer, spec = factory("mpileaks~debug target=x86_64")
        assert "foo-bar" in writer.layout.use_name
        assert "baz" not in writer.layout.use_name

        writer, spec = factory("mpileaks~debug+opt target=x86_64")
        assert "baz-foo-bar" in writer.layout.use_name

    def test_suffixes_format(self, module_configuration, factory):
        """Tests adding suffixes as spec format string to module file name."""
        module_configuration("suffix-format")

        writer, spec = factory("mpileaks +debug target=x86_64 ^mpich@3.0.4")
        assert "debug=True" in writer.layout.use_name
        assert "mpi=mpich-v3.0.4" in writer.layout.use_name

    def test_setup_environment(self, modulefile_content, module_configuration):
        """Tests the internal set-up of run-time environment."""

        module_configuration("suffix")
        content = modulefile_content("mpileaks")

        assert len([x for x in content if "setenv FOOBAR" in x]) == 1
        assert len([x for x in content if "setenv FOOBAR {mpileaks}" in x]) == 1

        spec = spack.concretize.concretize_one("mpileaks")
        content = modulefile_content(spec["callpath"])

        assert len([x for x in content if "setenv FOOBAR" in x]) == 1
        assert len([x for x in content if "setenv FOOBAR {callpath}" in x]) == 1

    def test_override_config(self, module_configuration, factory):
        """Tests overriding some sections of the configuration file."""
        module_configuration("override_config")

        writer, spec = factory("mpileaks~opt target=x86_64")
        assert "mpich-static" in writer.layout.use_name
        assert "over" not in writer.layout.use_name
        assert "ridden" not in writer.layout.use_name

        writer, spec = factory("mpileaks+opt target=x86_64")
        assert "over-ridden" in writer.layout.use_name
        assert "mpich" not in writer.layout.use_name
        assert "static" not in writer.layout.use_name

    def test_override_template_in_package(self, modulefile_content, module_configuration):
        """Tests overriding a template from and attribute in the package."""

        module_configuration("autoload_direct")
        content = modulefile_content("override-module-templates")

        assert "Override successful!" in content

    def test_override_template_in_modules_yaml(
        self, modulefile_content, module_configuration, host_architecture_str
    ):
        """Tests overriding a template from `modules.yaml`"""
        module_configuration("override_template")

        content = modulefile_content("override-module-templates")
        assert "Override even better!" in content

        content = modulefile_content(f"mpileaks target={host_architecture_str}")
        assert "Override even better!" in content

    def test_extend_context(self, modulefile_content, module_configuration):
        """Tests using a package defined context"""
        module_configuration("autoload_direct")
        content = modulefile_content("override-context-templates")

        assert 'puts stderr "sentence from package"' in content

        short_description = "module-whatis {This package updates the context for Tcl modulefiles.}"
        assert short_description in content

    @pytest.mark.regression("4400")
    @pytest.mark.db
    def test_hide_implicits_no_arg(self, module_configuration, mutable_database):
        module_configuration("exclude_implicits")

        # mpileaks has been installed explicitly when setting up
        # the tests database
        mpileaks_specs = mutable_database.query("mpileaks")
        for item in mpileaks_specs:
            writer = writer_cls.from_spec(item, "default")
            assert not writer.conf.excluded

        # callpath is a dependency of mpileaks, and has been pulled
        # in implicitly
        callpath_specs = mutable_database.query("callpath")
        for item in callpath_specs:
            writer = writer_cls.from_spec(item, "default")
            assert writer.conf.excluded

    @pytest.mark.regression("12105")
    def test_hide_implicits_with_arg(self, module_configuration):
        module_configuration("exclude_implicits")

        # mpileaks is defined as explicit with explicit argument set on writer
        mpileaks_spec = spack.concretize.concretize_one("mpileaks")
        writer = writer_cls.from_spec(mpileaks_spec, "default", True)
        assert not writer.conf.excluded

        # callpath is defined as implicit with explicit argument set on writer
        callpath_spec = spack.concretize.concretize_one("callpath")
        writer = writer_cls.from_spec(callpath_spec, "default", False)
        assert writer.conf.excluded

    @pytest.mark.regression("9624")
    def test_autoload_with_constraints(self, modulefile_content, module_configuration):
        """Tests the automatic loading of direct dependencies."""

        module_configuration("autoload_with_constraints")

        # Test the mpileaks that should have the autoloaded dependencies
        content = modulefile_content("mpileaks ^mpich2")
        # depends-on command defined once and used 3 times
        assert len([x for x in content if "depends-on " in x]) == 4

        # Test the mpileaks that should NOT have the autoloaded dependencies
        content = modulefile_content("mpileaks ^mpich")
        assert (
            len([x for x in content if "if {![info exists ::env(LMOD_VERSION_MAJOR)]} {" in x])
            == 0
        )
        assert len([x for x in content if "    proc depends-on {args} {" in x]) == 0
        assert len([x for x in content if "        module load {*}$args" in x]) == 0
        assert len([x for x in content if "depends-on " in x]) == 0

    def test_modules_no_arch(self, factory, module_configuration):
        module_configuration("no_arch")
        module, spec = factory(mpileaks_spec_string)
        path = module.layout.filename

        assert str(spec.os) not in path

    def test_hide_implicits(self, module_configuration, temporary_store):
        """Tests the addition and removal of hide command in modulerc."""
        module_configuration("hide_implicits")

        spec = spack.concretize.concretize_one("mpileaks@2.3")

        # mpileaks is defined as implicit, thus hide command should appear in modulerc
        writer = writer_cls.from_spec(spec, "default", False)
        writer.write()
        assert os.path.exists(writer.layout.modulerc)
        with open(writer.layout.modulerc, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines()]
        hide_implicit_mpileaks = f"module-hide --soft --hidden-loaded {writer.layout.use_name}"
        assert len([x for x in content if hide_implicit_mpileaks == x]) == 1

        # The direct dependencies are all implicit, and they should have depends-on with fixed
        # 7 character hash, even though the config is set to hash_length = 0.
        with open(writer.layout.filename, encoding="utf-8") as f:
            depends_statements = [line.strip() for line in f.readlines() if "depends-on" in line]
            for dep in spec.dependencies(deptype=("link", "run")):
                assert any(dep.dag_hash(7) in line for line in depends_statements)

        # when mpileaks becomes explicit, its file name changes (hash_length = 0), meaning an
        # extra module file is created; the old one still exists and remains hidden.
        writer = writer_cls.from_spec(spec, "default", True)
        writer.write()
        assert os.path.exists(writer.layout.modulerc)
        with open(writer.layout.modulerc, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines()]
        assert hide_implicit_mpileaks in content  # old, implicit mpileaks is still hidden
        assert f"module-hide --soft --hidden-loaded {writer.layout.use_name}" not in content

        # after removing both the implicit and explicit module, the modulerc file would be empty
        # and should be removed.
        writer_cls.from_spec(spec, "default", False).remove()
        writer_cls.from_spec(spec, "default", True).remove()
        assert not os.path.exists(writer.layout.modulerc)
        assert not os.path.exists(writer.layout.filename)

        # implicit module is removed
        writer = writer_cls.from_spec(spec, "default", False)
        writer.write()
        assert os.path.exists(writer.layout.filename)
        assert os.path.exists(writer.layout.modulerc)
        writer.remove()
        assert not os.path.exists(writer.layout.modulerc)
        assert not os.path.exists(writer.layout.filename)

        # three versions of mpileaks are implicit
        writer = writer_cls.from_spec(spec, "default", False)
        writer.write(overwrite=True)
        spec_alt1 = spack.concretize.concretize_one("mpileaks@2.2")
        spec_alt2 = spack.concretize.concretize_one("mpileaks@2.1")
        writer_alt1 = writer_cls.from_spec(spec_alt1, "default", False)
        writer_alt1.write(overwrite=True)
        writer_alt2 = writer_cls.from_spec(spec_alt2, "default", False)
        writer_alt2.write(overwrite=True)
        assert os.path.exists(writer.layout.modulerc)
        with open(writer.layout.modulerc, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines()]
        hide_cmd = f"module-hide --soft --hidden-loaded {writer.layout.use_name}"
        hide_cmd_alt1 = f"module-hide --soft --hidden-loaded {writer_alt1.layout.use_name}"
        hide_cmd_alt2 = f"module-hide --soft --hidden-loaded {writer_alt2.layout.use_name}"
        assert len([x for x in content if hide_cmd == x]) == 1
        assert len([x for x in content if hide_cmd_alt1 == x]) == 1
        assert len([x for x in content if hide_cmd_alt2 == x]) == 1

        # one version is removed
        writer_alt1.remove()
        assert os.path.exists(writer.layout.modulerc)
        with open(writer.layout.modulerc, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines()]
        assert len([x for x in content if hide_cmd == x]) == 1
        assert len([x for x in content if hide_cmd_alt1 == x]) == 0
        assert len([x for x in content if hide_cmd_alt2 == x]) == 1

    @pytest.mark.regression("37788")
    @pytest.mark.parametrize("modules_config", ["core_compilers", "core_compilers_at_equal"])
    def test_layout_for_specs_compiled_with_core_compilers(
        self, modules_config, module_configuration, factory
    ):
        """Tests that specs compiled with core compilers are in the 'Core' folder. Also tests that
        we can use both ``compiler@version`` and ``compiler@=version`` to specify a core compiler.
        """
        module_configuration(modules_config)
        module, spec = factory("libelf%clang@15.0.0")
        assert "Core" in module.layout.available_path_parts

    def test_file_layout(self, compiler, provider, factory, module_configuration):
        """Tests the layout of files in the hierarchy is the one expected."""
        module_configuration("complex_hierarchy")
        spec_string, services, use_compiler, place_in_core = provider

        # Non-python specs add compiler
        factory_string = spec_string
        if use_compiler:
            factory_string += "%" + compiler

        module, spec = factory(factory_string)

        layout = module.layout

        # Check that the services provided are in the hierarchy
        for s in services:
            assert s in layout.conf.hierarchy_tokens

        # Check that the compiler part of the path has no hash and that it
        # is transformed to r"Core" if the compiler is listed among core
        # compilers
        # Check that specs listed as core_specs are transformed to "Core"
        # Check that specs with no hierarchy components are transformed to "Core"
        if "clang@=15.0.0" in factory_string or place_in_core:
            assert "Core" in layout.available_path_parts
        else:
            assert compiler.replace("@=", "/") in layout.available_path_parts

        # Check that the provider part instead has always an hash even if
        # hash has been disallowed in the configuration file
        path_parts = layout.available_path_parts
        service_part = spec_string.replace("@", "/")
        service_part = "-".join([service_part, layout.spec.dag_hash(length=7)])

        if "mpi" in spec:
            # It's a user, not a provider, so create the provider string
            service_part = layout.spec["mpi"].format("{name}/{version}-{hash:7}")
        elif "python" in spec:
            # It's a user, not a provider, so create the provider string
            service_part = layout.spec["python"].format("{name}/{version}-{hash:7}")
        else:
            # Only relevant for providers, not users, of virtuals
            assert service_part in path_parts

        # Check that multi-providers have repetitions in path parts
        repetitions = len([x for x in path_parts if service_part == x])
        if spec_string == "openblas-with-lapack@0.2.15":
            assert repetitions == 2
        elif spec_string == "mpileaks@2.1":
            assert repetitions == 0
        else:
            assert repetitions == 1

    def test_compilers_provided_different_name(
        self, factory, module_configuration, compiler_factory, mutable_config: Configuration
    ):
        with mutable_config.override(
            "packages", {"llvm": {"externals": [compiler_factory(spec="llvm@3.3 +clang")]}}
        ):
            module_configuration("complex_hierarchy")
            module, spec = factory("intel-oneapi-compilers%clang@3.3")

            provides = module.conf.provides

            assert "compiler" in provides
            assert provides["compiler"] == spack.spec.Spec("intel-oneapi-compilers@=3.0")

    @pytest.mark.parametrize("language", ["c", "cxx", "fortran"])
    def test_compiler_language_virtuals(self, factory, module_configuration, language):
        """Tests all compiler virtuals for hierarchical module placement."""
        module_configuration("complex_hierarchy")
        module, spec = factory(f"single-language-virtual +{language} %{language}=gcc@=10.2.1")

        requires = module.conf.requires

        assert "gcc@=10.2.1" in requires["compiler"]

    def test_no_hash(self, factory, module_configuration):
        """Makes sure that virtual providers (in the hierarchy) always
        include a hash. Make sure that the module file for the spec
        does not include a hash if hash_length is 0.
        """

        module_configuration("no_hash")
        module, spec = factory(mpileaks_spec_string)
        path = module.layout.filename
        mpi_spec = spec["mpi"]

        mpi_element = "{0}/{1}-{2}/".format(
            mpi_spec.name, mpi_spec.version, mpi_spec.dag_hash(length=7)
        )

        assert mpi_element in path

        mpileaks_spec = spec
        mpileaks_element = "{0}/{1}".format(mpileaks_spec.name, mpileaks_spec.version)

        assert path.endswith(mpileaks_element)

    def test_no_core_compilers(self, factory, module_configuration):
        """Ensures that missing 'core_compilers' in the configuration file
        raises the right exception.
        """

        # In this case we miss the entry completely
        module_configuration("missing_core_compilers")

        module, spec = factory(mpileaks_spec_string)
        with pytest.raises(spack.modules.error.CoreCompilersNotFoundError):
            module.write()

        # Here we have an empty list
        module_configuration("core_compilers_empty")

        module, spec = factory(mpileaks_spec_string)
        with pytest.raises(spack.modules.error.CoreCompilersNotFoundError):
            module.write()

    def test_guess_core_compilers(self, factory, module_configuration, monkeypatch):
        """Check that we can guess core compilers."""

        # In this case we miss the entry completely
        module_configuration("missing_core_compilers")

        # Our mock paths must be detected as system paths
        monkeypatch.setattr(spack.util.environment, "SYSTEM_DIRS", ["/path/bin"])

        # We don't want to really write into user configuration
        # when running tests
        def no_op_set(*args, **kwargs):
            pass

        monkeypatch.setattr(spack.config.Configuration, "set", no_op_set)

        # Assert we have core compilers now
        writer, _ = factory(mpileaks_spec_string)
        assert writer.conf.core_compilers

    @pytest.mark.parametrize(
        "spec_str", ["mpileaks target=nocona", "mpileaks target=core2", "mpileaks target=x86_64"]
    )
    @pytest.mark.regression("13005")
    def test_only_generic_microarchitectures_in_root(
        self, spec_str, factory, module_configuration
    ):
        module_configuration("complex_hierarchy")
        writer, spec = factory(spec_str)

        assert str(spec.target.family) in writer.layout.arch_dirname
        if spec.target.family != spec.target:
            assert str(spec.target) not in writer.layout.arch_dirname

    def test_projections_specific_hierarchical(self, factory, module_configuration):
        """Tests reading the correct naming scheme in hierarchical mode."""

        # This configuration has no error, so check the conflicts directives
        # are there
        module_configuration("projections_hierarchical")

        # Test we read the expected configuration for the naming scheme
        writer, _ = factory("mpileaks")
        expected = {"all": "{name}/v{version}", "mpileaks": "{name}-mpiprojection"}

        assert writer.conf.projections == expected
        projection = writer.spec.format(writer.conf.projections["mpileaks"])
        assert projection in writer.layout.use_name

    def test_projections_all_hierarchical(self, factory, module_configuration):
        """Tests reading the correct naming scheme in hierarchical mode."""

        # This configuration has no error, so check the conflicts directives
        # are there
        module_configuration("projections_hierarchical")

        # Test we read the expected configuration for the naming scheme
        writer, _ = factory("libelf")
        expected = {"all": "{name}/v{version}", "mpileaks": "{name}-mpiprojection"}

        assert writer.conf.projections == expected
        projection = writer.spec.format(writer.conf.projections["all"])
        assert projection in writer.layout.use_name

    def test_hierarchical_conditional_modulepath_tcl_syntax(
        self, modulefile_content, module_configuration
    ):
        """Tests that conditional MODULEPATH lines use Tcl variable syntax ($var)."""
        module_configuration("complex_hierarchy")
        # mpich provides mpi; compiled with gcc (non-core), so lapack/blas/python are missing.
        # This produces conditional 'file join' lines that exercise manipulate_path.
        content = modulefile_content("mpich@3.0.4 %gcc@=10.2.1")

        file_join_lines = [line for line in content if "file join" in line]
        assert file_join_lines

        # Each line that mentions a missing token must use ${token_name} ${token_version}
        for line in file_join_lines:
            if "lapack" in line:
                assert "${lapack_name} ${lapack_version}" in line, (
                    f"Expected Tcl syntax '${{lapack_name}} ${{lapack_version}}' but got: {line!r}"
                )

    @pytest.mark.regression("7487")
    def test_suffix_does_not_propagate_to_dependents(self, factory, module_configuration):
        """A bare package-name suffix key matches only the root spec, while a '^name'
        key matches specs that depend on that package. The two must not overlap.
        """
        module_configuration("suffix_propagation")

        # mpileaks depends on mpich but is not mpich, so only the '^mpich' key applies
        writer, _ = factory("mpileaks ^mpich@3.0.4")
        assert "depmatch" in writer.layout.use_name
        assert "namematch" not in writer.layout.use_name

        # mpich itself is matched only by the bare 'mpich' key
        writer, _ = factory("mpich@3.0.4")
        assert "namematch" in writer.layout.use_name
        assert "depmatch" not in writer.layout.use_name

    def test_variants_none(self, modulefile_content, module_configuration):
        """Tests variant definitions when variants mode is disabled."""

        # module variants implicitly disabled
        module_configuration("autoload_direct")

        # test module file of package without variants
        content = modulefile_content("module-long-help target=core2")
        assert len([x for x in content if "variant " in x]) == 0

        # test module file of package with variants
        content = modulefile_content("mpileaks +debug -shared")
        assert len([x for x in content if "variant " in x]) == 0

        # module variants explicitly disabled
        module_configuration("variants_none")

        # test module file of package without variants
        content = modulefile_content("module-long-help target=core2")
        assert len([x for x in content if "variant " in x]) == 0

        # test module file of package with variants
        content = modulefile_content("mpileaks +debug -shared")
        assert len([x for x in content if "variant " in x]) == 0

        # test dependent module designation (no variant specifications)
        # depends-on command defined once and used 3 times
        assert len([x for x in content if "depends-on " in x]) == 4
        assert (
            len(
                [
                    x
                    for x in content
                    if re.match(
                        "depends-on callpath/1.0-gcc-10.2.1-\\w{7} build_system=generic", x
                    )
                ]
            )
            == 0
        )
        assert (
            len(
                [
                    x
                    for x in content
                    if re.match(
                        "depends-on mpich/3.0.4-gcc-10.2.1-\\w{7} build_system=generic ~debug", x
                    )
                ]
            )
            == 0
        )
        assert (
            len(
                [
                    x
                    for x in content
                    if re.match(
                        "depends-on gcc-runtime/10.2.1-none-none-\\w{7} build_system=generic", x
                    )
                ]
            )
            == 0
        )

    def test_variants_all(self, modulefile_content, module_configuration):
        """Tests variant definitions when variants mode is ``"all"``."""

        # module variants enabled
        module_configuration("variants_all")

        # test module file of package without variants
        content = modulefile_content("module-long-help target=core2")
        # Spack automatically defines a build_system variant
        assert len([x for x in content if "variant " in x]) == 2
        assert len([x for x in content if "getvariant " in x]) == 1

        # test module file of package with boolean variants
        content = modulefile_content("mpileaks +debug -shared")
        assert len([x for x in content if "variant " in x]) == 7
        assert len([x for x in content if "getvariant " in x]) == 1
        assert len([x for x in content if "variant --boolean --default True debug" in x]) == 1
        assert len([x for x in content if "variant --boolean --default False opt" in x]) == 1
        assert len([x for x in content if "variant --boolean --default False shared" in x]) == 1
        assert len([x for x in content if "variant --boolean --default True static" in x]) == 1
        assert len([x for x in content if "variant --boolean --default False fortran" in x]) == 1
        assert (
            len([x for x in content if "variant --default generic build_system generic" in x]) == 1
        )

        # test variant set module check code
        assert (
            len(
                [
                    x
                    for x in content
                    if "    {build_system=generic +debug ~fortran ~opt ~shared +static} " in x
                ]
            )
            == 1
        )
        assert (
            len(
                [
                    x
                    for x in content
                    if "foreach avail_spec [array names ::avail_installation] {" in x
                ]
            )
            == 1
        )
        assert len([x for x in content if 'append err_msg "* \\"$avail_spec\\"\\n' in x]) == 1
        assert len([x for x in content if "reportError $err_msg" in x]) == 1

        # test dependent module designation (containing variants specifications)
        # depends-on command defined once and used 3 times
        assert len([x for x in content if "depends-on " in x]) == 4
        assert (
            len(
                [
                    x
                    for x in content
                    if re.match(
                        "    depends-on callpath/1.0-gcc-10.2.1-\\w{7} build_system=generic", x
                    )
                ]
            )
            == 1
        )
        assert (
            len(
                [
                    x
                    for x in content
                    if re.match(
                        "    depends-on mpich/3.0.4-gcc-10.2.1-\\w{7} build_system=generic ~debug",
                        x,
                    )
                ]
            )
            == 1
        )
        assert (
            len(
                [
                    x
                    for x in content
                    if re.match(
                        "    depends-on gcc-runtime/10.2.1-none-none-\\w{7} build_system=generic",
                        x,
                    )
                ]
            )
            == 1
        )

        # test module file of package with valued variants
        content = modulefile_content("multivalue-variant-multi-defaults myvariant=bar")
        assert len([x for x in content if "variant " in x]) == 4
        assert len([x for x in content if "getvariant " in x]) == 1
        assert len([x for x in content if "variant_set_spec myvariant 0" in x]) == 1
        assert len([x for x in content if "variant --default bar myvariant bar" in x]) == 1
        assert (
            len([x for x in content if "variant --default generic build_system generic" in x]) == 1
        )
        assert len([x for x in content if "variant --boolean " in x]) == 0

        # test variant set module check code
        assert len([x for x in content if "    {build_system=generic myvariant=bar} " in x]) == 1
        assert (
            len(
                [
                    x
                    for x in content
                    if "foreach avail_spec [array names ::avail_installation] {" in x
                ]
            )
            == 1
        )
        assert len([x for x in content if 'append err_msg "* \\"$avail_spec\\"\\n' in x]) == 1
        assert len([x for x in content if "reportError $err_msg" in x]) == 1

        # test module file of package with multi-valued variants
        content = modulefile_content("multivalue-variant-multi-defaults")
        assert len([x for x in content if "variant " in x]) == 4
        assert len([x for x in content if "getvariant " in x]) == 1
        assert len([x for x in content if "variant_set_spec myvariant 0" in x]) == 1
        assert len([x for x in content if "variant --default bar_baz myvariant bar_baz" in x]) == 1
        assert (
            len([x for x in content if "variant --default generic build_system generic" in x]) == 1
        )
        content = modulefile_content("multivalue-variant-multi-defaults myvariant=baz,bar")
        assert len([x for x in content if "variant --default bar_baz myvariant bar_baz" in x]) == 1

    def test_exclude_variants(self, modulefile_content, module_configuration):
        """Tests excluding variant definitions in module file."""

        # default exclude list for "all" and specific list for some packages
        module_configuration("exclude_variants")
        content = modulefile_content("mpileaks +debug -shared")

        # test variant definition
        assert len([x for x in content if "variant " in x]) == 5
        assert len([x for x in content if "getvariant " in x]) == 1
        assert len([x for x in content if "variant --boolean --default True debug" in x]) == 0
        assert len([x for x in content if "variant --boolean --default False opt" in x]) == 1
        assert len([x for x in content if "variant --boolean --default False shared" in x]) == 1
        assert len([x for x in content if "variant --boolean --default True static" in x]) == 1
        assert len([x for x in content if "variant --boolean --default False fortran" in x]) == 0
        assert (
            len([x for x in content if "variant --default generic build_system generic" in x]) == 1
        )

        # test variant set module check code
        assert (
            len([x for x in content if "    {build_system=generic ~opt ~shared +static} " in x])
            == 1
        )

        # test dependent module designation (containing variants specifications)
        assert (
            len(
                [
                    x
                    for x in content
                    if re.match(
                        "    depends-on mpich/3.0.4-gcc-10.2.1-\\w{7} build_system=generic", x
                    )
                ]
            )
            == 1
        )

        # test cascading specific definition between "all" and some packages
        module_configuration("exclude_variants_cascading")
        content = modulefile_content("mpileaks +debug -shared")

        # test variant definition
        assert len([x for x in content if "variant " in x]) == 4
        assert len([x for x in content if "getvariant " in x]) == 1
        assert len([x for x in content if "variant --boolean --default True debug" in x]) == 0
        assert len([x for x in content if "variant --boolean --default False opt" in x]) == 1
        assert len([x for x in content if "variant --boolean --default False shared" in x]) == 0
        assert len([x for x in content if "variant --boolean --default True static" in x]) == 1
        assert len([x for x in content if "variant --boolean --default False fortran" in x]) == 0
        assert (
            len([x for x in content if "variant --default generic build_system generic" in x]) == 1
        )

        # test variant set module check code
        assert len([x for x in content if "    {build_system=generic ~opt +static} " in x]) == 1

        # test dependent module designation (containing variants specifications)
        assert (
            len(
                [
                    x
                    for x in content
                    if re.match(
                        "    depends-on mpich/3.0.4-gcc-10.2.1-\\w{7} build_system=generic", x
                    )
                ]
            )
            == 1
        )

    def test_fold_variants(self, install_mockery, module_configuration, modulefile_filenames):
        """Test generating and removing installations folded in same module file."""
        module_configuration("fold_variants_all")
        spec_o = "mpileaks@2.3 ~debug %clang@=15.0.0"
        spec_a = "mpileaks@2.3 ~debug ^zmpi"
        spec_b = "mpileaks@2.3 +debug ^zmpi"

        install("--fake", "--add", spec_o)
        module_file_o = modulefile_filenames("tcl", spec_o)[0]
        with open(module_file_o, encoding="utf-8") as f:
            content_o = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        # single installation for dependency, no hash variant defined
        assert (
            len(
                [
                    x
                    for x in content_o
                    if "depends-on callpath/1.0-gcc-10.2.1 build_system=generic" in x
                ]
            )
            == 1
        )

        # install 2 packages folded in same module file
        install("--fake", "--add", spec_a)
        module_file_a = modulefile_filenames("tcl", spec_a)[0]
        with open(module_file_a, encoding="utf-8") as f:
            content_a = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        install("--fake", "--add", spec_b)
        module_file_b = modulefile_filenames("tcl", spec_b)[0]
        with open(module_file_b, encoding="utf-8") as f:
            content_b = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert module_file_a == module_file_b and content_a != content_b

        # check module file content is coherent with folded installations
        assert len([x for x in content_a if "if {$selected_installation eq {" in x]) == 1
        assert len([x for x in content_a if "depends-on " in x]) == 4
        assert len([x for x in content_a if "prepend-path -d {:} PATH " in x]) == 1
        assert len([x for x in content_a if "setenv FOOBAR " in x]) == 1
        assert len([x for x in content_b if "if {$selected_installation eq {" in x]) == 2
        assert len([x for x in content_b if "depends-on " in x]) == 7
        # check alternative installation for dependency express its hash variant to disambiguate
        assert (
            len(
                [
                    x
                    for x in content_a
                    if re.match(
                        "depends-on callpath/1.0-gcc-10.2.1 build_system=generic hash=\\w{7}", x
                    )
                ]
            )
            == 1
        )
        assert (
            len(
                [
                    x
                    for x in content_b
                    if re.match(
                        "depends-on callpath/1.0-gcc-10.2.1 build_system=generic hash=\\w{7}", x
                    )
                ]
            )
            == 2
        )
        assert len([x for x in content_b if "prepend-path -d {:} PATH " in x]) == 2
        assert len([x for x in content_b if "setenv FOOBAR " in x]) == 2

        # check update of other installed package: still no hash variant defined for dependency
        with open(module_file_o, encoding="utf-8") as f:
            content_o = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert (
            len(
                [
                    x
                    for x in content_o
                    if "depends-on callpath/1.0-gcc-10.2.1 build_system=generic" in x
                ]
            )
            == 1
        )

        # uninstall one package, module file should persist with remaining installation
        uninstall("-y", spec_b)
        with open(module_file_a, encoding="utf-8") as f:
            content_c = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert content_a == content_c

        # uninstall second package, module file should be removed
        # but the other module file should stay
        uninstall("-y", spec_a)
        assert not os.path.exists(module_file_a) and os.path.exists(module_file_o)

        # test default value is set only for variants with a single value
        spec_a = "manyvariants@1.0.1"
        spec_b = "manyvariants@1.0.1 ~a c=v2"
        install("--fake", "--add", spec_a)
        install("--fake", "--add", spec_b)
        module_file_a = modulefile_filenames("tcl", spec_a)[0]
        with open(module_file_a, encoding="utf-8") as f:
            content_a = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content_a if "{+a ~b build_system=generic c=v1 d=v1} " in x]) == 1
        assert len([x for x in content_a if "{~a ~b build_system=generic c=v2 d=v1} " in x]) == 1
        assert len([x for x in content_a if "variant --boolean a" in x]) == 1
        assert len([x for x in content_a if "variant --boolean --default False b" in x]) == 1
        assert len([x for x in content_a if "variant c v2 v1" in x or "variant c v1 v2" in x]) == 1
        assert len([x for x in content_a if "variant --default v1 d v1" in x]) == 1

        # test valued conditional variant
        spec_a = "forward-multi-value@1.0"
        install("--fake", "--add", spec_a)
        module_file_a = modulefile_filenames("tcl", spec_a)[0]
        with open(module_file_a, encoding="utf-8") as f:
            content_a = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content_a if "variant --boolean --default False cuda" in x]) == 1
        assert len([x for x in content_a if "cuda_arch" in x]) == 0
        spec_b = "forward-multi-value@1.0 +cuda"
        install("--fake", "--add", spec_b)
        with open(module_file_a, encoding="utf-8") as f:
            content_b = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content_b if "variant --boolean cuda" in x]) == 1
        assert len([x for x in content_b if "variant --default none cuda_arch none" in x]) == 1
        spec_c = "forward-multi-value@1.0 +cuda cuda_arch=11"
        install("--fake", "--add", spec_c)
        with open(module_file_a, encoding="utf-8") as f:
            content_c = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content_c if "variant --boolean cuda" in x]) == 1
        assert (
            len(
                [
                    x
                    for x in content_c
                    if "variant --default none cuda_arch none 11" in x
                    or "variant --default none cuda_arch 11 none" in x
                ]
            )
            == 1
        )

        # test boolean conditional variant
        spec_a = "conditional-variant-pkg@2.0"
        install("--fake", "--add", spec_a)
        module_file_a = modulefile_filenames("tcl", spec_a)[0]
        with open(module_file_a, encoding="utf-8") as f:
            content_a = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert (
            len([x for x in content_a if "variant --boolean --default True version_based" in x])
            == 1
        )
        assert (
            len([x for x in content_a if "variant --boolean --default False variant_based" in x])
            == 1
        )
        assert len([x for x in content_a if "two_whens" in x]) == 0
        spec_b = "conditional-variant-pkg@2.0 ~version_based"
        install("--fake", "--add", spec_b)
        with open(module_file_a, encoding="utf-8") as f:
            content_b = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content_b if "variant --boolean version_based" in x]) == 1
        assert (
            len([x for x in content_b if "variant --boolean --default False variant_based" in x])
            == 1
        )
        assert len([x for x in content_b if "two_whens" in x]) == 0
        spec_c = "conditional-variant-pkg@2.0 +version_based +variant_based"
        install("--fake", "--add", spec_c)
        with open(module_file_a, encoding="utf-8") as f:
            content_c = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content_c if "variant --boolean version_based" in x]) == 1
        assert (
            len([x for x in content_c if "variant --boolean --default False variant_based" in x])
            == 1
        )
        assert (
            len([x for x in content_c if "variant --boolean --default False two_whens" in x]) == 1
        )

        # test conditional variant on dependency
        spec_a = "conditional-variant-pkg-dependent@1.0 a=v1"
        spec_b = "conditional-variant-pkg-dependent@1.0 a=v2"
        spec_c = "conditional-variant-pkg-dependent@1.0 a=v3"
        install("--fake", "--add", spec_a)
        install("--fake", "--add", spec_b)
        install("--fake", "--add", spec_c)
        module_file = modulefile_filenames("tcl", spec_a)[0]
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert (
            len(
                [
                    x
                    for x in content
                    if (
                        "depends-on conditional-variant-pkg/2.0-none-none "
                        "build_system=generic ~version_based"
                    )
                    in x
                ]
            )
            == 1
        )
        assert (
            len(
                [
                    x
                    for x in content
                    if (
                        "depends-on conditional-variant-pkg/2.0-none-none "
                        "build_system=generic +variant_based +version_based"
                    )
                    in x
                ]
            )
            == 1
        )
        assert (
            len(
                [
                    x
                    for x in content
                    if (
                        "depends-on conditional-variant-pkg/2.0-none-none "
                        "build_system=generic +two_whens +variant_based +version_based"
                    )
                    in x
                ]
            )
            == 1
        )

        # check module is considered explicit as soon as one install is explicit
        module_configuration("fold_variants_hide_implicits")
        spec_a = "manyvariants@1.0.0 +a ~b"
        install("--fake", "--add", spec_a)
        mark("--implicit", spec_a)
        writer = writer_cls.from_spec(spack.concretize.concretize_one(spec_a), "default", False)
        writer.write(overwrite=True)
        assert os.path.exists(writer.layout.modulerc)
        with open(writer.layout.modulerc, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines()]
        hide_implicit_rule = f"module-hide --soft --hidden-loaded {writer.layout.name}"
        assert len([x for x in content if hide_implicit_rule == x]) == 1

        spec_b = "manyvariants@1.0.0 +a +b"
        writer = writer_cls.from_spec(spack.concretize.concretize_one(spec_b), "default", False)
        writer.write()
        assert os.path.exists(writer.layout.modulerc)
        with open(writer.layout.modulerc, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines()]
        hide_implicit_rule = f"module-hide --soft --hidden-loaded {writer.layout.name}"
        assert len([x for x in content if hide_implicit_rule == x]) == 1

        spec_c = "manyvariants@1.0.0 ~a ~b"
        writer = writer_cls.from_spec(spack.concretize.concretize_one(spec_c), "default", True)
        writer.write()
        assert not os.path.exists(writer.layout.modulerc)

        install("--fake", "--add", spec_c)
        uninstall("-y", spec_c)
        assert os.path.exists(writer.layout.modulerc)
        with open(writer.layout.modulerc, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines()]
        hide_implicit_rule = f"module-hide --soft --hidden-loaded {writer.layout.name}"
        assert len([x for x in content if hide_implicit_rule == x]) == 1

        # check hash variant is added for 2 similar folded installations among 3
        spec_a = "mpileaks@2.3 +debug +opt ^mpich"
        spec_b = "mpileaks@2.3 +opt +debug ^zmpi"
        spec_c = "mpileaks@2.3 ~opt +debug ^zmpi"
        install("--fake", "--add", spec_a)
        install("--fake", "--add", spec_b)
        install("--fake", "--add", spec_c)
        module_file = modulefile_filenames("tcl", spec_a)[0]
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert (
            len(
                [
                    x
                    for x in content
                    if re.match(
                        "\\{build_system=generic \\+debug ~fortran hash=\\w{7} "
                        "\\+opt \\+shared \\+static\\}",
                        x,
                    )
                ]
            )
            == 2
        )
        assert (
            len(
                [
                    x
                    for x in content
                    if "{build_system=generic +debug ~fortran ~opt +shared +static}" in x
                ]
            )
            == 1
        )
        assert (
            len(
                [
                    x
                    for x in content
                    if re.match(
                        "variant --default none hash (\\w{7}|none) (\\w{7}|none) (\\w{7}|none)", x
                    )
                ]
            )
            == 1
        )

        # check hash variant is added for 2 similar folded installations due to excluded variants
        module_configuration("fold_variants_exclude_variants")
        spec_a = "mpileaks@2.2 ~debug"
        spec_b = "mpileaks@2.2 +debug"
        install("--fake", "--add", spec_a)
        install("--fake", "--add", spec_b)
        module_file = modulefile_filenames("tcl", spec_a)[0]
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert (
            len(
                [
                    x
                    for x in content
                    if re.match(
                        "\\{build_system=generic hash=\\w{7} ~opt \\+shared \\+static\\}", x
                    )
                ]
            )
            == 2
        )
        assert len([x for x in content if re.match("variant hash \\w{7} \\w{7}", x)]) == 1

    def test_variants_varying(self, modulefile_content, module_configuration):
        """Tests variant definitions when variants mode is ``"varying"``."""

        # module variants enabled
        module_configuration("variants_varying")

        # test module file of package without variants
        content = modulefile_content("module-long-help target=core2")
        # Spack automatically defines a build_system variant
        assert len([x for x in content if "variant " in x]) == 0
        assert len([x for x in content if "getvariant " in x]) == 0

        # test module file of package with boolean variants
        content = modulefile_content("mpileaks +debug -shared")
        assert len([x for x in content if "variant " in x]) == 0
        assert len([x for x in content if "getvariant " in x]) == 0

        # test variant set module check code
        assert (
            len(
                [
                    x
                    for x in content
                    if "    {build_system=generic +debug ~fortran ~opt ~shared +static} " in x
                ]
            )
            == 0
        )
        assert (
            len(
                [
                    x
                    for x in content
                    if "foreach avail_spec [array names ::avail_installation] {" in x
                ]
            )
            == 0
        )
        assert len([x for x in content if 'append err_msg "* \\"$avail_spec\\"\\n' in x]) == 0
        assert len([x for x in content if "reportError $err_msg" in x]) == 0

        # test dependent module designation (containing variants specifications)
        # depends-on command defined once and used 3 times
        assert len([x for x in content if "depends-on " in x]) == 4
        assert (
            len(
                [
                    x
                    for x in content
                    if re.match("    depends-on callpath/1.0-gcc-10.2.1-\\w{7}", x)
                ]
            )
            == 1
        )
        assert (
            len(
                [x for x in content if re.match("    depends-on mpich/3.0.4-gcc-10.2.1-\\w{7}", x)]
            )
            == 1
        )
        assert (
            len(
                [
                    x
                    for x in content
                    if re.match("    depends-on gcc-runtime/10.2.1-none-none-\\w{7}", x)
                ]
            )
            == 1
        )

    def test_fold_variants_varying(
        self, install_mockery, module_configuration, modulefile_filenames
    ):
        """Test installations folded in same module file when variants mode is ``"varying"``."""
        module_configuration("fold_variants_varying")
        spec_a = "mpileaks@2.3 ~debug ^zmpi"
        spec_b = "mpileaks@2.3 +debug ^zmpi"

        # install 2 packages folded in same module file, only varying variant should be defined
        install("--fake", "--add", spec_a)
        module_file_a = modulefile_filenames("tcl", spec_a)[0]
        with open(module_file_a, encoding="utf-8") as f:
            content_a = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        install("--fake", "--add", spec_b)
        module_file_b = modulefile_filenames("tcl", spec_b)[0]
        with open(module_file_b, encoding="utf-8") as f:
            content_b = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert module_file_a == module_file_b and content_a != content_b
        assert len([x for x in content_a if "variant " in x]) == 0
        assert len([x for x in content_a if "getvariant " in x]) == 0
        assert len([x for x in content_b if "variant " in x]) == 2
        assert len([x for x in content_b if "getvariant " in x]) == 1
        assert len([x for x in content_b if "variant --boolean debug" in x]) == 1

        # uninstall one package, no more variant definition
        uninstall("-y", spec_b)
        with open(module_file_b, encoding="utf-8") as f:
            content_c = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert content_a == content_c

        # test varying with valued conditional variant
        spec_a = "forward-multi-value@1.0"
        install("--fake", "--add", spec_a)
        module_file_a = modulefile_filenames("tcl", spec_a)[0]
        with open(module_file_a, encoding="utf-8") as f:
            content_a = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content_a if "variant --boolean" in x]) == 0
        spec_b = "forward-multi-value@1.0 +cuda"
        install("--fake", "--add", spec_b)
        with open(module_file_a, encoding="utf-8") as f:
            content_b = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content_b if "variant --boolean cuda" in x]) == 1
        assert len([x for x in content_b if "variant --default none cuda_arch none" in x]) == 0
        spec_c = "forward-multi-value@1.0 +cuda cuda_arch=11"
        install("--fake", "--add", spec_c)
        with open(module_file_a, encoding="utf-8") as f:
            content_c = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content_c if "variant --boolean cuda" in x]) == 1
        assert (
            len(
                [
                    x
                    for x in content_c
                    if "variant --default none cuda_arch none 11" in x
                    or "variant --default none cuda_arch 11 none" in x
                ]
            )
            == 1
        )

        # test varying on conditional variant dependency
        spec_a = "conditional-variant-pkg-dependent@1.0 a=v1"
        spec_b = "conditional-variant-pkg-dependent@1.0 a=v2"
        spec_c = "conditional-variant-pkg-dependent@1.0 a=v3"
        install("--fake", "--add", spec_a)
        install("--fake", "--add", spec_b)
        install("--fake", "--add", spec_c)
        module_file = modulefile_filenames("tcl", spec_a)[0]
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert (
            len(
                [
                    x
                    for x in content
                    if "depends-on conditional-variant-pkg/2.0-none-none ~version_based" in x
                ]
            )
            == 1
        )
        assert (
            len(
                [
                    x
                    for x in content
                    if (
                        "depends-on conditional-variant-pkg/2.0-none-none "
                        "+variant_based +version_based"
                    )
                    in x
                ]
            )
            == 1
        )
        assert (
            len(
                [
                    x
                    for x in content
                    if (
                        "depends-on conditional-variant-pkg/2.0-none-none "
                        "+two_whens +variant_based +version_based"
                    )
                    in x
                ]
            )
            == 1
        )

        # dependency has a variant defined, but not anymore after deletion of one package
        # check how dependency is loaded
        uninstall("-y", spec_c)
        uninstall("-y", spec_b)
        uninstall("-y", "conditional-variant-pkg@2.0 +two_whens +variant_based +version_based")
        uninstall("-y", "conditional-variant-pkg@2.0 +variant_based +version_based")
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        # variant still expressed on dependency load statement
        assert (
            len(
                [
                    x
                    for x in content
                    if "depends-on conditional-variant-pkg/2.0-none-none ~version_based" in x
                ]
            )
            == 1
        )
        module_file_dep = modulefile_filenames("tcl", "conditional-variant-pkg@2.0")[0]
        with open(module_file_dep, encoding="utf-8") as f:
            content_dep = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        # however variant not defined anymore in module
        assert len([x for x in content_dep if "variant --boolean" in x]) == 0

        # check two folded installations which only differs from their hash
        spec_a = "mpileaks@2.2 +debug +opt ^mpich"
        spec_b = "mpileaks@2.2 +opt +debug ^zmpi"
        install("--fake", "--add", spec_a)
        install("--fake", "--add", spec_b)
        module_file = modulefile_filenames("tcl", spec_a)[0]
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content if "variant " in x]) == 2
        assert len([x for x in content if "variant hash " in x]) == 1

    def test_variant_defaults_none(self, modulefile_content, module_configuration):
        """Tests variant defaults when variants mode is ``"none"``."""
        module_configuration("variant_defaults_none")

        content = modulefile_content("mpileaks@2.3")
        assert content and len([x for x in content if "variant " in x]) == 0
        content = modulefile_content("mpileaks@2.3 +debug ~shared +opt ~fortran")
        assert content and len([x for x in content if "variant " in x]) == 0
        content = modulefile_content("mpileaks@2.3 ~debug +shared ~opt +fortran")
        assert content and len([x for x in content if "variant " in x]) == 0

        content = modulefile_content("mpileaks@2.2")
        assert content and len([x for x in content if "variant " in x]) == 0
        content = modulefile_content("mpileaks@2.2 ~fortran")
        assert content and len([x for x in content if "variant " in x]) == 0
        content = modulefile_content("mpileaks@2.2 +fortran")
        assert content and len([x for x in content if "variant " in x]) == 0

        content = modulefile_content("mpich@3.0.4")
        assert content and len([x for x in content if "variant " in x]) == 0
        content = modulefile_content("mpich@3.0.4 +debug")
        assert content and len([x for x in content if "variant " in x]) == 0

        content = modulefile_content("manyvariants@1.0.1")
        assert content and len([x for x in content if "variant " in x]) == 0
        content = modulefile_content("manyvariants@1.0.1 ~a +b c=v2 d=v3")
        assert content and len([x for x in content if "variant " in x]) == 0

    def test_variant_defaults_all(
        self, install_mockery, module_configuration, modulefile_filenames
    ):
        """Tests variant defaults when installations are folded and variants mode is ``"all"``."""
        module_configuration("variant_defaults_all")

        spec_a = "mpileaks@2.3"
        spec_b = "mpileaks@2.3 +debug ~shared +opt ~fortran"
        spec_c = "mpileaks@2.3 ~debug +shared ~opt +fortran"
        install("--fake", "--add", spec_a)
        module_file = modulefile_filenames("tcl", spec_a)[0]
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content if "variant --boolean --default False debug" in x]) == 1
        assert len([x for x in content if "variant --boolean --default False fortran" in x]) == 1
        assert len([x for x in content if "variant --boolean --default True shared" in x]) == 1
        assert len([x for x in content if "variant --boolean --default False opt" in x]) == 1
        assert len([x for x in content if "variant --boolean --default True static" in x]) == 1
        install("--fake", "--add", spec_b)
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content if "variant --boolean --default False debug" in x]) == 1
        assert len([x for x in content if "variant --boolean --default False shared" in x]) == 1
        assert len([x for x in content if "variant --boolean opt" in x]) == 1
        assert len([x for x in content if "variant --boolean --default False fortran" in x]) == 1
        assert len([x for x in content if "variant --boolean --default True static" in x]) == 1
        install("--fake", "--add", spec_c)
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content if "variant --boolean --default False debug" in x]) == 1
        assert len([x for x in content if "variant --boolean --default False shared" in x]) == 1
        assert len([x for x in content if "variant --boolean opt" in x]) == 1
        assert len([x for x in content if "variant --boolean --default True fortran" in x]) == 1
        assert len([x for x in content if "variant --boolean --default True static" in x]) == 1
        uninstall("-y", spec_c)
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content if "variant --boolean --default False debug" in x]) == 1
        assert len([x for x in content if "variant --boolean --default False shared" in x]) == 1
        assert len([x for x in content if "variant --boolean opt" in x]) == 1
        assert len([x for x in content if "variant --boolean --default False fortran" in x]) == 1
        assert len([x for x in content if "variant --boolean --default True static" in x]) == 1

        spec_a = "mpileaks@2.2"
        spec_b = "mpileaks@2.2 +fortran"
        install("--fake", "--add", spec_a)
        module_file = modulefile_filenames("tcl", spec_a)[0]
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content if "variant --boolean --default False fortran" in x]) == 1
        install("--fake", "--add", spec_b)
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content if "variant --boolean --default False fortran" in x]) == 1

        spec_a = "mpich@3.0.4"
        spec_b = "mpich@3.0.4 +debug"
        install("--fake", "--add", spec_a)
        module_file = modulefile_filenames("tcl", spec_a)[0]
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content if "variant --boolean --default False debug" in x]) == 1
        install("--fake", "--add", spec_b)
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content if "variant --boolean debug" in x]) == 1

        spec_a = "manyvariants@1.0.1"
        spec_b = "manyvariants@1.0.1 ~a +b c=v2 d=v3"
        install("--fake", "--add", spec_a)
        module_file = modulefile_filenames("tcl", spec_a)[0]
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content if "variant --boolean --default True a" in x]) == 1
        assert len([x for x in content if "variant --boolean --default False b" in x]) == 1
        assert len([x for x in content if "variant --default v1 c v1" in x]) == 1
        assert len([x for x in content if "variant --default v1 d v1" in x]) == 1
        install("--fake", "--add", spec_b)
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content if "variant --boolean --default True a" in x]) == 1
        assert len([x for x in content if "variant --boolean --default False b" in x]) == 1
        assert (
            len(
                [
                    x
                    for x in content
                    if "variant --default v1 c v1 v2" in x or "variant --default v1 c v2 v1" in x
                ]
            )
            == 1
        )
        assert len([x for x in content if "variant d v1 v3" in x or "variant d v3 v1" in x]) == 1

        spec_a = "conditional-variant-pkg@1.0"
        spec_b = "conditional-variant-pkg@1.0 +two_whens"
        install("--fake", "--add", spec_a)
        module_file = modulefile_filenames("tcl", spec_a)[0]
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content if "variant --boolean --default False two_whens" in x]) == 1
        assert len([x for x in content if "variant " in x]) == 3
        install("--fake", "--add", spec_b)
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content if "variant --boolean --default True two_whens" in x]) == 1

        spec_a = "conditional-variant-pkg@2.0 ~version_based"
        spec_b = "conditional-variant-pkg@2.0 +version_based ~variant_based"
        spec_c = "conditional-variant-pkg@2.0 +version_based +variant_based +two_whens"
        install("--fake", "--add", spec_a)
        module_file = modulefile_filenames("tcl", spec_a)[0]
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert (
            len([x for x in content if "variant --boolean --default False version_based" in x])
            == 1
        )
        assert len([x for x in content if "variant " in x]) == 3
        install("--fake", "--add", spec_b)
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content if "variant --boolean version_based" in x]) == 1
        assert (
            len([x for x in content if "variant --boolean --default False variant_based" in x])
            == 1
        )
        assert len([x for x in content if "variant " in x]) == 4
        install("--fake", "--add", spec_c)
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content if "variant --boolean version_based" in x]) == 1
        assert (
            len([x for x in content if "variant --boolean --default False variant_based" in x])
            == 1
        )
        assert len([x for x in content if "variant --boolean --default False two_whens" in x]) == 1
        assert len([x for x in content if "variant " in x]) == 5
        uninstall("-y", spec_a)
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert (
            len([x for x in content if "variant --boolean --default True version_based" in x]) == 1
        )
        assert (
            len([x for x in content if "variant --boolean --default True variant_based" in x]) == 1
        )
        assert len([x for x in content if "variant --boolean --default False two_whens" in x]) == 1
        assert len([x for x in content if "variant " in x]) == 5

    def test_variant_defaults_all_exclude(
        self, install_mockery, module_configuration, modulefile_filenames
    ):
        """Tests variant defaults when installations are folded, variants mode is ``"all"``
        and some variants are excluded."""
        module_configuration("variant_defaults_all_exclude")

        spec_a = "mpileaks@2.3"
        spec_b = "mpileaks@2.3 +debug ~shared +opt ~fortran"
        spec_c = "mpileaks@2.3 ~debug +shared ~opt +fortran"
        install("--fake", "--add", spec_a)
        module_file = modulefile_filenames("tcl", spec_a)[0]
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content if "variant --boolean --default False fortran" in x]) == 1
        assert len([x for x in content if "variant --boolean --default True shared" in x]) == 1
        assert len([x for x in content if "variant --boolean --default True static" in x]) == 1
        assert len([x for x in content if "variant " in x]) == 5
        install("--fake", "--add", spec_b)
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content if "variant --boolean --default False shared" in x]) == 1
        assert len([x for x in content if "variant --boolean --default False fortran" in x]) == 1
        assert len([x for x in content if "variant --boolean --default True static" in x]) == 1
        install("--fake", "--add", spec_c)
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content if "variant --boolean --default False shared" in x]) == 1
        assert len([x for x in content if "variant --boolean --default True fortran" in x]) == 1
        assert len([x for x in content if "variant --boolean --default True static" in x]) == 1
        uninstall("-y", spec_c)
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content if "variant --boolean --default False shared" in x]) == 1
        assert len([x for x in content if "variant --boolean --default False fortran" in x]) == 1
        assert len([x for x in content if "variant --boolean --default True static" in x]) == 1

        spec_a = "mpich@3.0.4"
        spec_b = "mpich@3.0.4 +debug"
        install("--fake", "--add", spec_a)
        module_file = modulefile_filenames("tcl", spec_a)[0]
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content if "variant --boolean " in x]) == 0
        assert len([x for x in content if "variant " in x]) == 2
        install("--fake", "--add", spec_b)
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content if "variant --boolean " in x]) == 0
        assert len([x for x in content if "variant " in x]) == 3

        spec_a = "manyvariants@1.0.1"
        spec_b = "manyvariants@1.0.1 ~a +b c=v2 d=v3"
        install("--fake", "--add", spec_a)
        module_file = modulefile_filenames("tcl", spec_a)[0]
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content if "variant --boolean --default False b" in x]) == 1
        assert len([x for x in content if "variant --default v1 c v1" in x]) == 1
        assert len([x for x in content if "variant --default v1 d v1" in x]) == 1
        assert len([x for x in content if "variant " in x]) == 5
        install("--fake", "--add", spec_b)
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content if "variant --boolean --default False b" in x]) == 1
        assert (
            len(
                [
                    x
                    for x in content
                    if "variant --default v1 c v1 v2" in x or "variant --default v1 c v2 v1" in x
                ]
            )
            == 1
        )
        assert len([x for x in content if "variant d v1 v3" in x or "variant d v3 v1" in x]) == 1
        assert len([x for x in content if "variant " in x]) == 5

        spec_a = "conditional-variant-pkg@1.0"
        spec_b = "conditional-variant-pkg@1.0 +two_whens"
        install("--fake", "--add", spec_a)
        module_file = modulefile_filenames("tcl", spec_a)[0]
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content if "variant --boolean " in x]) == 0
        assert len([x for x in content if "variant " in x]) == 2
        install("--fake", "--add", spec_b)
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content if "variant --boolean " in x]) == 0
        assert len([x for x in content if "variant " in x]) == 3

        spec_a = "conditional-variant-pkg@2.0 ~version_based"
        spec_b = "conditional-variant-pkg@2.0 +version_based ~variant_based"
        spec_c = "conditional-variant-pkg@2.0 +version_based +variant_based +two_whens"
        install("--fake", "--add", spec_a)
        module_file = modulefile_filenames("tcl", spec_a)[0]
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert (
            len([x for x in content if "variant --boolean --default False version_based" in x])
            == 1
        )
        assert len([x for x in content if "variant " in x]) == 3
        install("--fake", "--add", spec_b)
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content if "variant --boolean version_based" in x]) == 1
        assert len([x for x in content if "variant --boolean " in x]) == 1
        assert len([x for x in content if "variant " in x]) == 3
        install("--fake", "--add", spec_c)
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content if "variant --boolean version_based" in x]) == 1
        assert len([x for x in content if "variant --boolean --default False two_whens" in x]) == 1
        assert len([x for x in content if "variant --boolean " in x]) == 2
        assert len([x for x in content if "variant " in x]) == 4
        uninstall("-y", spec_a)
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert (
            len([x for x in content if "variant --boolean --default True version_based" in x]) == 1
        )
        assert len([x for x in content if "variant --boolean --default False two_whens" in x]) == 1
        assert len([x for x in content if "variant --boolean " in x]) == 2
        assert len([x for x in content if "variant " in x]) == 4

    def test_variant_defaults_varying(
        self, install_mockery, module_configuration, modulefile_filenames
    ):
        """Tests variant defaults when installations are folded and variants mode is
        ``"varying"``."""
        module_configuration("variant_defaults_varying")

        spec_a = "mpileaks@2.3"
        spec_b = "mpileaks@2.3 +debug ~shared +opt ~fortran"
        spec_c = "mpileaks@2.3 ~debug +shared ~opt +fortran"
        install("--fake", "--add", spec_a)
        module_file = modulefile_filenames("tcl", spec_a)[0]
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content if "variant " in x]) == 0
        install("--fake", "--add", spec_b)
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content if "variant " in x]) == 4
        assert len([x for x in content if "variant --boolean --default False debug" in x]) == 1
        assert len([x for x in content if "variant --boolean --default False shared" in x]) == 1
        assert len([x for x in content if "variant --boolean opt" in x]) == 1
        install("--fake", "--add", spec_c)
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content if "variant " in x]) == 5
        assert len([x for x in content if "variant --boolean --default False debug" in x]) == 1
        assert len([x for x in content if "variant --boolean --default False shared" in x]) == 1
        assert len([x for x in content if "variant --boolean opt" in x]) == 1
        assert len([x for x in content if "variant --boolean --default True fortran" in x]) == 1
        uninstall("-y", spec_c)
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content if "variant " in x]) == 4
        assert len([x for x in content if "variant --boolean --default False debug" in x]) == 1
        assert len([x for x in content if "variant --boolean --default False shared" in x]) == 1
        assert len([x for x in content if "variant --boolean opt" in x]) == 1

        spec_a = "mpileaks@2.2"
        spec_b = "mpileaks@2.2 +fortran"
        install("--fake", "--add", spec_a)
        module_file = modulefile_filenames("tcl", spec_a)[0]
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content if "variant " in x]) == 0
        install("--fake", "--add", spec_b)
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content if "variant " in x]) == 2
        assert len([x for x in content if "variant --boolean --default False fortran" in x]) == 1

        spec_a = "mpich@3.0.4"
        spec_b = "mpich@3.0.4 +debug"
        install("--fake", "--add", spec_a)
        module_file = modulefile_filenames("tcl", spec_a)[0]
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content if "variant " in x]) == 0
        install("--fake", "--add", spec_b)
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content if "variant " in x]) == 2
        assert len([x for x in content if "variant --boolean debug" in x]) == 1

        spec_a = "manyvariants@1.0.1"
        spec_b = "manyvariants@1.0.1 ~a +b c=v2 d=v3"
        install("--fake", "--add", spec_a)
        module_file = modulefile_filenames("tcl", spec_a)[0]
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content if "variant " in x]) == 0
        install("--fake", "--add", spec_b)
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content if "variant " in x]) == 5
        assert len([x for x in content if "variant --boolean --default True a" in x]) == 1
        assert len([x for x in content if "variant --boolean --default False b" in x]) == 1
        assert (
            len(
                [
                    x
                    for x in content
                    if "variant --default v1 c v1 v2" in x or "variant --default v1 c v2 v1" in x
                ]
            )
            == 1
        )
        assert len([x for x in content if "variant d v1 v3" in x or "variant d v3 v1" in x]) == 1

        spec_a = "conditional-variant-pkg@1.0"
        spec_b = "conditional-variant-pkg@1.0 +two_whens"
        install("--fake", "--add", spec_a)
        module_file = modulefile_filenames("tcl", spec_a)[0]
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content if "variant " in x]) == 0
        install("--fake", "--add", spec_b)
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content if "variant " in x]) == 2
        assert len([x for x in content if "variant --boolean --default True two_whens" in x]) == 1

        spec_a = "conditional-variant-pkg@2.0 ~version_based"
        spec_b = "conditional-variant-pkg@2.0 +version_based ~variant_based"
        spec_c = "conditional-variant-pkg@2.0 +version_based +variant_based +two_whens"
        install("--fake", "--add", spec_a)
        module_file = modulefile_filenames("tcl", spec_a)[0]
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content if "variant " in x]) == 0
        install("--fake", "--add", spec_b)
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content if "variant --boolean version_based" in x]) == 1
        assert len([x for x in content if "variant " in x]) == 2
        install("--fake", "--add", spec_c)
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert len([x for x in content if "variant --boolean version_based" in x]) == 1
        assert (
            len([x for x in content if "variant --boolean --default False variant_based" in x])
            == 1
        )
        assert len([x for x in content if "variant --boolean --default False two_whens" in x]) == 1
        assert len([x for x in content if "variant " in x]) == 4
        uninstall("-y", spec_a)
        with open(module_file, encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines() if not line.startswith("## ")]
        assert (
            len([x for x in content if "variant --boolean --default True variant_based" in x]) == 1
        )
        assert len([x for x in content if "variant --boolean --default False two_whens" in x]) == 1
        assert len([x for x in content if "variant " in x]) == 3
