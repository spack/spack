# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import collections
import os
import pathlib
import warnings
from typing import ClassVar, Dict, List, Optional

import spack.compilers.config
import spack.config
import spack.error
import spack.llnl.util.lang as lang
import spack.spec
import spack.tengine as tengine
import spack.util.environment
from spack.aliases import BUILTIN_TO_LEGACY_COMPILER

from .common import BaseConfiguration, BaseContext, BaseFileLayout, BaseModuleFileWriter


def guess_core_compilers(name, store=False) -> List[spack.spec.Spec]:
    """Guesses the list of core compilers installed in the system.

    Args:
        store (bool): if True writes the core compilers to the
            modules.yaml configuration file

    Returns:
        List of found core compilers
    """
    core_compilers = []
    for compiler in spack.compilers.config.all_compilers(init_config=False):
        for attr in ("cc", "cxx", "fc"):
            try:
                path = getattr(compiler.package, attr)
                if path and str(pathlib.Path(path).parent) in spack.util.environment.SYSTEM_DIRS:
                    core_compilers.append(compiler)
                    break
            except (KeyError, TypeError, AttributeError):
                continue

    if store and core_compilers:
        # If we asked to store core compilers, update the entry
        # in the default modify scope (i.e. within the directory hierarchy
        # of Spack itself)
        modules_cfg = spack.config.get(
            "modules:" + name, {}, scope=spack.config.default_modify_scope()
        )
        modules_cfg.setdefault("lmod", {})["core_compilers"] = [str(x) for x in core_compilers]
        spack.config.set("modules:" + name, modules_cfg, scope=spack.config.default_modify_scope())

    return core_compilers


