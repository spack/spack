# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import os
import shlex
import sys
import tempfile
from typing import Any, Dict, Generator, List, Optional, Tuple, Union

import spack
import spack.caches
import spack.ci
import spack.config
import spack.llnl.util.filesystem as fs
import spack.llnl.util.tty as tty
import spack.repo
import spack.spec
import spack.util.executable
import spack.util.git
import spack.util.path
import spack.util.spack_json as sjson
import spack.util.spack_yaml
from spack.cmd.common import arguments
from spack.error import SpackError
from spack.llnl.util.tty import color
from spack.version import StandardVersion

from . import doc_dedented, doc_first_line

description = "manage package source repositories"
section = "config"
level = "long"


def setup_parser(subparser: argparse.ArgumentParser):
    sp = subparser.add_subparsers(metavar="SUBCOMMAND", dest="repo_command")

    # Create
    create_parser = sp.add_parser(
        "create", description=doc_dedented(repo_create), help=doc_first_line(repo_create)
    )
    create_parser.add_argument("directory", help="directory to create the repo in")
    create_parser.add_argument(
        "namespace", help="name or namespace to identify packages in the repository"
    )
    create_parser.add_argument(
        "-d",
        "--subdirectory",
        action="store",
        dest="subdir",
        default=spack.repo.packages_dir_name,
        help="subdirectory to store packages in the repository\n\n"
        "default 'packages'. use an empty string for no subdirectory",
    )

    # List
    list_parser = sp.add_parser(
        "list", aliases=["ls"], description=doc_dedented(repo_list), help=doc_first_line(repo_list)
    )
    list_parser.add_argument(
        "--scope",
        action=arguments.ConfigScope,
        type=arguments.config_scope_readable_validator,
        help="configuration scope to read from",
    )
    output_group = list_parser.add_mutually_exclusive_group()
    output_group.add_argument("--names", action="store_true", help="show configuration names only")
    output_group.add_argument(
        "--namespaces", action="store_true", help="show repository namespaces only"
    )
    output_group.add_argument(
        "--json", action="store_true", help="output repositories as machine-readable json records"
    )

    # Add
    add_parser = sp.add_parser(
        "add", description=doc_dedented(repo_add), help=doc_first_line(repo_add)
    )
    add_parser.add_argument(
        "path_or_repo", help="path or git repository of a Spack package repository"
    )
    # optional positional argument for destination name in case of git repository
    add_parser.add_argument(
        "destination",
        nargs="?",
        default=None,
        help="destination to clone git repository into (defaults to cache directory)",
    )
    add_parser.add_argument(
        "--name",
        action="store",
        help="config name for the package repository, defaults to the namespace of the repository",
    )
    add_parser.add_argument(
        "--path",
        help="relative path to the Spack package repository inside a git repository. Can be "
        "repeated to add multiple package repositories in case of a monorepo",
        action="append",
        default=[],
    )
    add_parser.add_argument(
        "--scope",
        action=arguments.ConfigScope,
        default=lambda: spack.config.default_modify_scope(),
        help="configuration scope to modify",
    )

    # Set (modify existing repository configuration)
    set_parser = sp.add_parser(
        "set", description=doc_dedented(repo_set), help=doc_first_line(repo_set)
    )
    set_parser.add_argument("namespace", help="namespace of a Spack package repository")
    set_parser.add_argument(
        "--destination", help="destination to clone git repository into", action="store"
    )
    set_parser.add_argument(
        "--path",
        help="relative path to the Spack package repository inside a git repository. Can be "
        "repeated to add multiple package repositories in case of a monorepo",
        action="append",
        default=[],
    )
    set_parser.add_argument(
        "--scope",
        action=arguments.ConfigScope,
        default=lambda: spack.config.default_modify_scope(),
        help="configuration scope to modify",
    )

    # Remove
    remove_parser = sp.add_parser(
        "remove",
        description=doc_dedented(repo_remove),
        help=doc_first_line(repo_remove),
        aliases=["rm"],
    )
    remove_parser.add_argument(
        "namespace_or_path", help="namespace or path of a Spack package repository"
    )
    remove_parser.add_argument(
        "--scope", action=arguments.ConfigScope, default=None, help="configuration scope to modify"
    )
    remove_parser.add_argument(
        "--all-scopes",
        action="store_true",
        default=False,
        help="remove from all config scopes (default: highest scope with matching repo)",
    )

    # Migrate
    migrate_parser = sp.add_parser(
        "migrate", description=doc_dedented(repo_migrate), help=doc_first_line(repo_migrate)
    )
    migrate_parser.add_argument(
        "namespace_or_path", help="path to a Spack package repository directory"
    )
    patch_or_fix = migrate_parser.add_mutually_exclusive_group(required=True)
    patch_or_fix.add_argument(
        "--dry-run",
        action="store_true",
        help="do not modify the repository, but dump a patch file",
    )
    patch_or_fix.add_argument(
        "--fix",
        action="store_true",
        help="automatically migrate the repository to the latest Package API",
    )

    # Update
    update_parser = sp.add_parser(
        "update", description=doc_dedented(repo_update), help=doc_first_line(repo_update)
    )
    update_parser.add_argument("names", nargs="*", default=[], help="repositories to update")
    update_parser.add_argument(
        "--remote",
        "-r",
        default="origin",
        nargs="?",
        help="name of remote to check for branches, tags, or commits",
    )
    update_parser.add_argument(
        "--scope",
        action=arguments.ConfigScope,
        default=lambda: spack.config.default_modify_scope(),
        help="configuration scope to modify",
    )
    update_parser.add_argument(
        "--branch", "-b", nargs="?", default=None, help="name of a branch to change to"
    )
    refspec = update_parser.add_mutually_exclusive_group(required=False)
    refspec.add_argument("--tag", "-t", nargs="?", default=None, help="name of a tag to change to")
    refspec.add_argument(
        "--commit", "-c", nargs="?", default=None, help="name of a commit to change to"
    )

    # Show updates
    show_version_updates_parser = sp.add_parser(
        "show-version-updates", help=repo_show_version_updates.__doc__
    )
    show_version_updates_parser.add_argument(
        "--no-manual-packages", action="store_true", help="exclude manual packages"
    )
    show_version_updates_parser.add_argument(
        "--no-git-versions", action="store_true", help="exclude versions from git"
    )
    show_version_updates_parser.add_argument(
        "--only-redistributable", action="store_true", help="exclude non-redistributable packages"
    )
    show_version_updates_parser.add_argument(
        "repository", help="name or path of the repository to analyze"
    )
    show_version_updates_parser.add_argument(
        "from_ref", help="git ref from which to start looking at changes"
    )
    show_version_updates_parser.add_argument("to_ref", help="git ref to end looking at changes")


