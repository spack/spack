# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Helpers to build an ExternalSpecsParser from Spack configuration."""

import copy
import hashlib
import itertools
from typing import TYPE_CHECKING, Any, Dict, List, Optional

import spack.compilers.config
import spack.compilers.libraries
import spack.error
import spack.platforms
import spack.repo
import spack.spec
import spack.util.path
from spack.externals import (
    ExternalDict,
    ExternalSpecsParser,
    complete_architecture,
    complete_variants_and_architecture,
    extract_dicts_from_configuration,
    move_inline_dependencies,
)
from spack.util import tty

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

    cache = spack.compilers.libraries.FileCompilerCache(context.misc_cache)
    attach_libc_dependencies(packages_yaml, repo=repo, cache=cache)
    return packages_yaml


def _has_libc_dependency(entry: ExternalDict, libc_providers: List[str]) -> bool:
    for dep in entry.get("dependencies", []):
        if "libc" in dep.get("virtuals", "").split(","):
            return True
        if "spec" in dep and spack.spec.Spec(dep["spec"]).name in libc_providers:
            return True
    return any(
        e.spec.name in libc_providers or "libc" in e.virtuals
        for e in spack.spec.Spec(entry["spec"]).traverse_edges(root=False)
    )


def _find_or_add_libc(packages_yaml: Dict[str, Any], libc: spack.spec.Spec) -> str:
    """Return the id of the external entry for ``libc``, adding one if needed."""
    externals = packages_yaml.setdefault(libc.name, {}).setdefault("externals", [])
    for entry in externals:
        try:
            version = spack.spec.parse_with_version_concrete(entry["spec"]).version
        except spack.error.SpackError:
            continue
        prefix = spack.util.path.path_to_os_path(entry.get("prefix"))[0]
        if version == libc.version and prefix == libc.external_path:
            return entry.setdefault("id", _libc_id(libc))
    externals.append({"spec": str(libc), "prefix": libc.external_path, "id": _libc_id(libc)})
    return externals[-1]["id"]


def _libc_id(libc: spack.spec.Spec) -> str:
    digest = hashlib.sha1(libc.external_path.encode("utf-8")).hexdigest()[:8]
    return f"{libc.name}-{libc.version}-{digest}"


def attach_libc_dependencies(
    packages_yaml: Dict[str, Any],
    *,
    repo: spack.repo.RepoPath,
    cache: Optional["spack.compilers.libraries.CompilerCache"] = None,
) -> None:
    """Give every external compiler in ``packages_yaml`` a dependency on the libc it targets.

    Compilers that already declare a libc dependency are left alone. For the others the libc is
    detected from the compiler's dynamic linker, and an external entry for it is added unless
    one with the same version and prefix exists."""
    try:
        libc_providers = [x.name for x in repo.providers_for("libc")]
    except spack.repo.UnknownPackageError:
        return

    for name in spack.compilers.config.supported_compilers(repo=repo):
        for entry in packages_yaml.get(name, {}).get("externals", []):
            if "extra_attributes" not in entry or _has_libc_dependency(entry, libc_providers):
                continue

            # Detect on the node alone: its dependencies don't matter here
            alone = copy.deepcopy(entry)
            alone.pop("dependencies", None)
            alone["spec"] = str(spack.spec.Spec(alone["spec"]).copy(deps=False))
            parser = ExternalSpecsParser([alone], repo=repo)
            if not parser.nodes:
                continue
            libc = spack.compilers.libraries.CompilerPropertyDetector(
                parser.nodes[0], repo=repo, cache=cache
            ).default_libc()
            if libc is None:
                tty.debug(f"[{__name__}] cannot detect the libc of {entry['spec']}")
                continue

            node = spack.spec.Spec(entry["spec"])
            if node.dependencies():
                move_inline_dependencies(node, entry)
                entry["spec"] = str(node)
            entry.setdefault("dependencies", []).append(
                {
                    "id": _find_or_add_libc(packages_yaml, libc),
                    "deptypes": "link",
                    "virtuals": "libc",
                }
            )


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
