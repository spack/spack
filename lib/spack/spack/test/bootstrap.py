# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import contextlib
import json
import pathlib
import re
from typing import Any, Dict, List, Optional

import pytest

import spack.binary_distribution
import spack.bootstrap
import spack.bootstrap._common
import spack.bootstrap.clingo
import spack.bootstrap.config
import spack.bootstrap.core
import spack.bootstrap.status
import spack.compilers.config
import spack.concretize
import spack.config
import spack.database
import spack.environment
import spack.error
import spack.mirrors.mirror
import spack.paths
import spack.spec
import spack.store
import spack.util.executable
import spack.util.spack_yaml
import spack.version
from spack.active_environment import active_environment

BUILDCACHE_METADATA = [
    x
    for x in sorted(pathlib.Path(spack.paths.share_path).glob("bootstrap/*/metadata.yaml"))
    if "type: buildcache" in x.read_text(encoding="utf-8")
]
if not BUILDCACHE_METADATA:
    raise RuntimeError(f"no buildcache metadata in {spack.paths.share_path}")

PROTOTYPE_DIR = pathlib.Path(spack.bootstrap.clingo.__file__).parent / "prototypes"
PROTOTYPES = sorted(x.name for x in PROTOTYPE_DIR.glob("*.json"))
if not PROTOTYPES:
    raise RuntimeError(f"no bootstrap prototypes in {PROTOTYPE_DIR}")


@pytest.fixture(autouse=True)
def isolated_bootstrap_root(monkeypatch, tmp_path: pathlib.Path):
    """Point the bootstrap root at a temporary directory, so that tests entering
    ``ensure_bootstrap_configuration`` do not mount the user's real bootstrap config.

    Two settings resolve the root: the default scope has ``root: $user_cache_path/bootstrap``,
    and ``root_path()`` falls back to ``default_user_bootstrap_path`` when no config defines
    it. Both are pinned here so that they agree.
    """
    user_cache_path = tmp_path / "user_cache"
    monkeypatch.setattr(spack.paths, "user_cache_path", str(user_cache_path))
    monkeypatch.setattr(
        spack.paths, "default_user_bootstrap_path", str(user_cache_path / "bootstrap")
    )


@pytest.fixture
def active_mock_environment(mutable_config, mutable_mock_env_path):
    with spack.environment.create("bootstrap-test") as env:
        yield env


def _assert_bootstrap_store_is_active() -> None:
    """Assert that the store in use is the bootstrap store, configured without padding."""
    bootstrap_store = spack.bootstrap.config.store_path()
    assert spack.store.STORE.root == bootstrap_store
    assert spack.config.CONFIG.get("config:install_tree:root") == bootstrap_store
    assert spack.config.CONFIG.get("config:install_tree:padded_length") == 0


@pytest.mark.regression("22294")
def test_store_is_restored_correctly_after_bootstrap(mutable_config, tmp_path: pathlib.Path):
    """Tests that the store is correctly swapped during bootstrapping, and restored afterward."""
    user_path = str(tmp_path / "store")
    with spack.store.use_store(user_path):
        assert spack.store.STORE.root == user_path
        assert spack.config.CONFIG.get("config:install_tree:root") == user_path
        with spack.bootstrap.ensure_bootstrap_configuration():
            _assert_bootstrap_store_is_active()
        assert spack.store.STORE.root == user_path
        assert spack.config.CONFIG.get("config:install_tree:root") == user_path


@pytest.mark.regression("38963")
def test_store_padding_length_is_zero_during_bootstrapping(mutable_config, tmp_path: pathlib.Path):
    """Tests that, even though padded length is set in user config, the bootstrap store maintains
    a padded length of zero.
    """
    user_path = str(tmp_path / "store")
    with spack.store.use_store(user_path, extra_data={"padded_length": 512}):
        assert spack.config.CONFIG.get("config:install_tree:padded_length") == 512
        with spack.bootstrap.ensure_bootstrap_configuration():
            _assert_bootstrap_store_is_active()
        assert spack.config.CONFIG.get("config:install_tree:padded_length") == 512


@pytest.mark.regression("38963")
def test_install_tree_customization_is_respected(mutable_config, tmp_path: pathlib.Path):
    """Tests that a custom user store is respected when we exit the bootstrapping
    environment.
    """
    spack.store.reinitialize()
    store_dir = tmp_path / "store"
    spack.config.CONFIG.set("config:install_tree:root", str(store_dir))
    with spack.bootstrap.ensure_bootstrap_configuration():
        _assert_bootstrap_store_is_active()
    assert spack.config.CONFIG.get("config:install_tree:root") == str(store_dir)
    assert spack.store.STORE.root == str(store_dir)


