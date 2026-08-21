# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import json
import pathlib
from typing import Any, Dict, List, Optional

import pytest

import spack.bootstrap
import spack.bootstrap._common
import spack.bootstrap.clingo
import spack.bootstrap.config
import spack.bootstrap.core
import spack.bootstrap.status
import spack.compilers.config
import spack.concretize
import spack.config
import spack.environment
import spack.installer_dispatch
import spack.paths
import spack.spec
import spack.store
import spack.util.executable
from spack.active_environment import active_environment

CLINGO_METADATA = sorted(pathlib.Path(spack.paths.share_path).glob("bootstrap/*/clingo.json"))
if not CLINGO_METADATA:
    raise RuntimeError(f"no clingo metadata in {spack.paths.share_path}")

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


@pytest.mark.regression("22294")
def test_store_is_restored_correctly_after_bootstrap(mutable_config, tmp_path: pathlib.Path):
    """Tests that the store is correctly swapped during bootstrapping, and restored afterward."""
    user_path = str(tmp_path / "store")
    with spack.store.use_store(user_path):
        assert spack.store.STORE.root == user_path
        assert spack.config.CONFIG.get("config:install_tree:root") == user_path
        with spack.bootstrap.ensure_bootstrap_configuration():
            assert spack.store.STORE.root == spack.bootstrap.config.store_path()
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
            assert spack.store.STORE.root == spack.bootstrap.config.store_path()
            assert spack.config.CONFIG.get("config:install_tree:padded_length") == 0
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
        assert spack.store.STORE.root == spack.bootstrap.config.store_path()
        assert (
            spack.config.CONFIG.get("config:install_tree:root")
            == spack.bootstrap.config.store_path()
        )
        assert spack.config.CONFIG.get("config:install_tree:padded_length") == 0
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
    assert not spack.compilers.config.all_compilers(init_config=False)
    with spack.bootstrap.ensure_bootstrap_configuration():
        spack.bootstrap.clingo._add_compilers_if_missing()
        assert spack.compilers.config.all_compilers(init_config=False)
    assert not spack.compilers.config.all_compilers(init_config=False)


@pytest.mark.regression("25992")
@pytest.mark.requires_executables("gcc")
def test_bootstrap_search_for_compilers_with_environment_active(
    no_packages_yaml, active_mock_environment, mock_packages
):
    assert not spack.compilers.config.all_compilers(init_config=False)
    with spack.bootstrap.ensure_bootstrap_configuration():
        spack.bootstrap.clingo._add_compilers_if_missing()
        assert spack.compilers.config.all_compilers(init_config=False)
    assert not spack.compilers.config.all_compilers(init_config=False)


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


@pytest.mark.regression("45247")
def test_use_store_does_not_try_writing_outside_root(
    tmp_path: pathlib.Path, monkeypatch, mutable_config
):
    """Tests that when we use the 'use_store' context manager, there is no attempt at creating
    a Store outside the given root.
    """
    initial_store = mutable_config.get("config:install_tree:root")
    user_store = tmp_path / "store"

    fn = spack.store.Store.__init__

    def _checked_init(self, root, *args, **kwargs):
        fn(self, root, *args, **kwargs)
        assert self.root == str(user_store)

    monkeypatch.setattr(spack.store.Store, "__init__", _checked_init)

    spack.store.reinitialize()
    with spack.store.use_store(user_store):
        assert spack.config.CONFIG.get("config:install_tree:root") == str(user_store)
    assert spack.config.CONFIG.get("config:install_tree:root") == initial_store


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
    """When no source is trusted, the error says so instead of listing failures."""
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
    """A good version string is not enough, the command must also succeed."""
    patchelf = spack.util.executable.Executable(
        str(mock_executable("patchelf", 'echo "patchelf 0.17.2"\nexit 1'))
    )
    assert spack.bootstrap.core.verify_patchelf(patchelf) is False


def _clingo_spec_for(platform: str, target: str, python_version: str) -> spack.spec.Spec:
    """Return the spec a host with the given platform, target and interpreter looks for."""
    parts = [
        x
        for x in spack.bootstrap.core.clingo_root_spec().split()
        if not x.startswith(("platform=", "target="))
    ]
    parts.extend([f"platform={platform}", f"target={target}", f"^python@{python_version}"])
    return spack.spec.Spec(" ".join(parts))