class LmodConfiguration(BaseConfiguration):
    """Configuration class for lmod module files."""

    module_system = "lmod"
    _registry: ClassVar[Dict] = {}

    @staticmethod
    def make_layout(
        spec: spack.spec.Spec, module_set_name: str, explicit: Optional[bool] = None
    ) -> BaseFileLayout:
        configuration = LmodConfiguration.make_configuration(spec, module_set_name, explicit)
        return LmodFileLayout(configuration)

    @staticmethod
    def make_context(
        spec: spack.spec.Spec,
        module_set_name: str,
        *,
        explicit: Optional[bool] = None,
        layout: BaseFileLayout,
    ) -> BaseContext:
        configuration = LmodConfiguration.make_configuration(spec, module_set_name, explicit)
        return LmodContext(configuration, layout)

    default_projections = {"all": "{name}/{version}"}

    compiler: Optional[spack.spec.Spec]

    def __init__(self, spec: spack.spec.Spec, module_set_name: str, explicit: bool) -> None:
        super().__init__(spec, module_set_name, explicit)

        candidates = collections.defaultdict(list)
        language_virtuals = ("c", "cxx", "fortran")

        for node in spec.traverse(deptype=("link", "run")):
            for language in language_virtuals:
                candidates[language].extend(node.dependencies(virtuals=(language,)))

        self.compiler = None

        for language in language_virtuals:
            if candidates[language]:
                self.compiler = candidates[language][0]
                if len(set(candidates[language])) > 1:
                    warnings.warn(
                        f"{spec.short_spec} uses more than one compiler, and might not fit the "
                        f"LMod hierarchy. Using {self.compiler.short_spec} as the LMod compiler."
                    )
                break

    @property
    def core_compilers(self) -> List[spack.spec.Spec]:
        """Returns the list of "Core" compilers

        Raises:
            CoreCompilersNotFoundError: if the key was not specified in the configuration file or
                the sequence is empty
        """
        compilers = []
        for c in self.configuration(self.name).get("core_compilers", []):
            compilers.extend(spack.spec.Spec(f"%{c}").dependencies())

        if not compilers:
            compilers = guess_core_compilers(self.name, store=True)

        if not compilers:
            msg = 'the key "core_compilers" must be set in modules.yaml'
            raise CoreCompilersNotFoundError(msg)

        return compilers

    @property
    def core_specs(self):
        """Returns the list of "Core" specs"""
        return self.configuration(self.name).get("core_specs", [])

    @property
    def filter_hierarchy_specs(self):
        """Returns the dict of specs with modified hierarchies"""
        return self.configuration(self.name).get("filter_hierarchy_specs", {})

    @property
    @lang.memoized
    def hierarchy_tokens(self):
        """Returns the list of tokens that are part of the modulefile
        hierarchy. ``compiler`` is always present.
        """
        tokens = self.configuration(self.name).get("hierarchy", [])

        # Append 'compiler' which is always implied
        tokens.append("compiler")

        # Deduplicate tokens in case duplicates have been coded
        tokens = list(lang.dedupe(tokens))

        return tokens

    @property
    @lang.memoized
    def requires(self):
        """Returns a dictionary mapping all the requirements of this spec to the actual provider.

        The ``compiler`` key is always present among the requirements.
        """
        # If it's a core_spec, lie and say it requires a core compiler
        if any(self.spec.satisfies(core_spec) for core_spec in self.core_specs):
            return {"compiler": self.core_compilers[0]}

        hierarchy_filter_list = []
        for spec, filter_list in self.filter_hierarchy_specs.items():
            if self.spec.satisfies(spec):
                hierarchy_filter_list = filter_list
                break

        # Keep track of the requirements that this package has in terms
        # of virtual packages that participate in the hierarchical structure
        requirements = {"compiler": self.compiler or self.core_compilers[0]}

        # For each dependency in the hierarchy
        for x in self.hierarchy_tokens:
            # Skip anything filtered for this spec
            if x in hierarchy_filter_list:
                continue

            # If I depend on it
            if x in self.spec and not (self.spec.name == x or self.spec.package.provides(x)):
                requirements[x] = self.spec[x]  # record the actual provider

        return requirements

    @property
    def provides(self):
        """Returns a dictionary mapping all the services provided by this
        spec to the spec itself.
        """
        provides = {}

        # Treat the 'compiler' case in a special way, as compilers are not
        # virtual dependencies in spack

        # If it is in the list of supported compilers family -> compiler
        if self.spec.name in spack.compilers.config.supported_compilers():
            provides["compiler"] = spack.spec.Spec(self.spec.format("{name}{@versions}"))
        elif self.spec.name in BUILTIN_TO_LEGACY_COMPILER:
            # If it is the package for a supported compiler, but of a different name
            cname = BUILTIN_TO_LEGACY_COMPILER[self.spec.name]
            provides["compiler"] = spack.spec.Spec(cname, self.spec.versions)

        # All the other tokens in the hierarchy must be virtual dependencies
        for x in self.hierarchy_tokens:
            if self.spec.name == x or self.spec.package.provides(x):
                provides[x] = self.spec
        return provides

    @property
    def available(self):
        """Returns a dictionary of the services that are currently
        available.
        """
        available = {}
        # What is available is what I require plus what I provide.
        # 'compiler' is the only key that may be overridden.
        available.update(self.requires)
        available.update(self.provides)
        return available

    @property
    @lang.memoized
    def missing(self):
        """Returns the list of tokens that are not available."""
        return [x for x in self.hierarchy_tokens if x not in self.available]

    @property
    def hidden(self):
        # Never hide a module that opens a hierarchy
        if any(
            self.spec.name == x or self.spec.package.provides(x) for x in self.hierarchy_tokens
        ):
            return False
        return super().hidden

    @property
    def hierarchical(self):
        """Returns if hierarchical mode has been enabled, True if not set."""
        return self.module.configuration(self.name).get("hierarchical", True)


class LmodFileLayout(BaseFileLayout):
    """File layout for lmod module files."""

    #: file extension of lua module files
    extension = "lua"

    @property
    def modulerc(self):
        """Returns the modulerc file associated with current module file"""
        return os.path.join(os.path.dirname(self.filename), f".modulerc.{self.extension}")


class LmodContext(BaseContext):
    """Context class for lmod module files."""

    @tengine.context_property
    def conditionally_unlocked_paths(self):
        """Returns the list of paths that are unlocked conditionally.
        Each item in the list is a tuple with the structure (condition, path).
        """
        value = []
        for services_needed, list_of_path_parts in self.layout.unlocked_paths.items():
            if services_needed is None:
                continue
            condition = " and ".join([x + "_name" for x in services_needed])
            for parts in list_of_path_parts:

                def manipulate_path(token):
                    if token in self.conf.hierarchy_tokens:
                        return "{0}_name, {0}_version".format(token)
                    return '"' + token + '"'

                path = ", ".join([manipulate_path(x) for x in parts])
                value.append((condition, path))
        return value


class LmodModulefileWriter(BaseModuleFileWriter):
    """Writer class for lmod module files."""

    configuration_class = LmodConfiguration

    default_template = "modules/modulefile.lua"

    modulerc_header = []

    hide_cmd_format = 'hide_version("%s")'


class CoreCompilersNotFoundError(spack.error.SpackError, KeyError):
    """Error raised if the key ``core_compilers`` has not been specified
    in the configuration file.
    """