@pytest.mark.parametrize(
    "config_value,expected",
    [
        # Absolute path without expansion
        ("/opt/spack/bootstrap", "/opt/spack/bootstrap/store"),
        # Path with placeholder
        ("$spack/opt/bootstrap", "$spack/opt/bootstrap/store"),
    ],
)
def test_store_path_customization(config_value, expected, mutable_config):
    # Set the current configuration to a specific value
    spack.config.CONFIG.set("bootstrap:root", config_value)

    # Check the store path
    current = spack.bootstrap.config.store_path()
    assert current == spack.config.canonicalize_path(expected)


def test_raising_exception_if_bootstrap_disabled(mutable_config):
    # Disable bootstrapping in config.yaml
    spack.config.CONFIG.set("bootstrap:enable", False)

    # Check the correct exception is raised
    with pytest.raises(RuntimeError, match="bootstrapping is currently disabled"):
        spack.bootstrap.config.store_path()


def test_raising_exception_module_importable(mutable_config):
    mutable_config.set("bootstrap:trusted", {"github-actions": True})
    with pytest.raises(ImportError, match='cannot bootstrap the "asdf" Python module'):
        spack.bootstrap.core.ensure_module_importable_or_raise("asdf")


def test_raising_exception_executables_in_path(mutable_config):
    mutable_config.set("bootstrap:trusted", {"github-actions": True})
    with pytest.raises(RuntimeError, match="cannot bootstrap any of the asdf, fdsa executables"):
        spack.bootstrap.core.ensure_executables_in_path_or_raise(["asdf", "fdsa"], "python")


@pytest.mark.regression("25603")
def test_bootstrap_deactivates_environments(active_mock_environment):
    assert active_environment() == active_mock_environment
    with spack.bootstrap.ensure_bootstrap_configuration():
        assert active_environment() is None
    assert active_environment() == active_mock_environment


def test_bootstrap_db_upgrade_error_points_at_b_flag(mutable_config, monkeypatch):
    """An outdated bootstrap store database must raise ExplicitDatabaseUpgradeError, and,
    because the store being read is the bootstrap store, the migration hint must be
    ``spack -b reindex`` rather than plain ``spack reindex``.
    """
    with pytest.raises(spack.error.ExplicitDatabaseUpgradeError) as exc_info:
        with spack.bootstrap.ensure_bootstrap_configuration():
            db_dir = pathlib.Path(spack.store.STORE.root) / ".spack-db"
            db_dir.mkdir(parents=True, exist_ok=True)
            (db_dir / "index.json").write_text(
                json.dumps(
                    {"database": {"version": str(spack.database._DB_VERSION), "installs": {}}}
                )
            )
            next_version = spack.version.Version(f"{spack.database._DB_VERSION[0] + 1}")
            monkeypatch.setattr(spack.database, "_DB_VERSION", next_version)
            spack.database.Database(spack.store.STORE.root)._read()

    long_message = exc_info.value.long_message
    assert "spack -b reindex" in long_message
    assert "spack reindex" not in long_message


@pytest.mark.regression("25805")
def test_bootstrap_disables_modulefile_generation(mutable_config):
    # Be sure to enable both lmod and tcl in modules.yaml
    spack.config.CONFIG.set("modules:default:enable", ["tcl", "lmod"])

    assert "tcl" in spack.config.CONFIG.get("modules:default:enable")
    assert "lmod" in spack.config.CONFIG.get("modules:default:enable")
    with spack.bootstrap.ensure_bootstrap_configuration():
        assert "tcl" not in spack.config.CONFIG.get("modules:default:enable")
        assert "lmod" not in spack.config.CONFIG.get("modules:default:enable")
    assert "tcl" in spack.config.CONFIG.get("modules:default:enable")
    assert "lmod" in spack.config.CONFIG.get("modules:default:enable")


