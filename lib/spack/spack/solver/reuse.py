# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import enum
import functools
from typing import Callable, List, Mapping

import spack.binary_distribution
import spack.config
import spack.environment
import spack.repo
import spack.spec
import spack.store

from .runtimes import _external_config_with_implicit_externals


class SpecFilter:
    """Given a method to produce a list of specs, this class can filter them according to
    different criteria.
    """

    def __init__(
        self,
        factory: Callable[[], List[spack.spec.Spec]],
        is_usable: Callable[[spack.spec.Spec], bool],
        include: List[str],
        exclude: List[str],
    ) -> None:
        """
        Args:
            factory: factory to produce a list of specs
            is_usable: predicate that takes a spec in input and returns False if the spec
                should not be considered for this filter, True otherwise.
            include: if present, a "good" spec must match at least one entry in the list
            exclude: if present, a "good" spec must not match any entry in the list
        """
        self.factory = factory
        self.is_usable = is_usable
        self.include = include
        self.exclude = exclude

    def is_selected(self, s: spack.spec.Spec) -> bool:
        if not self.is_usable(s):
            return False

        if self.include and not any(s.satisfies(c) for c in self.include):
            return False

        if self.exclude and any(s.satisfies(c) for c in self.exclude):
            return False

        return True

    def selected_specs(self) -> List[spack.spec.Spec]:
        return [s for s in self.factory() if self.is_selected(s)]

    @staticmethod
    def from_store(configuration, *, include, exclude) -> "SpecFilter":
        """Constructs a filter that takes the specs from the current store."""
        packages = _external_config_with_implicit_externals(configuration)
        is_reusable = functools.partial(_is_reusable, packages=packages, local=True)
        factory = functools.partial(_specs_from_store, configuration=configuration)
        return SpecFilter(factory=factory, is_usable=is_reusable, include=include, exclude=exclude)

    @staticmethod
    def from_buildcache(configuration, *, include, exclude) -> "SpecFilter":
        """Constructs a filter that takes the specs from the configured buildcaches."""
        packages = _external_config_with_implicit_externals(configuration)
        is_reusable = functools.partial(_is_reusable, packages=packages, local=False)
        return SpecFilter(
            factory=_specs_from_mirror, is_usable=is_reusable, include=include, exclude=exclude
        )

    @staticmethod
    def from_environment(configuration, *, include, exclude, env) -> "SpecFilter":
        packages = _external_config_with_implicit_externals(configuration)
        is_reusable = functools.partial(_is_reusable, packages=packages, local=True)
        factory = functools.partial(_specs_from_environment, env=env)
        return SpecFilter(factory=factory, is_usable=is_reusable, include=include, exclude=exclude)

    @staticmethod
    def from_environment_included_concrete(
        configuration,
        *,
        include: List[str],
        exclude: List[str],
        env: spack.environment.Environment,
        included_concrete: str,
    ) -> "SpecFilter":
        packages = _external_config_with_implicit_externals(configuration)
        is_reusable = functools.partial(_is_reusable, packages=packages, local=True)
        factory = functools.partial(
            _specs_from_environment_included_concrete, env=env, included_concrete=included_concrete
        )
        return SpecFilter(factory=factory, is_usable=is_reusable, include=include, exclude=exclude)


def _has_runtime_dependencies(spec: spack.spec.Spec) -> bool:
    # TODO (compiler as nodes): this function contains specific names from builtin, and should
    # be made more general
    if "gcc" in spec and "gcc-runtime" not in spec:
        return False

    if "intel-oneapi-compilers" in spec and "intel-oneapi-runtime" not in spec:
        return False

    return True


def _is_reusable(spec: spack.spec.Spec, packages, local: bool) -> bool:
    """A spec is reusable if it's not a dev spec, it's imported from the cray manifest, it's not
    external, or it's external with matching packages.yaml entry. The latter prevents two issues:

    1. Externals in build caches: avoid installing an external on the build machine not
       available on the target machine
    2. Local externals: avoid reusing an external if the local config changes. This helps in
       particular when a user removes an external from packages.yaml, and expects that that
       takes effect immediately.

    Arguments:
        spec: the spec to check
        packages: the packages configuration
    """
    if "dev_path" in spec.variants:
        return False

    if spec.name == "compiler-wrapper":
        return False

    if not spec.external:
        return _has_runtime_dependencies(spec)

    # Cray external manifest externals are always reusable
    if local:
        _, record = spack.store.STORE.db.query_by_spec_hash(spec.dag_hash())
        if record and record.origin == "external-db":
            return True

    try:
        provided = spack.repo.PATH.get(spec).provided_virtual_names()
    except spack.repo.RepoError:
        provided = []

    for name in {spec.name, *provided}:
        for entry in packages.get(name, {}).get("externals", []):
            if (
                spec.satisfies(entry["spec"])
                and spec.external_path == entry.get("prefix")
                and spec.external_modules == entry.get("modules")
            ):
                return True

    return False


