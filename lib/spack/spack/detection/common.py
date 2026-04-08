# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Define a common data structure to represent external packages and a
function to update packages.yaml given a list of detected packages.

Ideally, each detection method should be placed in a specific subpackage
and implement at least a function that returns a list of specs.

The update in packages.yaml can then be done using the function provided here.

The module also contains other functions that might be useful across different
detection mechanisms.
"""
import glob
import itertools
import os
import pathlib
import re
import sys
import uuid
import warnings
from typing import Any, Dict, List, NamedTuple, Optional, Set, Tuple, Union

from spack.vendor.typing_extensions import TypedDict

import spack.config
import spack.deptypes
import spack.error
import spack.operating_systems.windows_os as winOs
import spack.schema
import spack.spec
import spack.util.environment
import spack.util.spack_yaml
import spack.util.windows_registry
from spack.llnl.util import tty


def _externals_in_packages_yaml() -> Set[spack.spec.Spec]:
    """Returns all the specs mentioned as externals in packages.yaml"""
    packages_yaml = spack.config.get("packages")
    already_defined_specs = set()
    for pkg_name, package_configuration in packages_yaml.items():
        for item in package_configuration.get("externals", []):
            already_defined_specs.add(spack.spec.Spec(item["spec"]))
    return already_defined_specs


ExternalEntryType = Union[str, Dict[str, Any], List[Any]]


class DependencyHint(TypedDict, total=False):
    """Dict form accepted by ``determine_dependencies``.

    Package authors may return plain dicts with these keys instead of just a spec. When returning
    a dict, the ``spec`` key is required and all other keys are optional.
    """

    spec: str
    prefix: str
    deptypes: "spack.deptypes.DepTypes"
    virtuals: Tuple[str, ...]


#: Keys that are valid in a ``DependencyHint`` dict.
_DEPENDENCY_HINT_KEYS: frozenset = frozenset(DependencyHint.__annotations__)


class DetectedDependency(NamedTuple):
    """A dependency detected alongside an external package"""

    spec: "spack.spec.Spec"
    deptypes: Optional[spack.deptypes.DepTypes] = None
    virtuals: Optional[Tuple[str, ...]] = None


def _normalize_dependency(dep: Union[str, Dict]) -> DetectedDependency:
    """Normalize a single value returned by ``determine_dependencies``."""
    if isinstance(dep, dict):
        if "spec" not in dep:
            raise ValueError(
                f"determine_dependencies returned a dict without the required 'spec' key: {dep!r}"
            )
        unknown = set(dep) - _DEPENDENCY_HINT_KEYS
        if unknown:
            warnings.warn(
                f"determine_dependencies returned a dict with unknown keys {sorted(unknown)};"
                f" valid keys are {sorted(_DEPENDENCY_HINT_KEYS)}. Unknown keys are ignored."
            )
        spec = spack.spec.Spec(dep["spec"])
        if "prefix" in dep:
            spec.external_path = dep["prefix"]
        return DetectedDependency(
            spec=spec, deptypes=dep.get("deptypes"), virtuals=dep.get("virtuals")
        )

    return DetectedDependency(spec=spack.spec.Spec(dep))


def determine_external_dependencies(
    *,
    detected_packages: Dict[str, List["spack.spec.Spec"]],
    detected_dependencies: Dict["spack.spec.Spec", List["DetectedDependency"]],
    known_packages: Optional[List["spack.spec.Spec"]] = None,
) -> Dict["spack.spec.Spec", List["DetectedDependency"]]:
    """Resolves dependency candidates against the available specs.

    The resolution tries ``known_packages`` first (specs already present in ``packages.yaml``
    from a previous run), then falls back to the detected specs.

    For each resolved candidate:

    - 0 matches  -> warning, dependency skipped.
    - 1 match    -> the matching Spec object replaces the abstract candidate.
    - 2+ matches -> warning (ambiguous), dependency skipped.

    Args:
        detected_packages: mapping of package name to detected specs, used as the
            fallback resolution pool.
        detected_dependencies: pre-collected output of ``collect_dependencies``
        known_packages: optional list of specs already present in ``packages.yaml``.
            Each spec must have ``external_path`` set so that ``update_configuration``
            can locate the corresponding YAML entry via ``_find_entry``.

    Returns:
        Mapping of detected Spec to its list of resolved ``DetectedDependency`` entries.
        Only specs for which at least one dependency was successfully resolved appear as keys.
    """
    all_detected = [spec for specs in detected_packages.values() for spec in specs]
    known = known_packages or []

    result = {}

    for spec, deps in detected_dependencies.items():
        resolved = []
        for dep in deps:
            # Prefer known packages
            matches = [s for s in known if s.satisfies(dep.spec)]
            if not matches:
                matches = [s for s in all_detected if s.satisfies(dep.spec)]

            if len(matches) == 0:
                warnings.warn(
                    f'"{dep.spec}" declared as a dependency of "{spec}" was not detected'
                    f" on the system and will be skipped"
                )
            elif len(matches) > 1:
                warnings.warn(
                    f'"{dep.spec}" declared as a dependency of "{spec}" is ambiguous:'
                    f" {len(matches)} detected specs satisfy it. Skipping"
                )
            else:
                resolved.append(
                    DetectedDependency(
                        spec=matches[0], deptypes=dep.deptypes, virtuals=dep.virtuals
                    )
                )

        if resolved:
            result[spec] = resolved

    return result


def _find_entry(packages_yaml: Dict, spec: "spack.spec.Spec") -> Optional[Dict]:
    """Return the raw YAML external entry in ``packages_yaml`` that matches ``spec``."""
    if not spec.external_path:
        return None
    target_prefix = pathlib.Path(spec.external_path).as_posix()
    pkg_config = packages_yaml.get(spec.name)
    if not isinstance(pkg_config, dict):
        return None
    for entry in pkg_config.get("externals", []):
        entry_prefix = pathlib.Path(entry.get("prefix", "")).as_posix()
        if entry_prefix != target_prefix:
            continue
        if spec.satisfies(spack.spec.Spec(entry["spec"])):
            return entry
    return None


def _pkg_config_dict(
    external_pkg_entries: List["spack.spec.Spec"],
    *,
    ids: Optional[Dict["spack.spec.Spec", str]] = None,
    dependencies: Optional[Dict["spack.spec.Spec", List]] = None,
) -> Dict[str, Union[bool, List[Dict[str, ExternalEntryType]]]]:
    """Generate a package specific config dict according to the packages.yaml schema.

    This does not generate the entire packages.yaml. For example, given some
    external entries for the CMake package, this could return::

        {
            'externals': [{
                'spec': 'cmake@3.17.1',
                'prefix': '/opt/cmake-3.17.1/'
            }, {
                'spec': 'cmake@3.16.5',
                'prefix': '/opt/cmake-3.16.5/'
            }]
       }
    """
    pkg_dict = spack.util.spack_yaml.syaml_dict()
    pkg_dict["externals"] = []
    for e in external_pkg_entries:
        if not _spec_is_valid(e):
            continue

        external_items: List[Tuple[str, ExternalEntryType]] = [
            ("spec", str(e)),
            ("prefix", pathlib.Path(e.external_path).as_posix()),
        ]
        if e.external_modules:
            external_items.append(("modules", e.external_modules))

        if e.extra_attributes:
            external_items.append(
                ("extra_attributes", spack.util.spack_yaml.syaml_dict(e.extra_attributes.items()))
            )

        if ids and e in ids:
            external_items.append(("id", ids[e]))

        if dependencies and e in dependencies:
            external_items.append(("dependencies", dependencies[e]))

        # external_items.extend(e.spec.extra_attributes.items())
        pkg_dict["externals"].append(spack.util.spack_yaml.syaml_dict(external_items))

    return pkg_dict


def _spec_is_valid(spec: spack.spec.Spec) -> bool:
    try:
        str(spec)
    except spack.error.SpackError:
        # It is assumed here that we can at least extract the package name from the spec so we
        # can look up the implementation of determine_spec_details
        tty.warn(f"Constructed spec for {spec.name} does not have a string representation")
        return False

    try:
        spack.spec.Spec(str(spec))
    except spack.error.SpackError:
        tty.warn(
            "Constructed spec has a string representation but the string"
            " representation does not evaluate to a valid spec: {0}".format(str(spec))
        )
        return False

    return True


def path_to_dict(search_paths: List[str]) -> Dict[str, str]:
    """Return dictionary[fullpath]: basename from list of paths"""
    path_to_lib: Dict[str, str] = {}
    # Reverse order of search directories so that a lib in the first
    # entry overrides later entries
    for search_path in reversed(search_paths):
        try:
            dir_iter = os.scandir(search_path)
        except OSError as e:
            tty.debug(f"cannot scan '{search_path}' for external software: {e}")
            continue
        with dir_iter as entries:
            for entry in entries:
                try:
                    if entry.is_file():
                        path_to_lib[entry.path] = entry.name
                except OSError as e:
                    tty.debug(f"cannot scan '{search_path}' for external software: {e}")

    return path_to_lib


def is_executable(file_path: str) -> bool:
    """Return True if the path passed as argument is that of an executable"""
    return os.path.isfile(file_path) and os.access(file_path, os.X_OK)


def _convert_to_iterable(single_val_or_multiple):
    x = single_val_or_multiple
    if x is None:
        return []
    elif isinstance(x, str):
        return [x]
    elif isinstance(x, spack.spec.Spec):
        # Specs are iterable, but a single spec should be converted to a list
        return [x]

    try:
        iter(x)
        return x
    except TypeError:
        return [x]


def executable_prefix(executable_dir: str) -> str:
    """Given a directory where an executable is found, guess the prefix
    (i.e. the "root" directory of that installation) and return it.

    Args:
        executable_dir: directory where an executable is found
    """
    # Given a prefix where an executable is found, assuming that prefix
    # contains /bin/, strip off the 'bin' directory to get a Spack-compatible
    # prefix
    assert os.path.isdir(executable_dir)

    components = executable_dir.split(os.sep)
    # convert to lower to match Bin, BIN, bin
    lowered_components = executable_dir.lower().split(os.sep)
    if "bin" not in lowered_components:
        return executable_dir
    idx = lowered_components.index("bin")
    return os.sep.join(components[:idx])


def library_prefix(library_dir: str) -> str:
    """Given a directory where a library is found, guess the prefix
    (i.e. the "root" directory of that installation) and return it.

    Args:
        library_dir: directory where a library is found
    """
    # Given a prefix where an library is found, assuming that prefix
    # contains /lib/ or /lib64/, strip off the 'lib' or 'lib64' directory
    # to get a Spack-compatible prefix
    assert os.path.isdir(library_dir)

    components = library_dir.split(os.sep)
    # convert to lowercase to match lib, LIB, Lib, etc.
    lowered_components = library_dir.lower().split(os.sep)
    if "lib64" in lowered_components:
        idx = lowered_components.index("lib64")
        return os.sep.join(components[:idx])
    elif "lib" in lowered_components:
        idx = lowered_components.index("lib")
        return os.sep.join(components[:idx])
    elif sys.platform == "win32" and "bin" in lowered_components:
        idx = lowered_components.index("bin")
        return os.sep.join(components[:idx])
    else:
        return library_dir


def update_configuration(
    detected_packages: Dict[str, List["spack.spec.Spec"]],
    scope: Optional[str] = None,
    buildable: bool = True,
    resolved_dependencies: Optional[Dict["spack.spec.Spec", List[DetectedDependency]]] = None,
) -> List[spack.spec.Spec]:
    """Add the packages passed as arguments to packages.yaml

    Args:
        detected_packages: list of specs to be added
        scope: configuration scope where to add the detected packages
        buildable: whether the detected packages are buildable or not
        resolved_dependencies: optional mapping from a detected spec to the list of its resolved
            dependencies. When provided, the generated packages.yaml entries include ``id`` and
            ``dependencies`` fields. Pre-existing entries that lack ``dependencies`` are augmented
            in-place. Entries that already have ``dependencies`` are left untouched.
    """
    # Read the target scope up-front so we can reuse existing IDs and augment after merge.
    scope = scope or spack.config.default_modify_scope()
    packages_yaml = spack.config.CONFIG.deepcopy_as_builtin("packages", scope=scope)

    # Build stable IDs and serialized dependency lists for participating specs.
    ids, serialized_deps = {}, {}
    if resolved_dependencies:
        # Collect all specs that appear as a parent or a child in the dependency map.
        participating = set()
        for parent_spec, dependencies in resolved_dependencies.items():
            if dependencies:
                participating.add(parent_spec)
                participating.update(dep.spec for dep in dependencies)

        # Assign UUIDs, reusing any ID that already exists in the target scope.
        for spec in participating:
            existing_entry = _find_entry(packages_yaml, spec)
            if existing_entry and "id" in existing_entry:
                ids[spec] = existing_entry["id"]
            else:
                ids[spec] = str(uuid.uuid4())

        # Serialize each parent's dependency list into DependencyDict-compatible dicts.
        for parent_spec, dependencies in resolved_dependencies.items():
            dep_dicts = []
            for dep in dependencies:
                if dep.spec not in ids:
                    continue
                dep_items: List[Tuple[str, Any]] = [("id", ids[dep.spec])]
                if dep.deptypes is not None:
                    dep_items.append(("deptypes", list(dep.deptypes)))
                if dep.virtuals is not None:
                    dep_items.append(("virtuals", ",".join(dep.virtuals)))
                dep_dicts.append(spack.util.spack_yaml.syaml_dict(dep_items))
            if dep_dicts:
                serialized_deps[parent_spec] = dep_dicts

        # Record which parent specs already have a 'dependencies' field *before* we write
        # anything, so the post-merge warning only fires for truly pre-existing entries.
        specs_with_existing_deps = set()
        for parent_spec in resolved_dependencies:
            existing = _find_entry(packages_yaml, parent_spec)
            if existing is not None and "dependencies" in existing:
                specs_with_existing_deps.add(parent_spec)

    predefined_external_specs = _externals_in_packages_yaml()
    pkg_to_cfg, all_new_specs = {}, []
    for package_name, entries in detected_packages.items():
        new_entries = [s for s in entries if s not in predefined_external_specs]

        pkg_config = _pkg_config_dict(new_entries, ids=ids, dependencies=serialized_deps)
        external_entries = pkg_config.get("externals", [])
        assert not isinstance(external_entries, bool), "unexpected value for external entry"

        all_new_specs.extend(new_entries)
        if buildable is False:
            pkg_config["buildable"] = False
        pkg_to_cfg[package_name] = pkg_config

    packages_yaml = spack.schema.merge_yaml(packages_yaml, pkg_to_cfg)
    if resolved_dependencies:
        # Backfill 'id' on all pre-existing entries that participate in the
        # dependency graph so they can be referenced by other entries.
        # Never add a 'dependencies' field to a pre-existing entry: manually
        # written dependency relationships are authoritative and must not be
        # changed by auto-detection.
        for spec, spec_id in ids.items():
            entry = _find_entry(packages_yaml, spec)
            if entry is not None and "id" not in entry:
                entry["id"] = spec_id

        for parent_spec, deps in resolved_dependencies.items():
            if parent_spec in specs_with_existing_deps:
                dep_names = ", ".join(str(d.spec) for d in deps)
                warnings.warn(
                    f"{parent_spec} already exists in packages.yaml;"
                    f" skipping auto-detected dependencies [{dep_names}]."
                    f" Edit packages.yaml directly to update dependency relationships."
                )

    spack.config.set("packages", packages_yaml, scope=scope)

    return all_new_specs


def set_virtuals_nonbuildable(virtuals: Set[str], scope: Optional[str] = None) -> List[str]:
    """Update packages:virtual:buildable:False for the provided virtual packages, if the property
    is not set by the user. Returns the list of virtual packages that have been updated."""
    packages = spack.config.get("packages")
    new_config = {}
    for virtual in virtuals:
        # If the user has set the buildable prop do not override it
        if virtual in packages and "buildable" in packages[virtual]:
            continue
        new_config[virtual] = {"buildable": False}

    # Update the provided scope
    spack.config.set(
        "packages",
        spack.schema.merge_yaml(spack.config.get("packages", scope=scope), new_config),
        scope=scope,
    )

    return list(new_config.keys())


def _windows_drive() -> str:
    """Return Windows drive string extracted from the PROGRAMFILES environment variable,
    which is guaranteed to be defined for all logins.
    """
    match = re.match(r"([a-zA-Z]:)", os.environ["PROGRAMFILES"])
    if match is None:
        raise RuntimeError("cannot read the PROGRAMFILES environment variable")
    return match.group(1)


class WindowsCompilerExternalPaths:
    @staticmethod
    def find_windows_compiler_root_paths() -> List[str]:
        """Helper for Windows compiler installation root discovery

        At the moment simply returns location of VS install paths from VSWhere
        But should be extended to include more information as relevant"""
        return list(winOs.WindowsOs().vs_install_paths)

    @staticmethod
    def find_windows_compiler_cmake_paths() -> List[str]:
        """Semi hard-coded search path for cmake bundled with MSVC"""
        return [
            os.path.join(
                path, "Common7", "IDE", "CommonExtensions", "Microsoft", "CMake", "CMake", "bin"
            )
            for path in WindowsCompilerExternalPaths.find_windows_compiler_root_paths()
        ]

    @staticmethod
    def find_windows_compiler_ninja_paths() -> List[str]:
        """Semi hard-coded search heuristic for locating ninja bundled with MSVC"""
        return [
            os.path.join(path, "Common7", "IDE", "CommonExtensions", "Microsoft", "CMake", "Ninja")
            for path in WindowsCompilerExternalPaths.find_windows_compiler_root_paths()
        ]

    @staticmethod
    def find_windows_compiler_bundled_packages() -> List[str]:
        """Return all MSVC compiler bundled packages"""
        return (
            WindowsCompilerExternalPaths.find_windows_compiler_cmake_paths()
            + WindowsCompilerExternalPaths.find_windows_compiler_ninja_paths()
        )


class WindowsKitExternalPaths:
    @staticmethod
    def find_windows_kit_roots() -> List[str]:
        """Return Windows kit root, typically %programfiles%\\Windows Kits\\10|11\\"""
        if sys.platform != "win32":
            return []
        program_files = os.environ["PROGRAMFILES(x86)"]
        kit_base = os.path.join(program_files, "Windows Kits", "**")
        return glob.glob(kit_base)

    @staticmethod
    def find_windows_kit_bin_paths(
        kit_base: Union[Optional[str], Optional[list]] = None,
    ) -> List[str]:
        """Returns Windows kit bin directory per version"""
        kit_base = WindowsKitExternalPaths.find_windows_kit_roots() if not kit_base else kit_base
        assert kit_base, "Unexpectedly empty value for Windows kit base path"
        if isinstance(kit_base, str):
            kit_base = kit_base.split(";")
        kit_paths = []
        for kit in kit_base:
            kit_bin = os.path.join(kit, "bin")
            kit_paths.extend(glob.glob(os.path.join(kit_bin, "[0-9]*", "*\\")))
        return kit_paths

    @staticmethod
    def find_windows_kit_lib_paths(
        kit_base: Union[Optional[str], Optional[list]] = None,
    ) -> List[str]:
        """Returns Windows kit lib directory per version"""
        kit_base = WindowsKitExternalPaths.find_windows_kit_roots() if not kit_base else kit_base
        assert kit_base, "Unexpectedly empty value for Windows kit base path"
        if isinstance(kit_base, str):
            kit_base = kit_base.split(";")
        kit_paths = []
        for kit in kit_base:
            kit_lib = os.path.join(kit, "Lib")
            kit_paths.extend(glob.glob(os.path.join(kit_lib, "[0-9]*", "*", "*\\")))
        return kit_paths

    @staticmethod
    def find_windows_driver_development_kit_paths() -> List[str]:
        """Provides a list of all installation paths
        for the WDK by version and architecture
        """
        wdk_content_root = os.getenv("WDKContentRoot")
        return WindowsKitExternalPaths.find_windows_kit_lib_paths(wdk_content_root)

    @staticmethod
    def find_windows_kit_reg_installed_roots_paths() -> List[str]:
        reg = spack.util.windows_registry.WindowsRegistryView(
            "SOFTWARE\\Microsoft\\Windows Kits\\Installed Roots",
            root_key=spack.util.windows_registry.HKEY.HKEY_LOCAL_MACHINE,
        )
        if not reg:
            # couldn't find key, return empty list
            return []
        kit_root_reg = re.compile(r"KitsRoot[0-9]+")
        root_paths = []
        for kit_root in filter(kit_root_reg.match, reg.get_values().keys()):
            root_paths.extend(
                WindowsKitExternalPaths.find_windows_kit_lib_paths(reg.get_value(kit_root).value)
            )
        return root_paths

    @staticmethod
    def find_windows_kit_reg_sdk_paths() -> List[str]:
        sdk_paths = []
        sdk_regex = re.compile(r"v[0-9]+.[0-9]+")
        windows_reg = spack.util.windows_registry.WindowsRegistryView(
            "SOFTWARE\\WOW6432Node\\Microsoft\\Microsoft SDKs\\Windows",
            root_key=spack.util.windows_registry.HKEY.HKEY_LOCAL_MACHINE,
        )
        for key in filter(sdk_regex.match, [x.name for x in windows_reg.get_subkeys()]):
            reg = windows_reg.get_subkey(key)
            sdk_paths.extend(
                WindowsKitExternalPaths.find_windows_kit_lib_paths(
                    reg.get_value("InstallationFolder").value
                )
            )
        return sdk_paths


def find_win32_additional_install_paths() -> List[str]:
    """Not all programs on Windows live on the PATH
    Return a list of other potential install locations.
    """
    drive_letter = _windows_drive()
    windows_search_ext = []
    cuda_re = r"CUDA_PATH[a-zA-Z1-9_]*"
    # The list below should be expanded with other
    # common Windows install locations as necessary
    path_ext_keys = ["I_MPI_ONEAPI_ROOT", "MSMPI_BIN", "MLAB_ROOT", "NUGET_PACKAGES"]
    user = os.environ["USERPROFILE"]
    add_path = lambda key: re.search(cuda_re, key) or key in path_ext_keys
    windows_search_ext.extend([os.environ[key] for key in os.environ.keys() if add_path(key)])
    # note windows paths are fine here as this method should only ever be invoked
    # to interact with Windows
    # Add search path for default Chocolatey (https://github.com/chocolatey/choco)
    # install directory
    windows_search_ext.append("%s\\ProgramData\\chocolatey\\bin" % drive_letter)
    # Add search path for NuGet package manager default install location
    windows_search_ext.append(os.path.join(user, ".nuget", "packages"))
    windows_search_ext.extend(
        spack.config.get("config:additional_external_search_paths", default=[])
    )
    windows_search_ext.extend(spack.util.environment.get_path("PATH"))
    return windows_search_ext


def compute_windows_program_path_for_package(pkg: "spack.package_base.PackageBase") -> List[str]:
    """Given a package, attempts to compute its Windows program files location,
    and returns the list of best guesses.

    Args:
        pkg: package for which Program Files location is to be computed
    """
    if sys.platform != "win32":
        return []
    # note windows paths are fine here as this method should only ever be invoked
    # to interact with Windows
    program_files = "{}\\Program Files{}\\{}"
    drive_letter = _windows_drive()

    return [
        program_files.format(drive_letter, arch, name)
        for arch, name in itertools.product(("", " (x86)"), (pkg.name, pkg.name.capitalize()))
    ]


def compute_windows_user_path_for_package(pkg: "spack.package_base.PackageBase") -> List[str]:
    """Given a package attempt to compute its user scoped
    install location, return list of potential locations based
    on common heuristics. For more info on Windows user specific
    installs see:
    https://learn.microsoft.com/en-us/dotnet/api/system.environment.specialfolder?view=netframework-4.8
    """
    if sys.platform != "win32":
        return []

    # Current user directory
    user = os.environ["USERPROFILE"]
    app_data = "AppData"
    app_data_locations = ["Local", "Roaming"]
    user_appdata_install_stubs = [os.path.join(app_data, x) for x in app_data_locations]
    return [
        os.path.join(user, app_data, name)
        for app_data, name in list(
            itertools.product(user_appdata_install_stubs, (pkg.name, pkg.name.capitalize()))
        )
    ] + [os.path.join(user, name) for name in (pkg.name, pkg.name.capitalize())]
