# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import pathlib

import pytest

import spack.bootstrap.config
import spack.bootstrap.core
import spack.builder
import spack.concretize
import spack.config
import spack.error
import spack.paths
import spack.repo
import spack.store
from spack.util.filesystem import touch


@pytest.fixture()
def builder_test_repository(config):
    builder_test_path = os.path.join(spack.paths.test_repos_path, "spack_repo", "builder_test")
    with spack.repo.use_repositories(builder_test_path) as mock_repo:
        yield mock_repo


@pytest.mark.parametrize(
    "spec_str,expected_values",
    [
        (
            "callbacks@2.0",
            [
                ("BEFORE_INSTALL_1_CALLED", "1"),
                ("BEFORE_INSTALL_2_CALLED", "1"),
                ("CALLBACKS_INSTALL_CALLED", "1"),
                ("AFTER_INSTALL_1_CALLED", "1"),
                ("TEST_VALUE", "3"),
                ("INSTALL_VALUE", "CALLBACKS"),
            ],
        ),
        # The last callback is conditional on "@1.0", check it's being executed
        (
            "callbacks@1.0",
            [
                ("BEFORE_INSTALL_1_CALLED", "1"),
                ("BEFORE_INSTALL_2_CALLED", "1"),
                ("CALLBACKS_INSTALL_CALLED", "1"),
                ("AFTER_INSTALL_1_CALLED", "1"),
                ("AFTER_INSTALL_2_CALLED", "1"),
                ("TEST_VALUE", "4"),
                ("INSTALL_VALUE", "CALLBACKS"),
            ],
        ),
        # The package below adds to "callbacks" using inheritance, test that using super()
        # works with builder hierarchies
        (
            "inheritance@1.0",
            [
                ("DERIVED_BEFORE_INSTALL_CALLED", "1"),
                ("BEFORE_INSTALL_1_CALLED", "1"),
                ("BEFORE_INSTALL_2_CALLED", "1"),
                ("CALLBACKS_INSTALL_CALLED", "1"),
                ("INHERITANCE_INSTALL_CALLED", "1"),
                ("AFTER_INSTALL_1_CALLED", "1"),
                ("AFTER_INSTALL_2_CALLED", "1"),
                ("TEST_VALUE", "4"),
                ("INSTALL_VALUE", "INHERITANCE"),
            ],
        ),
        # Generate custom phases using a GenericBuilder
        (
            "custom-phases",
            [("CONFIGURE_CALLED", "1"), ("INSTALL_CALLED", "1"), ("LAST_PHASE", "INSTALL")],
        ),
        # Old-style package, with phase defined in base builder
        ("old-style-autotools@1.0", [("AFTER_AUTORECONF_1_CALLED", "1")]),
        ("old-style-autotools@2.0", [("AFTER_AUTORECONF_2_CALLED", "1")]),
        ("old-style-custom-phases", [("AFTER_CONFIGURE_CALLED", "1"), ("TEST_VALUE", "0")]),
    ],
)
@pytest.mark.usefixtures("builder_test_repository", "config")
@pytest.mark.disable_clean_stage_check
def test_callbacks_and_installation_procedure(
    spec_str, expected_values, working_env, temporary_store
):
    """Test the correct execution of callbacks and installation procedures for packages."""
    print("Visible configuration scopes:", flush=True)
    for scope in spack.config.CONFIG.scopes.values():
        print(f"  {scope.name}: {getattr(scope, 'path', None)}", flush=True)
    print(f"Store root: {spack.store.STORE.root}", flush=True)
    print(f"Store database root: {spack.store.STORE.db.root}", flush=True)
    print(f"Bootstrap root: {spack.bootstrap.config.root_path()}", flush=True)
    print(f"Bootstrap store: {spack.bootstrap.config.store_path()}", flush=True)

    try:
        s = spack.concretize.concretize_one(spec_str)
    except Exception as e:
        diagnostics = [
            f"worker exception: {type(e).__name__}: {e}",
            f"store root: {spack.store.STORE.root}",
            f"store database root: {spack.store.STORE.db.root}",
            f"bootstrap root config: {spack.config.CONFIG.get('bootstrap:root')}",
            f"bootstrap root: {spack.bootstrap.config.root_path()}",
            f"bootstrap store: {spack.bootstrap.config.store_path()}",
            f"bootstrap config: {spack.bootstrap.config._config_path()}",
            f"bootstrap settings: {spack.config.CONFIG.get('bootstrap')!r}",
            f"repositories config: {spack.config.CONFIG.get('repos')!r}",
            "visible configuration scopes:",
        ]
        diagnostics.extend(
            f"  {scope.name}: {getattr(scope, 'path', None)}"
            for scope in spack.config.CONFIG.scopes.values()
        )
        diagnostics.append(
            "active repositories: "
            + repr([(repo.namespace, repo.root) for repo in spack.repo.PATH.repos])
        )
        try:
            with spack.bootstrap.config.ensure_bootstrap_configuration():
                request = spack.bootstrap.core.BootstrapRequest.for_module(
                    "clingo",
                    spack.bootstrap.core.clingo_root_spec(),
                    concretize=spack.bootstrap.core._concretize_clingo,
                )
                database = spack.store.STORE.db
                index_path = database._index_path
                index_contents = (
                    index_path.read_text(encoding="utf-8") if index_path.exists() else None
                )
                exact_matches = database.query(request.abstract_spec, installed=True)
                name_matches = database.query("clingo-bootstrap", installed=True)
                bootstrap_root = pathlib.Path(spack.store.STORE.root)
                clingo_paths = sorted(
                    str(path) for path in bootstrap_root.rglob("*") if "clingo" in path.name
                )
                spec_paths = sorted(str(path) for path in bootstrap_root.rglob("spec.json"))
                diagnostics.extend(
                    [
                        f"bootstrap clingo paths: {clingo_paths!r}",
                        f"bootstrap spec files: {spec_paths!r}",
                        f"bootstrap-context store object: {id(spack.store.STORE)}",
                        f"bootstrap-context database object: {id(database)}",
                        f"bootstrap-context store root: {spack.store.STORE.root}",
                        f"bootstrap-context database root: {database.root}",
                        f"bootstrap store layout: {vars(spack.store.STORE.layout)!r}",
                        f"bootstrap database upstreams: {database.upstream_dbs!r}",
                        f"bootstrap database version: {database._db_version!r}",
                        f"bootstrap database installed prefixes: {database._installed_prefixes!r}",
                        f"bootstrap database directory: {database.database_directory}",
                        f"bootstrap database index: {index_path}",
                        f"bootstrap database index exists: {index_path.exists()}",
                        f"bootstrap database index size: "
                        f"{index_path.stat().st_size if index_path.exists() else None}",
                        f"bootstrap database index contents: {index_contents!r}",
                        f"bootstrap database files: "
                        f"{sorted(str(path) for path in database.database_directory.glob('*'))!r}",
                        f"clingo bootstrap request: {request.abstract_spec}",
                        f"clingo exact database matches: {exact_matches!r}",
                        f"clingo name database matches: {name_matches!r}",
                        f"clingo probe result: {request.probe(request.abstract_spec)!r}",
                        f"bootstrap database records: {list(database._data)!r}",
                    ]
                )
                for candidate in name_matches:
                    diagnostics.extend(
                        [
                            f"clingo candidate prefix: {candidate.prefix}",
                            f"clingo candidate dependencies: {candidate.dependencies()!r}",
                            f"clingo candidate prefix exists: "
                            f"{pathlib.Path(candidate.prefix).exists()}",
                        ]
                    )
        except Exception as probe_error:
            diagnostics.append(
                f"bootstrap diagnostics failed: {type(probe_error).__name__}: {probe_error}"
            )
        raise RuntimeError("Concretization diagnostics:\n" + "\n".join(diagnostics)) from e
    builder = spack.builder.create(s.package)
    for phase_fn in builder:
        phase_fn.execute()

    # Check calls have produced the expected side effects
    for var_name, expected in expected_values:
        assert os.environ[var_name] == expected, os.environ


