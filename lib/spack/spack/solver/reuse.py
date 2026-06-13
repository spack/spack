# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import enum
import functools
import typing
import warnings
from typing import Any, Callable, List, Mapping, Optional

import spack.binary_distribution
import spack.config
import spack.repo
import spack.spec
import spack.traverse
import spack.util.path
from spack.active_environment import active_environment
from spack.enums import InstallRecordStatus
from spack.externals import ExternalSpecsParser
from spack.externals_config import create_external_parser, external_config_with_implicit_externals
from spack.spec_filter import SpecFilter

from .context import Context
from .runtimes import all_libcs

if typing.TYPE_CHECKING:
    import spack.environment


def spec_filter_from_store(store, *, is_reusable, include=None, exclude=None) -> SpecFilter:
    """Constructs a filter that takes the specs from the store passed as argument."""
    factory = functools.partial(_specs_from_store, store=store)
    return SpecFilter(
        factory=factory, is_usable=is_reusable, include=include or [], exclude=exclude or []
    )


def spec_filter_from_buildcache(
    binary_index, *, is_reusable, include=None, exclude=None
) -> SpecFilter:
    """Constructs a filter that takes the specs from the configured buildcaches."""
    factory = functools.partial(_specs_from_mirror, binary_index=binary_index)
    return SpecFilter(
        factory=factory, is_usable=is_reusable, include=include or [], exclude=exclude or []
    )


def spec_filter_from_environment(*, is_reusable, env, include=None, exclude=None) -> SpecFilter:
    factory = functools.partial(_specs_from_environment, env=env)
    return SpecFilter(
        factory=factory, is_usable=is_reusable, include=include or [], exclude=exclude or []
    )


def spec_filter_from_packages_yaml(
    *, external_parser: ExternalSpecsParser, is_reusable, include=None, exclude=None
) -> SpecFilter:
    return SpecFilter(
        external_parser.all_specs,
        is_usable=is_reusable,
        include=include or [],
        exclude=exclude or [],
    )


def _has_runtime_dependencies(spec: spack.spec.Spec) -> bool:
    # Spack v1.0 specs and later
    return spec.original_spec_format() >= 5


def _is_reusable(
    spec: spack.spec.Spec,
    packages_with_externals,
    local: bool,
    external_db_hashes: typing.FrozenSet[str] = frozenset(),
) -> bool:
    """A spec is reusable if it's not a dev spec, it's imported from the cray manifest, it's not
    external, or it's external with matching packages.yaml entry. The latter prevents two issues:

    1. Externals in build caches: avoid installing an external on the build machine not
       available on the target machine
    2. Local externals: avoid reusing an external if the local config changes. This helps in
       particular when a user removes an external from packages.yaml, and expects that that
       takes effect immediately.

    Arguments:
        spec: the spec to check
        packages_with_externals: the pre-processed packages configuration
        local: whether the spec comes from a local source (the store or an environment)
        external_db_hashes: dag hashes of locally installed specs imported from a cray manifest
            (origin "external-db"). Pre-computed once by the caller so this check is O(1).
    """
    if "dev_path" in spec.variants:
        return False

    if spec.name == "compiler-wrapper":
        return False

    if not spec.external:
        return _has_runtime_dependencies(spec)

    # Cray external manifest externals are always reusable
    if local and spec.dag_hash() in external_db_hashes:
        return True

    try:
        provided = spack.repo.PATH.get(spec).provided_virtual_names()
    except spack.repo.RepoError:
        provided = []

    for name in {spec.name, *provided}:
        for entry in packages_with_externals.get(name, {}).get("externals", []):
            expected_prefix = entry.get("prefix")
            if expected_prefix is not None:
                expected_prefix = spack.util.path.path_to_os_path(expected_prefix)[0]
            if (
                spec.satisfies(entry["spec"])
                and spec.external_path == expected_prefix
                and spec.external_modules == entry.get("modules")
            ):
                return True

    return False


def reusable_external_specs(configuration: spack.config.Configuration) -> List[spack.spec.Spec]:
    """Return the reusable external specs declared in a configuration's ``packages.yaml``."""
    packages_with_externals = external_config_with_implicit_externals(configuration)
    completion_mode = configuration.get("concretizer:externals:completion")
    spec_filter = spec_filter_from_packages_yaml(
        external_parser=create_external_parser(packages_with_externals, completion_mode),
        is_reusable=functools.partial(
            _is_reusable, packages_with_externals=packages_with_externals, local=True
        ),
    )
    return spec_filter.selected_specs()


def _specs_from_store(store):
    with store.db.read_transaction():
        return store.db.query(installed=True)


def _specs_from_mirror(binary_index):
    try:
        binary_index.update()
        specs = binary_index.get_all_built_specs()
    except (spack.binary_distribution.FetchCacheError, IndexError):
        # this is raised when no mirrors had indices.
        # TODO: update mirror configuration so it can indicate that the
        # TODO: source cache (or any mirror really) doesn't have binaries.
        return []
    for url in sorted(binary_index.mirrors_without_index):
        warnings.warn(f"the mirror at {url} cannot be used in concretization (no index found)")
    return specs


def _specs_from_environment(env):
    """Return all concrete specs from the environment. This includes all included concrete"""
    if env:
        return list(spack.traverse.traverse_nodes([s for _, s in env.concretized_specs()]))
    else:
        return []


