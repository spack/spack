# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Classes and functions to register audit checks for various parts of
Spack and run them on-demand.

To register a new class of sanity checks (e.g. sanity checks for
compilers.yaml), the first action required is to create a new AuditClass
object:

.. code-block:: python

   audit_cfgcmp = AuditClass(
       tag='CFG-COMPILER',
       description='Sanity checks on compilers.yaml',
       kwargs=()
   )

This object is to be used as a decorator to register functions
that will perform each a single check:

.. code-block:: python

   @audit_cfgcmp
   def _search_duplicate_compilers(error_cls):
       pass

These functions need to take as argument the keywords declared when
creating the decorator object plus an ``error_cls`` argument at the
end, acting as a factory to create Error objects. It should return a
(possibly empty) list of errors.

Calls to each of these functions are triggered by the ``run`` method of
the decorator object, that will forward the keyword arguments passed
as input.
"""
import ast
import collections
import collections.abc
import glob
import inspect
import io
import itertools
import pathlib
import pickle
import re
import warnings
from urllib.request import urlopen

import llnl.util.lang

import spack.config
import spack.patch
import spack.repo
import spack.spec
import spack.util.crypto
import spack.util.spack_yaml as syaml
import spack.variant

#: Map an audit tag to a list of callables implementing checks
CALLBACKS = {}

#: Map a group of checks to the list of related audit tags
GROUPS = collections.defaultdict(list)


class Error:
    """Information on an error reported in a test."""

    def __init__(self, summary, details):
        self.summary = summary
        self.details = tuple(details)

    def __str__(self):
        return self.summary + "\n" + "\n".join(["    " + detail for detail in self.details])

    def __eq__(self, other):
        if self.summary != other.summary or self.details != other.details:
            return False
        return True

    def __hash__(self):
        value = (self.summary, self.details)
        return hash(value)


class AuditClass(collections.abc.Sequence):
    def __init__(self, group, tag, description, kwargs):
        """Return an object that acts as a decorator to register functions
        associated with a specific class of sanity checks.

        Args:
            group (str): group in which this check is to be inserted
            tag (str): tag uniquely identifying the class of sanity checks
            description (str): description of the sanity checks performed
                by this tag
            kwargs (tuple of str): keyword arguments that each registered
                function needs to accept
        """
        if tag in CALLBACKS:
            msg = 'audit class "{0}" already registered'
            raise ValueError(msg.format(tag))

        self.group = group
        self.tag = tag
        self.description = description
        self.kwargs = kwargs
        self.callbacks = []

        # Init the list of hooks
        CALLBACKS[self.tag] = self

        # Update the list of tags in the group
        GROUPS[self.group].append(self.tag)

    def __call__(self, func):
        self.callbacks.append(func)

    def __getitem__(self, item):
        return self.callbacks[item]

    def __len__(self):
        return len(self.callbacks)

    def run(self, **kwargs):
        msg = 'please pass "{0}" as keyword arguments'
        msg = msg.format(", ".join(self.kwargs))
        assert set(self.kwargs) == set(kwargs), msg

        errors = []
        kwargs["error_cls"] = Error
        for fn in self.callbacks:
            errors.extend(fn(**kwargs))

        return errors


def run_group(group, **kwargs):
    """Run the checks that are part of the group passed as argument.

    Args:
        group (str): group of checks to be run
        **kwargs: keyword arguments forwarded to the checks

    Returns:
        List of (tag, errors) that failed.
    """
    reports = []
    for check in GROUPS[group]:
        errors = run_check(check, **kwargs)
        reports.append((check, errors))
    return reports


def run_check(tag, **kwargs):
    """Run the checks associated with a single tag.

    Args:
        tag (str): tag of the check
        **kwargs: keyword arguments forwarded to the checks

    Returns:
        Errors occurred during the checks
    """
    return CALLBACKS[tag].run(**kwargs)


# TODO: For the generic check to be useful for end users,
# TODO: we need to implement hooks like described in
# TODO: https://github.com/spack/spack/pull/23053/files#r630265011
#: Generic checks relying on global state
generic = AuditClass(
    group="generic",
    tag="GENERIC",
    description="Generic checks relying on global variables",
    kwargs=(),
)


#: Sanity checks on compilers.yaml
config_compiler = AuditClass(
    group="configs", tag="CFG-COMPILER", description="Sanity checks on compilers.yaml", kwargs=()
)


@config_compiler
def _search_duplicate_compilers(error_cls):
    """Report compilers with the same spec and two different definitions"""
    errors = []

    compilers = list(sorted(spack.config.get("compilers"), key=lambda x: x["compiler"]["spec"]))
    for spec, group in itertools.groupby(compilers, key=lambda x: x["compiler"]["spec"]):
        group = list(group)
        if len(group) == 1:
            continue

        error_msg = "Compiler defined multiple times: {0}"
        try:
            details = [str(x._start_mark).strip() for x in group]
        except Exception:
            details = []
        errors.append(error_cls(summary=error_msg.format(spec), details=details))

    return errors


#: Sanity checks on packages.yaml
config_packages = AuditClass(
    group="configs", tag="CFG-PACKAGES", description="Sanity checks on packages.yaml", kwargs=()
)


@config_packages
def _search_duplicate_specs_in_externals(error_cls):
    """Search for duplicate specs declared as externals"""
    errors, externals = [], collections.defaultdict(list)
    packages_yaml = spack.config.get("packages")

    for name, pkg_config in packages_yaml.items():
        # No externals can be declared under all
        if name == "all" or "externals" not in pkg_config:
            continue

        current_externals = pkg_config["externals"]
        for entry in current_externals:
            # Ask for the string representation of the spec to normalize
            # aspects of the spec that may be represented in multiple ways
            # e.g. +foo or foo=true
            key = str(spack.spec.Spec(entry["spec"]))
            externals[key].append(entry)

    for spec, entries in sorted(externals.items()):
        # If there's a single external for a spec we are fine
        if len(entries) < 2:
            continue

        # Otherwise wwe need to report an error
        error_msg = "Multiple externals share the same spec: {0}".format(spec)
        try:
            lines = [str(x._start_mark).strip() for x in entries]
            details = (
                ["Please remove all but one of the following entries:"]
                + lines
                + ["as they might result in non-deterministic hashes"]
            )
        except (TypeError, AttributeError):
            details = []

        errors.append(error_cls(summary=error_msg, details=details))

    return errors


@config_packages
def _deprecated_preferences(error_cls):
    """Search package preferences deprecated in v0.21 (and slated for removal in v0.22)"""
    # TODO (v0.22): remove this audit as the attributes will not be allowed in config
    errors = []
    packages_yaml = spack.config.CONFIG.get_config("packages")

    def make_error(attribute_name, config_data, summary):
        s = io.StringIO()
        s.write("Occurring in the following file:\n")
        dict_view = syaml.syaml_dict((k, v) for k, v in config_data.items() if k == attribute_name)
        syaml.dump_config(dict_view, stream=s, blame=True)
        return error_cls(summary=summary, details=[s.getvalue()])

    if "all" in packages_yaml and "version" in packages_yaml["all"]:
        summary = "Using the deprecated 'version' attribute under 'packages:all'"
        errors.append(make_error("version", packages_yaml["all"], summary))

    for package_name in packages_yaml:
        if package_name == "all":
            continue

        package_conf = packages_yaml[package_name]
        for attribute in ("compiler", "providers", "target"):
            if attribute not in package_conf:
                continue
            summary = (
                f"Using the deprecated '{attribute}' attribute " f"under 'packages:{package_name}'"
            )
            errors.append(make_error(attribute, package_conf, summary))

    return errors


@config_packages
def _avoid_mismatched_variants(error_cls):
    """Warns if variant preferences have mismatched types or names."""
    errors = []
    packages_yaml = spack.config.CONFIG.get_config("packages")

    for pkg_name in packages_yaml:
        # 'all:' must be more forgiving, since it is setting defaults for everything
        if pkg_name == "all" or "variants" not in packages_yaml[pkg_name]:
            continue

        preferences = packages_yaml[pkg_name]["variants"]
        if not isinstance(preferences, list):
            preferences = [preferences]

        for variants in preferences:
            current_spec = spack.spec.Spec(variants)
            pkg_cls = spack.repo.PATH.get_pkg_class(pkg_name)
            for variant in current_spec.variants.values():
                # Variant does not exist at all
                if variant.name not in pkg_cls.variants:
                    summary = (
                        f"Setting a preference for the '{pkg_name}' package to the "
                        f"non-existing variant '{variant.name}'"
                    )
                    errors.append(_make_config_error(preferences, summary, error_cls=error_cls))
                    continue

                # Variant cannot accept this value
                s = spack.spec.Spec(pkg_name)
                try:
                    s.update_variant_validate(variant.name, variant.value)
                except Exception:
                    summary = (
                        f"Setting the variant '{variant.name}' of the '{pkg_name}' package "
                        f"to the invalid value '{str(variant)}'"
                    )
                    errors.append(_make_config_error(preferences, summary, error_cls=error_cls))

    return errors


@config_packages
def _wrongly_named_spec(error_cls):
    """Warns if the wrong name is used for an external spec"""
    errors = []
    packages_yaml = spack.config.CONFIG.get_config("packages")
    for pkg_name in packages_yaml:
        if pkg_name == "all":
            continue

        externals = packages_yaml[pkg_name].get("externals", [])
        is_virtual = spack.repo.PATH.is_virtual(pkg_name)
        for entry in externals:
            spec = spack.spec.Spec(entry["spec"])
            regular_pkg_is_wrong = not is_virtual and pkg_name != spec.name
            virtual_pkg_is_wrong = is_virtual and not any(
                p.name == spec.name for p in spack.repo.PATH.providers_for(pkg_name)
            )
            if regular_pkg_is_wrong or virtual_pkg_is_wrong:
                summary = f"Wrong external spec detected for '{pkg_name}': {spec}"
                errors.append(_make_config_error(entry, summary, error_cls=error_cls))
    return errors


def _make_config_error(config_data, summary, error_cls):
    s = io.StringIO()
    s.write("Occurring in the following file:\n")
    syaml.dump_config(config_data, stream=s, blame=True)
    return error_cls(summary=summary, details=[s.getvalue()])


#: Sanity checks on package directives
package_directives = AuditClass(
    group="packages",
    tag="PKG-DIRECTIVES",
    description="Sanity checks on specs used in directives",
    kwargs=("pkgs",),
)

package_attributes = AuditClass(
    group="packages",
    tag="PKG-ATTRIBUTES",
    description="Sanity checks on reserved attributes of packages",
    kwargs=("pkgs",),
)


package_properties = AuditClass(
    group="packages",
    tag="PKG-PROPERTIES",
    description="Sanity checks on properties a package should maintain",
    kwargs=("pkgs",),
)


#: Sanity checks on linting
# This can take some time, so it's run separately from packages
package_https_directives = AuditClass(
    group="packages-https",
    tag="PKG-HTTPS-DIRECTIVES",
    description="Sanity checks on https checks of package urls, etc.",
    kwargs=("pkgs",),
)


@package_directives
def _check_build_test_callbacks(pkgs, error_cls):
    """Ensure stand-alone test method is not included in build-time callbacks"""
    errors = []
    for pkg_name in pkgs:
        pkg_cls = spack.repo.PATH.get_pkg_class(pkg_name)
        test_callbacks = getattr(pkg_cls, "build_time_test_callbacks", None)

        # TODO (post-34236): "test*"->"test_*" once remove deprecated methods
        # TODO (post-34236): "test"->"test_" once remove deprecated methods
        has_test_method = test_callbacks and any([m.startswith("test") for m in test_callbacks])
        if has_test_method:
            msg = '{0} package contains "test*" method(s) in ' "build_time_test_callbacks"
            instr = 'Remove all methods whose names start with "test" from: [{0}]'.format(
                ", ".join(test_callbacks)
            )
            errors.append(error_cls(msg.format(pkg_name), [instr]))

    return errors


@package_directives
def _check_patch_urls(pkgs, error_cls):
    """Ensure that patches fetched from GitHub and GitLab have stable sha256
    hashes."""
    github_patch_url_re = (
        r"^https?://(?:patch-diff\.)?github(?:usercontent)?\.com/"
        r".+/.+/(?:commit|pull)/[a-fA-F0-9]+\.(?:patch|diff)"
    )
    # Only .diff URLs have stable/full hashes:
    # https://forum.gitlab.com/t/patches-with-full-index/29313
    gitlab_patch_url_re = (
        r"^https?://(?:.+)?gitlab(?:.+)/"
        r".+/.+/-/(?:commit|merge_requests)/[a-fA-F0-9]+\.(?:patch|diff)"
    )

    errors = []
    for pkg_name in pkgs:
        pkg_cls = spack.repo.PATH.get_pkg_class(pkg_name)
        for condition, patches in pkg_cls.patches.items():
            for patch in patches:
                if not isinstance(patch, spack.patch.UrlPatch):
                    continue

                if re.match(github_patch_url_re, patch.url):
                    full_index_arg = "?full_index=1"
                    if not patch.url.endswith(full_index_arg):
                        errors.append(
                            error_cls(
                                "patch URL in package {0} must end with {1}".format(
                                    pkg_cls.name, full_index_arg
                                ),
                                [patch.url],
                            )
                        )
                elif re.match(gitlab_patch_url_re, patch.url):
                    if not patch.url.endswith(".diff"):
                        errors.append(
                            error_cls(
                                "patch URL in package {0} must end with .diff".format(
                                    pkg_cls.name
                                ),
                                [patch.url],
                            )
                        )

    return errors


@package_attributes
def _search_for_reserved_attributes_names_in_packages(pkgs, error_cls):
    """Ensure that packages don't override reserved names"""
    RESERVED_NAMES = ("name",)
    errors = []
    for pkg_name in pkgs:
        name_definitions = collections.defaultdict(list)
        pkg_cls = spack.repo.PATH.get_pkg_class(pkg_name)

        for cls_item in inspect.getmro(pkg_cls):
            for name in RESERVED_NAMES:
                current_value = cls_item.__dict__.get(name)
                if current_value is None:
                    continue
                name_definitions[name].append((cls_item, current_value))

        for name in RESERVED_NAMES:
            if len(name_definitions[name]) == 1:
                continue

            error_msg = (
                "Package '{}' overrides the '{}' attribute or method, "
                "which is reserved for Spack internal use"
            )
            definitions = [
                "defined in '{}'".format(x[0].__module__) for x in name_definitions[name]
            ]
            errors.append(error_cls(error_msg.format(pkg_name, name), definitions))

    return errors


