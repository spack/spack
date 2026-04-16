# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys
from typing import TYPE_CHECKING, List, Optional, Set, Union

from spack.vendor.typing_extensions import Literal

import spack.config
import spack.traverse

if TYPE_CHECKING:
    import spack.installer
    import spack.new_installer
    import spack.package_base


def create_installer(
    packages: List["spack.package_base.PackageBase"],
    *,
    dirty: bool = False,
    explicit: Union[Set[str], bool] = False,
    overwrite: Optional[Union[List[str], Set[str]]] = None,
    fail_fast: bool = False,
    fake: bool = False,
    include_build_deps: bool = False,
    install_deps: bool = True,
    install_package: bool = True,
    install_source: bool = False,
    keep_prefix: bool = False,
    keep_stage: bool = False,
    restage: bool = True,
    skip_patch: bool = False,
    stop_at: Optional[str] = None,
    stop_before: Optional[str] = None,
    tests: Union[bool, List[str], Set[str]] = False,
    unsigned: Optional[bool] = None,
    verbose: bool = False,
    concurrent_packages: Optional[int] = None,
    root_policy: Literal["auto", "cache_only", "source_only"] = "auto",
    dependencies_policy: Literal["auto", "cache_only", "source_only"] = "auto",
    create_reports: bool = False,
) -> Union["spack.installer.PackageInstaller", "spack.new_installer.PackageInstaller"]:
    """Create an installer based on the current configuration and feature support."""
    use_old_installer = (
        sys.platform == "win32" or spack.config.get("config:installer", "new") == "old"
    )

    # Use the old installer if splicing is used.
    if not use_old_installer:
        specs = [pkg.spec for pkg in packages]
        for s in spack.traverse.traverse_nodes(specs):
            if s.build_spec is not s:
                use_old_installer = True
                break
    if use_old_installer:
        from spack.installer import PackageInstaller  # type: ignore
    else:
        from spack.new_installer import PackageInstaller  # type: ignore

    return PackageInstaller(
        packages,
        dirty=dirty,
        explicit=explicit,
        overwrite=overwrite,
        fail_fast=fail_fast,
        fake=fake,
        include_build_deps=include_build_deps,
        install_deps=install_deps,
        install_package=install_package,
        install_source=install_source,
        keep_prefix=keep_prefix,
        keep_stage=keep_stage,
        restage=restage,
        skip_patch=skip_patch,
        stop_at=stop_at,
        stop_before=stop_before,
        tests=tests,
        unsigned=unsigned,
        verbose=verbose,
        concurrent_packages=concurrent_packages,
        root_policy=root_policy,
        dependencies_policy=dependencies_policy,
        create_reports=create_reports,
    )
