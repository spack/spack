# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import stat
import warnings
from typing import Any, Iterable, NamedTuple, Optional

import spack.config
import spack.repo
import spack.spec
from spack.error import ConfigError
from spack.version import Version

_lesser_spec_types = {"compiler": spack.spec.CompilerSpec, "version": Version}


def _spec_type(component):
    """Map from component name to spec type for package prefs."""
    return _lesser_spec_types.get(component, spack.spec.Spec)


def _first_set(packages: dict, names: Iterable[str], *path: str) -> Any:
    """Return the first non-empty value at ``packages:<name>:<path>`` for ``name`` in ``names``,
    or None if there is none."""
    for name in names:
        value = packages.get(name)
        for key in path:
            if not value:
                break
            value = value.get(key)
        if value:
            return value
    return None


class PackagePrefs:
    """Defines the sort order for a set of specs.

    Spack's package preference implementation uses PackagePrefs to
    define sort order. The PackagePrefs class looks at Spack's
    packages.yaml configuration and, when called on a spec, returns a key
    that can be used to sort that spec in order of the user's
    preferences.

    You can use it like this::

       # key function sorts CompilerSpecs for `mpich` in order of preference
       kf = PackagePrefs("mpich", "compiler", configuration=spack.config.CONFIG)
       compiler_list.sort(key=kf)

    Or like this::

       # key function to sort VersionLists for OpenMPI in order of preference.
       kf = PackagePrefs("openmpi", "version", configuration=spack.config.CONFIG)
       version_list.sort(key=kf)

    Optionally, you can sort in order of preferred virtual dependency
    providers.  To do that, provide ``"providers"`` and a third argument
    denoting the virtual package (e.g., ``mpi``)::

       kf = PackagePrefs("trilinos", "providers", "mpi", configuration=spack.config.CONFIG)
       provider_spec_list.sort(key=kf)

    """

    def __init__(
        self, pkgname, component, vpkg=None, all=True, *, configuration: spack.config.Configuration
    ):
        self.pkgname = pkgname
        self.component = component
        self.vpkg = vpkg
        self.all = all
        self._configuration = configuration

        self._spec_order = None

    def __call__(self, spec):
        """Return a key object (an index) that can be used to sort spec.

        Sort is done in package order. We don't cache the result of
        this function as Python's sort functions already ensure that the
        key function is called at most once per sorted element.
        """
        if self._spec_order is None:
            self._spec_order = self._specs_for_pkg(
                self.pkgname,
                self.component,
                self.vpkg,
                self.all,
                configuration=self._configuration,
            )
        spec_order = self._spec_order

        # integer is the index of the first spec in order that satisfies
        # spec, or it's a number larger than any position in the order.
        match_index = next(
            (i for i, s in enumerate(spec_order) if spec.intersects(s)), len(spec_order)
        )
        if match_index < len(spec_order) and spec_order[match_index] == spec:
            # If this is called with multiple specs that all satisfy the same
            # minimum index in spec_order, the one which matches that element
            # of spec_order exactly is considered slightly better. Note
            # that because this decreases the value by less than 1, it is not
            # better than a match which occurs at an earlier index.
            match_index -= 0.5
        return match_index

    @classmethod
    def order_for_package(
        cls, pkgname, component, vpkg=None, all=True, *, configuration: spack.config.Configuration
    ):
        """Given a package name, sort component (e.g, version, compiler, ...),
        and an optional vpkg, return the list from the packages config.
        """
        pkglist = [pkgname, "all"] if all else [pkgname]
        path = (component,) if vpkg is None else (component, vpkg)
        order = _first_set(configuration.get_config("packages"), pkglist, *path)
        if not order:
            return []

        ret = [str(s).strip() for s in order]
        if component == "target":
            ret = ["target=%s" % tname for tname in ret]
        return ret

    @classmethod
    def _specs_for_pkg(
        cls, pkgname, component, vpkg=None, all=True, *, configuration: spack.config.Configuration
    ):
        """Given a sort order specified by the pkgname/component/second_key,
        return a list of CompilerSpecs, VersionLists, or Specs for
        that sorting list.
        """
        pkglist = cls.order_for_package(pkgname, component, vpkg, all, configuration=configuration)
        spec_type = _spec_type(component)
        return [spec_type(s) for s in pkglist]

    @classmethod
    def preferred_variants(
        cls, pkg_name, *, configuration: spack.config.Configuration, repo: spack.repo.RepoPath
    ):
        """Return a VariantMap of preferred variants/values for a spec."""
        packages = configuration.get_config("packages")
        variants = _first_set(packages, (pkg_name, "all"), "variants") or ""

        # allow variants to be list or string
        if not isinstance(variants, str):
            variants = " ".join(variants)

        # Only return variants that are actually supported by the package
        pkg_cls = repo.get_pkg_class(pkg_name)
        spec = spack.spec.Spec(f"{pkg_name} {variants}")
        return {
            name: variant
            for name, variant in spec.variants.items()
            if name in pkg_cls.variant_names()
        }


class Permissions(NamedTuple):
    """Permissions configured under ``packages:<name>:permissions``."""

    #: mode for files
    file_mode: int
    #: mode for directories: ``file_mode``, plus ``S_ISGID`` when group bits are set and
    #: ``config:allow_sgid`` is true
    dir_mode: int
    #: name of the group, or empty to leave the group unchanged
    group: str


def package_permissions(
    configuration: spack.config.Configuration, pkg_name: Optional[str]
) -> Permissions:
    """Return the permissions configured for a package.

    Each key of ``packages:<pkg_name>:permissions`` falls back to the same key under
    ``packages:all:permissions``. With ``pkg_name`` None, only ``packages:all`` is read.
    """
    packages = configuration.get_config("packages")
    names = ("all",) if pkg_name is None else (pkg_name, "all")
    readable = _first_set(packages, names, "permissions", "read") or ""
    writable = _first_set(packages, names, "permissions", "write") or ""
    group = _first_set(packages, names, "permissions", "group") or ""

    perms = stat.S_IRWXU
    if readable in ("world", "group"):  # world includes group
        perms |= stat.S_IRGRP | stat.S_IXGRP
    if readable == "world":
        perms |= stat.S_IROTH | stat.S_IXOTH

    if writable in ("world", "group"):
        if readable == "user":
            raise ConfigError(
                "Writable permissions may not be more"
                + " permissive than readable permissions.\n"
                + "      Violating package is %s" % (pkg_name or "all")
            )
        perms |= stat.S_IWGRP
    if writable == "world":
        if readable != "world":
            raise ConfigError(
                "Writable permissions may not be more"
                + " permissive than readable permissions.\n"
                + "      Violating package is %s" % (pkg_name or "all")
            )
        perms |= stat.S_IWOTH

    dir_perms = perms
    if perms & stat.S_IRWXG and configuration.get("config:allow_sgid", True):
        dir_perms |= stat.S_ISGID

    return Permissions(file_mode=perms, dir_mode=dir_perms, group=group)


def warn_if_sgid_on_afs(prefix: str, dir_mode: int) -> None:
    """Warn if ``dir_mode`` sets the sgid bit and ``prefix`` seems to be on AFS."""
    if dir_mode & stat.S_ISGID and "/afs/" in prefix:
        warnings.warn(
            f"Directory {prefix} seems to be located on AFS. If you encounter errors, try "
            "disabling the allow_sgid option using: spack config add 'config:allow_sgid:false'"
        )