@package_properties
def _ensure_all_package_names_are_lowercase(pkgs, error_cls):
    """Ensure package names are lowercase and consistent"""
    badname_regex, errors = re.compile(r"[_A-Z]"), []
    for pkg_name in pkgs:
        if badname_regex.search(pkg_name):
            error_msg = "Package name '{}' is either lowercase or conatine '_'".format(pkg_name)
            errors.append(error_cls(error_msg, []))
    return errors


@package_properties
def _ensure_packages_are_pickeleable(pkgs, error_cls):
    """Ensure that package objects are pickleable"""
    errors = []
    for pkg_name in pkgs:
        pkg_cls = spack.repo.PATH.get_pkg_class(pkg_name)
        pkg = pkg_cls(spack.spec.Spec(pkg_name))
        try:
            pickle.dumps(pkg)
        except Exception as e:
            error_msg = "Package '{}' failed to pickle".format(pkg_name)
            details = ["{}".format(str(e))]
            errors.append(error_cls(error_msg, details))
    return errors


@package_properties
def _ensure_packages_are_unparseable(pkgs, error_cls):
    """Ensure that all packages can unparse and that unparsed code is valid Python"""
    import spack.util.package_hash as ph

    errors = []
    for pkg_name in pkgs:
        try:
            source = ph.canonical_source(pkg_name, filter_multimethods=False)
        except Exception as e:
            error_msg = "Package '{}' failed to unparse".format(pkg_name)
            details = ["{}".format(str(e))]
            errors.append(error_cls(error_msg, details))
            continue

        try:
            compile(source, "internal", "exec", ast.PyCF_ONLY_AST)
        except Exception as e:
            error_msg = "The unparsed package '{}' failed to compile".format(pkg_name)
            details = ["{}".format(str(e))]
            errors.append(error_cls(error_msg, details))

    return errors


