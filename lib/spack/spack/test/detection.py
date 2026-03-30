# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import collections
import pathlib

import pytest

import spack.config
import spack.detection
import spack.detection.path
import spack.repo
import spack.spec
from spack.detection.common import DetectedDependency, _normalize_dependency
from spack.detection.path import _prefix_hints_from_unresolved_deps, by_path_with_dependencies


def test_detection_update_config(mutable_config):
    # mock detected package
    detected_packages = collections.defaultdict(list)
    detected_packages["cmake"] = [spack.spec.Spec("cmake@3.27.5", external_path="/usr/bin")]

    # update config for new package
    spack.detection.update_configuration(detected_packages)
    # Check entries in 'packages.yaml'
    packages_yaml = spack.config.get("packages")
    assert "cmake" in packages_yaml
    assert "externals" in packages_yaml["cmake"]
    externals = packages_yaml["cmake"]["externals"]
    assert len(externals) == 1
    external_gcc = externals[0]
    assert external_gcc["spec"] == "cmake@3.27.5"
    assert external_gcc["prefix"] == "/usr/bin"


def test_dedupe_paths(tmp_path: pathlib.Path):
    """Test that ``dedupe_paths`` deals with symlinked directories, retaining the target"""
    x = tmp_path / "x"
    y = tmp_path / "y"
    z = tmp_path / "z"

    x.mkdir()
    y.mkdir()
    z.symlink_to("x", target_is_directory=True)

    # dedupe repeated dirs, should preserve order
    assert spack.detection.path.dedupe_paths([str(x), str(y), str(x)]) == [str(x), str(y)]
    assert spack.detection.path.dedupe_paths([str(y), str(x), str(y)]) == [str(y), str(x)]

    # dedupe repeated symlinks
    assert spack.detection.path.dedupe_paths([str(z), str(y), str(z)]) == [str(z), str(y)]
    assert spack.detection.path.dedupe_paths([str(y), str(z), str(y)]) == [str(y), str(z)]

    # when both symlink and target are present, only target is retained, and it comes at the
    # priority of the first occurrence.
    assert spack.detection.path.dedupe_paths([str(x), str(y), str(z)]) == [str(x), str(y)]
    assert spack.detection.path.dedupe_paths([str(z), str(y), str(x)]) == [str(x), str(y)]
    assert spack.detection.path.dedupe_paths([str(y), str(z), str(x)]) == [str(y), str(x)]


@pytest.mark.usefixtures("mock_packages")
def test_detect_specs_deduplicates_across_prefixes(tmp_path, monkeypatch):
    """Tests that the same spec detected at two different prefixes should yield only one result.

    Returning both causes duplicate externals in packages.yaml and non-deterministic hashes
    during concretization.
    """
    # Create two independent bin/ directories, each containing the same executable name.
    prefix_a = tmp_path / "prefix_a"
    prefix_b = tmp_path / "prefix_b"
    (prefix_a / "bin").mkdir(parents=True)
    (prefix_b / "bin").mkdir(parents=True)
    exe_a = prefix_a / "bin" / "cmake"
    exe_b = prefix_b / "bin" / "cmake"
    exe_a.touch()
    exe_b.touch()

    cmake_cls = spack.repo.PATH.get_pkg_class("cmake")

    # Patch determine_spec_details to always return the same spec, regardless of prefix.
    @classmethod
    def _same_spec(cls, prefix, exes_in_prefix):
        return spack.spec.Spec("cmake@3.17.1")

    monkeypatch.setattr(cmake_cls, "determine_spec_details", _same_spec)

    finder = spack.detection.path.ExecutablesFinder()
    detected = finder.detect_specs(
        pkg=cmake_cls, paths=[str(exe_a), str(exe_b)], repo_path=spack.repo.PATH
    )

    # Both prefixes produce cmake@3.17.1; only the first should be kept.
    assert len(detected) == 1


def _make_detected(pkg_name, version, prefix):
    """Return a Spec with the external path set, as detection would produce."""
    return spack.spec.Spec(f"{pkg_name}@{version}", external_path=prefix)