def repo_create(args):
    """create a new package repository"""
    full_path, namespace = spack.repo.create_repo(args.directory, args.namespace, args.subdir)
    tty.msg("Created repo with namespace '%s'." % namespace)
    tty.msg("To register it with spack, run this command:", "spack repo add %s" % full_path)


def _add_repo(
    path_or_repo: str,
    name: Optional[str],
    scope: Optional[str],
    paths: List[str],
    destination: Optional[str],
    config: Optional[spack.config.Configuration] = None,
) -> str:
    config = config or spack.config.CONFIG

    existing: Dict[str, Any] = config.get("repos", default={}, scope=scope)

    if name and name in existing:
        raise SpackError(f"A repository with the name '{name}' already exists.")

    # Interpret as a git URL when it contains a colon at index 2 or more, not preceded by a
    # forward slash. That allows C:/ windows paths, while following git's convention to distinguish
    # between local paths on the one hand and URLs and SCP like syntax on the other.
    entry: Union[str, Dict[str, Any]]
    colon_idx = path_or_repo.find(":")

    if colon_idx > 1 and "/" not in path_or_repo[:colon_idx]:  # git URL
        entry = {"git": path_or_repo}
        if len(paths) >= 1:
            entry["paths"] = paths
        if destination:
            entry["destination"] = destination
    else:  # local path
        if destination:
            raise SpackError("The 'destination' argument is only valid for git repositories")
        elif paths:
            raise SpackError("The --paths flag is only valid for git repositories")
        entry = spack.util.path.canonicalize_path(path_or_repo)

    descriptor = spack.repo.parse_config_descriptor(
        name or "<unnamed>", entry, lock=spack.repo.package_repository_lock()
    )
    descriptor.initialize(git=spack.util.executable.which("git"))

    packages_repos = descriptor.construct(cache=spack.caches.MISC_CACHE)

    usable_repos: Dict[str, spack.repo.Repo] = {}

    for _path, _repo_or_err in packages_repos.items():
        if isinstance(_repo_or_err, Exception):
            tty.warn(f"Skipping package repository '{_path}' due to: {_repo_or_err}")
        else:
            usable_repos[_path] = _repo_or_err

    if not usable_repos:
        raise SpackError(f"No package repository could be constructed from {path_or_repo}")

    # For the config key, default to --name, then to the namespace if there's only one repo.
    # Otherwise, the name is unclear and we require the user to specify it.
    if name:
        key = name
    elif len(usable_repos) == 1:
        key = next(iter(usable_repos.values())).namespace
    else:
        raise SpackError("Multiple package repositories found, please specify a name with --name.")

    if key in existing:
        raise SpackError(f"A repository with the name '{key}' already exists.")

    # Prepend the new repository
    config.set("repos", spack.util.spack_yaml.syaml_dict({key: entry, **existing}), scope)
    return key


