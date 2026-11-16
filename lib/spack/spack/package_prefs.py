# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import stat
import warnings
from typing import Any, Callable, Iterable, NamedTuple, Optional

import spack.config
import spack.repo
import spack.spec
from spack.error import ConfigError


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


def target_sort_key(
    configuration: spack.config.Configuration,
) -> Callable[[spack.spec.Spec], float]:
    """Return a key to sort ``target=<name>`` specs in the order of ``packages:all:target``.

    The key of a spec is the index of the first preferred target it intersects, minus 0.5 if it is
    equal to that target, or the number of preferred targets if it intersects none.
    """
    names = _first_set(configuration.get_config("packages"), ("all",), "target") or []
    order = [spack.spec.Spec(f"target={str(name).strip()}") for name in names]

    def key(spec: spack.spec.Spec) -> float:
        index = next((i for i, s in enumerate(order) if spec.intersects(s)), len(order))
        if index < len(order) and order[index] == spec:
            return index - 0.5
        return index

    return key


def preferred_variants(
    pkg_name: str, *, configuration: spack.config.Configuration, repo: spack.repo.RepoPath
):
    """Return the variants in ``packages:<pkg_name>:variants``, or else in
    ``packages:all:variants``, that the package defines, by name."""
    packages = configuration.get_config("packages")
    variants = _first_set(packages, (pkg_name, "all"), "variants") or ""

    # allow variants to be list or string
    if not isinstance(variants, str):
        variants = " ".join(variants)

    # Only return variants that are actually supported by the package
    pkg_cls = repo.get_pkg_class(pkg_name)
    spec = spack.spec.Spec(f"{pkg_name} {variants}")
    return {
        name: variant for name, variant in spec.variants.items() if name in pkg_cls.variant_names()
    }


class Permissions(NamedTuple):
    """Permissions configured under ``packages:<name>:permissions``."""

    #: mode for files
    file_mode: int
    #: mode for directories, which is ``file_mode`` plus ``S_ISGID`` when group bits are set
    #: and ``config:allow_sgid`` is true
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