def _run_pipeline(detected, *, configuration):
    """Run one round of the detect -> resolve -> write pipeline against the current config.

    Reads known packages from whatever is already in ``packages`` config, resolves dependencies for
    ``detected``, and writes the result back.
    """
    packages_yaml = configuration.get_config("packages")
    known = [
        spack.spec.Spec(entry["spec"], external_path=entry.get("prefix", ""))
        for pkg_cfg in packages_yaml.values()
        if isinstance(pkg_cfg, dict)
        for entry in pkg_cfg.get("externals", [])
    ]
    raw_deps = spack.detection.collect_dependencies(detected)
    deps = spack.detection.determine_external_dependencies(
        detected_packages=detected, detected_dependencies=raw_deps, known_packages=known
    )
    spack.detection.update_configuration(detected, resolved_dependencies=deps)


@pytest.mark.parametrize(
    "dep_kwargs,expected_dep_keys,unexpected_dep_keys",
    [
        # No explicit deptypes or virtuals — only 'id' in the dependency entry
        ({}, ["id"], ["deptypes", "virtuals"]),
        # Explicit deptypes serialised as a list
        ({"deptypes": ("link", "run")}, ["id", "deptypes"], ["virtuals"]),
        # Explicit virtuals serialised as a comma-separated string
        ({"virtuals": ("mpi",)}, ["id", "virtuals"], ["deptypes"]),
    ],
)
def test_update_config_insert_with_dependencies(
    mutable_config, dep_kwargs, expected_dep_keys, unexpected_dep_keys
):
    """Tests that new external entries are written with 'id' and 'dependencies' fields."""
    mpich = _make_detected("mpich", "4.0", "/usr/local/mpich")
    hwloc = _make_detected("hwloc", "2.7", "/usr/local/hwloc")

    detected_packages = {"mpich": [mpich], "hwloc": [hwloc]}
    detected_dependencies = {mpich: [DetectedDependency(spec=hwloc, **dep_kwargs)]}

    spack.detection.update_configuration(
        detected_packages, resolved_dependencies=detected_dependencies
    )

    packages_yaml = mutable_config.get_config("packages")

    # Both packages must appear
    assert "mpich" in packages_yaml and "hwloc" in packages_yaml

    mpich_entries = packages_yaml["mpich"]["externals"]
    hwloc_entries = packages_yaml["hwloc"]["externals"]
    assert len(mpich_entries) == 1 and len(hwloc_entries) == 1

    mpich_entry, hwloc_entry = mpich_entries[0], hwloc_entries[0]

    # Both get 'id' because they participate in a dependency relationship
    assert "id" in mpich_entry and "id" in hwloc_entry

    # mpich references hwloc via 'dependencies'
    assert "dependencies" in mpich_entry
    assert len(mpich_entry["dependencies"]) == 1
    dep = mpich_entry["dependencies"][0]
    assert dep["id"] == hwloc_entry["id"]

    for key in expected_dep_keys:
        assert key in dep
    for key in unexpected_dep_keys:
        assert key not in dep

    # hwloc is a leaf: no 'dependencies' key
    assert "dependencies" not in hwloc_entry


def test_update_config_non_participating_spec_has_no_id(mutable_config):
    """Tests that specs that are not part of any dependency relationship must not get an 'id'"""
    cmake = _make_detected("cmake", "3.27.5", "/usr/bin")
    mpich = _make_detected("mpich", "4.0", "/usr/local/mpich")
    hwloc = _make_detected("hwloc", "2.7", "/usr/local/hwloc")

    detected_packages = {"cmake": [cmake], "mpich": [mpich], "hwloc": [hwloc]}
    detected_dependencies = {mpich: [DetectedDependency(spec=hwloc)]}

    spack.detection.update_configuration(
        detected_packages, resolved_dependencies=detected_dependencies
    )

    packages_yaml = mutable_config.get_config("packages")
    cmake_entry = packages_yaml["cmake"]["externals"][0]
    assert "id" not in cmake_entry


def test_update_config_augments_existing_entry(mutable_config):
    """Tests that pre-existing entries get an 'id' backfilled but never a 'dependencies' field"""
    mpich = _make_detected("mpich", "4.0", "/usr/local/mpich")
    hwloc = _make_detected("hwloc", "2.7", "/usr/local/hwloc")

    detected_packages = {"mpich": [mpich], "hwloc": [hwloc]}

    # First call: write entries without dependency info (simulating an older Spack run)
    spack.detection.update_configuration(detected_packages)
    pkgs_before = mutable_config.get_config("packages")
    assert "id" not in pkgs_before["mpich"]["externals"][0]

    # Second call: same specs but now with dependency information
    detected_dependencies = {mpich: [DetectedDependency(spec=hwloc)]}
    spack.detection.update_configuration(
        detected_packages, resolved_dependencies=detected_dependencies
    )

    packages_yaml = mutable_config.get_config("packages")
    mpich_entry = packages_yaml["mpich"]["externals"][0]

    # Original fields must be preserved
    assert mpich_entry["spec"] == "mpich@4.0"
    assert mpich_entry["prefix"] == "/usr/local/mpich"

    # 'id' is backfilled so this entry can be referenced; 'dependencies' is never added
    # to a pre-existing entry — the manually written (or absent) state is authoritative.
    assert "id" in mpich_entry
    assert "dependencies" not in mpich_entry