@pytest.mark.usefixtures("builder_test_repository", "config")
@pytest.mark.parametrize(
    "spec_str,method_name,expected",
    [
        # Call a function defined on the package, which calls the same function defined
        # on the super(builder)
        ("old-style-autotools", "configure_args", ["--with-foo"]),
        # Call a function defined on the package, which calls the same function defined on the
        # super(pkg), which calls the same function defined in the super(builder)
        ("old-style-derived", "configure_args", ["--with-bar", "--with-foo"]),
    ],
)
def test_old_style_compatibility_with_super(spec_str, method_name, expected):
    s = spack.concretize.concretize_one(spec_str)
    builder = spack.builder.create(s.package)
    value = getattr(builder, method_name)()
    assert value == expected


@pytest.mark.not_on_windows("log_ouput cannot currently be used outside of subprocess on Windows")
@pytest.mark.regression("33928")
@pytest.mark.usefixtures("builder_test_repository", "config", "working_env")
@pytest.mark.disable_clean_stage_check
def test_build_time_tests_are_executed_from_default_builder(temporary_store):
    s = spack.concretize.concretize_one("old-style-autotools")
    builder = spack.builder.create(s.package)
    builder.pkg.run_tests = True
    for phase_fn in builder:
        phase_fn.execute()

    assert os.environ.get("CHECK_CALLED") == "1", "Build time tests not executed"
    assert os.environ.get("INSTALLCHECK_CALLED") == "1", "Install time tests not executed"