def repo_add(args):
    """add package repositories to Spack's configuration"""
    name = _add_repo(
        path_or_repo=args.path_or_repo,
        name=args.name,
        scope=args.scope,
        paths=args.path,
        destination=args.destination,
    )
    tty.msg(f"Added repo to config with name '{name}'.")


def repo_remove(args):
    """remove a repository from Spack's configuration"""
    scopes = [args.scope] if args.scope else reversed(list(spack.config.CONFIG.scopes.keys()))
    found_and_removed = False
    for scope in scopes:
        found_and_removed |= _remove_repo(args.namespace_or_path, scope)
        if found_and_removed and not args.all_scopes:
            return
    if not found_and_removed:
        tty.die(f"No repository with path or namespace: {args.namespace_or_path}")


def _remove_repo(namespace_or_path, scope):
    repos: Dict[str, str] = spack.config.get("repos", scope=scope)

    if namespace_or_path in repos:
        # delete by name (from config)
        key = namespace_or_path
    else:
        # delete by namespace or path (requires constructing the repo)
        canon_path = spack.util.path.canonicalize_path(namespace_or_path)
        descriptors = spack.repo.RepoDescriptors.from_config(
            spack.repo.package_repository_lock(), spack.config.CONFIG, scope=scope
        )
        for name, descriptor in descriptors.items():
            descriptor.initialize(fetch=False)

            # For now you cannot delete monorepos with multiple package repositories from config,
            # hence "all" and not "any". We can improve this later if needed.
            if all(
                r.namespace == namespace_or_path or r.root == canon_path
                for r in descriptor.construct(cache=spack.caches.MISC_CACHE).values()
                if isinstance(r, spack.repo.Repo)
            ):
                key = name
                break
        else:
            return False

    del repos[key]
    spack.config.set("repos", repos, scope)
    tty.msg(f"Removed repository '{namespace_or_path}' from scope '{scope}'.")
    return True