@package_properties
def _ensure_all_versions_can_produce_a_fetcher(pkgs, error_cls):
    """Ensure all versions in a package can produce a fetcher"""
    errors = []
    for pkg_name in pkgs:
        pkg_cls = spack.repo.PATH.get_pkg_class(pkg_name)
        pkg = pkg_cls(spack.spec.Spec(pkg_name))
        try:
            spack.fetch_strategy.check_pkg_attributes(pkg)
            for version in pkg.versions:
                assert spack.fetch_strategy.for_package_version(pkg, version)
        except Exception as e:
            error_msg = "The package '{}' cannot produce a fetcher for some of its versions"
            details = ["{}".format(str(e))]
            errors.append(error_cls(error_msg.format(pkg_name), details))
    return errors


@package_properties
def _ensure_docstring_and_no_fixme(pkgs, error_cls):
    """Ensure the package has a docstring and no fixmes"""
    errors = []
    fixme_regexes = [
        re.compile(r"remove this boilerplate"),
        re.compile(r"FIXME: Put"),
        re.compile(r"FIXME: Add"),
        re.compile(r"example.com"),
    ]
    for pkg_name in pkgs:
        details = []
        filename = spack.repo.PATH.filename_for_package_name(pkg_name)
        with open(filename, "r") as package_file:
            for i, line in enumerate(package_file):
                pattern = next((r for r in fixme_regexes if r.search(line)), None)
                if pattern:
                    details.append(
                        "%s:%d: boilerplate needs to be removed: %s" % (filename, i, line.strip())
                    )
        if details:
            error_msg = "Package '{}' contains boilerplate that need to be removed"
            errors.append(error_cls(error_msg.format(pkg_name), details))

        pkg_cls = spack.repo.PATH.get_pkg_class(pkg_name)
        if not pkg_cls.__doc__:
            error_msg = "Package '{}' miss a docstring"
            errors.append(error_cls(error_msg.format(pkg_name), []))

    return errors