@pytest.mark.regression("34518")
@pytest.mark.usefixtures("builder_test_repository", "config", "working_env")
def test_monkey_patching_wrapped_pkg():
    """Confirm 'run_tests' is accessible through wrappers."""
    s = spack.concretize.concretize_one("old-style-autotools")
    builder = spack.builder.create(s.package)
    assert s.package.run_tests is False
    assert builder.pkg.run_tests is False
    assert builder.pkg_with_dispatcher.run_tests is False

    s.package.run_tests = True
    assert builder.pkg.run_tests is True
    assert builder.pkg_with_dispatcher.run_tests is True


@pytest.mark.regression("34440")
@pytest.mark.usefixtures("builder_test_repository", "config", "working_env")
def test_monkey_patching_test_log_file():
    """Confirm 'test_log_file' is accessible through wrappers."""
    s = spack.concretize.concretize_one("old-style-autotools")
    builder = spack.builder.create(s.package)

    s.package.tester.test_log_file = "/some/file"
    assert builder.pkg.tester.test_log_file == "/some/file"
    assert builder.pkg_with_dispatcher.tester.test_log_file == "/some/file"


# Windows context manager's __exit__ fails with ValueError ("I/O operation
# on closed file").
@pytest.mark.not_on_windows("Does not run on windows")
def test_install_time_test_callback(
    tmp_path: pathlib.Path, config, mock_packages, mock_stage, temporary_store
):
    """Confirm able to run stand-alone test as a post-install callback."""
    s = spack.concretize.concretize_one("py-test-callback")
    builder = spack.builder.create(s.package)
    builder.pkg.run_tests = True
    s.package.tester.test_log_file = str(tmp_path / "install_test.log")
    touch(s.package.tester.test_log_file)

    for phase_fn in builder:
        phase_fn.execute()

    with open(s.package.tester.test_log_file, "r", encoding="utf-8") as f:
        results = f.read().replace("\n", " ")
        assert "PyTestCallback test" in results