def repo_list(args):
    """show registered repositories and their namespaces

    List all package repositories known to Spack. Repositories
    can be local directories or remote git repositories.
    """
    descriptors = spack.repo.RepoDescriptors.from_config(
        lock=spack.repo.package_repository_lock(), config=spack.config.CONFIG, scope=args.scope
    )

    # --names: just print config names
    if args.names:
        for name in descriptors:
            print(name)
        return

    # --namespaces: print all repo namespaces
    if args.namespaces:
        for name, path, maybe_repo in _iter_repos_from_descriptors(descriptors):
            if isinstance(maybe_repo, spack.repo.Repo):
                print(maybe_repo.namespace)
        return

    # Collect all repository information
    repo_info = []

    for name, path, maybe_repo in _iter_repos_from_descriptors(descriptors):
        if isinstance(maybe_repo, spack.repo.Repo):
            status = "installed"
            namespace = maybe_repo.namespace
            api = maybe_repo.package_api_str
            repo_path = maybe_repo.root
        elif maybe_repo is None:  # Uninitialized Git-based repo case
            status = "uninitialized"
            namespace = name
            api = ""
            repo_path = path
        else:  # Exception/error case
            status = "error"
            namespace = name
            api = ""
            repo_path = path

        # Add the repo info to our list
        repo_info.append(
            {
                "name": name,
                "namespace": namespace,
                "path": repo_path,
                "api_version": api,
                "status": status,
                "error": str(maybe_repo) if isinstance(maybe_repo, Exception) else None,
            }
        )

    # Output in JSON format if requested
    if args.json:
        sjson.dump(repo_info, sys.stdout)
        return

    # Default table format with aligned output
    formatted_repo_info = []
    for repo in repo_info:
        if repo["status"] == "installed":
            status = "@g{[+]}"
        elif repo["status"] == "uninitialized":
            status = "@K{ - }"
        else:  # error
            status = "@r{[-]}"

        formatted_repo_info.append((status, repo["namespace"], repo["api_version"], repo["path"]))

    if formatted_repo_info:
        max_namespace_width = max(len(namespace) for _, namespace, _, _ in formatted_repo_info) + 3
        max_api_width = max(len(api) for _, _, api, _ in formatted_repo_info) + 3

        # Print aligned output
        for status, namespace, api, path in formatted_repo_info:
            cpath = color.cescape(path)
            color.cprint(
                f"{status} {namespace:<{max_namespace_width}} {api:<{max_api_width}} {cpath}"
            )


def _get_repo(name_or_path: str) -> Optional[spack.repo.Repo]:
    """get a repo by path or namespace"""
    try:
        return spack.repo.from_path(name_or_path)
    except spack.repo.RepoError:
        pass

    descriptors = spack.repo.RepoDescriptors.from_config(
        spack.repo.package_repository_lock(), spack.config.CONFIG
    )

    repo_path, _ = descriptors.construct(cache=spack.caches.MISC_CACHE, fetch=False)

    for repo in repo_path.repos:
        if repo.namespace == name_or_path:
            return repo

    return None


def repo_migrate(args: Any) -> int:
    """migrate a package repository to the latest Package API"""
    from spack.repo_migrate import migrate_v1_to_v2, migrate_v2_imports

    repo = _get_repo(args.namespace_or_path)

    if repo is None:
        tty.die(f"No such repository: {args.namespace_or_path}")

    if args.dry_run:
        fd, patch_file_path = tempfile.mkstemp(
            suffix=".patch", prefix="repo-migrate-", dir=os.getcwd()
        )
        patch_file = os.fdopen(fd, "bw")
        tty.msg(f"Patch file will be written to {patch_file_path}")
    else:
        patch_file_path = None
        patch_file = None

    try:
        if (1, 0) <= repo.package_api < (2, 0):
            success, repo_v2 = migrate_v1_to_v2(repo, patch_file=patch_file)
            exit_code = 0 if success else 1
        elif (2, 0) <= repo.package_api < (3, 0):
            repo_v2 = None
            exit_code = (
                0
                if migrate_v2_imports(repo.packages_path, repo.root, patch_file=patch_file)
                else 1
            )
        else:
            repo_v2 = None
            exit_code = 0
    finally:
        if patch_file is not None:
            patch_file.flush()
            patch_file.close()

    if patch_file_path:
        tty.warn(
            f"No changes were made to the '{repo.namespace}' repository with. Review "
            f"the changes written to {patch_file_path}. Run \n\n"
            f"    spack repo migrate --fix {args.namespace_or_path}\n\n"
            "to upgrade the repo."
        )

    elif exit_code == 1:
        tty.error(
            f"Repository '{repo.namespace}' could not be migrated to the latest Package API. "
            "Please check the error messages above."
        )

    elif isinstance(repo_v2, spack.repo.Repo):
        tty.info(
            f"Repository '{repo_v2.namespace}' was successfully migrated from "
            f"package API {repo.package_api_str} to {repo_v2.package_api_str}."
        )
        tty.warn(
            "Remove the old repository from Spack's configuration and add the new one using:\n"
            f"    spack repo remove {shlex.quote(repo.root)}\n"
            f"    spack repo add {shlex.quote(repo_v2.root)}"
        )

    else:
        tty.info(f"Repository '{repo.namespace}' was successfully migrated")

    return exit_code


