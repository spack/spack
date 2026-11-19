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

import os
import pathlib
import sys
from typing import Dict, List, Optional, Set, Tuple, Union

import spack.config
import spack.error
import spack.schema
import spack.spec
import spack.util.spack_yaml
from spack.util import tty


def _externals_in_packages_yaml(config: spack.config.Configuration) -> Set[spack.spec.Spec]:
    """Returns all the specs mentioned as externals in packages.yaml"""
    packages_yaml = config.get("packages")
    already_defined_specs = set()
    for pkg_name, package_configuration in packages_yaml.items():
        for item in package_configuration.get("externals", []):
            already_defined_specs.add(spack.spec.Spec(item["spec"]))
    return already_defined_specs


ExternalEntryType = Union[str, List[str], Dict[str, str]]


def _pkg_config_dict(
    external_pkg_entries: List["spack.spec.Spec"],
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


def prefix_before_last(path: pathlib.PurePath, names: Tuple[str, ...]) -> Optional[str]:
    """Parent of the innermost component whose lowercased name is in names, or None."""
    while path.name:
        if path.name.lower() in names:
            return str(path.parent) if path.parent.name else ""
        path = path.parent
    return None


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

    prefix = prefix_before_last(pathlib.PurePath(executable_dir), ("bin",))
    return executable_dir if prefix is None else prefix


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

    names = ("lib", "lib64", "bin") if sys.platform == "win32" else ("lib", "lib64")
    prefix = prefix_before_last(pathlib.PurePath(library_dir), names)
    return library_dir if prefix is None else prefix


def update_configuration(
    detected_packages: Dict[str, List["spack.spec.Spec"]],
    *,
    config: spack.config.Configuration,
    scope: Optional[str] = None,
    buildable: bool = True,
) -> List[spack.spec.Spec]:
    """Add the packages passed as arguments to packages.yaml

    Args:
        detected_packages: list of specs to be added
        config: configuration to be updated
        scope: configuration scope where to add the detected packages
        buildable: whether the detected packages are buildable or not
    """
    predefined_external_specs = _externals_in_packages_yaml(config)
    pkg_to_cfg, all_new_specs = {}, []
    for package_name, entries in detected_packages.items():
        new_entries = [s for s in entries if s not in predefined_external_specs]

        pkg_config = _pkg_config_dict(new_entries)
        external_entries = pkg_config.get("externals", [])
        assert not isinstance(external_entries, bool), "unexpected value for external entry"

        all_new_specs.extend(new_entries)
        if buildable is False:
            pkg_config["buildable"] = False
        pkg_to_cfg[package_name] = pkg_config

    # Don't rewrite configuration if there's nothing to add
    if not pkg_to_cfg:
        return all_new_specs

    scope = scope or config.default_modify_scope()
    pkgs_cfg = config.get("packages", scope=scope)
    pkgs_cfg = spack.schema.merge_yaml(pkgs_cfg, pkg_to_cfg)
    config.set("packages", pkgs_cfg, scope=scope)

    return all_new_specs


def set_virtuals_nonbuildable(virtuals: Set[str], scope: Optional[str] = None) -> List[str]:
    """Update packages:virtual:buildable:False for the provided virtual packages, if the property
    is not set by the user. Returns the list of virtual packages that have been updated."""
    packages = spack.config.CONFIG.get("packages")
    new_config = {}
    for virtual in virtuals:
        # If the user has set the buildable prop do not override it
        if virtual in packages and "buildable" in packages[virtual]:
            continue
        new_config[virtual] = {"buildable": False}

    # Update the provided scope
    spack.config.CONFIG.set(
        "packages",
        spack.schema.merge_yaml(spack.config.CONFIG.get("packages", scope=scope), new_config),
        scope=scope,
    )

    return list(new_config.keys())