@pytest.mark.regression("25992")
@pytest.mark.requires_executables("gcc")
def test_bootstrap_search_for_compilers_with_no_environment(no_packages_yaml, mock_packages):
    assert not spack.compilers.config.all_compilers(
        no_packages_yaml, repo=mock_packages, init_config=False
    )
    with spack.bootstrap.ensure_bootstrap_configuration():
        spack.bootstrap.clingo._add_compilers_if_missing(spack.config.CONFIG, repo=mock_packages)
        assert spack.compilers.config.all_compilers(
            spack.config.CONFIG, repo=mock_packages, init_config=False
        )
    assert not spack.compilers.config.all_compilers(
        no_packages_yaml, repo=mock_packages, init_config=False
    )


@pytest.mark.regression("25992")
@pytest.mark.requires_executables("gcc")
def test_bootstrap_search_for_compilers_with_environment_active(
    no_packages_yaml, active_mock_environment, mock_packages
):
    assert not spack.compilers.config.all_compilers(
        no_packages_yaml, repo=mock_packages, init_config=False
    )
    with spack.bootstrap.ensure_bootstrap_configuration():
        spack.bootstrap.clingo._add_compilers_if_missing(spack.config.CONFIG, repo=mock_packages)
        assert spack.compilers.config.all_compilers(
            spack.config.CONFIG, repo=mock_packages, init_config=False
        )
    assert not spack.compilers.config.all_compilers(
        no_packages_yaml, repo=mock_packages, init_config=False
    )


@pytest.mark.regression("26189")
def test_config_yaml_is_preserved_during_bootstrap(mutable_config):
    expected_dir = "/tmp/test"
    spack.config.CONFIG.set("config:test_stage", expected_dir, scope="command_line")

    assert spack.config.CONFIG.get("config:test_stage") == expected_dir
    with spack.bootstrap.ensure_bootstrap_configuration():
        assert spack.config.CONFIG.get("config:test_stage") == expected_dir
    assert spack.config.CONFIG.get("config:test_stage") == expected_dir


@pytest.mark.regression("26548")
def test_bootstrap_custom_store_in_environment(mutable_config, tmp_path: pathlib.Path):
    # Test that the custom store in an environment is taken into account
    # during bootstrapping
    spack_yaml = tmp_path / "spack.yaml"
    install_root = tmp_path / "store"
    spack_yaml.write_text(
        """
spack:
  specs:
  - libelf
  config:
    install_tree:
      root: {0}
""".format(install_root)
    )
    with spack.environment.Environment(str(tmp_path)):
        assert active_environment()
        assert spack.config.CONFIG.get("config:install_tree:root") == str(install_root)
        # Don't trigger evaluation here
        with spack.bootstrap.ensure_bootstrap_configuration():
            pass
        assert str(spack.store.STORE.root) == str(install_root)


def test_nested_use_of_context_manager(mutable_config):
    """Test nested use of the context manager"""
    user_config = spack.config.CONFIG
    with spack.bootstrap.ensure_bootstrap_configuration():
        assert spack.config.CONFIG != user_config
        with spack.bootstrap.ensure_bootstrap_configuration():
            assert spack.config.CONFIG != user_config
    assert spack.config.CONFIG == user_config


def test_bootstrapping_state_is_part_of_the_configuration(mutable_config, monkeypatch):
    """Installer child processes restore the configuration, so they see they are bootstrapping"""
    with spack.bootstrap.ensure_bootstrap_configuration():
        bootstrap_config = spack.config.CONFIG
    assert not spack.bootstrap.is_bootstrapping()
    monkeypatch.setattr(spack.config, "CONFIG", bootstrap_config)
    assert spack.bootstrap.is_bootstrapping()


@pytest.mark.parametrize("expected_missing", [False, True])
def test_status_function_find_files(
    mutable_config, mock_executable, tmp_path: pathlib.Path, monkeypatch, expected_missing
):
    if not expected_missing:
        mock_executable("foo", "echo Hello WWorld!")

    monkeypatch.setattr(
        spack.bootstrap.status,
        "_optional_requirements",
        lambda: [spack.bootstrap.status._required_system_executable("foo", "NOT FOUND")],
    )
    monkeypatch.setenv("PATH", str(tmp_path / "bin"))

    _, missing = spack.bootstrap.status_message("optional")
    assert missing is expected_missing