@package_properties
def _ensure_all_packages_use_sha256_checksums(pkgs, error_cls):
    """Ensure no packages use md5 checksums"""
    errors = []
    for pkg_name in pkgs:
        pkg_cls = spack.repo.PATH.get_pkg_class(pkg_name)
        if pkg_cls.manual_download:
            continue

        pkg = pkg_cls(spack.spec.Spec(pkg_name))

        def invalid_sha256_digest(fetcher):
            if getattr(fetcher, "digest", None):
                h = spack.util.crypto.hash_algo_for_digest(fetcher.digest)
                if h != "sha256":
                    return h, True
            return None, False

        error_msg = "Package '{}' does not use sha256 checksum".format(pkg_name)
        details = []
        for v, args in pkg.versions.items():
            fetcher = spack.fetch_strategy.for_package_version(pkg, v)
            digest, is_bad = invalid_sha256_digest(fetcher)
            if is_bad:
                details.append("{}@{} uses {}".format(pkg_name, v, digest))

        for _, resources in pkg.resources.items():
            for resource in resources:
                digest, is_bad = invalid_sha256_digest(resource.fetcher)
                if is_bad:
                    details.append("Resource in '{}' uses {}".format(pkg_name, digest))
        if details:
            errors.append(error_cls(error_msg, details))

    return errors


