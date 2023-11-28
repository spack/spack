# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""This is where most of the action happens in Spack.

The spack package class structure is based strongly on Homebrew
(http://brew.sh/), mainly because Homebrew makes it very easy to create
packages.
"""

import base64
import collections
import copy
import functools
import glob
import hashlib
import inspect
import io
import os
import re
import shutil
import sys
import textwrap
import time
import traceback
import warnings
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Type, TypeVar

import llnl.util.filesystem as fsys
import llnl.util.tty as tty
from llnl.util.lang import classproperty, memoized
from llnl.util.link_tree import LinkTree

import spack.compilers
import spack.config
import spack.deptypes as dt
import spack.directives
import spack.directory_layout
import spack.environment
import spack.error
import spack.fetch_strategy as fs
import spack.hooks
import spack.mirror
import spack.mixins
import spack.multimethod
import spack.patch
import spack.paths
import spack.repo
import spack.spec
import spack.store
import spack.url
import spack.util.environment
import spack.util.path
import spack.util.web
from spack.filesystem_view import YamlFilesystemView
from spack.install_test import (
    PackageTest,
    TestFailure,
    TestStatus,
    TestSuite,
    cache_extra_test_sources,
    install_test_root,
)
from spack.installer import InstallError, PackageInstaller
from spack.stage import DIYStage, ResourceStage, Stage, StageComposite, compute_stage_name
from spack.util.executable import ProcessError, which
from spack.util.package_hash import package_hash
from spack.version import GitVersion, StandardVersion, Version

FLAG_HANDLER_RETURN_TYPE = Tuple[
    Optional[Iterable[str]], Optional[Iterable[str]], Optional[Iterable[str]]
]
FLAG_HANDLER_TYPE = Callable[[str, Iterable[str]], FLAG_HANDLER_RETURN_TYPE]

"""Allowed URL schemes for spack packages."""
_ALLOWED_URL_SCHEMES = ["http", "https", "ftp", "file", "git"]


#: Filename for the Spack build/install log.
_spack_build_logfile = "spack-build-out.txt"

#: Filename for the Spack build/install environment file.
_spack_build_envfile = "spack-build-env.txt"

#: Filename for the Spack build/install environment modifications file.
_spack_build_envmodsfile = "spack-build-env-mods.txt"

#: Filename for the Spack configure args file.
_spack_configure_argsfile = "spack-configure-args.txt"

#: Filename of json with total build and phase times (seconds)
spack_times_log = "install_times.json"


def deprecated_version(pkg, version):
    """Return True if the version is deprecated, False otherwise.

    Arguments:
        pkg (PackageBase): The package whose version is to be checked.
        version (str or spack.version.StandardVersion): The version being checked
    """
    if not isinstance(version, StandardVersion):
        version = Version(version)

    for k, v in pkg.versions.items():
        if version == k and v.get("deprecated", False):
            return True

    return False


def preferred_version(pkg):
    """
    Returns a sorted list of the preferred versions of the package.

    Arguments:
        pkg (PackageBase): The package whose versions are to be assessed.
    """
    # Here we sort first on the fact that a version is marked
    # as preferred in the package, then on the fact that the
    # version is not develop, then lexicographically
    key_fn = lambda v: (pkg.versions[v].get("preferred", False), not v.isdevelop(), v)
    return max(pkg.versions, key=key_fn)


class WindowsRPath:
    """Collection of functionality surrounding Windows RPATH specific features

    This is essentially meaningless for all other platforms
    due to their use of RPATH. All methods within this class are no-ops on
    non Windows. Packages can customize and manipulate this class as
    they would a genuine RPATH, i.e. adding directories that contain
    runtime library dependencies"""

    def win_add_library_dependent(self):
        """Return extra set of directories that require linking for package

        This method should be overridden by packages that produce
        binaries/libraries/python extension modules/etc that are installed into
        directories outside a package's `bin`, `lib`, and `lib64` directories,
        but still require linking against one of the packages dependencies, or
        other components of the package itself. No-op otherwise.

        Returns:
            List of additional directories that require linking
        """
        return []

    def win_add_rpath(self):
        """Return extra set of rpaths for package

        This method should be overridden by packages needing to
        include additional paths to be searched by rpath. No-op otherwise

        Returns:
            List of additional rpaths
        """
        return []

    def windows_establish_runtime_linkage(self):
        """Establish RPATH on Windows

        Performs symlinking to incorporate rpath dependencies to Windows runtime search paths
        """
        if sys.platform == "win32":
            self.win_rpath.add_library_dependent(*self.win_add_library_dependent())
            self.win_rpath.add_rpath(*self.win_add_rpath())
            self.win_rpath.establish_link()


#: Registers which are the detectable packages, by repo and package name
#: Need a pass of package repositories to be filled.
detectable_packages = collections.defaultdict(list)


class DetectablePackageMeta(type):
    """Check if a package is detectable and add default implementations
    for the detection function.
    """

    TAG = "detectable"

    def __init__(cls, name, bases, attr_dict):
        if hasattr(cls, "executables") and hasattr(cls, "libraries"):
            msg = "a package can have either an 'executables' or 'libraries' attribute"
            raise spack.error.SpackError(f"{msg} [package '{name}' defines both]")

        # On windows, extend the list of regular expressions to look for
        # filenames ending with ".exe"
        # (in some cases these regular expressions include "$" to avoid
        # pulling in filenames with unexpected suffixes, but this allows
        # for example detecting "foo.exe" when the package writer specified
        # that "foo" was a possible executable.

        # If a package has the executables or libraries  attribute then it's
        # assumed to be detectable
        if hasattr(cls, "executables") or hasattr(cls, "libraries"):
            # Append a tag to each detectable package, so that finding them is faster
            if hasattr(cls, "tags"):
                getattr(cls, "tags").append(DetectablePackageMeta.TAG)
            else:
                setattr(cls, "tags", [DetectablePackageMeta.TAG])

            @classmethod
            def platform_executables(cls):
                def to_windows_exe(exe):
                    if exe.endswith("$"):
                        exe = exe.replace("$", "%s$" % spack.util.path.win_exe_ext())
                    else:
                        exe += spack.util.path.win_exe_ext()
                    return exe

                plat_exe = []
                if hasattr(cls, "executables"):
                    for exe in cls.executables:
                        if sys.platform == "win32":
                            exe = to_windows_exe(exe)
                        plat_exe.append(exe)
                return plat_exe

            @classmethod
            def determine_spec_details(cls, prefix, objs_in_prefix):
                """Allow ``spack external find ...`` to locate installations.

                Args:
                    prefix (str): the directory containing the executables
                                  or libraries
                    objs_in_prefix (set): the executables or libraries that
                                          match the regex

                Returns:
                    The list of detected specs for this package
                """
                objs_by_version = collections.defaultdict(list)
                # The default filter function is the identity function for the
                # list of executables
                filter_fn = getattr(cls, "filter_detected_exes", lambda x, exes: exes)
                objs_in_prefix = filter_fn(prefix, objs_in_prefix)
                for obj in objs_in_prefix:
                    try:
                        version_str = cls.determine_version(obj)
                        if version_str:
                            objs_by_version[version_str].append(obj)
                    except Exception as e:
                        msg = (
                            "An error occurred when trying to detect " 'the version of "{0}" [{1}]'
                        )
                        tty.debug(msg.format(obj, str(e)))

                specs = []
                for version_str, objs in objs_by_version.items():
                    variants = cls.determine_variants(objs, version_str)
                    # Normalize output to list
                    if not isinstance(variants, list):
                        variants = [variants]

                    for variant in variants:
                        if isinstance(variant, str):
                            variant = (variant, {})
                        variant_str, extra_attributes = variant
                        spec_str = "{0}@{1} {2}".format(cls.name, version_str, variant_str)

                        # Pop a few reserved keys from extra attributes, since
                        # they have a different semantics
                        external_path = extra_attributes.pop("prefix", None)
                        external_modules = extra_attributes.pop("modules", None)
                        try:
                            spec = spack.spec.Spec(
                                spec_str,
                                external_path=external_path,
                                external_modules=external_modules,
                            )
                        except Exception as e:
                            msg = 'Parsing failed [spec_str="{0}", error={1}]'
                            tty.debug(msg.format(spec_str, str(e)))
                        else:
                            specs.append(
                                spack.spec.Spec.from_detection(
                                    spec, extra_attributes=extra_attributes
                                )
                            )

                return sorted(specs)

            @classmethod
            def determine_variants(cls, objs, version_str):
                return ""

            # Register the class as a detectable package
            detectable_packages[cls.namespace].append(cls.name)

            # Attach function implementations to the detectable class
            default = False
            if not hasattr(cls, "determine_spec_details"):
                default = True
                cls.determine_spec_details = determine_spec_details

            if default and not hasattr(cls, "determine_version"):
                msg = (
                    'the package "{0}" in the "{1}" repo needs to define'
                    ' the "determine_version" method to be detectable'
                )
                NotImplementedError(msg.format(cls.name, cls.namespace))

            if default and not hasattr(cls, "determine_variants"):
                cls.determine_variants = determine_variants

            # This function should not be overridden by subclasses,
            # as it is not designed for bespoke pkg detection but rather
            # on a per-platform basis
            if "platform_executables" in cls.__dict__.keys():
                raise PackageError("Packages should not override platform_executables")
            cls.platform_executables = platform_executables

        super(DetectablePackageMeta, cls).__init__(name, bases, attr_dict)


class PackageMeta(
    spack.builder.PhaseCallbacksMeta,
    DetectablePackageMeta,
    spack.directives.DirectiveMeta,
    spack.multimethod.MultiMethodMeta,
):
    """
    Package metaclass for supporting directives (e.g., depends_on) and phases
    """

    def __new__(cls, name, bases, attr_dict):
        """
        FIXME: REWRITE
        Instance creation is preceded by phase attribute transformations.

        Conveniently transforms attributes to permit extensible phases by
        iterating over the attribute 'phases' and creating / updating private
        InstallPhase attributes in the class that will be initialized in
        __init__.
        """
        attr_dict["_name"] = None

        return super(PackageMeta, cls).__new__(cls, name, bases, attr_dict)


def on_package_attributes(**attr_dict):
    """Decorator: executes instance function only if object has attr valuses.

    Executes the decorated method only if at the moment of calling the
    instance has attributes that are equal to certain values.

    Args:
        attr_dict (dict): dictionary mapping attribute names to their
            required values
    """

    def _execute_under_condition(func):
        @functools.wraps(func)
        def _wrapper(instance, *args, **kwargs):
            # If all the attributes have the value we require, then execute
            has_all_attributes = all([hasattr(instance, key) for key in attr_dict])
            if has_all_attributes:
                has_the_right_values = all(
                    [
                        getattr(instance, key) == value for key, value in attr_dict.items()
                    ]  # NOQA: ignore=E501
                )
                if has_the_right_values:
                    func(instance, *args, **kwargs)

        return _wrapper

    return _execute_under_condition


class PackageViewMixin:
    """This collects all functionality related to adding installed Spack
    package to views. Packages can customize how they are added to views by
    overriding these functions.
    """

    def view_source(self):
        """The source root directory that will be added to the view: files are
        added such that their path relative to the view destination matches
        their path relative to the view source.
        """
        return self.spec.prefix

    def view_destination(self, view):
        """The target root directory: each file is added relative to this
        directory.
        """
        return view.get_projection_for_spec(self.spec)

    def view_file_conflicts(self, view, merge_map):
        """Report any files which prevent adding this package to the view. The
        default implementation looks for any files which already exist.
        Alternative implementations may allow some of the files to exist in
        the view (in this case they would be omitted from the results).
        """
        return set(dst for dst in merge_map.values() if os.path.lexists(dst))

    def add_files_to_view(self, view, merge_map, skip_if_exists=True):
        """Given a map of package files to destination paths in the view, add
        the files to the view. By default this adds all files. Alternative
        implementations may skip some files, for example if other packages
        linked into the view already include the file.

        Args:
            view (spack.filesystem_view.FilesystemView): the view that's updated
            merge_map (dict): maps absolute source paths to absolute dest paths for
                all files in from this package.
            skip_if_exists (bool): when True, don't link files in view when they
                already exist. When False, always link files, without checking
                if they already exist.
        """
        if skip_if_exists:
            for src, dst in merge_map.items():
                if not os.path.lexists(dst):
                    view.link(src, dst, spec=self.spec)
        else:
            for src, dst in merge_map.items():
                view.link(src, dst, spec=self.spec)

    def remove_files_from_view(self, view, merge_map):
        """Given a map of package files to files currently linked in the view,
        remove the files from the view. The default implementation removes all
        files. Alternative implementations may not remove all files. For
        example if two packages include the same file, it should only be
        removed when both packages are removed.
        """
        view.remove_files(merge_map.values())


Pb = TypeVar("Pb", bound="PackageBase")


class PackageBase(WindowsRPath, PackageViewMixin, metaclass=PackageMeta):
    """This is the superclass for all spack packages.

    ***The Package class***

    At its core, a package consists of a set of software to be installed.
    A package may focus on a piece of software and its associated software
    dependencies or it may simply be a set, or bundle, of software.  The
    former requires defining how to fetch, verify (via, e.g., sha256), build,
    and install that software and the packages it depends on, so that
    dependencies can be installed along with the package itself.   The latter,
    sometimes referred to as a ``no-source`` package, requires only defining
    the packages to be built.

    Packages are written in pure Python.

    There are two main parts of a Spack package:

      1. **The package class**.  Classes contain ``directives``, which are
         special functions, that add metadata (versions, patches,
         dependencies, and other information) to packages (see
         ``directives.py``). Directives provide the constraints that are
         used as input to the concretizer.

      2. **Package instances**. Once instantiated, a package is
         essentially a software installer.  Spack calls methods like
         ``do_install()`` on the ``Package`` object, and it uses those to
         drive user-implemented methods like ``patch()``, ``install()``, and
         other build steps.  To install software, an instantiated package
         needs a *concrete* spec, which guides the behavior of the various
         install methods.

    Packages are imported from repos (see ``repo.py``).

    **Package DSL**

    Look in ``lib/spack/docs`` or check https://spack.readthedocs.io for
    the full documentation of the package domain-specific language.  That
    used to be partially documented here, but as it grew, the docs here
    became increasingly out of date.

    **Package Lifecycle**

    A package's lifecycle over a run of Spack looks something like this:

    .. code-block:: python

       p = Package()             # Done for you by spack

       p.do_fetch()              # downloads tarball from a URL (or VCS)
       p.do_stage()              # expands tarball in a temp directory
       p.do_patch()              # applies patches to expanded source
       p.do_install()            # calls package's install() function
       p.do_uninstall()          # removes install directory

    although packages that do not have code have nothing to fetch so omit
    ``p.do_fetch()``.

    There are also some other commands that clean the build area:

    .. code-block:: python

       p.do_clean()              # removes the stage directory entirely
       p.do_restage()            # removes the build directory and
                                 # re-expands the archive.

    The convention used here is that a ``do_*`` function is intended to be
    called internally by Spack commands (in ``spack.cmd``).  These aren't for
    package writers to override, and doing so may break the functionality
    of the Package class.

    Package creators have a lot of freedom, and they could technically
    override anything in this class.  That is not usually required.

    For most use cases.  Package creators typically just add attributes
    like ``homepage`` and, for a code-based package, ``url``, or functions
    such as ``install()``.
    There are many custom ``Package`` subclasses in the
    ``spack.build_systems`` package that make things even easier for
    specific build systems.

    """

    #
    # These are default values for instance variables.
    #

    # Declare versions dictionary as placeholder for values.
    # This allows analysis tools to correctly interpret the class attributes.
    versions: dict

    # Same for dependencies
    dependencies: dict

    #: By default, packages are not virtual
    #: Virtual packages override this attribute
    virtual = False

    #: Most Spack packages are used to install source or binary code while
    #: those that do not can be used to install a set of other Spack packages.
    has_code = True

    #: By default we build in parallel.  Subclasses can override this.
    parallel = True

    #: By default do not run tests within package's install()
    run_tests = False

    #: Keep -Werror flags, matches config:flags:keep_werror to override config
    # NOTE: should be type Optional[Literal['all', 'specific', 'none']] in 3.8+
    keep_werror: Optional[str] = None

    #: Most packages are NOT extendable. Set to True if you want extensions.
    extendable = False

    #: When True, add RPATHs for the entire DAG. When False, add RPATHs only
    #: for immediate dependencies.
    transitive_rpaths = True

    #: List of shared objects that should be replaced with a different library at
    #: runtime. Typically includes stub libraries like libcuda.so. When linking
    #: against a library listed here, the dependent will only record its soname
    #: or filename, not its absolute path, so that the dynamic linker will search
    #: for it. Note: accepts both file names and directory names, for example
    #: ``["libcuda.so", "stubs"]`` will ensure libcuda.so and all libraries in the
    #: stubs directory are not bound by path."""
    non_bindable_shared_objects: List[str] = []

    #: List of prefix-relative file paths (or a single path). If these do
    #: not exist after install, or if they exist but are not files,
    #: sanity checks fail.
    sanity_check_is_file: List[str] = []

    #: List of prefix-relative directory paths (or a single path). If
    #: these do not exist after install, or if they exist but are not
    #: directories, sanity checks will fail.
    sanity_check_is_dir: List[str] = []

    #: Boolean. Set to ``True`` for packages that require a manual download.
    #: This is currently used by package sanity tests and generation of a
    #: more meaningful fetch failure error.
    manual_download = False

    #: Set of additional options used when fetching package versions.
    fetch_options: Dict[str, Any] = {}

    #
    # Set default licensing information
    #
    #: Boolean. If set to ``True``, this software requires a license.
    #: If set to ``False``, all of the ``license_*`` attributes will
    #: be ignored. Defaults to ``False``.
    license_required = False

    #: String. Contains the symbol used by the license manager to denote
    #: a comment. Defaults to ``#``.
    license_comment = "#"

    #: List of strings. These are files that the software searches for when
    #: looking for a license. All file paths must be relative to the
    #: installation directory. More complex packages like Intel may require
    #: multiple licenses for individual components. Defaults to the empty list.
    license_files: List[str] = []

    #: List of strings. Environment variables that can be set to tell the
    #: software where to look for a license if it is not in the usual location.
    #: Defaults to the empty list.
    license_vars: List[str] = []

    #: String. A URL pointing to license setup instructions for the software.
    #: Defaults to the empty string.
    license_url = ""

    #: Verbosity level, preserved across installs.
    _verbose = None

    #: index of patches by sha256 sum, built lazily
    _patches_by_hash = None

    #: Package homepage where users can find more information about the package
    homepage: Optional[str] = None

    #: Default list URL (place to find available versions)
    list_url: Optional[str] = None

    #: Link depth to which list_url should be searched for new versions
    list_depth = 0

    #: List of strings which contains GitHub usernames of package maintainers.
    #: Do not include @ here in order not to unnecessarily ping the users.
    maintainers: List[str] = []

    #: List of attributes to be excluded from a package's hash.
    metadata_attrs = [
        "homepage",
        "url",
        "urls",
        "list_url",
        "extendable",
        "parallel",
        "make_jobs",
        "maintainers",
        "tags",
    ]

    #: Set to ``True`` to indicate the stand-alone test requires a compiler.
    #: It is used to ensure a compiler and build dependencies like 'cmake'
    #: are available to build a custom test code.
    test_requires_compiler: bool = False

    #: TestSuite instance used to manage stand-alone tests for 1+ specs.
    test_suite: Optional["TestSuite"] = None

    def __init__(self, spec):
        # this determines how the package should be built.
        self.spec: "spack.spec.Spec" = spec

        # Allow custom staging paths for packages
        self.path = None

        # Keep track of whether or not this package was installed from
        # a binary cache.
        self.installed_from_binary_cache = False

        # Ensure that only one of these two attributes are present
        if getattr(self, "url", None) and getattr(self, "urls", None):
            msg = "a package can have either a 'url' or a 'urls' attribute"
            msg += " [package '{0.name}' defines both]"
            raise ValueError(msg.format(self))

        # init internal variables
        self._stage = None
        self._fetcher = None
        self._tester: Optional["PackageTest"] = None

        # Set up timing variables
        self._fetch_time = 0.0

        self.win_rpath = fsys.WindowsSimulatedRPath(self)

        if self.is_extension:
            pkg_cls = spack.repo.PATH.get_pkg_class(self.extendee_spec.name)
            pkg_cls(self.extendee_spec)._check_extendable()

        super().__init__()

    @classmethod
    def possible_dependencies(
        cls,
        transitive=True,
        expand_virtuals=True,
        depflag: dt.DepFlag = dt.ALL,
        visited=None,
        missing=None,
        virtuals=None,
    ):
        """Return dict of possible dependencies of this package.

        Args:
            transitive (bool or None): return all transitive dependencies if
                True, only direct dependencies if False (default True)..
            expand_virtuals (bool or None): expand virtual dependencies into
                all possible implementations (default True)
            depflag: dependency types to consider
            visited (dict or None): dict of names of dependencies visited so
                far, mapped to their immediate dependencies' names.
            missing (dict or None): dict to populate with packages and their
                *missing* dependencies.
            virtuals (set): if provided, populate with virtuals seen so far.

        Returns:
            (dict): dictionary mapping dependency names to *their*
                immediate dependencies

        Each item in the returned dictionary maps a (potentially
        transitive) dependency of this package to its possible
        *immediate* dependencies. If ``expand_virtuals`` is ``False``,
        virtual package names wil be inserted as keys mapped to empty
        sets of dependencies.  Virtuals, if not expanded, are treated as
        though they have no immediate dependencies.

        Missing dependencies by default are ignored, but if a
        missing dict is provided, it will be populated with package names
        mapped to any dependencies they have that are in no
        repositories. This is only populated if transitive is True.

        Note: the returned dict *includes* the package itself.

        """
        visited = {} if visited is None else visited
        missing = {} if missing is None else missing

        visited.setdefault(cls.name, set())

        for name, conditions in cls.dependencies.items():
            # check whether this dependency could be of the type asked for
            depflag_union = 0
            for dep in conditions.values():
                depflag_union |= dep.depflag
            if not (depflag & depflag_union):
                continue

            # expand virtuals if enabled, otherwise just stop at virtuals
            if spack.repo.PATH.is_virtual(name):
                if virtuals is not None:
                    virtuals.add(name)
                if expand_virtuals:
                    providers = spack.repo.PATH.providers_for(name)
                    dep_names = [spec.name for spec in providers]
                else:
                    visited.setdefault(cls.name, set()).add(name)
                    visited.setdefault(name, set())
                    continue
            else:
                dep_names = [name]

            # add the dependency names to the visited dict
            visited.setdefault(cls.name, set()).update(set(dep_names))

            # recursively traverse dependencies
            for dep_name in dep_names:
                if dep_name in visited:
                    continue

                visited.setdefault(dep_name, set())

                # skip the rest if not transitive
                if not transitive:
                    continue

                try:
                    dep_cls = spack.repo.PATH.get_pkg_class(dep_name)
                except spack.repo.UnknownPackageError:
                    # log unknown packages
                    missing.setdefault(cls.name, set()).add(dep_name)
                    continue

                dep_cls.possible_dependencies(
                    transitive, expand_virtuals, depflag, visited, missing, virtuals
                )

        return visited

    @classproperty
    def package_dir(cls):
        """Directory where the package.py file lives."""
        return os.path.abspath(os.path.dirname(cls.module.__file__))

    @classproperty
    def module(cls):
        """Module object (not just the name) that this package is defined in.

        We use this to add variables to package modules.  This makes
        install() methods easier to write (e.g., can call configure())
        """
        return __import__(cls.__module__, fromlist=[cls.__name__])

    @classproperty
    def namespace(cls):
        """Spack namespace for the package, which identifies its repo."""
        return spack.repo.namespace_from_fullname(cls.__module__)

    @classproperty
    def fullname(cls):
        """Name of this package, including the namespace"""
        return "%s.%s" % (cls.namespace, cls.name)

    @classproperty
    def fullnames(cls):
        """Fullnames for this package and any packages from which it inherits."""
        fullnames = []
        for cls in inspect.getmro(cls):
            namespace = getattr(cls, "namespace", None)
            if namespace:
                fullnames.append("%s.%s" % (namespace, cls.name))
            if namespace == "builtin":
                # builtin packages cannot inherit from other repos
                break
        return fullnames

    @classproperty
    def name(cls):
        """The name of this package.

        The name of a package is the name of its Python module, without
        the containing module names.
        """
        if cls._name is None:
            cls._name = cls.module.__name__
            if "." in cls._name:
                cls._name = cls._name[cls._name.rindex(".") + 1 :]
        return cls._name

    @classproperty
    def global_license_dir(cls):
        """Returns the directory where license files for all packages are stored."""
        return spack.util.path.canonicalize_path(spack.config.get("config:license_dir"))

    @property
    def global_license_file(self):
        """Returns the path where a global license file for this
        particular package should be stored."""
        if not self.license_files:
            return
        return os.path.join(
            self.global_license_dir, self.name, os.path.basename(self.license_files[0])
        )

    @property
    def version(self):
        if not self.spec.versions.concrete:
            raise ValueError(
                "Version requested for a package that" " does not have a concrete version."
            )
        return self.spec.versions[0]

    @classmethod
    @memoized
    def version_urls(cls):
        """OrderedDict of explicitly defined URLs for versions of this package.

        Return:
           An OrderedDict (version -> URL) different versions of this
           package, sorted by version.

        A version's URL only appears in the result if it has an an
        explicitly defined ``url`` argument. So, this list may be empty
        if a package only defines ``url`` at the top level.
        """
        version_urls = collections.OrderedDict()
        for v, args in sorted(cls.versions.items()):
            if "url" in args:
                version_urls[v] = args["url"]
        return version_urls

    def nearest_url(self, version):
        """Finds the URL with the "closest" version to ``version``.

        This uses the following precedence order:

          1. Find the next lowest or equal version with a URL.
          2. If no lower URL, return the next *higher* URL.
          3. If no higher URL, return None.

        """
        version_urls = self.version_urls()

        if version in version_urls:
            return version_urls[version]

        last_url = None
        for v, u in self.version_urls().items():
            if v > version:
                if last_url:
                    return last_url
            last_url = u

        return last_url

    def url_for_version(self, version):
        """Returns a URL from which the specified version of this package
        may be downloaded.

        version: class Version
            The version for which a URL is sought.

        See Class Version (version.py)
        """
        return self._implement_all_urls_for_version(version)[0]

    def update_external_dependencies(self, extendee_spec=None):
        """
        Method to override in package classes to handle external dependencies
        """
        pass

    def all_urls_for_version(self, version):
        """Return all URLs derived from version_urls(), url, urls, and
        list_url (if it contains a version) in a package in that order.

        Args:
            version (spack.version.Version): the version for which a URL is sought
        """
        uf = None
        if type(self).url_for_version != PackageBase.url_for_version:
            uf = self.url_for_version
        return self._implement_all_urls_for_version(version, uf)

    def _implement_all_urls_for_version(self, version, custom_url_for_version=None):
        if not isinstance(version, StandardVersion):
            version = Version(version)

        urls = []

        # If we have a specific URL for this version, don't extrapolate.
        version_urls = self.version_urls()
        if version in version_urls:
            urls.append(version_urls[version])

        # if there is a custom url_for_version, use it
        if custom_url_for_version is not None:
            u = custom_url_for_version(version)
            if u not in urls and u is not None:
                urls.append(u)

        def sub_and_add(u):
            if u is None:
                return
            # skip the url if there is no version to replace
            try:
                spack.url.parse_version(u)
            except spack.url.UndetectableVersionError:
                return
            nu = spack.url.substitute_version(u, self.url_version(version))

            urls.append(nu)

        # If no specific URL, use the default, class-level URL
        sub_and_add(getattr(self, "url", None))
        for u in getattr(self, "urls", []):
            sub_and_add(u)

        sub_and_add(getattr(self, "list_url", None))

        # if no version-bearing URLs can be found, try them raw
        if not urls:
            default_url = getattr(self, "url", getattr(self, "urls", [None])[0])

            # if no exact match AND no class-level default, use the nearest URL
            if not default_url:
                default_url = self.nearest_url(version)

                # if there are NO URLs to go by, then we can't do anything
                if not default_url:
                    raise NoURLError(self.__class__)
            urls.append(spack.url.substitute_version(default_url, self.url_version(version)))

        return urls

    def find_valid_url_for_version(self, version):
        """Returns a URL from which the specified version of this package
        may be downloaded after testing whether the url is valid. Will try
        url, urls, and list_url before failing.

        version: class Version
            The version for which a URL is sought.

        See Class Version (version.py)
        """
        urls = self.all_urls_for_version(version)

        for u in urls:
            if spack.util.web.url_exists(u):
                return u

        return None

    def _make_resource_stage(self, root_stage, resource):
        pretty_resource_name = fsys.polite_filename(f"{resource.name}-{self.version}")
        return ResourceStage(
            resource.fetcher,
            root=root_stage,
            resource=resource,
            name=self._resource_stage(resource),
            mirror_paths=spack.mirror.mirror_archive_paths(
                resource.fetcher, os.path.join(self.name, pretty_resource_name)
            ),
            path=self.path,
        )

    def _download_search(self):
        dynamic_fetcher = fs.from_list_url(self)
        return [dynamic_fetcher] if dynamic_fetcher else []

    def _make_root_stage(self, fetcher):
        # Construct a mirror path (TODO: get this out of package.py)
        format_string = "{name}-{version}"
        pretty_name = self.spec.format_path(format_string)
        mirror_paths = spack.mirror.mirror_archive_paths(
            fetcher, os.path.join(self.name, pretty_name), self.spec
        )
        # Construct a path where the stage should build..
        s = self.spec
        stage_name = compute_stage_name(s)
        stage = Stage(
            fetcher,
            mirror_paths=mirror_paths,
            name=stage_name,
            path=self.path,
            search_fn=self._download_search,
        )
        return stage

    def _make_stage(self):
        # If it's a dev package (not transitively), use a DIY stage object
        dev_path_var = self.spec.variants.get("dev_path", None)
        if dev_path_var:
            return DIYStage(dev_path_var.value)

        # To fetch the current version
        source_stage = self._make_root_stage(self.fetcher)

        # Extend it with all resources and patches
        all_stages = StageComposite()
        all_stages.append(source_stage)
        all_stages.extend(
            self._make_resource_stage(source_stage, r) for r in self._get_needed_resources()
        )
        all_stages.extend(
            p.stage for p in self.spec.patches if isinstance(p, spack.patch.UrlPatch)
        )
        return all_stages

    @property
    def stage(self):
        """Get the build staging area for this package.

        This automatically instantiates a ``Stage`` object if the package
        doesn't have one yet, but it does not create the Stage directory
        on the filesystem.
        """
        if not self.spec.versions.concrete:
            raise ValueError("Cannot retrieve stage for package without concrete version.")
        if self._stage is None:
            self._stage = self._make_stage()
        return self._stage

    @stage.setter
    def stage(self, stage):
        """Allow a stage object to be set to override the default."""
        self._stage = stage

    @property
    def env_path(self):
        """Return the build environment file path associated with staging."""
        # Backward compatibility: Return the name of an existing log path;
        # otherwise, return the current install env path name.
        old_filename = os.path.join(self.stage.path, "spack-build.env")
        if os.path.exists(old_filename):
            return old_filename
        else:
            return os.path.join(self.stage.path, _spack_build_envfile)

    @property
    def env_mods_path(self):
        """
        Return the build environment modifications file path associated with
        staging.
        """
        return os.path.join(self.stage.path, _spack_build_envmodsfile)

    @property
    def metadata_dir(self):
        """Return the install metadata directory."""
        return spack.store.STORE.layout.metadata_path(self.spec)

    @property
    def install_env_path(self):
        """
        Return the build environment file path on successful installation.
        """
        # Backward compatibility: Return the name of an existing log path;
        # otherwise, return the current install env path name.
        old_filename = os.path.join(self.metadata_dir, "build.env")
        if os.path.exists(old_filename):
            return old_filename
        else:
            return os.path.join(self.metadata_dir, _spack_build_envfile)

    @property
    def log_path(self):
        """Return the build log file path associated with staging."""
        # Backward compatibility: Return the name of an existing log path.
        for filename in ["spack-build.out", "spack-build.txt"]:
            old_log = os.path.join(self.stage.path, filename)
            if os.path.exists(old_log):
                return old_log

        # Otherwise, return the current log path name.
        return os.path.join(self.stage.path, _spack_build_logfile)

    @property
    def phase_log_files(self):
        """Find sorted phase log files written to the staging directory"""
        logs_dir = os.path.join(self.stage.path, "spack-build-*-out.txt")
        log_files = glob.glob(logs_dir)
        log_files.sort()
        return log_files

    @property
    def install_log_path(self):
        """Return the build log file path on successful installation."""
        # Backward compatibility: Return the name of an existing install log.
        for filename in ["build.out", "build.txt"]:
            old_log = os.path.join(self.metadata_dir, filename)
            if os.path.exists(old_log):
                return old_log

        # Otherwise, return the current install log path name.
        return os.path.join(self.metadata_dir, _spack_build_logfile)

    @property
    def configure_args_path(self):
        """Return the configure args file path associated with staging."""
        return os.path.join(self.stage.path, _spack_configure_argsfile)

    @property
    def times_log_path(self):
        """Return the times log json file."""
        return os.path.join(self.metadata_dir, spack_times_log)

    @property
    def install_configure_args_path(self):
        """Return the configure args file path on successful installation."""
        return os.path.join(self.metadata_dir, _spack_configure_argsfile)

    # TODO (post-34236): Update tests and all packages that use this as a
    # TODO (post-34236): package method to the function already available
    # TODO (post-34236): to packages. Once done, remove this property.
    @property
    def install_test_root(self):
        """Return the install test root directory."""
        tty.warn(
            "The 'pkg.install_test_root' property is deprecated with removal "
            "expected v0.22. Use 'install_test_root(pkg)' instead."
        )
        return install_test_root(self)

    def archive_install_test_log(self):
        """Archive the install-phase test log, if present."""
        if getattr(self, "tester", None):
            self.tester.archive_install_test_log(self.metadata_dir)

    @property
    def tester(self):
        if not self.spec.versions.concrete:
            raise ValueError("Cannot retrieve tester for package without concrete version.")

        if not self._tester:
            self._tester = PackageTest(self)
        return self._tester

    @property
    def installed(self):
        msg = (
            'the "PackageBase.installed" property is deprecated and will be '
            'removed in Spack v0.19, use "Spec.installed" instead'
        )
        warnings.warn(msg)
        return self.spec.installed

    @property
    def installed_upstream(self):
        msg = (
            'the "PackageBase.installed_upstream" property is deprecated and will '
            'be removed in Spack v0.19, use "Spec.installed_upstream" instead'
        )
        warnings.warn(msg)
        return self.spec.installed_upstream

    @property
    def fetcher(self):
        if not self.spec.versions.concrete:
            raise ValueError("Cannot retrieve fetcher for package without concrete version.")
        if not self._fetcher:
            self._fetcher = fs.for_package_version(self)
        return self._fetcher

    @fetcher.setter
    def fetcher(self, f):
        self._fetcher = f
        self._fetcher.set_package(self)

    @classmethod
    def dependencies_of_type(cls, deptypes: dt.DepFlag):
        """Get dependencies that can possibly have these deptypes.

        This analyzes the package and determines which dependencies *can*
        be a certain kind of dependency. Note that they may not *always*
        be this kind of dependency, since dependencies can be optional,
        so something may be a build dependency in one configuration and a
        run dependency in another.
        """
        return dict(
            (name, conds)
            for name, conds in cls.dependencies.items()
            if any(deptypes & cls.dependencies[name][cond].depflag for cond in conds)
        )

    # TODO: allow more than one active extendee.
    @property
    def extendee_spec(self):
        """
        Spec of the extendee of this package, or None if it is not an extension
        """
        if not self.extendees:
            return None

        deps = []

        # If the extendee is in the spec's deps already, return that.
        for dep in self.spec.traverse(deptype=("link", "run")):
            if dep.name in self.extendees:
                deps.append(dep)

        if deps:
            assert len(deps) == 1
            return deps[0]

        # if the spec is concrete already, then it extends something
        # that is an *optional* dependency, and the dep isn't there.
        if self.spec._concrete:
            return None
        else:
            # If it's not concrete, then return the spec from the
            # extends() directive since that is all we know so far.
            spec_str, kwargs = next(iter(self.extendees.items()))
            return spack.spec.Spec(spec_str)

    @property
    def extendee_args(self):
        """
        Spec of the extendee of this package, or None if it is not an extension
        """
        if not self.extendees:
            return None

        # TODO: allow multiple extendees.
        name = next(iter(self.extendees))
        return self.extendees[name][1]

    @property
    def is_extension(self):
        # if it is concrete, it's only an extension if it actually
        # dependes on the extendee.
        if self.spec._concrete:
            return self.extendee_spec is not None
        else:
            # If not, then it's an extension if it *could* be an extension
            return bool(self.extendees)

    def extends(self, spec):
        """
        Returns True if this package extends the given spec.

        If ``self.spec`` is concrete, this returns whether this package extends
        the given spec.

        If ``self.spec`` is not concrete, this returns whether this package may
        extend the given spec.
        """
        if spec.name not in self.extendees:
            return False
        s = self.extendee_spec
        return s and spec.satisfies(s)

    def provides(self, vpkg_name):
        """
        True if this package provides a virtual package with the specified name
        """
        return any(
            any(self.spec.intersects(c) for c in constraints)
            for s, constraints in self.provided.items()
            if s.name == vpkg_name
        )

    @property
    def virtuals_provided(self):
        """
        virtual packages provided by this package with its spec
        """
        return [
            vspec
            for vspec, constraints in self.provided.items()
            if any(self.spec.satisfies(c) for c in constraints)
        ]

    @property
    def prefix(self):
        """Get the prefix into which this package should be installed."""
        return self.spec.prefix

    @property
    def home(self):
        return self.prefix

    @property  # type: ignore[misc]
    @memoized
    def compiler(self):
        """Get the spack.compiler.Compiler object used to build this package"""
        if not self.spec.concrete:
            raise ValueError("Can only get a compiler for a concrete package.")

        return spack.compilers.compiler_for_spec(self.spec.compiler, self.spec.architecture)

    def url_version(self, version):
        """
        Given a version, this returns a string that should be substituted
        into the package's URL to download that version.

        By default, this just returns the version string. Subclasses may need
        to override this, e.g. for boost versions where you need to ensure that
        there are _'s in the download URL.
        """
        return str(version)

    def remove_prefix(self):
        """
        Removes the prefix for a package along with any empty parent
        directories
        """
        spack.store.STORE.layout.remove_install_directory(self.spec)

    @property
    def download_instr(self):
        """
        Defines the default manual download instructions.  Packages can
        override the property to provide more information.

        Returns:
            (str):  default manual download instructions
        """
        required = (
            "Manual download is required for {0}. ".format(self.spec.name)
            if self.manual_download
            else ""
        )
        return "{0}Refer to {1} for download instructions.".format(
            required, self.spec.package.homepage
        )

    def do_fetch(self, mirror_only=False):
        """
        Creates a stage directory and downloads the tarball for this package.
        Working directory will be set to the stage directory.
        """
        if not self.has_code or self.spec.external:
            tty.debug("No fetch required for {0}".format(self.name))
            return

        checksum = spack.config.get("config:checksum")
        fetch = self.stage.managed_by_spack
        if (
            checksum
            and fetch
            and (self.version not in self.versions)
            and (not isinstance(self.version, GitVersion))
        ):
            tty.warn(
                "There is no checksum on file to fetch %s safely."
                % self.spec.cformat("{name}{@version}")
            )

            # Ask the user whether to skip the checksum if we're
            # interactive, but just fail if non-interactive.
            ck_msg = "Add a checksum or use --no-checksum to skip this check."
            ignore_checksum = False
            if sys.stdout.isatty():
                ignore_checksum = tty.get_yes_or_no("  Fetch anyway?", default=False)
                if ignore_checksum:
                    tty.debug("Fetching with no checksum. {0}".format(ck_msg))

            if not ignore_checksum:
                raise spack.error.FetchError(
                    "Will not fetch %s" % self.spec.format("{name}{@version}"), ck_msg
                )

        deprecated = spack.config.get("config:deprecated")
        if not deprecated and self.versions.get(self.version, {}).get("deprecated", False):
            tty.warn(
                "{0} is deprecated and may be removed in a future Spack "
                "release.".format(self.spec.format("{name}{@version}"))
            )

            # Ask the user whether to install deprecated version if we're
            # interactive, but just fail if non-interactive.
            dp_msg = (
                "If you are willing to be a maintainer for this version "
                "of the package, submit a PR to remove `deprecated=False"
                "`, or use `--deprecated` to skip this check."
            )
            ignore_deprecation = False
            if sys.stdout.isatty():
                ignore_deprecation = tty.get_yes_or_no("  Fetch anyway?", default=False)

                if ignore_deprecation:
                    tty.debug("Fetching deprecated version. {0}".format(dp_msg))

            if not ignore_deprecation:
                raise spack.error.FetchError(
                    "Will not fetch {0}".format(self.spec.format("{name}{@version}")), dp_msg
                )

        self.stage.create()
        err_msg = None if not self.manual_download else self.download_instr
        start_time = time.time()
        self.stage.fetch(mirror_only, err_msg=err_msg)
        self._fetch_time = time.time() - start_time

        if checksum and self.version in self.versions:
            self.stage.check()

        self.stage.cache_local()

    def do_stage(self, mirror_only=False):
        """Unpacks and expands the fetched tarball."""
        # Always create the stage directory at this point.  Why?  A no-code
        # package may want to use the installation process to install metadata.
        self.stage.create()

        # Fetch/expand any associated code.
        if self.has_code:
            self.do_fetch(mirror_only)
            self.stage.expand_archive()

            if not os.listdir(self.stage.path):
                raise spack.error.FetchError("Archive was empty for %s" % self.name)
        else:
            # Support for post-install hooks requires a stage.source_path
            fsys.mkdirp(self.stage.source_path)

    def do_patch(self):
        """Applies patches if they haven't been applied already."""
        if not self.spec.concrete:
            raise ValueError("Can only patch concrete packages.")

        # Kick off the stage first.  This creates the stage.
        self.do_stage()

        # Package can add its own patch function.
        has_patch_fun = hasattr(self, "patch") and callable(self.patch)

        # Get the patches from the spec (this is a shortcut for the MV-variant)
        patches = self.spec.patches

        # If there are no patches, note it.
        if not patches and not has_patch_fun:
            tty.msg("No patches needed for {0}".format(self.name))
            return

        # Construct paths to special files in the archive dir used to
        # keep track of whether patches were successfully applied.
        archive_dir = self.stage.source_path
        good_file = os.path.join(archive_dir, ".spack_patched")
        no_patches_file = os.path.join(archive_dir, ".spack_no_patches")
        bad_file = os.path.join(archive_dir, ".spack_patch_failed")

        # If we encounter an archive that failed to patch, restage it
        # so that we can apply all the patches again.
        if os.path.isfile(bad_file):
            if self.stage.managed_by_spack:
                tty.debug("Patching failed last time. Restaging.")
                self.stage.restage()
            else:
                # develop specs/ DIYStages may have patch failures but
                # should never be restaged
                msg = (
                    "A patch failure was detected in %s." % self.name
                    + " Build errors may occur due to this."
                )
                tty.warn(msg)
                return

        # If this file exists, then we already applied all the patches.
        if os.path.isfile(good_file):
            tty.msg("Already patched {0}".format(self.name))
            return
        elif os.path.isfile(no_patches_file):
            tty.msg("No patches needed for {0}".format(self.name))
            return

        # Apply all the patches for specs that match this one
        patched = False
        for patch in patches:
            try:
                with fsys.working_dir(self.stage.source_path):
                    patch.apply(self.stage)
                tty.msg("Applied patch {0}".format(patch.path_or_url))
                patched = True
            except spack.error.SpackError as e:
                tty.debug(e)

                # Touch bad file if anything goes wrong.
                tty.msg("Patch %s failed." % patch.path_or_url)
                fsys.touch(bad_file)
                raise

        if has_patch_fun:
            try:
                with fsys.working_dir(self.stage.source_path):
                    self.patch()
                tty.msg("Ran patch() for {0}".format(self.name))
                patched = True
            except spack.multimethod.NoSuchMethodError:
                # We are running a multimethod without a default case.
                # If there's no default it means we don't need to patch.
                if not patched:
                    # if we didn't apply a patch from a patch()
                    # directive, AND the patch function didn't apply, say
                    # no patches are needed.  Otherwise, we already
                    # printed a message for each patch.
                    tty.msg("No patches needed for {0}".format(self.name))
            except spack.error.SpackError as e:
                tty.debug(e)

                # Touch bad file if anything goes wrong.
                tty.msg("patch() function failed for {0}".format(self.name))
                fsys.touch(bad_file)
                raise

        # Get rid of any old failed file -- patches have either succeeded
        # or are not needed.  This is mostly defensive -- it's needed
        # if the restage() method doesn't clean *everything* (e.g., for a repo)
        if os.path.isfile(bad_file):
            os.remove(bad_file)

        # touch good or no patches file so that we skip next time.
        if patched:
            fsys.touch(good_file)
        else:
            fsys.touch(no_patches_file)

    @classmethod
    def all_patches(cls):
        """Retrieve all patches associated with the package.

        Retrieves patches on the package itself as well as patches on the
        dependencies of the package."""
        patches = []
        for _, patch_list in cls.patches.items():
            for patch in patch_list:
                patches.append(patch)

        pkg_deps = cls.dependencies
        for dep_name in pkg_deps:
            for _, dependency in pkg_deps[dep_name].items():
                for _, patch_list in dependency.patches.items():
                    for patch in patch_list:
                        patches.append(patch)

        return patches

    def content_hash(self, content=None):
        """Create a hash based on the artifacts and patches used to build this package.

        This includes:
            * source artifacts (tarballs, repositories) used to build;
            * content hashes (``sha256``'s) of all patches applied by Spack; and
            * canonicalized contents the ``package.py`` recipe used to build.

        This hash is only included in Spack's DAG hash for concrete specs, but if it
        happens to be called on a package with an abstract spec, only applicable (i.e.,
        determinable) portions of the hash will be included.

        """
        # list of components to make up the hash
        hash_content = []

        # source artifacts/repositories
        # TODO: resources
        if self.spec.versions.concrete:
            try:
                source_id = fs.for_package_version(self).source_id()
            except (fs.ExtrapolationError, fs.InvalidArgsError):
                # ExtrapolationError happens if the package has no fetchers defined.
                # InvalidArgsError happens when there are version directives with args,
                #     but none of them identifies an actual fetcher.
                source_id = None

            if not source_id:
                # TODO? in cases where a digest or source_id isn't available,
                # should this attempt to download the source and set one? This
                # probably only happens for source repositories which are
                # referenced by branch name rather than tag or commit ID.
                env = spack.environment.active_environment()
                from_local_sources = env and env.is_develop(self.spec)
                if self.has_code and not self.spec.external and not from_local_sources:
                    message = "Missing a source id for {s.name}@{s.version}"
                    tty.debug(message.format(s=self))
                hash_content.append("".encode("utf-8"))
            else:
                hash_content.append(source_id.encode("utf-8"))

        # patch sha256's
        # Only include these if they've been assigned by the concretizer.
        # We check spec._patches_assigned instead of spec.concrete because
        # we have to call package_hash *before* marking specs concrete
        if self.spec._patches_assigned():
            hash_content.extend(
                ":".join((p.sha256, str(p.level))).encode("utf-8") for p in self.spec.patches
            )

        # package.py contents
        hash_content.append(package_hash(self.spec, source=content).encode("utf-8"))

        # put it all together and encode as base32
        b32_hash = base64.b32encode(
            hashlib.sha256(bytes().join(sorted(hash_content))).digest()
        ).lower()
        b32_hash = b32_hash.decode("utf-8")

        return b32_hash

    @property
    def cmake_prefix_paths(self):
        return [self.prefix]

    def _has_make_target(self, target):
        """Checks to see if 'target' is a valid target in a Makefile.

        Parameters:
            target (str): the target to check for

        Returns:
            bool: True if 'target' is found, else False
        """
        # Prevent altering LC_ALL for 'make' outside this function
        make = copy.deepcopy(inspect.getmodule(self).make)

        # Use English locale for missing target message comparison
        make.add_default_env("LC_ALL", "C")

        # Check if we have a Makefile
        for makefile in ["GNUmakefile", "Makefile", "makefile"]:
            if os.path.exists(makefile):
                break
        else:
            tty.debug("No Makefile found in the build directory")
            return False

        # Check if 'target' is a valid target.
        #
        # `make -n target` performs a "dry run". It prints the commands that
        # would be run but doesn't actually run them. If the target does not
        # exist, you will see one of the following error messages:
        #
        # GNU Make:
        #     make: *** No rule to make target `test'.  Stop.
        #           *** No rule to make target 'test'.  Stop.
        #
        # BSD Make:
        #     make: don't know how to make test. Stop
        missing_target_msgs = [
            "No rule to make target `{0}'.  Stop.",
            "No rule to make target '{0}'.  Stop.",
            "don't know how to make {0}. Stop",
        ]

        kwargs = {"fail_on_error": False, "output": os.devnull, "error": str}

        stderr = make("-n", target, **kwargs)

        for missing_target_msg in missing_target_msgs:
            if missing_target_msg.format(target) in stderr:
                tty.debug("Target '{0}' not found in {1}".format(target, makefile))
                return False

        return True

    def _if_make_target_execute(self, target, *args, **kwargs):
        """Runs ``make target`` if 'target' is a valid target in the Makefile.

        Parameters:
            target (str): the target to potentially execute
        """
        if self._has_make_target(target):
            # Execute target
            inspect.getmodule(self).make(target, *args, **kwargs)

    def _has_ninja_target(self, target):
        """Checks to see if 'target' is a valid target in a Ninja build script.

        Parameters:
            target (str): the target to check for

        Returns:
            bool: True if 'target' is found, else False
        """
        ninja = inspect.getmodule(self).ninja

        # Check if we have a Ninja build script
        if not os.path.exists("build.ninja"):
            tty.debug("No Ninja build script found in the build directory")
            return False

        # Get a list of all targets in the Ninja build script
        # https://ninja-build.org/manual.html#_extra_tools
        all_targets = ninja("-t", "targets", "all", output=str).split("\n")

        # Check if 'target' is a valid target
        matches = [line for line in all_targets if line.startswith(target + ":")]

        if not matches:
            tty.debug("Target '{0}' not found in build.ninja".format(target))
            return False

        return True

    def _if_ninja_target_execute(self, target, *args, **kwargs):
        """Runs ``ninja target`` if 'target' is a valid target in the Ninja
        build script.

        Parameters:
            target (str): the target to potentially execute
        """
        if self._has_ninja_target(target):
            # Execute target
            inspect.getmodule(self).ninja(target, *args, **kwargs)

    def _get_needed_resources(self):
        resources = []
        # Select the resources that are needed for this build
        if self.spec.concrete:
            for when_spec, resource_list in self.resources.items():
                if when_spec in self.spec:
                    resources.extend(resource_list)
        else:
            for when_spec, resource_list in self.resources.items():
                # Note that variant checking is always strict for specs where
                # the name is not specified. But with strict variant checking,
                # only variants mentioned in 'other' are checked. Here we only
                # want to make sure that no constraints in when_spec
                # conflict with the spec, so we need to invoke
                # when_spec.satisfies(self.spec) vs.
                # self.spec.satisfies(when_spec)
                if when_spec.intersects(self.spec):
                    resources.extend(resource_list)
        # Sorts the resources by the length of the string representing their
        # destination. Since any nested resource must contain another
        # resource's name in its path, it seems that should work
        resources = sorted(resources, key=lambda res: len(res.destination))
        return resources

    def _resource_stage(self, resource):
        pieces = ["resource", resource.name, self.spec.dag_hash()]
        resource_stage_folder = "-".join(pieces)
        return resource_stage_folder

    def do_install(self, **kwargs):
        """Called by commands to install a package and or its dependencies.

        Package implementations should override install() to describe
        their build process.

        Args:
            cache_only (bool): Fail if binary package unavailable.
            dirty (bool): Don't clean the build environment before installing.
            explicit (bool): True if package was explicitly installed, False
                if package was implicitly installed (as a dependency).
            fail_fast (bool): Fail if any dependency fails to install;
                otherwise, the default is to install as many dependencies as
                possible (i.e., best effort installation).
            fake (bool): Don't really build; install fake stub files instead.
            force (bool): Install again, even if already installed.
            install_deps (bool): Install dependencies before installing this
                package
            install_source (bool): By default, source is not installed, but
                for debugging it might be useful to keep it around.
            keep_prefix (bool): Keep install prefix on failure. By default,
                destroys it.
            keep_stage (bool): By default, stage is destroyed only if there
                are no exceptions during build. Set to True to keep the stage
                even with exceptions.
            restage (bool): Force spack to restage the package source.
            skip_patch (bool): Skip patch stage of build if True.
            stop_before (str): stop execution before this
                installation phase (or None)
            stop_at (str): last installation phase to be executed
                (or None)
            tests (bool or list or set): False to run no tests, True to test
                all packages, or a list of package names to run tests for some
            use_cache (bool): Install from binary package, if available.
            verbose (bool): Display verbose build output (by default,
                suppresses it)
        """
        PackageInstaller([(self, kwargs)]).install()

    # TODO (post-34236): Update tests and all packages that use this as a
    # TODO (post-34236): package method to the routine made available to
    # TODO (post-34236): packages. Once done, remove this method.
    def cache_extra_test_sources(self, srcs):
        """Copy relative source paths to the corresponding install test subdir

        This method is intended as an optional install test setup helper for
        grabbing source files/directories during the installation process and
        copying them to the installation test subdirectory for subsequent use
        during install testing.

        Args:
            srcs (str or list): relative path for files and or
                subdirectories located in the staged source path that are to
                be copied to the corresponding location(s) under the install
                testing directory.
        """
        msg = (
            "'pkg.cache_extra_test_sources(srcs) is deprecated with removal "
            "expected in v0.22. Use 'cache_extra_test_sources(pkg, srcs)' "
            "instead."
        )
        warnings.warn(msg)
        cache_extra_test_sources(self, srcs)

    def do_test(self, dirty=False, externals=False):
        if self.test_requires_compiler:
            compilers = spack.compilers.compilers_for_spec(
                self.spec.compiler, arch_spec=self.spec.architecture
            )
            if not compilers:
                tty.error(
                    "Skipping tests for package %s\n"
                    % self.spec.format("{name}-{version}-{hash:7}")
                    + "Package test requires missing compiler %s" % self.spec.compiler
                )
                return

        kwargs = {
            "dirty": dirty,
            "fake": False,
            "context": "test",
            "externals": externals,
            "verbose": tty.is_verbose(),
        }

        self.tester.stand_alone_tests(kwargs)

    # TODO (post-34236): Remove this deprecated method when eliminate test,
    # TODO (post-34236): run_test, etc.
    @property
    def _test_deprecated_warning(self):
        alt = f"Use any name starting with 'test_' instead in {self.spec.name}."
        return f"The 'test' method is deprecated. {alt}"

    # TODO (post-34236): Remove this deprecated method when eliminate test,
    # TODO (post-34236): run_test, etc.
    def test(self):
        # Defer tests to virtual and concrete packages
        warnings.warn(self._test_deprecated_warning)

    # TODO (post-34236): Remove this deprecated method when eliminate test,
    # TODO (post-34236): run_test, etc.
    def run_test(
        self,
        exe,
        options=[],
        expected=[],
        status=0,
        installed=False,
        purpose=None,
        skip_missing=False,
        work_dir=None,
    ):
        """Run the test and confirm the expected results are obtained

        Log any failures and continue, they will be re-raised later

        Args:
            exe (str): the name of the executable
            options (str or list): list of options to pass to the runner
            expected (str or list): list of expected output strings.
                Each string is a regex expected to match part of the output.
            status (int or list): possible passing status values
                with 0 meaning the test is expected to succeed
            installed (bool): if ``True``, the executable must be in the
                install prefix
            purpose (str): message to display before running test
            skip_missing (bool): skip the test if the executable is not
                in the install prefix bin directory or the provided work_dir
            work_dir (str or None): path to the smoke test directory
        """

        def test_title(purpose, test_name):
            if not purpose:
                return f"test: {test_name}: execute {test_name}"

            match = re.search(r"test: ([^:]*): (.*)", purpose)
            if match:
                # The test title has all the expected parts
                return purpose

            match = re.search(r"test: (.*)", purpose)
            if match:
                reason = match.group(1)
                return f"test: {test_name}: {reason}"

            return f"test: {test_name}: {purpose}"

        base_exe = os.path.basename(exe)
        alternate = f"Use 'test_part' instead for {self.spec.name} to process {base_exe}."
        warnings.warn(f"The 'run_test' method is deprecated. {alternate}")

        extra = re.compile(r"[\s,\- ]")
        details = (
            [extra.sub("", options)]
            if isinstance(options, str)
            else [extra.sub("", os.path.basename(opt)) for opt in options]
        )
        details = "_".join([""] + details) if details else ""
        test_name = f"test_{base_exe}{details}"
        tty.info(test_title(purpose, test_name), format="g")

        wdir = "." if work_dir is None else work_dir
        with fsys.working_dir(wdir, create=True):
            try:
                runner = which(exe)
                if runner is None and skip_missing:
                    self.tester.status(test_name, TestStatus.SKIPPED, f"{exe} is missing")
                    return
                assert runner is not None, f"Failed to find executable '{exe}'"

                self._run_test_helper(runner, options, expected, status, installed, purpose)
                self.tester.status(test_name, TestStatus.PASSED, None)
                return True
            except (AssertionError, BaseException) as e:
                # print a summary of the error to the log file
                # so that cdash and junit reporters know about it
                exc_type, _, tb = sys.exc_info()

                self.tester.status(test_name, TestStatus.FAILED, str(e))

                import traceback

                # remove the current call frame to exclude the extract_stack
                # call from the error
                stack = traceback.extract_stack()[:-1]

                # Package files have a line added at import time, so we re-read
                # the file to make line numbers match. We have to subtract two
                # from the line number because the original line number is
                # inflated once by the import statement and the lines are
                # displaced one by the import statement.
                for i, entry in enumerate(stack):
                    filename, lineno, function, text = entry
                    if spack.repo.is_package_file(filename):
                        with open(filename, "r") as f:
                            lines = f.readlines()
                        new_lineno = lineno - 2
                        text = lines[new_lineno]
                        stack[i] = (filename, new_lineno, function, text)

                # Format the stack to print and print it
                out = traceback.format_list(stack)
                for line in out:
                    print(line.rstrip("\n"))

                if exc_type is spack.util.executable.ProcessError:
                    out = io.StringIO()
                    spack.build_environment.write_log_summary(
                        out, "test", self.tester.test_log_file, last=1
                    )
                    m = out.getvalue()
                else:
                    # We're below the package context, so get context from
                    # stack instead of from traceback.
                    # The traceback is truncated here, so we can't use it to
                    # traverse the stack.
                    context = spack.build_environment.get_package_context(tb)
                    m = "\n".join(context) if context else ""

                exc = e  # e is deleted after this block

                # If we fail fast, raise another error
                if spack.config.get("config:fail_fast", False):
                    raise TestFailure([(exc, m)])
                else:
                    self.tester.add_failure(exc, m)
                return False

    # TODO (post-34236): Remove this deprecated method when eliminate test,
    # TODO (post-34236): run_test, etc.
    def _run_test_helper(self, runner, options, expected, status, installed, purpose):
        status = [status] if isinstance(status, int) else status
        expected = [expected] if isinstance(expected, str) else expected
        options = [options] if isinstance(options, str) else options

        if installed:
            msg = f"Executable '{runner.name}' expected in prefix, "
            msg += f"found in {runner.path} instead"
            assert runner.path.startswith(self.spec.prefix), msg

        tty.msg(f"Expecting return code in {status}")

        try:
            output = runner(*options, output=str.split, error=str.split)

            assert 0 in status, f"Expected {runner.name} execution to fail"
        except ProcessError as err:
            output = str(err)
            match = re.search(r"exited with status ([0-9]+)", output)
            if not (match and int(match.group(1)) in status):
                raise

        for check in expected:
            cmd = " ".join([runner.name] + options)
            msg = f"Expected '{check}' to match output of `{cmd}`"
            msg += f"\n\nOutput: {output}"
            assert re.search(check, output), msg

    def unit_test_check(self):
        """Hook for unit tests to assert things about package internals.

        Unit tests can override this function to perform checks after
        ``Package.install`` and all post-install hooks run, but before
        the database is updated.

        The overridden function may indicate that the install procedure
        should terminate early (before updating the database) by
        returning ``False`` (or any value such that ``bool(result)`` is
        ``False``).

        Return:
            (bool): ``True`` to continue, ``False`` to skip ``install()``
        """
        return True

    @property
    def build_log_path(self):
        """
        Return the expected (or current) build log file path.  The path points
        to the staging build file until the software is successfully installed,
        when it points to the file in the installation directory.
        """
        return self.install_log_path if self.spec.installed else self.log_path

    @classmethod
    def inject_flags(cls: Type[Pb], name: str, flags: Iterable[str]) -> FLAG_HANDLER_RETURN_TYPE:
        """
        flag_handler that injects all flags through the compiler wrapper.
        """
        return flags, None, None

    @classmethod
    def env_flags(cls: Type[Pb], name: str, flags: Iterable[str]) -> FLAG_HANDLER_RETURN_TYPE:
        """
        flag_handler that adds all flags to canonical environment variables.
        """
        return None, flags, None

    @classmethod
    def build_system_flags(
        cls: Type[Pb], name: str, flags: Iterable[str]
    ) -> FLAG_HANDLER_RETURN_TYPE:
        """
        flag_handler that passes flags to the build system arguments.  Any
        package using `build_system_flags` must also implement
        `flags_to_build_system_args`, or derive from a class that
        implements it.  Currently, AutotoolsPackage and CMakePackage
        implement it.
        """
        return None, None, flags

    def setup_run_environment(self, env):
        """Sets up the run environment for a package.

        Args:
            env (spack.util.environment.EnvironmentModifications): environment
                modifications to be applied when the package is run. Package authors
                can call methods on it to alter the run environment.
        """
        pass

    def setup_dependent_run_environment(self, env, dependent_spec):
        """Sets up the run environment of packages that depend on this one.

        This is similar to ``setup_run_environment``, but it is used to
        modify the run environments of packages that *depend* on this one.

        This gives packages like Python and others that follow the extension
        model a way to implement common environment or run-time settings
        for dependencies.

        Args:
            env (spack.util.environment.EnvironmentModifications): environment
                modifications to be applied when the dependent package is run.
                Package authors can call methods on it to alter the build environment.

            dependent_spec (spack.spec.Spec): The spec of the dependent package
                about to be run. This allows the extendee (self) to query
                the dependent's state. Note that *this* package's spec is
                available as ``self.spec``
        """
        pass

    def setup_dependent_package(self, module, dependent_spec):
        """Set up Python module-scope variables for dependent packages.

        Called before the install() method of dependents.

        Default implementation does nothing, but this can be
        overridden by an extendable package to set up the module of
        its extensions. This is useful if there are some common steps
        to installing all extensions for a certain package.

        Examples:

        1. Extensions often need to invoke the ``python`` interpreter
           from the Python installation being extended. This routine
           can put a ``python()`` Executable object in the module scope
           for the extension package to simplify extension installs.

        2. MPI compilers could set some variables in the dependent's
           scope that point to ``mpicc``, ``mpicxx``, etc., allowing
           them to be called by common name regardless of which MPI is used.

        3. BLAS/LAPACK implementations can set some variables
           indicating the path to their libraries, since these
           paths differ by BLAS/LAPACK implementation.

        Args:
            module (spack.package_base.PackageBase.module): The Python ``module``
                object of the dependent package. Packages can use this to set
                module-scope variables for the dependent to use.

            dependent_spec (spack.spec.Spec): The spec of the dependent package
                about to be built. This allows the extendee (self) to
                query the dependent's state.  Note that *this*
                package's spec is available as ``self.spec``.
        """
        pass

    _flag_handler: Optional[FLAG_HANDLER_TYPE] = None

    @property
    def flag_handler(self) -> FLAG_HANDLER_TYPE:
        if self._flag_handler is None:
            self._flag_handler = PackageBase.inject_flags
        return self._flag_handler

    @flag_handler.setter
    def flag_handler(self, var: FLAG_HANDLER_TYPE) -> None:
        self._flag_handler = var

    # The flag handler method is called for each of the allowed compiler flags.
    # It returns a triple of inject_flags, env_flags, build_system_flags.
    # The flags returned as inject_flags are injected through the spack
    #  compiler wrappers.
    # The flags returned as env_flags are passed to the build system through
    #  the environment variables of the same name.
    # The flags returned as build_system_flags are passed to the build system
    #  package subclass to be turned into the appropriate part of the standard
    #  arguments. This is implemented for build system classes where
    #  appropriate and will otherwise raise a NotImplementedError.

    def flags_to_build_system_args(self, flags):
        # Takes flags as a dict name: list of values
        if any(v for v in flags.values()):
            msg = "The {0} build system".format(self.__class__.__name__)
            msg += " cannot take command line arguments for compiler flags"
            raise NotImplementedError(msg)

    @staticmethod
    def uninstall_by_spec(spec, force=False, deprecator=None):
        if not os.path.isdir(spec.prefix):
            # prefix may not exist, but DB may be inconsistent. Try to fix by
            # removing, but omit hooks.
            specs = spack.store.STORE.db.query(spec, installed=True)
            if specs:
                if deprecator:
                    spack.store.STORE.db.deprecate(specs[0], deprecator)
                    tty.debug("Deprecating stale DB entry for {0}".format(spec.short_spec))
                else:
                    spack.store.STORE.db.remove(specs[0])
                    tty.debug("Removed stale DB entry for {0}".format(spec.short_spec))
                return
            else:
                raise InstallError(str(spec) + " is not installed.")

        if not force:
            dependents = spack.store.STORE.db.installed_relatives(
                spec, direction="parents", transitive=True, deptype=("link", "run")
            )
            if dependents:
                raise PackageStillNeededError(spec, dependents)

        # Try to get the package for the spec
        try:
            pkg = spec.package
        except spack.repo.UnknownEntityError:
            pkg = None

        # Pre-uninstall hook runs first.
        with spack.store.STORE.prefix_locker.write_lock(spec):
            if pkg is not None:
                try:
                    spack.hooks.pre_uninstall(spec)
                except Exception as error:
                    if force:
                        error_msg = (
                            "One or more pre_uninstall hooks have failed"
                            " for {0}, but Spack is continuing with the"
                            " uninstall".format(str(spec))
                        )
                        if isinstance(error, spack.error.SpackError):
                            error_msg += "\n\nError message: {0}".format(str(error))
                        tty.warn(error_msg)
                        # Note that if the uninstall succeeds then we won't be
                        # seeing this error again and won't have another chance
                        # to run the hook.
                    else:
                        raise

            # Uninstalling in Spack only requires removing the prefix.
            if not spec.external:
                msg = "Deleting package prefix [{0}]"
                tty.debug(msg.format(spec.short_spec))
                # test if spec is already deprecated, not whether we want to
                # deprecate it now
                deprecated = bool(spack.store.STORE.db.deprecator(spec))
                spack.store.STORE.layout.remove_install_directory(spec, deprecated)
            # Delete DB entry
            if deprecator:
                msg = "deprecating DB entry [{0}] in favor of [{1}]"
                tty.debug(msg.format(spec.short_spec, deprecator.short_spec))
                spack.store.STORE.db.deprecate(spec, deprecator)
            else:
                msg = "Deleting DB entry [{0}]"
                tty.debug(msg.format(spec.short_spec))
                spack.store.STORE.db.remove(spec)

        if pkg is not None:
            try:
                spack.hooks.post_uninstall(spec)
            except Exception:
                # If there is a failure here, this is our only chance to do
                # something about it: at this point the Spec has been removed
                # from the DB and prefix, so the post-uninstallation hooks
                # will not have another chance to run.
                error_msg = (
                    "One or more post-uninstallation hooks failed for"
                    " {0}, but the prefix has been removed (if it is not"
                    " external).".format(str(spec))
                )
                tb_msg = traceback.format_exc()
                error_msg += "\n\nThe error:\n\n{0}".format(tb_msg)
                tty.warn(error_msg)

        tty.msg("Successfully uninstalled {0}".format(spec.short_spec))

    def do_uninstall(self, force=False):
        """Uninstall this package by spec."""
        # delegate to instance-less method.
        PackageBase.uninstall_by_spec(self.spec, force)

    def do_deprecate(self, deprecator, link_fn):
        """Deprecate this package in favor of deprecator spec"""
        spec = self.spec

        # Install deprecator if it isn't installed already
        if not spack.store.STORE.db.query(deprecator):
            deprecator.package.do_install()

        old_deprecator = spack.store.STORE.db.deprecator(spec)
        if old_deprecator:
            # Find this specs yaml file from its old deprecation
            self_yaml = spack.store.STORE.layout.deprecated_file_path(spec, old_deprecator)
        else:
            self_yaml = spack.store.STORE.layout.spec_file_path(spec)

        # copy spec metadata to "deprecated" dir of deprecator
        depr_yaml = spack.store.STORE.layout.deprecated_file_path(spec, deprecator)
        fsys.mkdirp(os.path.dirname(depr_yaml))
        shutil.copy2(self_yaml, depr_yaml)

        # Any specs deprecated in favor of this spec are re-deprecated in
        # favor of its new deprecator
        for deprecated in spack.store.STORE.db.specs_deprecated_by(spec):
            deprecated.package.do_deprecate(deprecator, link_fn)

        # Now that we've handled metadata, uninstall and replace with link
        PackageBase.uninstall_by_spec(spec, force=True, deprecator=deprecator)
        link_fn(deprecator.prefix, spec.prefix)

    def _check_extendable(self):
        if not self.extendable:
            raise ValueError("Package %s is not extendable!" % self.name)

    def view(self):
        """Create a view with the prefix of this package as the root.
        Extensions added to this view will modify the installation prefix of
        this package.
        """
        return YamlFilesystemView(self.prefix, spack.store.STORE.layout)

    def do_restage(self):
        """Reverts expanded/checked out source to a pristine state."""
        self.stage.restage()

    def do_clean(self):
        """Removes the package's build stage and source tarball."""
        self.stage.destroy()

    @classmethod
    def format_doc(cls, **kwargs):
        """Wrap doc string at 72 characters and format nicely"""
        indent = kwargs.get("indent", 0)

        if not cls.__doc__:
            return ""

        doc = re.sub(r"\s+", " ", cls.__doc__)
        lines = textwrap.wrap(doc, 72)
        results = io.StringIO()
        for line in lines:
            results.write((" " * indent) + line + "\n")
        return results.getvalue()

    @property
    def all_urls(self):
        """A list of all URLs in a package.

        Check both class-level and version-specific URLs.

        Returns:
            list: a list of URLs
        """
        urls = []
        if hasattr(self, "url") and self.url:
            urls.append(self.url)

        # fetch from first entry in urls to save time
        if hasattr(self, "urls") and self.urls:
            urls.append(self.urls[0])

        for args in self.versions.values():
            if "url" in args:
                urls.append(args["url"])
        return urls

    def fetch_remote_versions(self, concurrency=None):
        """Find remote versions of this package.

        Uses ``list_url`` and any other URLs listed in the package file.

        Returns:
            dict: a dictionary mapping versions to URLs
        """
        if not self.all_urls:
            return {}

        try:
            return spack.url.find_versions_of_archive(
                self.all_urls, self.list_url, self.list_depth, concurrency, reference_package=self
            )
        except spack.util.web.NoNetworkConnectionError as e:
            tty.die("Package.fetch_versions couldn't connect to:", e.url, e.message)

    @property
    def rpath(self):
        """Get the rpath this package links with, as a list of paths."""
        deps = self.spec.dependencies(deptype="link")

        # on Windows, libraries of runtime interest are typically
        # stored in the bin directory
        if sys.platform == "win32":
            rpaths = [self.prefix.bin]
            rpaths.extend(d.prefix.bin for d in deps if os.path.isdir(d.prefix.bin))
        else:
            rpaths = [self.prefix.lib, self.prefix.lib64]
            rpaths.extend(d.prefix.lib for d in deps if os.path.isdir(d.prefix.lib))
            rpaths.extend(d.prefix.lib64 for d in deps if os.path.isdir(d.prefix.lib64))
        return rpaths

    @property
    def rpath_args(self):
        """
        Get the rpath args as a string, with -Wl,-rpath, for each element
        """
        return " ".join("-Wl,-rpath,%s" % p for p in self.rpath)

    @property
    def builder(self):
        return spack.builder.create(self)


inject_flags = PackageBase.inject_flags
env_flags = PackageBase.env_flags
build_system_flags = PackageBase.build_system_flags


def install_dependency_symlinks(pkg, spec, prefix):
    """
    Execute a dummy install and flatten dependencies.

    This routine can be used in a ``package.py`` definition by setting
    ``install = install_dependency_symlinks``.

    This feature comes in handy for creating a common location for the
    the installation of third-party libraries.
    """
    flatten_dependencies(spec, prefix)


def use_cray_compiler_names():
    """Compiler names for builds that rely on cray compiler names."""
    os.environ["CC"] = "cc"
    os.environ["CXX"] = "CC"
    os.environ["FC"] = "ftn"
    os.environ["F77"] = "ftn"


def flatten_dependencies(spec, flat_dir):
    """Make each dependency of spec present in dir via symlink."""
    for dep in spec.traverse(root=False):
        name = dep.name

        dep_path = spack.store.STORE.layout.path_for_spec(dep)
        dep_files = LinkTree(dep_path)

        os.mkdir(flat_dir + "/" + name)

        conflict = dep_files.find_conflict(flat_dir + "/" + name)
        if conflict:
            raise DependencyConflictError(conflict)

        dep_files.merge(flat_dir + "/" + name)


def possible_dependencies(*pkg_or_spec, **kwargs):
    """Get the possible dependencies of a number of packages.

    See ``PackageBase.possible_dependencies`` for details.
    """
    packages = []
    for pos in pkg_or_spec:
        if isinstance(pos, PackageMeta):
            packages.append(pos)
            continue

        if not isinstance(pos, spack.spec.Spec):
            pos = spack.spec.Spec(pos)

        if spack.repo.PATH.is_virtual(pos.name):
            packages.extend(p.package_class for p in spack.repo.PATH.providers_for(pos.name))
            continue
        else:
            packages.append(pos.package_class)

    visited = {}
    for pkg in packages:
        pkg.possible_dependencies(visited=visited, **kwargs)

    return visited


class PackageStillNeededError(InstallError):
    """Raised when package is still needed by another on uninstall."""

    def __init__(self, spec, dependents):
        super().__init__("Cannot uninstall %s" % spec)
        self.spec = spec
        self.dependents = dependents


class PackageError(spack.error.SpackError):
    """Raised when something is wrong with a package definition."""

    def __init__(self, message, long_msg=None):
        super().__init__(message, long_msg)


class NoURLError(PackageError):
    """Raised when someone tries to build a URL for a package with no URLs."""

    def __init__(self, cls):
        super().__init__("Package %s has no version with a URL." % cls.__name__)


class InvalidPackageOpError(PackageError):
    """Raised when someone tries perform an invalid operation on a package."""


class ExtensionError(PackageError):
    """Superclass for all errors having to do with extension packages."""


class ActivationError(ExtensionError):
    """Raised when there are problems activating an extension."""

    def __init__(self, msg, long_msg=None):
        super().__init__(msg, long_msg)


class DependencyConflictError(spack.error.SpackError):
    """Raised when the dependencies cannot be flattened as asked for."""

    def __init__(self, conflict):
        super().__init__("%s conflicts with another file in the flattened directory." % (conflict))