@pytest.mark.parametrize(
    "gpg_in_path,gpg_in_store,expected_missing",
    [
        (True, False, False),  # gpg exists in PATH
        (False, True, False),  # gpg exists in the bootstrap store
        (False, False, True),  # gpg is missing
    ],
)
def test_gpg_status_check(
    mutable_config,
    mock_executable,
    tmp_path: pathlib.Path,
    monkeypatch,
    gpg_in_path,
    gpg_in_store,
    expected_missing,
):
    """Test that gpg/gpg2 status is detected whether it's in PATH or in the bootstrap store."""
    if gpg_in_path:
        mock_executable("gpg2", "echo GPG 2.3.4")
    monkeypatch.setenv("PATH", str(tmp_path / "bin"))

    def _only_gnupg_in_store(exes, query_spec):
        if not gpg_in_store or "gpg2" not in exes:
            return None
        return spack.bootstrap._common.ExecutableInfo(
            spec=spack.spec.Spec("gnupg@2.5.12"), command=spack.util.executable.Executable("gpg")
        )

    monkeypatch.setattr(spack.bootstrap.status, "_executables_in_store", _only_gnupg_in_store)

    msg, _ = spack.bootstrap.status_message("buildcache")
    assert ('MISSING "gpg2"' in msg) is expected_missing


@pytest.mark.regression("31042")
def test_source_is_disabled(mutable_config):
    # Get the configuration dictionary of the current bootstrapping source
    conf = next(iter(spack.bootstrap.core.bootstrapping_sources()))

    # The source is not explicitly enabled or disabled, so the following should return False
    assert not spack.bootstrap.core.source_is_enabled(conf)

    # Try to explicitly disable the source and verify that the behavior is the same as above
    spack.config.CONFIG.add("bootstrap:trusted:{0}:{1}".format(conf["name"], False))
    assert not spack.bootstrap.core.source_is_enabled(conf)


@pytest.mark.parametrize("prototype", PROTOTYPES)
def test_prototype_matches_a_constraint_on_its_compiler(prototype):
    """The bootstrap concretizer edits a prototype with the concreteness flag cleared, picking
    patches from conditions such as '%msvc@19.38:'. The compiler the prototype records has to
    match such a condition."""
    s = spack.spec.Spec.from_specfile(str(PROTOTYPE_DIR / prototype))
    compilers = [x.spec for x in s.edges_to_dependencies() if "cxx" in x.virtuals]
    assert compilers, f"{prototype} has no cxx provider"
    compiler = compilers[0]

    s._mark_concrete(False)

    assert s.satisfies(f"%{compiler.name}")
    assert s.satisfies(f"%{compiler.name}@{compiler.version}")


def test_no_bootstrapping_sources_enabled(mutable_config):
    """Tests the message raised when no source is trusted."""
    mutable_config.set("bootstrap:trusted", {})
    with pytest.raises(ImportError, match="no bootstrapping sources are enabled"):
        spack.bootstrap.core.ensure_module_importable_or_raise("asdf")


@pytest.mark.not_on_windows("The mock executable quotes its output on Windows")
@pytest.mark.parametrize(
    "version_output,expected",
    [
        ("patchelf 0.17.2", True),
        # 0.13.1 is the oldest version we accept
        ("patchelf 0.13.1", True),
        ("patchelf 0.12", False),
        # no version at all in the output
        ("patchelf", False),
        # a second token that is not a version
        ("patchelf /usr/bin/patchelf", False),
    ],
)
def test_verify_patchelf(version_output, expected, mock_executable):
    patchelf = spack.util.executable.Executable(
        str(mock_executable("patchelf", f'echo "{version_output}"'))
    )
    assert spack.bootstrap.core.verify_patchelf(patchelf) is expected


@pytest.mark.not_on_windows("The mock executable quotes its output on Windows")
def test_verify_patchelf_when_the_command_fails(mock_executable):
    """Tests that a non-zero exit status is rejected, whatever the version string is."""
    patchelf = spack.util.executable.Executable(
        str(mock_executable("patchelf", 'echo "patchelf 0.17.2"\nexit 1'))
    )
    assert spack.bootstrap.core.verify_patchelf(patchelf) is False


@pytest.mark.parametrize("metadata_file", BUILDCACHE_METADATA, ids=lambda x: x.parent.name)
def test_pinned_binaries_map_dag_hashes_to_sha256(metadata_file: pathlib.Path):
    sha256 = spack.util.spack_yaml.load(metadata_file.read_text(encoding="utf-8"))["sha256"]
    assert sha256
    for dag_hash, checksum in sha256.items():
        assert re.fullmatch("[a-z2-7]{32}", dag_hash) and re.fullmatch("[0-9a-f]{64}", checksum)


