# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Helpers to build an ExternalSpecsParser from Spack configuration."""

import itertools
from typing import Any, Dict

import spack.compilers.config
import spack.compilers.libraries
import spack.config
import spack.platforms
import spack.repo
import spack.spec
from spack.externals import (
    ExternalSpecsParser,
    complete_architecture,
    complete_variants_and_architecture,
    extract_dicts_from_configuration,
)


def _normalize_packages_yaml(packages_yaml: Dict[str, Any]) -> None:
    for pkg_name in list(packages_yaml.keys()):
        is_virtual = spack.repo.PATH.is_virtual(pkg_name)
        if pkg_name == "all" or not is_virtual:
            continue

        # Remove the virtual entry from the normalized configuration
        data = packages_yaml.pop(pkg_name)
        is_buildable = data.get("buildable", True)
        if not is_buildable:
            for provider in spack.repo.PATH.providers_for(pkg_name):
                entry = packages_yaml.setdefault(provider.name, {})
                entry["buildable"] = False

        externals = data.get("externals", [])

        def keyfn(x):
            return spack.spec.Spec(x["spec"]).name

        for provider, specs in itertools.groupby(externals, key=keyfn):
            entry = packages_yaml.setdefault(provider, {})
            entry.setdefault("externals", []).extend(specs)


def external_config_with_implicit_externals(
    configuration: spack.config.Configuration,
) -> Dict[str, Any]:
    """Return packages.yaml augmented with implicit libc externals on Linux.

    Normalizes the configuration so that virtual-package keys are replaced by
    their concrete providers, then adds any libc specs detected from configured
    compilers when running on a libc-compatibility platform.
    """
    packages_yaml = configuration.deepcopy_as_builtin("packages", line_info=True)
    _normalize_packages_yaml(packages_yaml)

    # Add externals for libc from compilers on Linux
    if not spack.platforms.using_libc_compatibility():
        return packages_yaml

    seen = set()
    for compiler in spack.compilers.config.all_compilers_from(configuration):
        libc = spack.compilers.libraries.CompilerPropertyDetector(compiler).default_libc()
        if libc and libc not in seen:
            seen.add(libc)
            entry = {"spec": f"{libc}", "prefix": libc.external_path}
            packages_yaml.setdefault(libc.name, {}).setdefault("externals", []).append(entry)
    return packages_yaml


def create_external_parser(
    packages_with_externals: Any, completion_mode: str
) -> ExternalSpecsParser:
    """Get externals from a pre-processed packages.yaml (with implicit externals)."""
    external_dicts = extract_dicts_from_configuration(packages_with_externals)
    if completion_mode == "default_variants":
        complete_fn = complete_variants_and_architecture
    elif completion_mode == "architecture_only":
        complete_fn = complete_architecture
    else:
        raise ValueError(
            f"Unknown value for concretizer:externals:completion: {completion_mode!r}"
        )
    return ExternalSpecsParser(external_dicts, complete_node=complete_fn)