def test_update_config_preserves_existing_dependencies(mutable_config):
    """Tests that auto-detection never overwrites pre-existing 'dependencies' fields"""
    mpich = _make_detected("mpich", "4.0", "/usr/local/mpich")
    hwloc = _make_detected("hwloc", "2.7", "/usr/local/hwloc")

    detected_packages = {"mpich": [mpich], "hwloc": [hwloc]}

    # The first call writes a fresh entry that includes dependencies
    spack.detection.update_configuration(
        detected_packages, resolved_dependencies={mpich: [DetectedDependency(spec=hwloc)]}
    )
    original_deps = mutable_config.get("packages")["mpich"]["externals"][0]["dependencies"]

    # The second call must not touch the dependencies that are now part of the stored entry
    # and must warn the user that auto-detected dependencies were suppressed.
    with pytest.warns(UserWarning, match="mpich@4.0.*skipping auto-detected dependencies"):
        spack.detection.update_configuration(
            detected_packages, resolved_dependencies={mpich: [DetectedDependency(spec=hwloc)]}
        )

    packages_yaml = mutable_config.get_config("packages")
    assert packages_yaml["mpich"]["externals"][0]["dependencies"] == original_deps


def test_update_config_without_dependencies_is_unchanged(mutable_config):
    """Tests that calling update_configuration without detected_dependencies preserves existing
    behavior.
    """
    detected_packages = collections.defaultdict(list)
    detected_packages["cmake"] = [spack.spec.Spec("cmake@3.27.5", external_path="/usr/bin")]

    spack.detection.update_configuration(detected_packages)

    entry = mutable_config.get_config("packages")["cmake"]["externals"][0]
    assert "id" not in entry
    assert "dependencies" not in entry


@pytest.fixture()
def mock_deps(monkeypatch):

    def _detect(pkg_cls, *, dependencies):
        @classmethod
        def _deps(cls, spec):
            return dependencies

        monkeypatch.setattr(pkg_cls, "determine_dependencies", _deps, raising=False)

    return _detect


def _make_pkg_with_determine_deps(pkg_name, dependencies):
    """Return a classmethod suitable for monkeypatching determine_dependencies."""

    @classmethod
    def _determine_dependencies(cls, spec):
        return dependencies

    return _determine_dependencies


# ── tests for determine_external_dependencies ─────────────────────────────────


@pytest.mark.usefixtures("mock_packages")
@pytest.mark.parametrize(
    "dep_return,expected_deptypes",
    [
        # Bare str — parsed to Spec, deptypes remain None
        (["mpich@4.0"], None),
        # Dict with str spec and explicit deptypes
        ([{"spec": "mpich@4.0", "deptypes": ("link", "run")}], ("link", "run")),
        # Dict with str spec, no deptypes
        ([{"spec": "mpich@4.0"}], None),
    ],
)
def test_determine_external_dependencies_resolves(mock_deps, dep_return, expected_deptypes):
    """Tests that str and dict returns are normalized and resolved correctly."""
    cmake = spack.spec.Spec("cmake@3.27.5", external_path="/usr/bin")
    mpich = spack.spec.Spec("mpich@4.0", external_path="/usr/local/mpich")
    detected = {"cmake": [cmake], "mpich": [mpich]}

    cmake_cls = spack.repo.PATH.get_pkg_class("cmake")
    mock_deps(cmake_cls, dependencies=dep_return)

    raw_deps = spack.detection.collect_dependencies(detected)
    result = spack.detection.determine_external_dependencies(
        detected_packages=detected, detected_dependencies=raw_deps
    )

    assert len(result) == 1 and cmake in result
    deps = result[cmake]
    assert len(deps) == 1
    # The resolved spec must be the *same object* as mpich (not just an equal spec).
    assert deps[0].spec is mpich and deps[0].deptypes == expected_deptypes


