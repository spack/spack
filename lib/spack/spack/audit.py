# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
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
import inspect
import itertools
import pickle
import re
from urllib.request import urlopen

import llnl.util.lang

import spack.config
import spack.patch
import spack.repo
import spack.spec
import spack.util.crypto
import spack.variant

#: Map an audit tag to a list of callables implementing checks
CALLBACKS = {}

#: Map a group of checks to the list of related audit tags
GROUPS = collections.defaultdict(list)


class Error(object):
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
        except TypeError:
            details = []

        errors.append(error_cls(summary=error_msg, details=details))

    return errors


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
        pkg_cls = spack.repo.path.get_pkg_class(pkg_name)
        test_callbacks = getattr(pkg_cls, "build_time_test_callbacks", None)

        if test_callbacks and "test" in test_callbacks:
            msg = '{0} package contains "test" method in ' "build_time_test_callbacks"
            instr = 'Remove "test" from: [{0}]'.format(", ".join(test_callbacks))
            errors.append(error_cls(msg.format(pkg_name), [instr]))

    return errors


@package_directives
def _check_patch_urls(pkgs, error_cls):
    """Ensure that patches fetched from GitHub have stable sha256 hashes."""
    github_patch_url_re = (
        r"^https?://(?:patch-diff\.)?github(?:usercontent)?\.com/"
        ".+/.+/(?:commit|pull)/[a-fA-F0-9]*.(?:patch|diff)"
    )

    errors = []
    for pkg_name in pkgs:
        pkg_cls = spack.repo.path.get_pkg_class(pkg_name)
        for condition, patches in pkg_cls.patches.items():
            for patch in patches:
                if not isinstance(patch, spack.patch.UrlPatch):
                    continue

                if not re.match(github_patch_url_re, patch.url):
                    continue

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

    return errors


@package_attributes
def _search_for_reserved_attributes_names_in_packages(pkgs, error_cls):
    """Ensure that packages don't override reserved names"""
    RESERVED_NAMES = ("name",)
    errors = []
    for pkg_name in pkgs:
        name_definitions = collections.defaultdict(list)
        pkg_cls = spack.repo.path.get_pkg_class(pkg_name)

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
        pkg_cls = spack.repo.path.get_pkg_class(pkg_name)
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
        pkg_cls = spack.repo.path.get_pkg_class(pkg_name)
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
        filename = spack.repo.path.filename_for_package_name(pkg_name)
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

        pkg_cls = spack.repo.path.get_pkg_class(pkg_name)
        if not pkg_cls.__doc__:
            error_msg = "Package '{}' miss a docstring"
            errors.append(error_cls(error_msg.format(pkg_name), []))

    return errors


@package_properties
def _ensure_all_packages_use_sha256_checksums(pkgs, error_cls):
    """Ensure no packages use md5 checksums"""
    errors = []
    for pkg_name in pkgs:
        pkg_cls = spack.repo.path.get_pkg_class(pkg_name)
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
        pkg_cls = spack.repo.path.get_pkg_class(pkg_name)
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
        pkg_cls = spack.repo.path.get_pkg_class(pkg_name)

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
        pkg_cls = spack.repo.path.get_pkg_class(pkg_name)

        # Check "conflicts" directive
        for conflict, triggers in pkg_cls.conflicts.items():
            for trigger, _ in triggers:
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
        for _, triggers in pkg_cls.dependencies.items():
            triggers = list(triggers)
            for trigger in list(triggers):
                vrn = spack.spec.Spec(trigger)
                errors.extend(
                    _analyze_variants_in_directive(
                        pkg_cls, vrn, directive="depends_on", error_cls=error_cls
                    )
                )

        # Check "patch" directive
        for _, triggers in pkg_cls.provided.items():
            triggers = [spack.spec.Spec(x) for x in triggers]
            for vrn in triggers:
                errors.extend(
                    _analyze_variants_in_directive(
                        pkg_cls, vrn, directive="patch", error_cls=error_cls
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
def _unknown_variants_in_dependencies(pkgs, error_cls):
    """Report unknown dependencies and wrong variants for dependencies"""
    errors = []
    for pkg_name in pkgs:
        pkg_cls = spack.repo.path.get_pkg_class(pkg_name)
        filename = spack.repo.path.filename_for_package_name(pkg_name)
        for dependency_name, dependency_data in pkg_cls.dependencies.items():
            # No need to analyze virtual packages
            if spack.repo.path.is_virtual(dependency_name):
                continue

            try:
                dependency_pkg_cls = spack.repo.path.get_pkg_class(dependency_name)
            except spack.repo.UnknownPackageError:
                # This dependency is completely missing, so report
                # and continue the analysis
                summary = pkg_name + ": unknown package '{0}' in " "'depends_on' directive".format(
                    dependency_name
                )
                details = [" in " + filename]
                errors.append(error_cls(summary=summary, details=details))
                continue

            for _, dependency_edge in dependency_data.items():
                dependency_variants = dependency_edge.spec.variants
                for name, value in dependency_variants.items():
                    try:
                        v, _ = dependency_pkg_cls.variants[name]
                        v.validate_or_raise(value, pkg_cls=dependency_pkg_cls)
                    except Exception as e:
                        summary = (
                            pkg_name + ": wrong variant used for a "
                            "dependency in a 'depends_on' directive"
                        )
                        error_msg = str(e).strip()
                        if isinstance(e, KeyError):
                            error_msg = "the variant {0} does not " "exist".format(error_msg)
                        error_msg += " in package '" + dependency_name + "'"

                        errors.append(
                            error_cls(summary=summary, details=[error_msg, "in " + filename])
                        )

    return errors


@package_directives
def _ensure_variant_defaults_are_parsable(pkgs, error_cls):
    """Ensures that variant defaults are present and parsable from cli"""
    errors = []
    for pkg_name in pkgs:
        pkg_cls = spack.repo.path.get_pkg_class(pkg_name)
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
                error_msg = "The variant '{}' default value in package '{}' cannot be validated"
                errors.append(error_cls(error_msg.format(variant_name, pkg_name), []))

    return errors


@package_directives
def _version_constraints_are_satisfiable_by_some_version_in_repo(pkgs, error_cls):
    """Report if version constraints used in directives are not satisfiable"""
    errors = []
    for pkg_name in pkgs:
        pkg_cls = spack.repo.path.get_pkg_class(pkg_name)
        filename = spack.repo.path.filename_for_package_name(pkg_name)
        dependencies_to_check = []
        for dependency_name, dependency_data in pkg_cls.dependencies.items():
            # Skip virtual dependencies for the time being, check on
            # their versions can be added later
            if spack.repo.path.is_virtual(dependency_name):
                continue

            dependencies_to_check.extend([edge.spec for edge in dependency_data.values()])

        for s in dependencies_to_check:
            dependency_pkg_cls = None
            try:
                dependency_pkg_cls = spack.repo.path.get_pkg_class(s.name)
                assert any(v.intersects(s.versions) for v in list(dependency_pkg_cls.versions))
            except Exception:
                summary = (
                    "{0}: dependency on {1} cannot be satisfied " "by known versions of {1.name}"
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
            filename = spack.repo.path.filename_for_package_name(pkg.name)

            error_msg = str(e).strip()
            if isinstance(e, KeyError):
                error_msg = "the variant {0} does not exist".format(error_msg)

            err = error_cls(summary=summary, details=[error_msg, "in " + filename])

            errors.append(err)

    return errors
