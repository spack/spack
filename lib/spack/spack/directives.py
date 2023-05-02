# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""This package contains directives that can be used within a package.

Directives are functions that can be called inside a package
definition to modify the package, for example:

    class OpenMpi(Package):
        depends_on("hwloc")
        provides("mpi")
        ...

``provides`` and ``depends_on`` are spack directives.

The available directives are:

  * ``build_system``
  * ``conflicts``
  * ``depends_on``
  * ``extends``
  * ``patch``
  * ``provides``
  * ``resource``
  * ``variant``
  * ``version``
  * ``requires``

"""
import collections.abc
import functools
import os.path
import re
from typing import Any, Callable, List, Optional, Set, Tuple, Union

import llnl.util.lang
import llnl.util.tty.color

import spack.deptypes as dt
import spack.error
import spack.patch
import spack.spec
import spack.url
import spack.util.crypto
import spack.variant
from spack.dependency import Dependency
from spack.fetch_strategy import from_kwargs
from spack.resource import Resource
from spack.version import (
    GitVersion,
    Version,
    VersionChecksumError,
    VersionError,
    VersionLookupError,
)

__all__ = [
    "DirectiveError",
    "DirectiveMeta",
    "version",
    "conflicts",
    "depends_on",
    "extends",
    "maintainers",
    "license",
    "provides",
    "patch",
    "variant",
    "resource",
    "build_system",
    "requires",
]

#: These are variant names used by Spack internally; packages can't use them
reserved_names = ["patches", "dev_path"]

#: Names of possible directives. This list is mostly populated using the @directive decorator.
#: Some directives leverage others and in that case are not automatically added.
directive_names = ["build_system"]

_patch_order_index = 0


def make_when_spec(value):
    """Create a ``Spec`` that indicates when a directive should be applied.

    Directives with ``when`` specs, e.g.:

        patch('foo.patch', when='@4.5.1:')
        depends_on('mpi', when='+mpi')
        depends_on('readline', when=sys.platform() != 'darwin')

    are applied conditionally depending on the value of the ``when``
    keyword argument.  Specifically:

      1. If the ``when`` argument is ``True``, the directive is always applied
      2. If it is ``False``, the directive is never applied
      3. If it is a ``Spec`` string, it is applied when the package's
         concrete spec satisfies the ``when`` spec.

    The first two conditions are useful for the third example case above.
    It allows package authors to include directives that are conditional
    at package definition time, in additional to ones that are evaluated
    as part of concretization.

    Arguments:
        value (spack.spec.Spec or bool): a conditional Spec or a constant ``bool``
           value indicating when a directive should be applied.

    """
    if isinstance(value, spack.spec.Spec):
        return value

    # Unsatisfiable conditions are discarded by the caller, and never
    # added to the package class
    if value is False:
        return False

    # If there is no constraint, the directive should always apply;
    # represent this by returning the unconstrained `Spec()`, which is
    # always satisfied.
    if value is None or value is True:
        return spack.spec.Spec()

    # This is conditional on the spec
    return spack.spec.Spec(value)


class DirectiveMeta(type):
    """Flushes the directives that were temporarily stored in the staging
    area into the package.
    """

    # Set of all known directives
    _directive_dict_names: Set[str] = set()
    _directives_to_be_executed: List[str] = []
    _when_constraints_from_context: List[str] = []
    _default_args: List[dict] = []

    def __new__(cls, name, bases, attr_dict):
        # Initialize the attribute containing the list of directives
        # to be executed. Here we go reversed because we want to execute
        # commands:
        # 1. in the order they were defined
        # 2. following the MRO
        attr_dict["_directives_to_be_executed"] = []
        for base in reversed(bases):
            try:
                directive_from_base = base._directives_to_be_executed
                attr_dict["_directives_to_be_executed"].extend(directive_from_base)
            except AttributeError:
                # The base class didn't have the required attribute.
                # Continue searching
                pass

        # De-duplicates directives from base classes
        attr_dict["_directives_to_be_executed"] = [
            x for x in llnl.util.lang.dedupe(attr_dict["_directives_to_be_executed"])
        ]

        # Move things to be executed from module scope (where they
        # are collected first) to class scope
        if DirectiveMeta._directives_to_be_executed:
            attr_dict["_directives_to_be_executed"].extend(
                DirectiveMeta._directives_to_be_executed
            )
            DirectiveMeta._directives_to_be_executed = []

        return super(DirectiveMeta, cls).__new__(cls, name, bases, attr_dict)

    def __init__(cls, name, bases, attr_dict):
        # The instance is being initialized: if it is a package we must ensure
        # that the directives are called to set it up.

        if "spack.pkg" in cls.__module__:
            # Ensure the presence of the dictionaries associated
            # with the directives
            for d in DirectiveMeta._directive_dict_names:
                setattr(cls, d, {})

            # Lazily execute directives
            for directive in cls._directives_to_be_executed:
                directive(cls)

            # Ignore any directives executed *within* top-level
            # directives by clearing out the queue they're appended to
            DirectiveMeta._directives_to_be_executed = []

        super(DirectiveMeta, cls).__init__(name, bases, attr_dict)

    @staticmethod
    def push_to_context(when_spec):
        """Add a spec to the context constraints."""
        DirectiveMeta._when_constraints_from_context.append(when_spec)

    @staticmethod
    def pop_from_context():
        """Pop the last constraint from the context"""
        return DirectiveMeta._when_constraints_from_context.pop()

    @staticmethod
    def push_default_args(default_args):
        """Push default arguments"""
        DirectiveMeta._default_args.append(default_args)

    @staticmethod
    def pop_default_args():
        """Pop default arguments"""
        return DirectiveMeta._default_args.pop()

    @staticmethod
    def directive(dicts=None):
        """Decorator for Spack directives.

        Spack directives allow you to modify a package while it is being
        defined, e.g. to add version or dependency information.  Directives
        are one of the key pieces of Spack's package "language", which is
        embedded in python.

        Here's an example directive:

        .. code-block:: python

            @directive(dicts='versions')
            version(pkg, ...):
                ...

        This directive allows you write:

        .. code-block:: python

            class Foo(Package):
                version(...)

        The ``@directive`` decorator handles a couple things for you:

          1. Adds the class scope (pkg) as an initial parameter when
             called, like a class method would.  This allows you to modify
             a package from within a directive, while the package is still
             being defined.

          2. It automatically adds a dictionary called "versions" to the
             package so that you can refer to pkg.versions.

        The ``(dicts='versions')`` part ensures that ALL packages in Spack
        will have a ``versions`` attribute after they're constructed, and
        that if no directive actually modified it, it will just be an
        empty dict.

        This is just a modular way to add storage attributes to the
        Package class, and it's how Spack gets information from the
        packages to the core.
        """
        global directive_names

        if isinstance(dicts, str):
            dicts = (dicts,)

        if not isinstance(dicts, collections.abc.Sequence):
            message = "dicts arg must be list, tuple, or string. Found {0}"
            raise TypeError(message.format(type(dicts)))

        # Add the dictionary names if not already there
        DirectiveMeta._directive_dict_names |= set(dicts)

        # This decorator just returns the directive functions
        def _decorator(decorated_function):
            directive_names.append(decorated_function.__name__)

            @functools.wraps(decorated_function)
            def _wrapper(*args, **_kwargs):
                # First merge default args with kwargs
                kwargs = dict()
                for default_args in DirectiveMeta._default_args:
                    kwargs.update(default_args)
                kwargs.update(_kwargs)

                # Inject when arguments from the context
                if DirectiveMeta._when_constraints_from_context:
                    # Check that directives not yet supporting the when= argument
                    # are not used inside the context manager
                    if decorated_function.__name__ == "version":
                        msg = (
                            'directive "{0}" cannot be used within a "when"'
                            ' context since it does not support a "when=" '
                            "argument"
                        )
                        msg = msg.format(decorated_function.__name__)
                        raise DirectiveError(msg)

                    when_constraints = [
                        spack.spec.Spec(x) for x in DirectiveMeta._when_constraints_from_context
                    ]
                    if kwargs.get("when"):
                        when_constraints.append(spack.spec.Spec(kwargs["when"]))
                    when_spec = spack.spec.merge_abstract_anonymous_specs(*when_constraints)

                    kwargs["when"] = when_spec

                # If any of the arguments are executors returned by a
                # directive passed as an argument, don't execute them
                # lazily. Instead, let the called directive handle them.
                # This allows nested directive calls in packages.  The
                # caller can return the directive if it should be queued.
                def remove_directives(arg):
                    directives = DirectiveMeta._directives_to_be_executed
                    if isinstance(arg, (list, tuple)):
                        # Descend into args that are lists or tuples
                        for a in arg:
                            remove_directives(a)
                    else:
                        # Remove directives args from the exec queue
                        remove = next((d for d in directives if d is arg), None)
                        if remove is not None:
                            directives.remove(remove)

                # Nasty, but it's the best way I can think of to avoid
                # side effects if directive results are passed as args
                remove_directives(args)
                remove_directives(list(kwargs.values()))

                # A directive returns either something that is callable on a
                # package or a sequence of them
                result = decorated_function(*args, **kwargs)

                # ...so if it is not a sequence make it so
                values = result
                if not isinstance(values, collections.abc.Sequence):
                    values = (values,)

                DirectiveMeta._directives_to_be_executed.extend(values)

                # wrapped function returns same result as original so
                # that we can nest directives
                return result

            return _wrapper

        return _decorator


directive = DirectiveMeta.directive


@directive("versions")
def version(
    ver: Union[str, int],
    # this positional argument is deprecated, use sha256=... instead
    checksum: Optional[str] = None,
    *,
    # generic version options
    preferred: Optional[bool] = None,
    deprecated: Optional[bool] = None,
    no_cache: Optional[bool] = None,
    # url fetch options
    url: Optional[str] = None,
    extension: Optional[str] = None,
    expand: Optional[bool] = None,
    fetch_options: Optional[dict] = None,
    # url archive verification options
    md5: Optional[str] = None,
    sha1: Optional[str] = None,
    sha224: Optional[str] = None,
    sha256: Optional[str] = None,
    sha384: Optional[str] = None,
    sha512: Optional[str] = None,
    # git fetch options
    git: Optional[str] = None,
    commit: Optional[str] = None,
    tag: Optional[str] = None,
    branch: Optional[str] = None,
    get_full_repo: Optional[bool] = None,
    submodules: Optional[bool] = None,
    submodules_delete: Optional[bool] = None,
    # other version control
    svn: Optional[str] = None,
    hg: Optional[str] = None,
    cvs: Optional[str] = None,
    revision: Optional[str] = None,
    date: Optional[str] = None,
):
    """Adds a version and, if appropriate, metadata for fetching its code.

    The ``version`` directives are aggregated into a ``versions`` dictionary
    attribute with ``Version`` keys and metadata values, where the metadata
    is stored as a dictionary of ``kwargs``.

    The (keyword) arguments are turned into a valid fetch strategy for
    code packages later. See ``spack.fetch_strategy.for_package_version()``.
    """
    kwargs = {
        key: value
        for key, value in (
            ("sha256", sha256),
            ("sha384", sha384),
            ("sha512", sha512),
            ("preferred", preferred),
            ("deprecated", deprecated),
            ("expand", expand),
            ("url", url),
            ("extension", extension),
            ("no_cache", no_cache),
            ("fetch_options", fetch_options),
            ("git", git),
            ("svn", svn),
            ("hg", hg),
            ("cvs", cvs),
            ("get_full_repo", get_full_repo),
            ("branch", branch),
            ("submodules", submodules),
            ("submodules_delete", submodules_delete),
            ("commit", commit),
            ("tag", tag),
            ("revision", revision),
            ("date", date),
            ("md5", md5),
            ("sha1", sha1),
            ("sha224", sha224),
            ("checksum", checksum),
        )
        if value is not None
    }
    return lambda pkg: _execute_version(pkg, ver, **kwargs)


def _execute_version(pkg, ver, **kwargs):
    if (
        (any(s in kwargs for s in spack.util.crypto.hashes) or "checksum" in kwargs)
        and hasattr(pkg, "has_code")
        and not pkg.has_code
    ):
        raise VersionChecksumError(
            "{0}: Checksums not allowed in no-code packages "
            "(see '{1}' version).".format(pkg.name, ver)
        )

    if not isinstance(ver, (int, str)):
        raise VersionError(
            f"{pkg.name}: declared version '{ver!r}' in package should be a string or int."
        )

    # Declared versions are concrete
    version = Version(ver)

    if isinstance(version, GitVersion) and not hasattr(pkg, "git") and "git" not in kwargs:
        args = ", ".join(f"{argname}='{value}'" for argname, value in kwargs.items())
        raise VersionLookupError(
            f"{pkg.name}: spack version directives cannot include git hashes fetched from URLs.\n"
            f"    version('{ver}', {args})"
        )

    # Store kwargs for the package to later with a fetch_strategy.
    pkg.versions[version] = kwargs


def _depends_on(pkg, spec, when=None, type=dt.DEFAULT_TYPES, patches=None):
    when_spec = make_when_spec(when)
    if not when_spec:
        return

    dep_spec = spack.spec.Spec(spec)
    if not dep_spec.name:
        raise DependencyError("Invalid dependency specification in package '%s':" % pkg.name, spec)
    if pkg.name == dep_spec.name:
        raise CircularReferenceError("Package '%s' cannot depend on itself." % pkg.name)

    depflag = dt.canonicalize(type)
    conditions = pkg.dependencies.setdefault(dep_spec.name, {})

    # call this patches here for clarity -- we want patch to be a list,
    # but the caller doesn't have to make it one.

    # Note: we cannot check whether a package is virtual in a directive
    # because directives are run as part of class instantiation, and specs
    # instantiate the package class as part of the `virtual` check.
    # To be technical, specs only instantiate the package class as part of the
    # virtual check if the provider index hasn't been created yet.
    # TODO: There could be a cache warming strategy that would allow us to
    # ensure `Spec.virtual` is a valid thing to call in a directive.
    # For now, we comment out the following check to allow for virtual packages
    # with package files.
    # if patches and dep_spec.virtual:
    #     raise DependencyPatchError("Cannot patch a virtual dependency.")

    # ensure patches is a list
    if patches is None:
        patches = []
    elif not isinstance(patches, (list, tuple)):
        patches = [patches]

    # auto-call patch() directive on any strings in patch list
    patches = [patch(p) if isinstance(p, str) else p for p in patches]
    assert all(callable(p) for p in patches)

    # this is where we actually add the dependency to this package
    if when_spec not in conditions:
        dependency = Dependency(pkg, dep_spec, depflag=depflag)
        conditions[when_spec] = dependency
    else:
        dependency = conditions[when_spec]
        dependency.spec.constrain(dep_spec, deps=False)
        dependency.depflag |= depflag

    # apply patches to the dependency
    for execute_patch in patches:
        execute_patch(dependency)


@directive("conflicts")
def conflicts(conflict_spec, when=None, msg=None):
    """Allows a package to define a conflict.

    Currently, a "conflict" is a concretized configuration that is known
    to be non-valid. For example, a package that is known not to be
    buildable with intel compilers can declare::

        conflicts('%intel')

    To express the same constraint only when the 'foo' variant is
    activated::

        conflicts('%intel', when='+foo')

    Args:
        conflict_spec (spack.spec.Spec): constraint defining the known conflict
        when (spack.spec.Spec): optional constraint that triggers the conflict
        msg (str): optional user defined message
    """

    def _execute_conflicts(pkg):
        # If when is not specified the conflict always holds
        when_spec = make_when_spec(when)
        if not when_spec:
            return

        # Save in a list the conflicts and the associated custom messages
        when_spec_list = pkg.conflicts.setdefault(conflict_spec, [])
        msg_with_name = f"{pkg.name}: {msg}" if msg is not None else msg
        when_spec_list.append((when_spec, msg_with_name))

    return _execute_conflicts


@directive(("dependencies"))
def depends_on(spec, when=None, type=dt.DEFAULT_TYPES, patches=None, version_translator=None):
    """Creates a dict of deps with specs defining when they apply.

    Args:
        spec (spack.spec.Spec or str): the package and constraints depended on
        when (spack.spec.Spec or str): when the dependent satisfies this, it has
            the dependency represented by ``spec``
        type (str or tuple): str or tuple of legal Spack deptypes
        patches (typing.Callable or list): single result of ``patch()`` directive, a
            ``str`` to be passed to ``patch``, or a list of these
        version_translator (function): function to generate a version-ish for spec
            from a parent version. If provided, this function will be called for
            each version defined for pkg, and any non-vacuous result will be used to
            add a dependency with that version as an extra constraint on spec.
            Examples of suitable functions: ``spack.version.Version`` (NOP) or
            ``lambda v: v.up_to(2)`` (minor version match)

    This directive is to be used inside a Package definition to declare
    that the package requires other packages to be built first.
    @see The section "Dependency specs" in the Spack Packaging Guide.

    """

    def _execute_depends_on(pkg):
        executed = False
        if version_translator:
            # Produce a different dependency for every package version
            # for which version_translator returns an answer that alters
            # the spec.
            for pkg_version in pkg.versions:
                version_ish = version_translator(pkg_version)
                if version_ish is not None:
                    constrained_spec = spack.spec.Spec(spec)
                    if constrained_spec.constrain(f"@{version_ish}"):
                        _depends_on(
                            pkg,
                            constrained_spec,
                            when=f"@{pkg_version} {when}" if when else f"@{pkg_version}",
                            type=type,
                            patches=patches,
                        )
                        executed = True

        # If we haven't already produced one or more version-specific
        # dependencies, do the basic dependency for spec.
        if not executed:
            _depends_on(pkg, spec, when=when, type=type, patches=patches)

    return _execute_depends_on


@directive(("extendees", "dependencies"))
def extends(spec, type=("build", "run"), **kwargs):
    """Same as depends_on, but also adds this package to the extendee list.

    keyword arguments can be passed to extends() so that extension
    packages can pass parameters to the extendee's extension
    mechanism.

    """

    def _execute_extends(pkg):
        when = kwargs.get("when")
        when_spec = make_when_spec(when)
        if not when_spec:
            return

        _depends_on(pkg, spec, when=when, type=type)
        spec_obj = spack.spec.Spec(spec)
        pkg.extendees[spec_obj.name] = (spec_obj, kwargs)

    return _execute_extends


@directive(dicts=("provided", "provided_together"))
def provides(*specs, when: Optional[str] = None):
    """Allows packages to provide a virtual dependency.

    If a package provides "mpi", other packages can declare that they depend on "mpi",
    and spack can use the providing package to satisfy the dependency.

    Args:
        *specs: virtual specs provided by this package
        when: condition when this provides clause needs to be considered
    """

    def _execute_provides(pkg):
        import spack.parser  # Avoid circular dependency

        when_spec = make_when_spec(when)
        if not when_spec:
            return

        # ``when`` specs for ``provides()`` need a name, as they are used
        # to build the ProviderIndex.
        when_spec.name = pkg.name
        spec_objs = [spack.spec.Spec(x) for x in specs]
        spec_names = [x.name for x in spec_objs]
        if len(spec_names) > 1:
            pkg.provided_together.setdefault(when_spec, []).append(set(spec_names))

        for provided_spec in spec_objs:
            if pkg.name == provided_spec.name:
                raise CircularReferenceError("Package '%s' cannot provide itself." % pkg.name)

            if provided_spec not in pkg.provided:
                pkg.provided[provided_spec] = set()
            pkg.provided[provided_spec].add(when_spec)

    return _execute_provides


@directive("patches")
def patch(url_or_filename, level=1, when=None, working_dir=".", **kwargs):
    """Packages can declare patches to apply to source.  You can
    optionally provide a when spec to indicate that a particular
    patch should only be applied when the package's spec meets
    certain conditions (e.g. a particular version).

    Args:
        url_or_filename (str): url or relative filename of the patch
        level (int): patch level (as in the patch shell command)
        when (spack.spec.Spec): optional anonymous spec that specifies when to apply
            the patch
        working_dir (str): dir to change to before applying

    Keyword Args:
        sha256 (str): sha256 sum of the patch, used to verify the patch
            (only required for URL patches)
        archive_sha256 (str): sha256 sum of the *archive*, if the patch
            is compressed (only required for compressed URL patches)

    """

    def _execute_patch(pkg_or_dep):
        pkg = pkg_or_dep
        if isinstance(pkg, Dependency):
            pkg = pkg.pkg

        if hasattr(pkg, "has_code") and not pkg.has_code:
            raise UnsupportedPackageDirective(
                "Patches are not allowed in {0}: package has no code.".format(pkg.name)
            )

        when_spec = make_when_spec(when)
        if not when_spec:
            return

        # If this spec is identical to some other, then append this
        # patch to the existing list.
        cur_patches = pkg_or_dep.patches.setdefault(when_spec, [])

        global _patch_order_index
        ordering_key = (pkg.name, _patch_order_index)
        _patch_order_index += 1

        if "://" in url_or_filename:
            patch = spack.patch.UrlPatch(
                pkg, url_or_filename, level, working_dir, ordering_key=ordering_key, **kwargs
            )
        else:
            patch = spack.patch.FilePatch(
                pkg, url_or_filename, level, working_dir, ordering_key=ordering_key
            )

        cur_patches.append(patch)

    return _execute_patch


@directive("variants")
def variant(
    name: str,
    default: Optional[Any] = None,
    description: str = "",
    values: Optional[Union[collections.abc.Sequence, Callable[[Any], bool]]] = None,
    multi: Optional[bool] = None,
    validator: Optional[Callable[[str, str, Tuple[Any, ...]], None]] = None,
    when: Optional[Union[str, bool]] = None,
    sticky: bool = False,
):
    """Define a variant for the package.

    Packager can specify a default value as well as a text description.

    Args:
        name: Name of the variant
        default: Default value for the variant, if not specified otherwise the default will be
            False for a boolean variant and 'nothing' for a multi-valued variant
        description: Description of the purpose of the variant
        values: Either a tuple of strings containing the allowed values, or a callable accepting
            one value and returning True if it is valid
        multi: If False only one value per spec is allowed for this variant
        validator: Optional group validator to enforce additional logic. It receives the package
            name, the variant name and a tuple of values and should raise an instance of SpackError
            if the group doesn't meet the additional constraints
        when: Optional condition on which the variant applies
        sticky: The variant should not be changed by the concretizer to find a valid concrete spec

    Raises:
        DirectiveError: If arguments passed to the directive are invalid
    """

    def format_error(msg, pkg):
        msg += " @*r{{[{0}, variant '{1}']}}"
        return llnl.util.tty.color.colorize(msg.format(pkg.name, name))

    if name in reserved_names:

        def _raise_reserved_name(pkg):
            msg = "The name '%s' is reserved by Spack" % name
            raise DirectiveError(format_error(msg, pkg))

        return _raise_reserved_name

    # Ensure we have a sequence of allowed variant values, or a
    # predicate for it.
    if values is None:
        if str(default).upper() in ("TRUE", "FALSE"):
            values = (True, False)
        else:
            values = lambda x: True

    # The object defining variant values might supply its own defaults for
    # all the other arguments. Ensure we have no conflicting definitions
    # in place.
    for argument in ("default", "multi", "validator"):
        # TODO: we can consider treating 'default' differently from other
        # TODO: attributes and let a packager decide whether to use the fluent
        # TODO: interface or the directive argument
        if hasattr(values, argument) and locals()[argument] is not None:

            def _raise_argument_error(pkg):
                msg = (
                    "Remove specification of {0} argument: it is handled "
                    "by an attribute of the 'values' argument"
                )
                raise DirectiveError(format_error(msg.format(argument), pkg))

            return _raise_argument_error

    # Allow for the object defining the allowed values to supply its own
    # default value and group validator, say if it supports multiple values.
    default = getattr(values, "default", default)
    validator = getattr(values, "validator", validator)
    multi = getattr(values, "multi", bool(multi))

    # Here we sanitize against a default value being either None
    # or the empty string, as the former indicates that a default
    # was not set while the latter will make the variant unparsable
    # from the command line
    if default is None or default == "":

        def _raise_default_not_set(pkg):
            if default is None:
                msg = "either a default was not explicitly set, " "or 'None' was used"
            elif default == "":
                msg = "the default cannot be an empty string"
            raise DirectiveError(format_error(msg, pkg))

        return _raise_default_not_set

    description = str(description).strip()

    def _execute_variant(pkg):
        when_spec = make_when_spec(when)
        when_specs = [when_spec]

        if not re.match(spack.spec.IDENTIFIER_RE, name):
            directive = "variant"
            msg = "Invalid variant name in {0}: '{1}'"
            raise DirectiveError(directive, msg.format(pkg.name, name))

        if name in pkg.variants:
            # We accumulate when specs, but replace the rest of the variant
            # with the newer values
            _, orig_when = pkg.variants[name]
            when_specs += orig_when

        pkg.variants[name] = (
            spack.variant.Variant(name, default, description, values, multi, validator, sticky),
            when_specs,
        )

    return _execute_variant


@directive("resources")
def resource(**kwargs):
    """Define an external resource to be fetched and staged when building the
    package. Based on the keywords present in the dictionary the appropriate
    FetchStrategy will be used for the resource. Resources are fetched and
    staged in their own folder inside spack stage area, and then moved into
    the stage area of the package that needs them.

    List of recognized keywords:

    * 'when' : (optional) represents the condition upon which the resource is
      needed
    * 'destination' : (optional) path where to move the resource. This path
      must be relative to the main package stage area.
    * 'placement' : (optional) gives the possibility to fine tune how the
      resource is moved into the main package stage area.
    """

    def _execute_resource(pkg):
        when = kwargs.get("when")
        when_spec = make_when_spec(when)
        if not when_spec:
            return

        destination = kwargs.get("destination", "")
        placement = kwargs.get("placement", None)

        # Check if the path is relative
        if os.path.isabs(destination):
            message = (
                "The destination keyword of a resource directive " "can't be an absolute path.\n"
            )
            message += "\tdestination : '{dest}\n'".format(dest=destination)
            raise RuntimeError(message)

        # Check if the path falls within the main package stage area
        test_path = "stage_folder_root"
        normalized_destination = os.path.normpath(
            os.path.join(test_path, destination)
        )  # Normalized absolute path

        if test_path not in normalized_destination:
            message = (
                "The destination folder of a resource must fall "
                "within the main package stage directory.\n"
            )
            message += "\tdestination : '{dest}'\n".format(dest=destination)
            raise RuntimeError(message)

        resources = pkg.resources.setdefault(when_spec, [])
        name = kwargs.get("name")
        fetcher = from_kwargs(**kwargs)
        resources.append(Resource(name, fetcher, destination, placement))

    return _execute_resource


def build_system(*values, **kwargs):
    default = kwargs.get("default", None) or values[0]
    return variant(
        "build_system",
        values=tuple(values),
        description="Build systems supported by the package",
        default=default,
        multi=False,
    )


@directive(dicts=())
def maintainers(*names: str):
    """Add a new maintainer directive, to specify maintainers in a declarative way.

    Args:
        names: GitHub username for the maintainer
    """

    def _execute_maintainer(pkg):
        maintainers_from_base = getattr(pkg, "maintainers", [])
        # Here it is essential to copy, otherwise we might add to an empty list in the parent
        pkg.maintainers = list(sorted(set(maintainers_from_base + list(names))))

    return _execute_maintainer


def _execute_license(pkg, license_identifier: str, when):
    # If when is not specified the license always holds
    when_spec = make_when_spec(when)
    if not when_spec:
        return

    for other_when_spec in pkg.licenses:
        if when_spec.intersects(other_when_spec):
            when_message = ""
            if when_spec != make_when_spec(None):
                when_message = f"when {when_spec}"
            other_when_message = ""
            if other_when_spec != make_when_spec(None):
                other_when_message = f"when {other_when_spec}"
            err_msg = (
                f"{pkg.name} is specified as being licensed as {license_identifier} "
                f"{when_message}, but it is also specified as being licensed under "
                f"{pkg.licenses[other_when_spec]} {other_when_message}, which conflict."
            )
            raise OverlappingLicenseError(err_msg)

    pkg.licenses[when_spec] = license_identifier


@directive("licenses")
def license(license_identifier: str, when=None):
    """Add a new license directive, to specify the SPDX identifier the software is
    distributed under.

    Args:
        license_identifiers: A list of SPDX identifiers specifying the licenses
            the software is distributed under.
        when: A spec specifying when the license applies.
    """

    return lambda pkg: _execute_license(pkg, license_identifier, when)


@directive("requirements")
def requires(*requirement_specs, policy="one_of", when=None, msg=None):
    """Allows a package to request a configuration to be present in all valid solutions.

    For instance, a package that is known to compile only with GCC can declare:

        requires("%gcc")

    A package that requires Apple-Clang on Darwin can declare instead:

        requires("%apple-clang", when="platform=darwin", msg="Apple Clang is required on Darwin")

    Args:
        requirement_specs: spec expressing the requirement
        when: optional constraint that triggers the requirement. If None the requirement
            is applied unconditionally.

        msg: optional user defined message
    """

    def _execute_requires(pkg):
        if policy not in ("one_of", "any_of"):
            err_msg = (
                f"the 'policy' argument of the 'requires' directive in {pkg.name} is set "
                f"to a wrong value (only 'one_of' or 'any_of' are allowed)"
            )
            raise DirectiveError(err_msg)

        when_spec = make_when_spec(when)
        if not when_spec:
            return

        # Save in a list the requirements and the associated custom messages
        when_spec_list = pkg.requirements.setdefault(tuple(requirement_specs), [])
        msg_with_name = f"{pkg.name}: {msg}" if msg is not None else msg
        when_spec_list.append((when_spec, policy, msg_with_name))

    return _execute_requires


class DirectiveError(spack.error.SpackError):
    """This is raised when something is wrong with a package directive."""


class DependencyError(DirectiveError):
    """This is raised when a dependency specification is invalid."""


class CircularReferenceError(DependencyError):
    """This is raised when something depends on itself."""


class DependencyPatchError(DirectiveError):
    """Raised for errors with patching dependencies."""


class UnsupportedPackageDirective(DirectiveError):
    """Raised when an invalid or unsupported package directive is specified."""


class OverlappingLicenseError(DirectiveError):
    """Raised when two licenses are declared that apply on overlapping specs."""