@pytest.mark.regression("43097")
@pytest.mark.usefixtures("builder_test_repository", "config")
def test_mixins_with_builders(working_env):
    """Tests that run_after and run_before callbacks are accumulated correctly,
    when mixins are used with builders.
    """
    s = spack.concretize.concretize_one("builder-and-mixins")
    builder = spack.builder.create(s.package)

    # Check that callbacks added by the mixin are in the list
    assert any(fn.__name__ == "before_install" for _, fn in builder._run_before_callbacks)
    assert any(fn.__name__ == "after_install" for _, fn in builder._run_after_callbacks)

    # Check that callback from the GenericBuilder are in the list too
    assert any(fn.__name__ == "sanity_check_prefix" for _, fn in builder._run_after_callbacks)


def test_reading_api_v20_attributes():
    """Tests that we can read attributes from API v2.0 builders."""

    class TestBuilder(spack.builder.Builder):
        legacy_methods = ("configure", "install")
        legacy_attributes = ("foo", "bar")
        legacy_long_methods = ("baz", "fee")

    methods = spack.builder.package_methods(TestBuilder)
    assert methods == ("configure", "install")
    attributes = spack.builder.package_attributes(TestBuilder)
    assert attributes == ("foo", "bar")
    long_methods = spack.builder.package_long_methods(TestBuilder)
    assert long_methods == ("baz", "fee")


def test_reading_api_v22_attributes():
    """Tests that we can read attributes from API v2.2 builders."""

    class TestBuilder(spack.builder.Builder):
        package_methods = ("configure", "install")
        package_attributes = ("foo", "bar")
        package_long_methods = ("baz", "fee")

    methods = spack.builder.package_methods(TestBuilder)
    assert methods == ("configure", "install")
    attributes = spack.builder.package_attributes(TestBuilder)
    assert attributes == ("foo", "bar")
    long_methods = spack.builder.package_long_methods(TestBuilder)
    assert long_methods == ("baz", "fee")


@pytest.mark.regression("51917")
@pytest.mark.usefixtures("builder_test_repository", "config")
def test_builder_when_inheriting_just_package(working_env):
    """Tests that if we inherit a package from another package that has a builder defined,
    but we don't need to modify the builder ourselves, we'll get the builder of the base
    package class.
    """
    base_spec = spack.concretize.concretize_one("callbacks")
    derived_spec = spack.concretize.concretize_one("inheritance-only-package")

    base_builder = spack.builder.create(base_spec.package)
    derived_builder = spack.builder.create(derived_spec.package)

    # The derived class doesn't redefine a builder, so we should
    # get the builder of the base class.
    assert type(base_builder) is type(derived_builder)


@pytest.mark.usefixtures("builder_test_repository", "config")
def test_get_builder_class_accepts_objects_and_classes():
    """Tests that get_builder_class works on both package objects and package classes."""
    pkg_cls = spack.repo.PATH.get_pkg_class("callbacks")
    builder_cls = spack.builder.get_builder_class(pkg_cls, "GenericBuilder")

    # The builder is defined in the package module, so it is found from the class
    assert builder_cls is not None
    assert spack.repo.is_package_module(builder_cls.__module__)

    # ... and an object of that class gives the same answer
    pkg = spack.concretize.concretize_one("callbacks").package
    assert spack.builder.get_builder_class(pkg, "GenericBuilder") is builder_cls

    # Derived packages that don't redefine a builder get it from the base package module
    derived_cls = spack.repo.PATH.get_pkg_class("inheritance-only-package")
    assert spack.builder.get_builder_class(derived_cls, "GenericBuilder") is builder_cls

    # Names that are not defined in any package module are not builders
    assert spack.builder.get_builder_class(pkg_cls, "UnknownBuilder") is None


def test_register_builder_rejects_duplicate_names():
    """A build system name can be registered by only one builder class."""

    @spack.builder.register_builder("test-duplicate")
    class FirstBuilder:
        pass

    try:
        # re-registering the same class is idempotent
        assert spack.builder.register_builder("test-duplicate")(FirstBuilder) is FirstBuilder

        with pytest.raises(spack.error.SpackError, match="already registered"):

            @spack.builder.register_builder("test-duplicate")
            class SecondBuilder:
                pass

    finally:
        del spack.builder.BUILDER_CLS["test-duplicate"]