@pytest.mark.usefixtures("mock_packages")
def test_determine_external_dependencies_dict_unknown_keys(mock_deps):
    """Tests that a dict with unknown keys produces a warning and the unknown keys are ignored"""
    cmake = spack.spec.Spec("cmake@3.27.5", external_path="/usr/bin")
    mpich = spack.spec.Spec("mpich@4.0", external_path="/usr/local/mpich")
    detected = {"cmake": [cmake], "mpich": [mpich]}

    cmake_cls = spack.repo.PATH.get_pkg_class("cmake")
    mock_deps(cmake_cls, dependencies=[{"spec": "mpich@4.0", "typo_key": "oops"}])

    with pytest.warns(UserWarning, match="unknown keys.*typo_key"):
        raw_deps = spack.detection.collect_dependencies(detected)

    assert cmake in raw_deps
    assert raw_deps[cmake][0].spec.satisfies("mpich@4.0")


@pytest.mark.usefixtures("mock_packages")
def test_determine_external_dependencies_no_method():
    """Tests that packages without determine_dependencies produce no output."""
    cmake = spack.spec.Spec("cmake@3.27.5", external_path="/usr/bin")
    detected = {"cmake": [cmake]}

    raw_deps = spack.detection.collect_dependencies(detected)
    result = spack.detection.determine_external_dependencies(
        detected_packages=detected, detected_dependencies=raw_deps
    )

    assert result == {}


@pytest.mark.usefixtures("mock_packages")
def test_determine_external_dependencies_zero_matches(mock_deps):
    """Tests that a dependency spec that matches no detected spec is warned about and skipped"""
    cmake = spack.spec.Spec("cmake@3.27.5", external_path="/usr/bin")
    detected = {"cmake": [cmake]}  # mpich is NOT detected

    cmake_cls = spack.repo.PATH.get_pkg_class("cmake")
    mock_deps(cmake_cls, dependencies=["mpich@4.0"])

    raw_deps = spack.detection.collect_dependencies(detected)
    with pytest.warns(UserWarning, match="mpich"):
        result = spack.detection.determine_external_dependencies(
            detected_packages=detected, detected_dependencies=raw_deps
        )

    assert result == {}


@pytest.mark.usefixtures("mock_packages")
def test_determine_external_dependencies_multiple_matches(mock_deps):
    """A dependency spec matching multiple detected specs is warned about and skipped."""
    mpileaks = spack.spec.Spec("mpileaks@2.3", external_path="/usr/bin")
    mpich_40 = spack.spec.Spec("mpich@4.0", external_path="/usr/local/mpich40")
    mpich_41 = spack.spec.Spec("mpich@4.1", external_path="/usr/local/mpich41")
    detected = {"mpileaks": [mpileaks], "mpich": [mpich_40, mpich_41]}

    mpileaks_cls = spack.repo.PATH.get_pkg_class("mpileaks")
    # "mpich" (no version) matches both mpich@4.0 and mpich@4.1.
    mock_deps(mpileaks_cls, dependencies=["mpich"])

    raw_deps = spack.detection.collect_dependencies(detected)
    with pytest.warns(UserWarning, match="ambiguous"):
        result = spack.detection.determine_external_dependencies(
            detected_packages=detected, detected_dependencies=raw_deps
        )

    assert result == {}


@pytest.mark.usefixtures("mock_packages")
def test_determine_external_dependencies_exception_is_skipped(monkeypatch):
    """Tests that an exception from determine_dependencies is caught, warned about, and skipped"""
    cmake = spack.spec.Spec("cmake@3.27.5", external_path="/usr/bin")
    detected = {"cmake": [cmake]}

    @classmethod
    def _raises(cls, spec):
        raise RuntimeError("boom")

    cmake_cls = spack.repo.PATH.get_pkg_class("cmake")
    monkeypatch.setattr(cmake_cls, "determine_dependencies", _raises, raising=False)

    with pytest.warns(UserWarning, match="boom"):
        raw_deps = spack.detection.collect_dependencies(detected)
    result = spack.detection.determine_external_dependencies(
        detected_packages=detected, detected_dependencies=raw_deps
    )

    assert result == {}