@package_properties
def _ensure_env_methods_are_ported_to_builders(pkgs, error_cls):
    """Ensure that methods modifying the build environment are ported to builder classes."""
    errors = []
    for pkg_name in pkgs:
        pkg_cls = spack.repo.PATH.get_pkg_class(pkg_name)
        buildsystem_variant, _ = pkg_cls.variants["build_system"]
        buildsystem_names = [getattr(x, "value", x) for x in buildsystem_variant.values]
        builder_cls_names = [spack.builder.BUILDER_CLS[x].__name__ for x in buildsystem_names]
        module = pkg_cls.module
        has_builders_in_package_py = any(
            getattr(module, name, False) for name in builder_cls_names
        )
        if not has_builders_in_package_py:
            continue

        for method_name in ("setup_build_environment", "setup_dependent_build_environment"):
            if hasattr(pkg_cls, method_name):
                msg = (
                    "Package '{}' need to move the '{}' method from the package class to the"
                    " appropriate builder class".format(pkg_name, method_name)
                )
                errors.append(error_cls(msg, []))

    return errors


@package_https_directives
def _linting_package_file(pkgs, error_cls):
    """Check for correctness of links"""
    errors = []
    for pkg_name in pkgs:
        pkg_cls = spack.repo.PATH.get_pkg_class(pkg_name)

        # Does the homepage have http, and if so, does https work?
        if pkg_cls.homepage.startswith("http://"):
            https = re.sub("http", "https", pkg_cls.homepage, 1)
            try:
                response = urlopen(https)
            except Exception as e:
                msg = 'Error with attempting https for "{0}": '
                errors.append(error_cls(msg.format(pkg_cls.name), [str(e)]))
                continue

            if response.getcode() == 200:
                msg = 'Package "{0}" uses http but has a valid https endpoint.'
                errors.append(msg.format(pkg_cls.name))

    return llnl.util.lang.dedupe(errors)


@package_directives
def _unknown_variants_in_directives(pkgs, error_cls):
    """Report unknown or wrong variants in directives for this package"""
    errors = []
    for pkg_name in pkgs:
        pkg_cls = spack.repo.PATH.get_pkg_class(pkg_name)

        # Check "conflicts" directive
        for trigger, conflicts in pkg_cls.conflicts.items():
            for conflict, _ in conflicts:
                vrn = spack.spec.Spec(conflict)
                try:
                    vrn.constrain(trigger)
                except Exception:
                    # If one of the conflict/trigger includes a platform and the other
                    # includes an os or target, the constraint will fail if the current
                    # platform is not the plataform in the conflict/trigger. Audit the
                    # conflict and trigger separately in that case.
                    # When os and target constraints can be created independently of
                    # the platform, TODO change this back to add an error.
                    errors.extend(
                        _analyze_variants_in_directive(
                            pkg_cls,
                            spack.spec.Spec(trigger),
                            directive="conflicts",
                            error_cls=error_cls,
                        )
                    )
                errors.extend(
                    _analyze_variants_in_directive(
                        pkg_cls, vrn, directive="conflicts", error_cls=error_cls
                    )
                )

        # Check "depends_on" directive
        for trigger in pkg_cls.dependencies:
            vrn = spack.spec.Spec(trigger)
            errors.extend(
                _analyze_variants_in_directive(
                    pkg_cls, vrn, directive="depends_on", error_cls=error_cls
                )
            )

        # Check "provides" directive
        for when_spec in pkg_cls.provided:
            errors.extend(
                _analyze_variants_in_directive(
                    pkg_cls, when_spec, directive="provides", error_cls=error_cls
                )
            )

        # Check "resource" directive
        for vrn in pkg_cls.resources:
            errors.extend(
                _analyze_variants_in_directive(
                    pkg_cls, vrn, directive="resource", error_cls=error_cls
                )
            )

    return llnl.util.lang.dedupe(errors)