def _specs_from_store(configuration):
    store = spack.store.create(configuration)
    with store.db.read_transaction():
        return store.db.query(installed=True)


def _specs_from_mirror():
    try:
        return spack.binary_distribution.update_cache_and_get_specs()
    except (spack.binary_distribution.FetchCacheError, IndexError):
        # this is raised when no mirrors had indices.
        # TODO: update mirror configuration so it can indicate that the
        # TODO: source cache (or any mirror really) doesn't have binaries.
        return []


def _specs_from_environment(env):
    """Return all concrete specs from the environment. This includes all included concrete"""
    if env:
        return [concrete for _, concrete in env.concretized_specs()]
    else:
        return []


def _specs_from_environment_included_concrete(env, included_concrete):
    """Return only concrete specs from the environment included from the included_concrete"""
    if env:
        assert included_concrete in env.included_concrete_envs
        return [concrete for concrete in env.included_specs_by_hash[included_concrete].values()]
    else:
        return []


class ReuseStrategy(enum.Enum):
    ROOTS = enum.auto()
    DEPENDENCIES = enum.auto()
    NONE = enum.auto()


class ReusableSpecsSelector:
    """Selects specs that can be reused during concretization."""

    def __init__(self, configuration: spack.config.Configuration) -> None:
        self.configuration = configuration
        self.store = spack.store.create(configuration)
        self.reuse_strategy = ReuseStrategy.ROOTS

        reuse_yaml = self.configuration.get("concretizer:reuse", False)
        self.reuse_sources = []
        if not isinstance(reuse_yaml, Mapping):
            if reuse_yaml is False:
                self.reuse_strategy = ReuseStrategy.NONE
            if reuse_yaml == "dependencies":
                self.reuse_strategy = ReuseStrategy.DEPENDENCIES
            self.reuse_sources.extend(
                [
                    SpecFilter.from_store(
                        configuration=self.configuration, include=[], exclude=[]
                    ),
                    SpecFilter.from_buildcache(
                        configuration=self.configuration, include=[], exclude=[]
                    ),
                    SpecFilter.from_environment(
                        configuration=self.configuration,
                        include=[],
                        exclude=[],
                        env=spack.environment.active_environment(),  # with all concrete includes
                    ),
                ]
            )
        else:
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
                    active_env = spack.environment.active_environment()
                    if active_env and env_dir in active_env.included_concrete_envs:
                        # If the environment is included as a concrete environment, use the
                        # local copy of specs in the active environment.
                        # note: included concrete environments are only updated at concretization
                        #       time, and reuse needs to match the included specs.
                        self.reuse_sources.append(
                            SpecFilter.from_environment_included_concrete(
                                self.configuration,
                                include=include,
                                exclude=exclude,
                                env=active_env,
                                included_concrete=env_dir,
                            )
                        )
                    else:
                        # If the environment is not included as a concrete environment, use the
                        # current specs from its lockfile.
                        self.reuse_sources.append(
                            SpecFilter.from_environment(
                                self.configuration,
                                include=include,
                                exclude=exclude,
                                env=spack.environment.environment_from_name_or_dir(env_dir),
                            )
                        )
                elif source["type"] == "environment":
                    # reusing from the current environment implicitly reuses from all of the
                    # included concrete environments
                    self.reuse_sources.append(
                        SpecFilter.from_environment(
                            self.configuration,
                            include=include,
                            exclude=exclude,
                            env=spack.environment.active_environment(),
                        )
                    )
                elif source["type"] == "local":
                    self.reuse_sources.append(
                        SpecFilter.from_store(self.configuration, include=include, exclude=exclude)
                    )
                elif source["type"] == "buildcache":
                    self.reuse_sources.append(
                        SpecFilter.from_buildcache(
                            self.configuration, include=include, exclude=exclude
                        )
                    )

    def reusable_specs(self, specs: List[spack.spec.Spec]) -> List[spack.spec.Spec]:
        if self.reuse_strategy == ReuseStrategy.NONE:
            return []

        result = []
        for reuse_source in self.reuse_sources:
            result.extend(reuse_source.selected_specs())
        # If we only want to reuse dependencies, remove the root specs
        if self.reuse_strategy == ReuseStrategy.DEPENDENCIES:
            result = [spec for spec in result if not any(root in spec for root in specs)]

        return result