@pytest.mark.usefixtures("mock_packages")
def test_determine_external_dependencies_empty_return(mock_deps):
    """Tests that an empty list from determine_dependencies produces no output."""
    cmake = spack.spec.Spec("cmake@3.27.5", external_path="/usr/bin")
    detected = {"cmake": [cmake]}

    cmake_cls = spack.repo.PATH.get_pkg_class("cmake")
    mock_deps(cmake_cls, dependencies=[])

    raw_deps = spack.detection.collect_dependencies(detected)
    result = spack.detection.determine_external_dependencies(
        detected_packages=detected, detected_dependencies=raw_deps
    )

    assert result == {}


@pytest.mark.usefixtures("mock_packages")
def test_determine_external_dependencies_partial_resolution(mock_deps):
    """Tests that only fully resolved dependencies are kept, while unresolved ones are warned
    and skipped.
    """
    cmake = spack.spec.Spec("cmake@3.27.5", external_path="/usr/bin")
    mpich = spack.spec.Spec("mpich@4.0", external_path="/usr/local/mpich")
    detected = {"cmake": [cmake], "mpich": [mpich]}

    cmake_cls = spack.repo.PATH.get_pkg_class("cmake")
    # mpich resolves (1 match); hwloc does not (0 matches → warning).
    mock_deps(cmake_cls, dependencies=["mpich@4.0", "hwloc@2.7"])

    raw_deps = spack.detection.collect_dependencies(detected)
    with pytest.warns(UserWarning, match="hwloc"):
        result = spack.detection.determine_external_dependencies(
            detected_packages=detected, detected_dependencies=raw_deps
        )

    assert cmake in result and len(result[cmake]) == 1
    assert result[cmake][0].spec is mpich


@pytest.mark.usefixtures("mock_packages")
def test_determine_external_dependencies_resolves_against_known_packages(mock_deps):
    """Tests that a dep not in detected_packages but present in known_packages resolves
    correctly.
    """
    mpich = _make_detected("mpich", "4.0", "/usr/local/mpich")
    hwloc = _make_detected("hwloc", "2.7", "/usr/local/hwloc")

    detected = {"mpich": [mpich]}  # hwloc is NOT detected
    known = [hwloc]  # hwloc IS in known_packages

    mpich_cls = spack.repo.PATH.get_pkg_class("mpich")
    mock_deps(mpich_cls, dependencies=["hwloc@2.7"])

    raw_deps = spack.detection.collect_dependencies(detected)
    result = spack.detection.determine_external_dependencies(
        detected_packages=detected, detected_dependencies=raw_deps, known_packages=known
    )

    assert mpich in result and len(result[mpich]) == 1
    assert result[mpich][0].spec is hwloc


@pytest.mark.usefixtures("mock_packages")
def test_determine_external_dependencies_prefers_known_over_detected(mock_deps):
    """Tests that when both known_packages and detected_packages match, known_packages wins"""
    mpich = _make_detected("mpich", "4.0", "/usr/local/mpich")
    hwloc_known = _make_detected("hwloc", "2.7", "/usr/local/hwloc-old")
    hwloc_detected = _make_detected("hwloc", "2.7", "/usr/local/hwloc-new")

    detected = {"mpich": [mpich], "hwloc": [hwloc_detected]}
    known = [hwloc_known]

    mpich_cls = spack.repo.PATH.get_pkg_class("mpich")
    mock_deps(mpich_cls, dependencies=["hwloc@2.7"])

    raw_deps = spack.detection.collect_dependencies(detected)
    result = spack.detection.determine_external_dependencies(
        detected_packages=detected, detected_dependencies=raw_deps, known_packages=known
    )

    assert mpich in result
    # known_packages entry (hwloc_known) is preferred over the freshly detected one.
    assert result[mpich][0].spec is hwloc_known


@pytest.mark.usefixtures("mock_packages")
def test_determine_external_dependencies_idempotent_from_empty(mutable_config, mock_deps):
    """Tests that running the pipeline twice from an empty config produces stable config."""
    mpich = _make_detected("mpich", "4.0", "/usr/local/mpich")
    hwloc = _make_detected("hwloc", "2.7", "/usr/local/hwloc")
    detected = {"mpich": [mpich], "hwloc": [hwloc]}

    mpich_cls = spack.repo.PATH.get_pkg_class("mpich")
    mock_deps(mpich_cls, dependencies=["hwloc@2.7"])

    _run_pipeline(detected, configuration=mutable_config)
    pkgs_first = spack.config.get("packages")

    _run_pipeline(detected, configuration=mutable_config)
    pkgs_second = spack.config.get("packages")

    # IDs and deps must be identical after the second run.
    assert pkgs_first == pkgs_second