@pytest.mark.regression("52922")
@pytest.mark.parametrize("metadata_file", CLINGO_METADATA, ids=lambda x: x.parent.name)
def test_at_most_one_clingo_binary_matches_an_interpreter(metadata_file: pathlib.Path):
    """A host must select a single clingo binary. When more than one matched, a cold
    bootstrap installed a prefix per interpreter until one of them imported.
    """
    data = json.loads(metadata_file.read_text(encoding="utf-8"))
    entries = [spack.spec.Spec(x["spec"]) for x in data["verified"]]
    combinations = {
        (str(x.architecture.platform), str(x.architecture.target), str(x["python"].versions))
        for x in entries
    }

    for platform, target, python_version in sorted(combinations):
        abstract_spec = _clingo_spec_for(platform, target, python_version)
        matching = spack.bootstrap.core._matching_entries(data, abstract_spec)
        assert len(matching) <= 1, [str(x["spec"]) for x in matching]


class _FakeBootstrapper(spack.bootstrap.core.Bootstrapper):
    """Bootstrapper returning a canned result, or raising it when it is an exception."""

    def __init__(self, conf: Dict[str, Any]) -> None:
        self.name = conf["name"]
        self.result = conf["result"]
        self.tried = conf["tried"]

    def try_to_bootstrap(self, request):
        self.tried.append(self.name)
        if isinstance(self.result, Exception):
            raise self.result
        return self.result


@pytest.fixture
def fake_bootstrap_type(monkeypatch):
    """Register a bootstrapper type used by the sources built with ``_fake_sources``."""
    monkeypatch.setitem(spack.bootstrap.core._bootstrap_methods, "fake", _FakeBootstrapper)


def _fake_sources(tried: List[str], *results: Any) -> List[Dict[str, Any]]:
    """Return one source per result, appending its name to ``tried`` when it is used."""
    return [
        {"name": f"src{i}", "type": "fake", "result": x, "tried": tried}
        for i, x in enumerate(results)
    ]


def _fake_request(probes: List[Any], result: Optional[str] = None):
    """Return a request whose probe records its calls and returns ``result``."""

    def probe(query_spec):
        probes.append(query_spec)
        return result

    return spack.bootstrap.core.BootstrapRequest(
        abstract_spec=spack.spec.Spec("zlib"), metadata_name="zlib", probe=probe, installer_args={}
    )


def test_the_store_is_probed_once_for_all_the_sources(fake_bootstrap_type):
    """The store does not depend on the source, so it is queried once, before the loop."""
    probes: List[Any] = []
    tried: List[str] = []
    sources = _fake_sources(tried, RuntimeError("no"), RuntimeError("no"), RuntimeError("no"))

    with pytest.raises(RuntimeError, match="cannot bootstrap zlib"):
        spack.bootstrap.core._bootstrap_or_raise(
            _fake_request(probes), "zlib", "zlib", RuntimeError, sources=sources
        )

    assert len(probes) == 1
    assert tried == ["src0", "src1", "src2"]


def test_software_in_the_store_skips_every_source(fake_bootstrap_type):
    """When the probe finds the software, no source is tried."""
    probes: List[Any] = []
    tried: List[str] = []
    sources = _fake_sources(tried, "from the source")

    result = spack.bootstrap.core._bootstrap_or_raise(
        _fake_request(probes, result="from the store"),
        "zlib",
        "zlib",
        RuntimeError,
        sources=sources,
    )

    assert result == "from the store"
    assert tried == []


def test_the_first_successful_source_wins(fake_bootstrap_type):
    probes: List[Any] = []
    tried: List[str] = []
    sources = _fake_sources(tried, RuntimeError("no"), "from src1", "from src2")

    result = spack.bootstrap.core._bootstrap_or_raise(
        _fake_request(probes), "zlib", "zlib", RuntimeError, sources=sources
    )

    assert result == "from src1"
    assert tried == ["src0", "src1"]


def test_every_source_failure_is_reported(fake_bootstrap_type):
    """The last failure is rarely the interesting one, so all of them are reported."""
    probes: List[Any] = []
    tried: List[str] = []
    sources = _fake_sources(tried, RuntimeError("first boom"), ValueError("second boom"))

    with pytest.raises(RuntimeError) as exc_info:
        spack.bootstrap.core._bootstrap_or_raise(
            _fake_request(probes), "zlib", "zlib", RuntimeError, sources=sources
        )

    message = str(exc_info.value)
    for expected in ("src0", "first boom", "src1", "second boom"):
        assert expected in message


def test_sources_that_provide_nothing_are_reported_as_such(fake_bootstrap_type):
    """A source can decline without failing, e.g. when no binary matches the interpreter."""
    probes: List[Any] = []
    tried: List[str] = []
    sources = _fake_sources(tried, None, None)

    with pytest.raises(RuntimeError, match="no bootstrapping source could provide it"):
        spack.bootstrap.core._bootstrap_or_raise(
            _fake_request(probes), "zlib", "zlib", RuntimeError, sources=sources
        )

    assert tried == ["src0", "src1"]


