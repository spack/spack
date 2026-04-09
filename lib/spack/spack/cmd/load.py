# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import glob
import os
import sys

import spack.cmd
import spack.cmd.common
import spack.environment as ev
import spack.hooks.generate_spec_scripts as generate_script
import spack.repo
import spack.user_environment as uenv
from spack.cmd.common import arguments

description = "add package to the user environment"
section = "user environment"
level = "short"


def setup_parser(subparser: argparse.ArgumentParser) -> None:
    """Parser is only constructed so that this prints a nice help
    message with -h."""
    arguments.add_common_arguments(subparser, ["constraint"])

    shells = subparser.add_mutually_exclusive_group()
    shells.add_argument(
        "--sh",
        action="store_const",
        dest="shell",
        const="sh",
        help="print sh commands to load the package",
    )
    shells.add_argument(
        "--csh",
        action="store_const",
        dest="shell",
        const="csh",
        help="print csh commands to load the package",
    )
    shells.add_argument(
        "--fish",
        action="store_const",
        dest="shell",
        const="fish",
        help="print fish commands to load the package",
    )
    shells.add_argument(
        "--bat",
        action="store_const",
        dest="shell",
        const="bat",
        help="print bat commands to load the package",
    )
    shells.add_argument(
        "--pwsh",
        action="store_const",
        dest="shell",
        const="pwsh",
        help="print pwsh commands to load the package",
    )

    subparser.add_argument(
        "--first",
        action="store_true",
        default=False,
        dest="load_first",
        help="load the first match if multiple packages match the spec",
    )

    subparser.add_argument(
        "--list",
        action="store_true",
        default=False,
        help="show loaded packages: same as ``spack find --loaded``",
    )


def _get_environment_modifications(spec, shell, repo) -> str:
    """Find the environment modifcations for spec

    Args:
        spec: the spec that needs environment modifications
        shell: user's shell
        repo: optional repo to use when spec is not in builtin repo
    """

    # TODO: if spec is not in builtin repo, pass cached repo or repo path

    env_mod = uenv.environment_modifications_for_specs(spec, repo=repo)
    env_mod.prepend_path(uenv.spack_loaded_hashes_var, spec.dag_hash())

    return env_mod.shell_modifications(shell)


def _make_repo_path(root):
    """Make a RepoPath from the repo subdirectories in an environment."""
    repos = (
        spack.repo.from_path(os.path.dirname(p))
        for p in glob.glob(os.path.join(root, "**", "repo.yaml"), recursive=True)
    )
    return spack.repo.RepoPath(*repos)


def load(parser, args):
    env = ev.active_environment()

    if args.list:
        results = spack.cmd.filter_loaded_specs(args.specs())
        if sys.stdout.isatty():
            spack.cmd.print_how_many_pkgs(results, "loaded")
        spack.cmd.display_specs(results)
        return

    constraint_specs = spack.cmd.parse_specs(args.constraint)
    specs = [
        spack.cmd.disambiguate_spec(spec, env, first=args.load_first) for spec in constraint_specs
    ]

    if not args.shell:
        specs_str = " ".join(str(s) for s in constraint_specs) or "SPECS"
        spack.cmd.common.shell_init_instructions(
            "spack load", f"    eval `spack load {{sh_arg}} {specs_str}`"
        )
        return 1

    shell = args.shell if args.shell else os.environ.get("SPACK_SHELL")

    for spec in specs:
        commands = ""
        if spec.external:
            commands = _get_environment_modifications(spec, shell)
        else:
            load_script_path = generate_script.path_to_load_shell_script(spec, shell)

            if not os.path.isfile(load_script_path):
                try:
                    repo_path = _make_repo_path(os.path.join(spec.prefix, ".spack"))
                    cached_repo = repo_path if repo_path.repos else None
                    mods = _get_environment_modifications(spec, shell, cached_repo)

                    generate_script.write_spec_scripts(load_script_path, mods)
                except OSError as e:
                    raise OSError(f"Error writing to {load_script_path}\n{e}")

            source = "." if shell == "sh" else "source"
            commands = f"{source} {load_script_path}"

        print(f"{commands}")