def _fake_install_from_source(request, source):
    """Return the canned result of a source built by ``_fake_sources``, or raise it."""
    source["tried"].append(source["name"])
    if isinstance(source["result"], Exception):
        raise source["result"]
    return source["result"]


@pytest.fixture
def fake_install(monkeypatch):
    """Let the sources built with ``_fake_sources`` return their canned result."""
    monkeypatch.setattr(spack.bootstrap.core, "_install_from_source", _fake_install_from_source)


def _fake_sources(tried: List[str], *results: Any) -> List[Dict[str, Any]]:
    """Return one source per result, appending its name to ``tried`` when it is used."""
    return [{"name": f"src{i}", "result": x, "tried": tried} for i, x in enumerate(results)]


def _fake_request(probes: List[Any], result: Optional[str] = None):
    """Return a request whose probe records its calls and returns ``result``."""

    def probe(query_spec):
        probes.append(query_spec)
        return result

    return spack.bootstrap.core.BootstrapRequest(
        abstract_spec=spack.spec.Spec("zlib"),
        probe=probe,
        installer_args={},
        concretize=spack.concretize.concretize_one,
    )


def test_the_store_is_probed_once_for_all_the_sources(fake_install):
    """The store does not depend on the source, so it is queried once, before the loop."""
    probes: List[Any] = []
    tried: List[str] = []
    sources = _fake_sources(tried, RuntimeError("no"), RuntimeError("no"), RuntimeError("no"))

    with pytest.raises(RuntimeError, match="cannot bootstrap zlib"):
        spack.bootstrap.core._bootstrap_or_raise(
            _fake_request(probes), "zlib", RuntimeError, sources=sources
        )

    assert len(probes) == 1
    assert tried == ["src0", "src1", "src2"]


def test_software_in_the_store_skips_every_source(fake_install):
    """When the probe finds the software, no source is tried."""
    probes: List[Any] = []
    tried: List[str] = []
    sources = _fake_sources(tried, "from the source")

    result = spack.bootstrap.core._bootstrap_or_raise(
        _fake_request(probes, result="from the store"), "zlib", RuntimeError, sources=sources
    )

    assert result == "from the store"
    assert tried == []


def test_the_first_successful_source_wins(fake_install):
    probes: List[Any] = []
    tried: List[str] = []
    sources = _fake_sources(tried, RuntimeError("no"), "from src1", "from src2")

    result = spack.bootstrap.core._bootstrap_or_raise(
        _fake_request(probes), "zlib", RuntimeError, sources=sources
    )

    assert result == "from src1"
    assert tried == ["src0", "src1"]


def test_every_source_failure_is_reported(fake_install):
    """Tests that the message includes the name and the failure of every source."""
    probes: List[Any] = []
    tried: List[str] = []
    sources = _fake_sources(tried, RuntimeError("first boom"), ValueError("second boom"))

    with pytest.raises(RuntimeError) as exc_info:
        spack.bootstrap.core._bootstrap_or_raise(
            _fake_request(probes), "zlib", RuntimeError, sources=sources
        )

    message = str(exc_info.value)
    for expected in ("src0", "first boom", "src1", "second boom"):
        assert expected in message


def test_sources_that_provide_nothing_are_reported_as_such(fake_install):
    """Tests the message when every source returns None, without raising."""
    probes: List[Any] = []
    tried: List[str] = []
    sources = _fake_sources(tried, None, None)

    with pytest.raises(RuntimeError, match="no bootstrapping source could provide it"):
        spack.bootstrap.core._bootstrap_or_raise(
            _fake_request(probes), "zlib", RuntimeError, sources=sources
        )

    assert tried == ["src0", "src1"]


def test_no_sources_to_try_is_reported_as_such(fake_install):
    """Tests the message when the list of sources is empty."""
    probes: List[Any] = []

    with pytest.raises(RuntimeError, match='from spec "zlib": no bootstrapping sources'):
        spack.bootstrap.core._bootstrap_or_raise(
            _fake_request(probes), "zlib", RuntimeError, sources=[]
        )


#: The source, shipped with Spack, that builds the software it needs from sources
SPACK_INSTALL_SOURCE = {
    "name": "spack-install",
    "metadata": "$spack/share/spack/bootstrap/spack-install",
}


