# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Helpers to build an ExternalSpecsParser from Spack configuration."""

import itertools
from typing import TYPE_CHECKING, Any, Dict, Set

import spack.compilers.config
import spack.compilers.libraries
import spack.platforms
import spack.repo
import spack.spec
import spack.util.libc
from spack.externals import (
    ExternalSpecsParser,
    complete_architecture,
    complete_variants_and_architecture,
    extract_dicts_from_configuration,
)

if TYPE_CHECKING:
    import spack.context


def _normalize_packages_yaml(packages_yaml: Dict[str, Any], *, repo: spack.repo.RepoPath) -> None:
    for pkg_name in list(packages_yaml.keys()):
        is_virtual = repo.is_virtual(pkg_name)
        if pkg_name == "all" or not is_virtual:
            continue

        # Remove the virtual entry from the normalized configuration
        data = packages_yaml.pop(pkg_name)
        is_buildable = data.get("buildable", True)
        if not is_buildable:
            for provider in repo.providers_for(pkg_name):
                entry = packages_yaml.setdefault(provider.name, {})
                entry["buildable"] = False

        externals = data.get("externals", [])

        def keyfn(x):
            return spack.spec.Spec(x["spec"]).name

        for provider, specs in itertools.groupby(externals, key=keyfn):
            entry = packages_yaml.setdefault(provider, {})
            entry.setdefault("externals", []).extend(specs)


def external_config_with_implicit_externals(
    context: "spack.context.SpackContext",
) -> Dict[str, Any]:
    """Return packages.yaml augmented with implicit libc externals on Linux.

    Normalizes the configuration so that virtual-package keys are replaced by
    their concrete providers, then adds any libc specs detected from configured
    compilers when running on a libc-compatibility platform.

    Args:
        context: resources to read the ``packages`` section, the package repositories and the
            cached compiler output from.
    """
    configuration, repo = context.config, context.repo
    packages_yaml = configuration.deepcopy_as_builtin("packages", line_info=True)
    _normalize_packages_yaml(packages_yaml, repo=repo)

    # Add externals for libc from compilers on Linux
    if not spack.platforms.using_libc_compatibility():
        return packages_yaml

    for libc in sorted(all_libcs(context)):
        entry = {"spec": f"{libc}", "prefix": libc.external_path}
        packages_yaml.setdefault(libc.name, {}).setdefault("externals", []).append(entry)
    return packages_yaml


def all_libcs(context: "spack.context.SpackContext") -> Set[spack.spec.Spec]:
    """Return a set of all libc specs targeted by any configured compiler. If none, fall back to
    libc determined from the current Python process if dynamically linked.
    """
    cache = spack.compilers.libraries.FileCompilerCache(context.misc_cache)
    libcs = set()
    for c in spack.compilers.config.all_compilers_from(context.config, repo=context.repo):
        candidate = spack.compilers.libraries.CompilerPropertyDetector(
            c, repo=context.repo, cache=cache
        ).default_libc()
        if candidate is not None:
            libcs.add(candidate)

    if libcs:
        return libcs

    libc = spack.util.libc.libc_from_current_python_process()
    return {libc} if libc else set()


def create_external_parser(
    packages_with_externals: Any, *, context: "spack.context.SpackContext"
) -> ExternalSpecsParser:
    """Get externals from a pre-processed packages.yaml (with implicit externals).

    Args:
        packages_with_externals: pre-processed packages.yaml configuration.
        context: resources to read the completion mode and the package repositories from.
    """
    external_dicts = extract_dicts_from_configuration(packages_with_externals)
    completion_mode = context.config.get("concretizer:externals:completion")
    if completion_mode == "default_variants":
        complete_fn = complete_variants_and_architecture
    elif completion_mode == "architecture_only":
        complete_fn = complete_architecture
    else:
        raise ValueError(
            f"Unknown value for concretizer:externals:completion: {completion_mode!r}"
        )
    return ExternalSpecsParser(external_dicts, complete_node=complete_fn, repo=context.repo)