def repo_set(args):
    """modify an existing repository configuration"""
    namespace = args.namespace

    # First, check if the repository exists across all scopes for validation
    all_repos: Dict[str, Any] = spack.config.get("repos", default={})

    if namespace not in all_repos:
        raise SpackError(f"No repository with namespace '{namespace}' found in configuration.")

    # Validate that it's a git repository
    if not isinstance(all_repos[namespace], dict):
        raise SpackError(
            f"Repository '{namespace}' is not a git repository. "
            "The 'set' command only works with git repositories."
        )

    # Now get the repos for the specific scope we're modifying
    scope_repos: Dict[str, Any] = spack.config.get("repos", default={}, scope=args.scope)

    updated_entry = scope_repos[namespace] if namespace in scope_repos else {}

    if args.destination:
        updated_entry["destination"] = args.destination

    if args.path:
        updated_entry["paths"] = args.path

    scope_repos[namespace] = updated_entry
    spack.config.set("repos", scope_repos, args.scope)

    tty.msg(f"Updated repo '{namespace}'")


def _iter_repos_from_descriptors(
    descriptors: spack.repo.RepoDescriptors,
) -> Generator[Tuple[str, str, Union[spack.repo.Repo, Exception, None]], None, None]:
    """Iterate through repository descriptors and yield (name, path, maybe_repo) tuples.

    Yields:
        Tuple of (config_name, path, maybe_repo) where maybe_repo is a Repo instance if it could
        be instantiated, an Exception if it could not be instantiated, or None if it was not
        initialized yet.
    """
    for name, descriptor in descriptors.items():
        descriptor.initialize(fetch=False)
        repos_for_descriptor = descriptor.construct(cache=spack.caches.MISC_CACHE)

        for path, maybe_repo in repos_for_descriptor.items():
            yield name, path, maybe_repo

        # If there are no repos, it means it's not yet cloned; yield descriptor info
        if not repos_for_descriptor and isinstance(descriptor, spack.repo.RemoteRepoDescriptor):
            yield name, descriptor.repository, None  # None indicates remote descriptor


def repo_update(args):
    """update one or more package repositories"""
    descriptors = spack.repo.RepoDescriptors.from_config(
        spack.repo.package_repository_lock(), spack.config.CONFIG
    )

    git_flags = ["commit", "tag", "branch"]
    active_flag = next((attr for attr in git_flags if getattr(args, attr)), None)
    if active_flag and len(args.names) != 1:
        raise SpackError(
            f"Unable to set --{active_flag} because more than one namespace was given."
            if len(args.names) > 1
            else f"Unable to apply --{active_flag} without a namespace"
        )

    for name in args.names:
        if name not in descriptors:
            raise SpackError(f"{name} is not a known repository name.")

        # filter descriptors when namespaces are provided as arguments
        descriptors = spack.repo.RepoDescriptors(
            {name: descriptor for name, descriptor in descriptors.items() if name in args.names}
        )

    # Get the repos for the specific scope we're modifying
    scope_repos: Dict[str, Any] = spack.config.get("repos", default={}, scope=args.scope)

    for name, descriptor in descriptors.items():
        if not isinstance(descriptor, spack.repo.RemoteRepoDescriptor):
            continue

        if active_flag:
            # update the git commit, tag, or branch of the descriptor
            setattr(descriptor, active_flag, getattr(args, active_flag))

            updated_entry = scope_repos[name] if name in scope_repos else {}

            # prune previous values of git fields
            for entry in {"commit", "tag"} - {active_flag}:
                setattr(descriptor, entry, None)
                updated_entry.pop(entry, None)

            updated_entry[active_flag] = args.commit or args.tag or args.branch
            scope_repos[name] = updated_entry

        git = spack.util.git.git(required=True)

        previous_commit = descriptor.get_commit(git=git)
        descriptor.update(git=git, remote=args.remote)
        new_commit = descriptor.get_commit(git=git)

        if previous_commit == new_commit:
            tty.msg(f"{name}: Already up to date.")
        else:
            fails = [
                r
                for r in descriptor.construct(cache=spack.caches.MISC_CACHE).values()
                if type(r) is spack.repo.BadRepoVersionError
            ]
            if fails:
                min_ver = ".".join(str(n) for n in spack.min_package_api_version)
                max_ver = ".".join(str(n) for n in spack.package_api_version)
                tty.error(
                    f"{name}: repo is too new for this version of Spack. ",
                    f"  Spack supports API v{min_ver} to v{max_ver}, but repo is {fails[0].api}",
                    "  Please upgrade Spack or revert with:\n",
                    f"       spack repo update --commit {previous_commit}\n",
                )

            else:
                tty.msg(f"{name}: Updated successfully.")

    if active_flag:
        spack.config.set("repos", scope_repos, args.scope)