@package_directives
def _issues_in_depends_on_directive(pkgs, error_cls):
    """Reports issues with 'depends_on' directives.

    Issues might be unknown dependencies, unknown variants or variant values, or declaration
    of nested dependencies.
    """
    errors = []
    for pkg_name in pkgs:
        pkg_cls = spack.repo.PATH.get_pkg_class(pkg_name)
        filename = spack.repo.PATH.filename_for_package_name(pkg_name)

        for when, deps_by_name in pkg_cls.dependencies.items():
            for dep_name, dep in deps_by_name.items():
                # Check if there are nested dependencies declared. We don't want directives like:
                #
                #     depends_on('foo+bar ^fee+baz')
                #
                # but we'd like to have two dependencies listed instead.
                nested_dependencies = dep.spec.dependencies()
                if nested_dependencies:
                    summary = f"{pkg_name}: nested dependency declaration '{dep.spec}'"
                    ndir = len(nested_dependencies) + 1
                    details = [
                        f"split depends_on('{dep.spec}', when='{when}') into {ndir} directives",
                        f"in {filename}",
                    ]
                    errors.append(error_cls(summary=summary, details=details))

                def check_virtual_with_variants(spec, msg):
                    if not spec.virtual or not spec.variants:
                        return
                    error = error_cls(
                        f"{pkg_name}: {msg}",
                        f"remove variants from '{spec}' in depends_on directive in {filename}",
                    )
                    errors.append(error)

                check_virtual_with_variants(dep.spec, "virtual dependency cannot have variants")
                check_virtual_with_variants(dep.spec, "virtual when= spec cannot have variants")

                # No need to analyze virtual packages
                if spack.repo.PATH.is_virtual(dep_name):
                    continue

                # check for unknown dependencies
                try:
                    dependency_pkg_cls = spack.repo.PATH.get_pkg_class(dep_name)
                except spack.repo.UnknownPackageError:
                    # This dependency is completely missing, so report
                    # and continue the analysis
                    summary = f"{pkg_name}: unknown package '{dep_name}' in 'depends_on' directive"
                    details = [f" in {filename}"]
                    errors.append(error_cls(summary=summary, details=details))
                    continue

                # Check for self-referential specs similar to:
                #
                # depends_on("foo@X.Y", when="^foo+bar")
                #
                # That would allow clingo to choose whether to have foo@X.Y+bar in the graph.
                problematic_edges = [
                    x for x in when.edges_to_dependencies(dep_name) if not x.virtuals
                ]
                if problematic_edges and not dep.patches:
                    summary = (
                        f"{pkg_name}: dependency on '{dep.spec}' when '{when}' is self-referential"
                    )
                    details = [
                        (
                            f" please specify better using '^[virtuals=...] {dep_name}', or "
                            f"substitute with an equivalent condition on '{pkg_name}'"
                        ),
                        f" in {filename}",
                    ]
                    errors.append(error_cls(summary=summary, details=details))
                    continue

                # check variants
                dependency_variants = dep.spec.variants
                for name, value in dependency_variants.items():
                    try:
                        v, _ = dependency_pkg_cls.variants[name]
                        v.validate_or_raise(value, pkg_cls=dependency_pkg_cls)
                    except Exception as e:
                        summary = (
                            f"{pkg_name}: wrong variant used for dependency in 'depends_on()'"
                        )

                        if isinstance(e, KeyError):
                            error_msg = (
                                f"variant {str(e).strip()} does not exist in package {dep_name}"
                            )
                        error_msg += f" in package '{dep_name}'"

                        errors.append(
                            error_cls(summary=summary, details=[error_msg, f"in {filename}"])
                        )

    return errors