@pytest.mark.usefixtures("mock_packages")
def test_determine_external_dependencies_idempotent_partial_initial(mutable_config, mock_deps):
    """Tests that running pipeline when a package is already in YAML (no id) augments and then
    stabilizes.
    """
    mpich = _make_detected("mpich", "4.0", "/usr/local/mpich")
    hwloc = _make_detected("hwloc", "2.7", "/usr/local/hwloc")

    # Pre-populate config with hwloc only (no id, no deps).
    spack.detection.update_configuration({"hwloc": [hwloc]})
    pkgs_before = spack.config.get("packages")
    assert "id" not in pkgs_before["hwloc"]["externals"][0]

    mpich_cls = spack.repo.PATH.get_pkg_class("mpich")
    mock_deps(mpich_cls, dependencies=["hwloc@2.7"])

    detected_mpich = {"mpich": [mpich]}

    _run_pipeline(detected_mpich, configuration=mutable_config)
    packages_yaml_first = spack.config.get("packages")

    # hwloc must have been augmented with an id.
    assert "id" in packages_yaml_first["hwloc"]["externals"][0]
    hwloc_id = packages_yaml_first["hwloc"]["externals"][0]["id"]

    _run_pipeline(detected_mpich, configuration=mutable_config)
    packages_yaml_second = spack.config.get("packages")

    # Second run must not change anything.
    assert packages_yaml_second == packages_yaml_first
    assert packages_yaml_second["hwloc"]["externals"][0]["id"] == hwloc_id


@pytest.mark.usefixtures("mock_packages")
def test_determine_external_dependencies_idempotent_existing_deps(mutable_config, mock_deps):
    """Tests that entries that already have dependencies are left untouched by subsequent runs"""
    mpich = _make_detected("mpich", "4.0", "/usr/local/mpich")
    hwloc = _make_detected("hwloc", "2.7", "/usr/local/hwloc")

    mpich_cls = spack.repo.PATH.get_pkg_class("mpich")
    mock_deps(mpich_cls, dependencies=["mpich", "hwloc@2.7"])
    detected_both = {"mpich": [mpich], "hwloc": [hwloc]}

    # The first run writes everything fresh
    _run_pipeline(detected_both, configuration=mutable_config)
    pkgs_after_first = spack.config.get("packages")
    mpich_deps_first = pkgs_after_first["mpich"]["externals"][0]["dependencies"]

    # Second run — deps already present, must not overwrite
    _run_pipeline(detected_both, configuration=mutable_config)
    pkgs_after_second = spack.config.get("packages")
    assert pkgs_after_second == pkgs_after_first
    assert pkgs_after_second["mpich"]["externals"][0]["dependencies"] == mpich_deps_first


@pytest.mark.not_on_windows("Uses POSIX paths")
def test_normalize_dependency_dict_with_prefix():
    """Tests that a dict hint with 'prefix' sets external_path on the resulting spec."""
    dep = _normalize_dependency({"spec": "hwloc@2.7", "prefix": "/opt/hwloc"})
    assert dep.spec.external_path == "/opt/hwloc"
    assert dep.spec.satisfies("hwloc@2.7")


def test_normalize_dependency_dict_without_prefix():
    """Tests that a dict hint without 'prefix' leaves external_path unset."""
    dep = _normalize_dependency({"spec": "hwloc@2.7"})
    assert not dep.spec.external_path


def test_normalize_dependency_bare_string_no_prefix():
    """Tests that a bare string produces a spec with no external_path."""
    dep = _normalize_dependency("hwloc@2.7")
    assert not dep.spec.external_path


@pytest.mark.not_on_windows("Uses POSIX paths")
def test_prefix_hints_returns_hint_for_unresolved_dep():
    """Tests that external_path is returned as a hint when the dep is not yet resolved."""
    mpich = spack.spec.Spec("mpich@4.0", external_path="/usr/local/mpich")
    hwloc_dep = _normalize_dependency({"spec": "hwloc@2.7", "prefix": "/opt/hwloc"})

    detected_packages = {"mpich": [mpich]}
    detected_dependencies = {mpich: [hwloc_dep]}

    hints = _prefix_hints_from_unresolved_deps(detected_dependencies, detected_packages, [])
    assert "/opt/hwloc" in hints