def repo_show_version_updates(args):
    """show version specs that were added between two commits"""
    # Get the repository by name or path
    repo = _get_repo(args.repository)

    if repo is None:
        tty.die(f"No such repository: {args.repository}")

    # Get packages that were changed or added between the refs
    pkgs = spack.repo.get_all_package_diffs("AC", repo, args.from_ref, args.to_ref)

    # Filter out manual packages if requested
    if args.no_manual_packages:
        pkgs = {
            pkg_name
            for pkg_name in pkgs
            if not spack.repo.PATH.get_pkg_class(pkg_name).manual_download
        }

    if not pkgs:
        tty.info("No packages were added or changed between the specified refs", stream=sys.stderr)
        return 0

    # Collect version specs that were added
    specs_to_output = []

    for pkg_name in pkgs:
        pkg_cls = spack.repo.PATH.get_pkg_class(pkg_name)
        path = spack.repo.PATH.package_path(pkg_name)

        # Get all versions with checksums or commits
        version_to_checksum: Dict[StandardVersion, str] = {}
        for version in pkg_cls.versions:
            version_dict = pkg_cls.versions[version]
            if "sha256" in version_dict:
                version_to_checksum[version] = version_dict["sha256"]
            elif "commit" in version_dict:
                version_to_checksum[version] = version_dict["commit"]

        # Find versions added between the refs
        with fs.working_dir(os.path.dirname(path)):
            added_checksums = spack.ci.filter_added_checksums(
                version_to_checksum.values(), path, from_ref=args.from_ref, to_ref=args.to_ref
            )
            new_versions = [v for v, c in version_to_checksum.items() if c in added_checksums]

        # Create specs for new versions
        for version in new_versions:
            version_spec = spack.spec.Spec(pkg_name)
            version_spec.constrain(f"@={version}")
            specs_to_output.append(version_spec)

    # Filter out git versions if requested
    if args.no_git_versions:
        specs_to_output = [
            spec
            for spec in specs_to_output
            if "commit" not in spack.repo.PATH.get_pkg_class(spec.name).versions[spec.version]
        ]

    # Filter out non-redistributable packages if requested
    if args.only_redistributable:
        specs_to_output = [
            spec
            for spec in specs_to_output
            if spack.repo.PATH.get_pkg_class(spec.name).redistribute_source(spec)
        ]

    if not specs_to_output:
        tty.info("No new package versions found between the specified refs", stream=sys.stderr)
        return 0

    # Output specs one per line
    for spec in specs_to_output:
        print(spec)


def repo(parser, args):
    return {
        "create": repo_create,
        "list": repo_list,
        "ls": repo_list,
        "add": repo_add,
        "set": repo_set,
        "remove": repo_remove,
        "rm": repo_remove,
        "migrate": repo_migrate,
        "update": repo_update,
        "show-version-updates": repo_show_version_updates,
    }[args.repo_command](args)