@package_directives
def _ensure_variant_defaults_are_parsable(pkgs, error_cls):
    """Ensures that variant defaults are present and parsable from cli"""
    errors = []
    for pkg_name in pkgs:
        pkg_cls = spack.repo.PATH.get_pkg_class(pkg_name)
        for variant_name, entry in pkg_cls.variants.items():
            variant, _ = entry
            default_is_parsable = (
                # Permitting a default that is an instance on 'int' permits
                # to have foo=false or foo=0. Other falsish values are
                # not allowed, since they can't be parsed from cli ('foo=')
                isinstance(variant.default, int)
                or variant.default
            )
            if not default_is_parsable:
                error_msg = "Variant '{}' of package '{}' has a bad default value"
                errors.append(error_cls(error_msg.format(variant_name, pkg_name), []))
                continue

            try:
                vspec = variant.make_default()
            except spack.variant.MultipleValuesInExclusiveVariantError:
                error_msg = "Cannot create a default value for the variant '{}' in package '{}'"
                errors.append(error_cls(error_msg.format(variant_name, pkg_name), []))
                continue

            try:
                variant.validate_or_raise(vspec, pkg_cls=pkg_cls)
            except spack.variant.InvalidVariantValueError:
                error_msg = (
                    "The default value of the variant '{}' in package '{}' failed validation"
                )
                question = "Is it among the allowed values?"
                errors.append(error_cls(error_msg.format(variant_name, pkg_name), [question]))

    return errors


@package_directives
def _ensure_variants_have_descriptions(pkgs, error_cls):
    """Ensures that all variants have a description."""
    errors = []
    for pkg_name in pkgs:
        pkg_cls = spack.repo.PATH.get_pkg_class(pkg_name)
        for variant_name, entry in pkg_cls.variants.items():
            variant, _ = entry
            if not variant.description:
                error_msg = "Variant '{}' in package '{}' is missing a description"
                errors.append(error_cls(error_msg.format(variant_name, pkg_name), []))

    return errors


@package_directives
def _version_constraints_are_satisfiable_by_some_version_in_repo(pkgs, error_cls):
    """Report if version constraints used in directives are not satisfiable"""
    errors = []
    for pkg_name in pkgs:
        pkg_cls = spack.repo.PATH.get_pkg_class(pkg_name)
        filename = spack.repo.PATH.filename_for_package_name(pkg_name)

        dependencies_to_check = []

        for _, deps_by_name in pkg_cls.dependencies.items():
            for dep_name, dep in deps_by_name.items():
                # Skip virtual dependencies for the time being, check on
                # their versions can be added later
                if spack.repo.PATH.is_virtual(dep_name):
                    continue

                dependencies_to_check.append(dep.spec)

        host_architecture = spack.spec.ArchSpec.default_arch()
        for s in dependencies_to_check:
            dependency_pkg_cls = None
            try:
                dependency_pkg_cls = spack.repo.PATH.get_pkg_class(s.name)
                # Some packages have hacks that might cause failures on some platform
                # Allow to explicitly set conditions to skip version checks in that case
                skip_conditions = getattr(dependency_pkg_cls, "skip_version_audit", [])
                skip_version_check = False
                for condition in skip_conditions:
                    if host_architecture.satisfies(spack.spec.Spec(condition).architecture):
                        skip_version_check = True
                        break
                assert skip_version_check or any(
                    v.intersects(s.versions) for v in list(dependency_pkg_cls.versions)
                )
            except Exception:
                summary = (
                    "{0}: dependency on {1} cannot be satisfied by known versions of {1.name}"
                ).format(pkg_name, s)
                details = ["happening in " + filename]
                if dependency_pkg_cls is not None:
                    details.append(
                        "known versions of {0.name} are {1}".format(
                            s, ", ".join([str(x) for x in dependency_pkg_cls.versions])
                        )
                    )
                errors.append(error_cls(summary=summary, details=details))

    return errors


def _analyze_variants_in_directive(pkg, constraint, directive, error_cls):
    variant_exceptions = (
        spack.variant.InconsistentValidationError,
        spack.variant.MultipleValuesInExclusiveVariantError,
        spack.variant.InvalidVariantValueError,
        KeyError,
    )
    errors = []
    for name, v in constraint.variants.items():
        try:
            variant, _ = pkg.variants[name]
            variant.validate_or_raise(v, pkg_cls=pkg)
        except variant_exceptions as e:
            summary = pkg.name + ': wrong variant in "{0}" directive'
            summary = summary.format(directive)
            filename = spack.repo.PATH.filename_for_package_name(pkg.name)

            error_msg = str(e).strip()
            if isinstance(e, KeyError):
                error_msg = "the variant {0} does not exist".format(error_msg)

            err = error_cls(summary=summary, details=[error_msg, "in " + filename])

            errors.append(err)

    return errors