class ReuseStrategy(enum.Enum):
    ROOTS = enum.auto()
    DEPENDENCIES = enum.auto()
    NONE = enum.auto()


SpecFiltersFactory = Callable[
    [Callable[[spack.spec.Spec], bool], spack.config.Configuration], List[SpecFilter]
]


class ReusableSpecsSelector:
    """Selects specs that can be reused during concretization."""

    def __init__(
        self,
        *,
        context: Context,
        external_parser: ExternalSpecsParser,
        packages_with_externals: Any,
        factory: Optional[SpecFiltersFactory] = None,
    ) -> None:
        # Local import to break circular dependencies
        import spack.environment

        self.configuration = context.config
        self.store = context.store
        self.binary_index = context.binary_index
        # Pre-compute the hashes of locally installed cray-manifest ("external-db") specs once,
        # so the per-spec reusability check is O(1) membership instead of a DB query per spec.
        external_db_hashes = frozenset(
            s.dag_hash()
            for s in self.store.db.query_local(
                origin="external-db", installed=InstallRecordStatus.ANY
            )
        )
        # The reusability predicate only depends on the source being local vs. a build cache, so
        # build the two variants once and share them across all the filters below.
        local_is_reusable = functools.partial(
            _is_reusable,
            packages_with_externals=packages_with_externals,
            local=True,
            external_db_hashes=external_db_hashes,
        )
        mirror_is_reusable = functools.partial(
            _is_reusable, packages_with_externals=packages_with_externals, local=False
        )
        self.reuse_strategy = ReuseStrategy.ROOTS
        reuse_yaml = self.configuration.get("concretizer:reuse", False)

        self.reuse_sources = []
        if factory is not None:
            self.reuse_sources.extend(factory(local_is_reusable, self.configuration))

        if not isinstance(reuse_yaml, Mapping):
            self.reuse_sources.append(
                spec_filter_from_packages_yaml(
                    external_parser=external_parser, is_reusable=local_is_reusable
                )
            )
            if reuse_yaml is False:
                self.reuse_strategy = ReuseStrategy.NONE
                return

            if reuse_yaml == "dependencies":
                self.reuse_strategy = ReuseStrategy.DEPENDENCIES
            self.reuse_sources.extend(
                [
                    spec_filter_from_store(self.store, is_reusable=local_is_reusable),
                    spec_filter_from_buildcache(self.binary_index, is_reusable=mirror_is_reusable),
                ]
            )
        else:
            has_external_source = False
            roots = reuse_yaml.get("roots", True)
            if roots is True:
                self.reuse_strategy = ReuseStrategy.ROOTS
            else:
                self.reuse_strategy = ReuseStrategy.DEPENDENCIES
            default_include = reuse_yaml.get("include", [])
            default_exclude = reuse_yaml.get("exclude", [])
            default_sources = [{"type": "local"}, {"type": "buildcache"}]
            for source in reuse_yaml.get("from", default_sources):
                include = source.get("include", default_include)
                exclude = source.get("exclude", default_exclude)
                if source["type"] == "environment" and "path" in source:
                    env_dir = spack.environment.as_env_dir(source["path"])
                    active_env = active_environment()
                    if not active_env or env_dir not in active_env.included_concrete_env_root_dirs:
                        # If the environment is not included as a concrete environment, use the
                        # current specs from its lockfile.
                        self.reuse_sources.append(
                            spec_filter_from_environment(
                                is_reusable=local_is_reusable,
                                include=include,
                                exclude=exclude,
                                env=spack.environment.environment_from_name_or_dir(env_dir),
                            )
                        )
                elif source["type"] == "local":
                    self.reuse_sources.append(
                        spec_filter_from_store(
                            self.store,
                            is_reusable=local_is_reusable,
                            include=include,
                            exclude=exclude,
                        )
                    )
                elif source["type"] == "buildcache":
                    self.reuse_sources.append(
                        spec_filter_from_buildcache(
                            self.binary_index,
                            is_reusable=mirror_is_reusable,
                            include=include,
                            exclude=exclude,
                        )
                    )
                elif source["type"] == "external":
                    has_external_source = True
                    if include:
                        # Since libcs are implicit externals, we need to implicitly include them
                        include = include + sorted(all_libcs(self.configuration))  # type: ignore[type-var]
                    self.reuse_sources.append(
                        spec_filter_from_packages_yaml(
                            external_parser=external_parser,
                            is_reusable=local_is_reusable,
                            include=include,
                            exclude=exclude,
                        )
                    )

            # If "external" is not specified, we assume that all externals have to be included
            if not has_external_source:
                self.reuse_sources.append(
                    spec_filter_from_packages_yaml(
                        external_parser=external_parser, is_reusable=local_is_reusable
                    )
                )

    def reusable_specs(self, specs: List[spack.spec.Spec]) -> List[spack.spec.Spec]:
        result = []
        for reuse_source in self.reuse_sources:
            result.extend(reuse_source.selected_specs())
        # If we only want to reuse dependencies, remove the root specs
        if self.reuse_strategy == ReuseStrategy.DEPENDENCIES:
            result = [spec for spec in result if not any(root in spec for root in specs)]

        return result