class _RecordingEnvironment:
    """Stand-in for the core environment, recording what it is asked to install."""

    def __init__(self) -> None:
        self.concretized_roots: List[Any] = []
        self.installs: List[Any] = []

    def write_transaction(self):
        return contextlib.suppress()

    def add_concrete_spec(self, abstract_spec, concrete_spec):
        pass

    def write(self, regenerate):
        pass

    def install_specs(self, specs, **installer_args):
        self.installs.append((specs, installer_args, spack.config.CONFIG.get("mirrors")))


class _FakeConcreteSpec:
    """Stand-in for the result of concretization."""

    def __init__(self, abstract_spec: Any) -> None:
        self.abstract_spec = abstract_spec


@pytest.fixture
def recording_environment(monkeypatch):
    """Let a source install run without detecting, concretizing or installing."""
    env = _RecordingEnvironment()
    monkeypatch.setattr(spack.bootstrap.core, "_add_externals_if_missing", lambda: None)
    monkeypatch.setattr(spack.concretize, "concretize_one", _FakeConcreteSpec)
    monkeypatch.setattr(spack.bootstrap.core, "_core_environment", lambda: env)
    return env


@pytest.mark.parametrize(
    "make_request,expected_installer_args",
    [
        # A module is always built from sources, while an executable may come from a build cache
        (
            lambda: spack.bootstrap.core.BootstrapRequest.for_module("pytest", "py-pytest"),
            {
                "fail_fast": True,
                "root_policy": "source_only",
                "dependencies_policy": "source_only",
            },
        ),
        (
            lambda: spack.bootstrap.core.BootstrapRequest.for_executables(
                ["patchelf"], "patchelf@0.13.1:"
            ),
            {"fail_fast": True},
        ),
    ],
    ids=["module", "executable"],
)
def test_a_source_install_uses_the_request_and_the_mirror_of_the_source(
    make_request, expected_installer_args, recording_environment, mutable_config
):
    mutable_config.set("bootstrap:sources", [SPACK_INSTALL_SOURCE])
    source = spack.bootstrap.core.bootstrapping_sources()[0]
    assert source["type"] == "install"

    request = make_request()
    request.probe = lambda concrete_spec: f"probed {concrete_spec.abstract_spec}"
    result = spack.bootstrap.core._install_from_source(request, source)

    ((specs, installer_args, mirrors),) = recording_environment.installs
    assert [x.abstract_spec for x in specs] == [request.abstract_spec]
    assert installer_args == expected_installer_args
    url = spack.mirrors.mirror.Mirror(source["info"]["url"]).fetch_url
    assert mirrors == {"spack-install": url}
    assert result == f"probed {request.abstract_spec}"


def test_a_source_install_concretizes_with_the_request(
    recording_environment, mutable_config, monkeypatch
):
    """Tests that a source install concretizes with ``request.concretize``, and never calls
    ``spack.concretize.concretize_one``.
    """

    def _regular_concretizer(abstract_spec):
        raise AssertionError("concretize_one was called instead of request.concretize")

    monkeypatch.setattr(spack.concretize, "concretize_one", _regular_concretizer)
    mutable_config.set("bootstrap:sources", [SPACK_INSTALL_SOURCE])
    source = spack.bootstrap.core.bootstrapping_sources()[0]

    request = spack.bootstrap.core.BootstrapRequest.for_module(
        "clingo", "clingo-bootstrap", concretize=lambda _: _FakeConcreteSpec("a prototype")
    )
    request.probe = lambda concrete_spec: concrete_spec.abstract_spec

    assert spack.bootstrap.core._install_from_source(request, source) == "a prototype"


@pytest.fixture
def binary_index(mutable_config, mock_packages, monkeypatch):
    """Return an extension in the index of a buildcache, built with the python of another host,
    and the python of this host.
    """

    def concretize_with_python(spec_str, prefix):
        externals = [{"spec": "python@3.8.0", "prefix": prefix}]
        mutable_config.set("packages:python", {"buildable": False, "externals": externals})
        return spack.concretize.concretize_one(spec_str)

    built = concretize_with_python("py-extension1", "/ci/python")
    host_python = concretize_with_python("python", "/host/python")
    monkeypatch.setattr(
        spack.binary_distribution, "update_cache_and_get_specs", lambda config: [built]
    )
    monkeypatch.setattr(spack.bootstrap.core, "host_externals", lambda: [host_python])
    return built, host_python