@pytest.mark.not_on_windows("Uses POSIX paths")
def test_prefix_hints_excludes_already_resolved_dep():
    """Tests that no hint is returned when the dep is already in detected_packages."""
    mpich = spack.spec.Spec("mpich@4.0", external_path="/usr/local/mpich")
    hwloc_detected = spack.spec.Spec("hwloc@2.7", external_path="/usr/local/hwloc")
    hwloc_dep = _normalize_dependency({"spec": "hwloc@2.7", "prefix": "/opt/hwloc"})

    detected_packages = {"mpich": [mpich], "hwloc": [hwloc_detected]}
    detected_dependencies = {mpich: [hwloc_dep]}

    hints = _prefix_hints_from_unresolved_deps(detected_dependencies, detected_packages, [])
    assert hints == []


@pytest.mark.not_on_windows("Uses POSIX paths")
def test_prefix_hints_excludes_dep_satisfied_by_known_packages():
    """Tests that no hint is returned when the dep is satisfied by known_packages."""
    mpich = spack.spec.Spec("mpich@4.0", external_path="/usr/local/mpich")
    hwloc_known = spack.spec.Spec("hwloc@2.7", external_path="/usr/local/hwloc")
    hwloc_dep = _normalize_dependency({"spec": "hwloc@2.7", "prefix": "/opt/hwloc"})

    detected_packages = {"mpich": [mpich]}
    detected_dependencies = {mpich: [hwloc_dep]}

    hints = _prefix_hints_from_unresolved_deps(
        detected_dependencies, detected_packages, [hwloc_known]
    )
    assert hints == []


@pytest.mark.not_on_windows("Uses POSIX paths")
def test_prefix_hints_no_hint_for_abstract_dep():
    """Tests that a dep with no external_path (bare string) yields no path hint"""
    mpich = spack.spec.Spec("mpich@4.0", external_path="/usr/local/mpich")
    hwloc_dep = _normalize_dependency("hwloc@2.7")

    detected_packages = {"mpich": [mpich]}
    detected_dependencies = {mpich: [hwloc_dep]}

    hints = _prefix_hints_from_unresolved_deps(detected_dependencies, detected_packages, [])
    assert hints == []


@pytest.mark.usefixtures("mock_packages")
@pytest.mark.not_on_windows("Uses POSIX paths")
def test_by_path_with_dependencies_uses_prefix_hint(monkeypatch):
    """Tests that the detection loop passes dep prefix hints to subsequent by_path calls"""
    hwloc_prefix = "/opt/hwloc"
    mpich = spack.spec.Spec("mpich@4.0", external_path="/usr/local/mpich")
    hwloc = spack.spec.Spec("hwloc@2.7", external_path=hwloc_prefix)

    mpich_cls = spack.repo.PATH.get_pkg_class("mpich")

    @classmethod
    def _deps(cls, spec):
        return [{"spec": "hwloc@2.7", "prefix": hwloc_prefix}]

    monkeypatch.setattr(mpich_cls, "determine_dependencies", _deps, raising=False)

    # Track what path_hints each by_path call receives.
    call_hints: list = []
    call_count = {"n": 0}

    def fake_by_path(pkgs, *, path_hints=None, max_workers=None):
        call_hints.append(path_hints)
        call_count["n"] += 1
        if call_count["n"] == 1:
            return {"mpich": [mpich]}
        # Second call: return hwloc only if the prefix hint was injected.
        if path_hints and hwloc_prefix in path_hints:
            return {"hwloc": [hwloc]}
        return {}

    monkeypatch.setattr(spack.detection.path, "by_path", fake_by_path)
    monkeypatch.setattr(
        spack.detection.path, "packages_to_search_for", lambda *, names, tags, exclude: names or []
    )

    detected_pkgs, resolved_deps = by_path_with_dependencies(
        ["mpich"], path_hints=["/usr/local/mpich/bin"]
    )

    # The second by_path call must have received the dep prefix as a hint.
    assert len(call_hints) == 2 and hwloc_prefix in call_hints[1]

    # hwloc must appear in detected packages and be resolved as a dependency of mpich.
    assert "hwloc" in detected_pkgs and mpich in resolved_deps
    assert resolved_deps[mpich][0].spec is hwloc