@package_directives
def _named_specs_in_when_arguments(pkgs, error_cls):
    """Reports named specs in the 'when=' attribute of a directive.

    Note that 'conflicts' is the only directive allowing that.
    """
    errors = []
    for pkg_name in pkgs:
        pkg_cls = spack.repo.PATH.get_pkg_class(pkg_name)

        def _refers_to_pkg(when):
            when_spec = spack.spec.Spec(when)
            return when_spec.name is None or when_spec.name == pkg_name

        def _error_items(when_dict):
            for when, elts in when_dict.items():
                if not _refers_to_pkg(when):
                    yield when, elts, [f"using '{when}', should be '^{when}'"]

        def _extracts_errors(triggers, summary):
            _errors = []
            for trigger in list(triggers):
                if not _refers_to_pkg(trigger):
                    details = [f"using '{trigger}', should be '^{trigger}'"]
                    _errors.append(error_cls(summary=summary, details=details))
            return _errors

        for when, dnames, details in _error_items(pkg_cls.dependencies):
            errors.extend(
                error_cls(f"{pkg_name}: wrong 'when=' condition for '{dname}' dependency", details)
                for dname in dnames
            )

        for vname, (variant, triggers) in pkg_cls.variants.items():
            summary = f"{pkg_name}: wrong 'when=' condition for the '{vname}' variant"
            errors.extend(_extracts_errors(triggers, summary))

        for when, providers, details in _error_items(pkg_cls.provided):
            errors.extend(
                error_cls(f"{pkg_name}: wrong 'when=' condition for '{provided}' virtual", details)
                for provided in providers
            )

        for when, requirements, details in _error_items(pkg_cls.requirements):
            errors.append(
                error_cls(f"{pkg_name}: wrong 'when=' condition in 'requires' directive", details)
            )

        for when, _, details in _error_items(pkg_cls.patches):
            errors.append(
                error_cls(f"{pkg_name}: wrong 'when=' condition in 'patch' directives", details)
            )

        for when, _, details in _error_items(pkg_cls.resources):
            errors.append(
                error_cls(f"{pkg_name}: wrong 'when=' condition in 'resource' directives", details)
            )

    return llnl.util.lang.dedupe(errors)


#: Sanity checks on package directives
external_detection = AuditClass(
    group="externals",
    tag="PKG-EXTERNALS",
    description="Sanity checks for external software detection",
    kwargs=("pkgs",),
)


def packages_with_detection_tests():
    """Return the list of packages with a corresponding detection_test.yaml file."""
    import spack.config
    import spack.util.path

    to_be_tested = []
    for current_repo in spack.repo.PATH.repos:
        namespace = current_repo.namespace
        packages_dir = pathlib.PurePath(current_repo.packages_path)
        pattern = packages_dir / "**" / "detection_test.yaml"
        pkgs_with_tests = [
            f"{namespace}.{str(pathlib.PurePath(x).parent.name)}" for x in glob.glob(str(pattern))
        ]
        to_be_tested.extend(pkgs_with_tests)

    return to_be_tested


@external_detection
def _test_detection_by_executable(pkgs, error_cls):
    """Test drive external detection for packages"""
    import spack.detection

    errors = []

    # Filter the packages and retain only the ones with detection tests
    pkgs_with_tests = packages_with_detection_tests()
    selected_pkgs = []
    for current_package in pkgs_with_tests:
        _, unqualified_name = spack.repo.partition_package_name(current_package)
        # Check for both unqualified name and qualified name
        if unqualified_name in pkgs or current_package in pkgs:
            selected_pkgs.append(current_package)
    selected_pkgs.sort()

    if not selected_pkgs:
        summary = "No detection test to run"
        details = [f'  "{p}" has no detection test' for p in pkgs]
        warnings.warn("\n".join([summary] + details))
        return errors

    for pkg_name in selected_pkgs:
        for idx, test_runner in enumerate(
            spack.detection.detection_tests(pkg_name, spack.repo.PATH)
        ):
            specs = test_runner.execute()
            expected_specs = test_runner.expected_specs

            not_detected = set(expected_specs) - set(specs)
            if not_detected:
                summary = pkg_name + ": cannot detect some specs"
                details = [f'"{s}" was not detected [test_id={idx}]' for s in sorted(not_detected)]
                errors.append(error_cls(summary=summary, details=details))

            not_expected = set(specs) - set(expected_specs)
            if not_expected:
                summary = pkg_name + ": detected unexpected specs"
                msg = '"{0}" was detected, but was not expected [test_id={1}]'
                details = [msg.format(s, idx) for s in sorted(not_expected)]
                errors.append(error_cls(summary=summary, details=details))

    return errors