def test_a_pinned_binary_is_spliced_for_the_host(binary_index):
    built, host_python = binary_index
    sha256 = {built.dag_hash(): "0" * 64}

    result = spack.bootstrap.core._pinned_binary(spack.spec.Spec("py-extension1"), sha256)

    assert result.build_spec.dag_hash() == built.dag_hash()
    assert result["python"].dag_hash() == host_python.dag_hash()
    # The venv is created anew for the python of the host
    assert not result["python-venv"].spliced
    assert result["python-venv"]["python"].dag_hash() == host_python.dag_hash()


@pytest.mark.parametrize(
    "abstract_spec,pinned,host",
    [
        ("py-extension1 ^python@3.7", True, True),
        ("py-extension1", False, True),
        ("py-extension1", True, False),
    ],
    ids=["unsatisfied", "unpinned", "no-host-external"],
)
def test_a_binary_must_be_pinned_and_spliceable(
    abstract_spec, pinned, host, binary_index, monkeypatch
):
    built, _ = binary_index
    if not host:
        monkeypatch.setattr(spack.bootstrap.core, "host_externals", lambda: [])
    sha256 = {built.dag_hash(): "0" * 64} if pinned else {}

    with pytest.raises(RuntimeError, match="no pinned binary"):
        spack.bootstrap.core._pinned_binary(spack.spec.Spec(abstract_spec), sha256)


def test_a_pinned_binary_is_installed_with_its_checksums(binary_index, recording_environment):
    """Tests that the policy is left to the installer, which builds nodes without a binary"""
    built, _ = binary_index
    source = {
        "name": "binaries",
        "type": "buildcache",
        "metadata": "/metadata",
        "info": {"url": "https://example.com"},
        "sha256": {built.dag_hash(): "0" * 64},
    }
    request = spack.bootstrap.core.BootstrapRequest.for_executables(["foo"], "py-extension1")
    request.probe = lambda concrete_spec: concrete_spec

    result = spack.bootstrap.core._install_from_source(request, source)

    ((specs, installer_args, mirrors),) = recording_environment.installs
    assert specs == [result]
    assert installer_args == {"fail_fast": True, "binary_checksums": source["sha256"]}
    assert mirrors == {"binaries": "https://example.com"}


def test_clingo_is_not_concretized_by_the_regular_concretizer(mutable_config, monkeypatch):
    """Among the binaries we have clingo, so we can't concretize that with clingo."""
    requests: List[Any] = []
    monkeypatch.setattr(spack.bootstrap.core, "_python_import", lambda module: False)
    monkeypatch.setattr(
        spack.bootstrap.core,
        "_bootstrap_or_raise",
        lambda request, **kwargs: requests.append(request),
    )

    spack.bootstrap.core.ensure_clingo_importable_or_raise()

    assert requests[0].concretize is spack.bootstrap.core._concretize_clingo


@pytest.fixture
def backtrace_flags(monkeypatch):
    """Return a function setting the two flags that turn tracebacks on. Sets them both
    off to start.
    """

    def _set(**flags: bool) -> None:
        monkeypatch.setattr(spack.error, "debug", flags.get("debug", False))
        monkeypatch.setattr(spack.error, "SHOW_BACKTRACE", flags.get("SHOW_BACKTRACE", False))

    _set()
    return _set


def test_source_failures_point_at_the_backtrace_flag(fake_install, backtrace_flags):
    """Tests that by default the failures are reported without their tracebacks."""
    tried: List[str] = []
    sources = _fake_sources(tried, RuntimeError("boom"))

    with pytest.raises(RuntimeError) as exc_info:
        spack.bootstrap.core._bootstrap_or_raise(
            _fake_request([]), "zlib", RuntimeError, sources=sources
        )

    message = str(exc_info.value)
    assert "boom" in message
    assert 'File "' not in message
    assert "spack --backtrace" in message


@pytest.mark.parametrize("flag", ["debug", "SHOW_BACKTRACE"])
def test_source_failures_include_their_traceback_when_the_flag_is_set(
    fake_install, backtrace_flags, flag
):
    """Tests that either flag turns the tracebacks on, and the hint to enable them off."""
    backtrace_flags(**{flag: True})
    tried: List[str] = []
    sources = _fake_sources(tried, RuntimeError("boom"))

    with pytest.raises(RuntimeError) as exc_info:
        spack.bootstrap.core._bootstrap_or_raise(
            _fake_request([]), "zlib", RuntimeError, sources=sources
        )

    message = str(exc_info.value)
    assert "boom" in message
    assert 'File "' in message and "_fake_install_from_source" in message
    assert "spack --backtrace" not in message