def test_no_sources_to_try_is_reported_as_such(fake_bootstrap_type):
    """Without sources there is no failure to report, so the message says why."""
    probes: List[Any] = []

    with pytest.raises(RuntimeError, match='from spec "zlib": no bootstrapping sources'):
        spack.bootstrap.core._bootstrap_or_raise(
            _fake_request(probes), "zlib", "zlib", RuntimeError, sources=[]
        )


#: The source, shipped with Spack, that builds the software it needs from sources
SPACK_INSTALL_SOURCE = {
    "name": "spack-install",
    "metadata": "$spack/share/spack/bootstrap/spack-install",
}


class _RecordingInstaller:
    """Stand-in for ``create_installer``, recording what it is asked to install."""

    def __init__(self) -> None:
        self.packages: Any = None
        self.installer_args: Optional[Dict[str, Any]] = None
        self.mirrors_when_installing: Optional[Dict[str, Any]] = None

    def __call__(self, packages: Any, **installer_args: Any) -> "_RecordingInstaller":
        self.packages = packages
        self.installer_args = installer_args
        return self

    def install(self) -> None:
        self.mirrors_when_installing = spack.config.CONFIG.get("mirrors")


class _FakeConcreteSpec:
    """Stand-in for the result of concretization, carrying a recognizable package."""

    def __init__(self, abstract_spec: Any) -> None:
        self.abstract_spec = abstract_spec
        self.package = f"package of {abstract_spec}"


@pytest.fixture
def recording_installer(monkeypatch):
    """Let the source bootstrapper run without detecting, concretizing or installing."""
    installer = _RecordingInstaller()
    monkeypatch.setattr(spack.bootstrap.core, "_add_externals_if_missing", lambda: None)
    monkeypatch.setattr(spack.concretize, "concretize_one", _FakeConcreteSpec)
    monkeypatch.setattr(spack.installer_dispatch, "create_installer", installer)
    return installer


def test_the_install_type_maps_to_the_source_bootstrapper(mutable_config):
    """Tests that the source shipped with Spack to build from sources is dispatched to the
    right class.
    """
    mutable_config.set("bootstrap:sources", [SPACK_INSTALL_SOURCE])
    conf = spack.bootstrap.core.bootstrapping_sources()[0]
    assert conf["type"] == "install"
    assert isinstance(
        spack.bootstrap.core.create_bootstrapper(conf), spack.bootstrap.core.SourceBootstrapper
    )


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
            {},
        ),
    ],
    ids=["module", "executable"],
)
def test_the_source_bootstrapper_installs_from_its_own_mirror(
    make_request, expected_installer_args, recording_installer, mutable_config
):
    """Tests that the request decides what is installed and how, the source decides where it
    comes from.
    """
    mutable_config.set("bootstrap:sources", [SPACK_INSTALL_SOURCE])
    conf = spack.bootstrap.core.bootstrapping_sources()[0]
    bootstrapper = spack.bootstrap.core.create_bootstrapper(conf)

    request = make_request()
    request.probe = lambda concrete_spec: f"probed {concrete_spec.package}"
    result = bootstrapper.try_to_bootstrap(request)

    assert recording_installer.packages == [f"package of {request.abstract_spec}"]
    assert recording_installer.installer_args == expected_installer_args
    assert recording_installer.mirrors_when_installing == {"spack-install": bootstrapper.url}
    assert result == f"probed package of {request.abstract_spec}"


def test_clingo_is_not_concretized_by_the_regular_concretizer(
    recording_installer, mutable_config, monkeypatch
):
    """Among the binaries we have clingo, so we can't concretize that with clingo."""

    class _FakeClingoConcretizer:
        def __init__(self, configuration) -> None:
            self.configuration = configuration

        def concretize(self) -> "_FakeConcreteSpec":
            return _FakeConcreteSpec("the clingo prototype")

    def _regular_concretizer(abstract_spec):
        raise AssertionError("clingo must not go through the regular concretizer")

    monkeypatch.setattr(spack.concretize, "concretize_one", _regular_concretizer)
    monkeypatch.setattr(spack.bootstrap.core, "ClingoBootstrapConcretizer", _FakeClingoConcretizer)

    mutable_config.set("bootstrap:sources", [SPACK_INSTALL_SOURCE])
    conf = spack.bootstrap.core.bootstrapping_sources()[0]
    bootstrapper = spack.bootstrap.core.create_bootstrapper(conf)

    request = spack.bootstrap.core.BootstrapRequest.for_module("clingo", "clingo-bootstrap")
    request.probe = lambda concrete_spec: concrete_spec.package

    assert bootstrapper.try_to_bootstrap(request) == "package of the clingo prototype"
