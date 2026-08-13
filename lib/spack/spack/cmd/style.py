# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import argparse
import ast
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Union

import spack.paths
import spack.repo
import spack.util.git
from spack.cmd.common.spec_strings import (
    _check_spec_strings,
    _spec_str_default_handler,
    _spec_str_fix_handler,
)
from spack.util import tty
from spack.util.executable import Executable, which
from spack.util.filesystem import working_dir
from spack.util.lang import memoized
from spack.util.tty import color

description = "runs source code style checks on spack"
section = "developer"
level = "long"

#: List of paths to exclude from checks -- relative to spack root
exclude_paths = [os.path.relpath(spack.paths.vendor_path, spack.paths.prefix)]

#: Order in which tools should be run.
#: The list maps an executable name to a method to ensure the tool is
#: bootstrapped or present in the environment.
tool_names = ["import", "ruff-format", "ruff-check", "mypy"]

#: warnings to ignore in mypy
mypy_ignores = [
    # same as `disable_error_code = "annotation-unchecked"` in pyproject.toml, which
    # doesn't exist in mypy 0.971 for Python 3.6
    "[annotation-unchecked]"
]

DEFAULT_REPO = "builtin"


#: decorator for adding tools to the list
class tool:
    def __init__(
        self, name: str, cmd: Optional[str] = None, required: bool = False, external: bool = True
    ) -> None:
        self.name = name
        self.external = external
        self.required = required
        self.cmd = cmd if cmd else name

    def __call__(self, fun):
        self.fun = fun
        tools[self.name] = self
        return fun

    @property
    def installed(self) -> bool:
        return bool(which(self.cmd)) if self.external else True

    @property
    def executable(self) -> Optional[Executable]:
        return which(self.cmd) if self.external else None


#: tools we run in spack style
tools: Dict[str, tool] = {}


@memoized
def get_git() -> Executable:
    return spack.util.git.git(required=True)


def get_repo_git_root(repo: spack.repo.Repo) -> Optional[Path]:
    """Root of the git checkout holding ``repo``, or None if it isn't in one."""
    git = get_git()
    with working_dir(repo.root):
        git_root = git("rev-parse", "--show-toplevel", fail_on_error=False, output=str, error=str)
    if git.returncode != 0:
        tty.debug(f"{repo.root} is not in a git repository")
        return None
    return Path(git_root.strip())


def base_sha(root: str, base: str) -> Optional[str]:
    """SHA that ``base`` resolves to in the repository at ``root``, if it exists there."""
    git = get_git()
    with working_dir(root):
        sha = git(
            "rev-parse",
            "--quiet",
            "--verify",
            "--revs-only",
            base,
            fail_on_error=False,
            output=str,
        )
    return sha.strip() if git.returncode == 0 else None


def changed_files_repo(
    repo: spack.repo.Repo, base="develop", untracked=True, all_files=False
) -> List[Path]:
    """Get the list of changed files in a package repo, as absolute paths.

    Package repos aren't necessarily git checkouts, and the ones that are don't necessarily
    have a ``base`` revision, so fall back to every Python file in the repo.

    Arguments:
        repo: repo object for which to determine changed files
        base: name of base branch to evaluate differences with
        untracked: include untracked files in the list
        all_files: list all files in the repo
    """
    root = get_repo_git_root(repo)
    if root and base_sha(str(root), base):
        # The repo may be a subdirectory of its checkout, so only keep files below it.
        # git reports a physical path, so resolve the repo's too or a symlinked repo root
        # yields a "../" prefix that matches nothing and silently hides every file.
        prefix = Path(os.path.relpath(os.path.realpath(repo.root), os.path.realpath(root)))
        files = changed_files(root=str(root), base=base, untracked=untracked, all_files=all_files)
        return [root / f for f in files if prefix in f.parents]
    return list(Path(repo.root).rglob("*.py"))


def changed_files(base="develop", untracked=True, all_files=False, root=None) -> List[Path]:
    """Get list of changed files in the Spack repository.

    Arguments:
        base (str): name of base branch to evaluate differences with.
        untracked (bool): include untracked files in the list.
        all_files (bool): list all files in the repository.
        root (str): use this directory instead of the Spack prefix.
    """
    if root is None:
        root = spack.paths.prefix

    git = get_git()
    sha = base_sha(str(root), base)
    if sha is None:
        tty.die(
            "This repository does not have a '%s' revision." % base,
            "spack style needs this branch to determine which files changed.",
            "Ensure that '%s' exists, or specify files to check explicitly." % base,
        )

    with working_dir(root):
        range = "{0}...".format(sha)

        git_args = [
            # Add changed files committed since branching off of develop
            ["diff", "--name-only", "--diff-filter=ACMR", range],
            # Add changed files that have been staged but not yet committed
            ["diff", "--name-only", "--diff-filter=ACMR", "--cached"],
            # Add changed files that are unstaged
            ["diff", "--name-only", "--diff-filter=ACMR"],
        ]

        # Add new files that are untracked
        if untracked:
            git_args.append(["ls-files", "--exclude-standard", "--other"])

        # add everything if the user asked for it
        if all_files:
            git_args.append(["ls-files", "--exclude-standard"])

        excludes = [os.path.realpath(os.path.join(root, f)) for f in exclude_paths]
        changed = set()

        for arg_list in git_args:
            files = git(*arg_list, output=str).split("\n")

            for f in files:
                # Ignore non-Python files
                if not (f.endswith(".py") or f == "bin/spack"):
                    continue

                # Ignore files in the exclude locations
                if any(os.path.realpath(f).startswith(e) for e in excludes):
                    continue

                changed.add(Path(f))

        return sorted(changed)


def setup_parser(subparser: argparse.ArgumentParser) -> None:
    subparser.add_argument(
        "-b",
        "--base",
        action="store",
        default="develop",
        help="branch to compare against to determine changed files (default: develop)",
    )
    subparser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="check all files, not just changed files (applies only to Import Check)",
    )
    subparser.add_argument(
        "-r",
        "--root-relative",
        action="store_true",
        default=False,
        help="print root-relative paths (default: cwd-relative; --repo is always repo-relative)",
    )
    subparser.add_argument(
        "-U",
        "--no-untracked",
        dest="untracked",
        action="store_false",
        default=True,
        help="exclude untracked files from checks",
    )
    subparser.add_argument(
        "-f",
        "--fix",
        action="store_true",
        default=False,
        help="format and fix issues automatically (e.g., with ruff)",
    )
    subparser.add_argument(
        "--root", action="store", default=None, help="style check a different spack instance"
    )
    subparser.add_argument(
        "--repo",
        nargs="?",
        const=DEFAULT_REPO,
        default=None,
        metavar="NAMESPACE",
        help="check a package repo instead of core spack, by namespace"
        " (default: %s)" % DEFAULT_REPO,
    )

    tool_group = subparser.add_mutually_exclusive_group()
    tool_group.add_argument(
        "-t",
        "--tool",
        action="append",
        help="specify which tools to run (default: %s)" % ", ".join(tool_names),
    )
    tool_group.add_argument(
        "-s",
        "--skip",
        metavar="TOOL",
        action="append",
        help="specify tools to skip (choose from %s)" % ", ".join(tool_names),
    )
    subparser.add_argument(
        "--spec-strings",
        action="store_true",
        help="upgrade spec strings in Python, JSON and YAML files for compatibility with Spack "
        "v1.0 and v0.x. Example: spack style ``--spec-strings $(git ls-files)``. Note: must be "
        "used only on specs from spack v0.X.",
    )

    subparser.add_argument("files", nargs=argparse.REMAINDER, help="specific files to check")


def cwd_relative(path: Path, root: Union[Path, str], report_dir: Union[Path, str]) -> Path:
    """Translate a root-relative path to one relative to ``report_dir``.

    ``report_dir`` is the initial working directory for core spack, and the repo root when
    checking a package repo. Absolute paths are already unambiguous, so they pass through.
    """
    if path.is_absolute():
        return path
    return Path(os.path.relpath((root / path), report_dir))


def rewrite_and_print_output(
    output,
    root,
    report_dir,
    root_relative,
    re_obj=re.compile(r"^(.+):([0-9]+):"),
    replacement=r"{0}:{1}:",
):
    """rewrite output with <file>:<line>: format to respect path args"""

    # print results relative to the reporting directory
    def translate(match):
        return replacement.format(
            cwd_relative(Path(match.group(1)), root, report_dir), *list(match.groups()[1:])
        )

    for line in output.split("\n"):
        if not line:
            continue
        if any(ignore in line for ignore in mypy_ignores):
            # some mypy annotations can't be disabled in older mypys (e.g. .971, which
            # is the only mypy that supports python 3.6), so we filter them here.
            continue
        if not root_relative and re_obj:
            line = re_obj.sub(translate, line)
        print(line)


def print_tool_result(tool, returncode):
    if returncode == 0:
        color.cprint("  @g{%s checks were clean}" % tool)
    else:
        color.cprint("  @r{%s found errors}" % tool)


def setup_baseline_ruff_config(args, repo: Optional[spack.repo.Repo] = None):
    """Common ruff args, the directory to run in, and the one to report paths relative to."""
    if repo:
        # Let ruff locate a package repo's config itself, by searching up from the files it
        # checks, as it would for any other project. Passing --config would override that, and
        # picking the file ourselves would mean reimplementing ruff's rules for which files
        # count -- a pyproject.toml only configures ruff if it has a [tool.ruff] section.
        # A repo inside a spack prefix finds spack's config this way; one outside with no
        # config of its own gets ruff's defaults, same as running ruff there by hand.
        return ["--quiet"], Path(repo.root), Path(repo.root)
    config = os.path.join(spack.paths.prefix, "pyproject.toml")
    return ["--config", config, "--quiet"], args.root, args.initial_working_dir


@tool("ruff-check", cmd="ruff")
def ruff_check(file_list, args, repo: Optional[spack.repo.Repo] = None):
    """Run the ruff-check command. Handles config and non generic ruff argument logic"""
    cmd_args, root, report_dir = setup_baseline_ruff_config(args, repo)
    if args.fix:
        cmd_args += ["--fix", "--no-unsafe-fixes"]
    else:
        cmd_args += ["--no-fix"]
    return run_ruff(file_list, "check", cmd_args, root, report_dir, args.root_relative)


@tool("ruff-format", cmd="ruff")
def ruff_format(file_list, args, repo: Optional[spack.repo.Repo] = None):
    """Run the ruff format command"""
    cmd_args, root, report_dir = setup_baseline_ruff_config(args, repo)
    if not args.fix:
        cmd_args += ["--check", "--diff"]
    return run_ruff(file_list, "format", cmd_args, root, report_dir, args.root_relative)


def run_ruff(
    file_list: List[Path],
    cmd: str,
    args: List[str],
    root: Union[Path, str],
    report_dir: Union[Path, str],
    root_relative: bool,
):
    """Run the ruff tool"""
    ruff_cmd = tools[f"ruff-{cmd}"].executable
    if not ruff_cmd:
        tty.warn("Cannot execute requested tool: ruff\nCannot find tool")
        return -1

    files = (str(x) for x in file_list)
    if color.get_color_when():
        args += ("--color", "auto")
    pat = re.compile("would reformat +(.*)")
    replacement = "would reformat {0}"

    packed_args = (cmd,) + (*args,) + tuple(files)
    with working_dir(str(root)):
        output = ruff_cmd(*packed_args, fail_on_error=False, output=str, error=str)
        returncode = ruff_cmd.returncode
    rewrite_and_print_output(output, root, report_dir, root_relative, pat, replacement)

    print_tool_result(f"ruff-{cmd}", returncode)
    return returncode


@tool("mypy")
def run_mypy(file_list, args, repo: Optional[spack.repo.Repo] = None):
    # ``repo`` is accepted for a uniform tool signature but unused: mypy type checks an
    # importable spack, so ``style()`` drops it when checking a package repo.
    mypy_cmd = tools["mypy"].executable
    if not mypy_cmd:
        tty.warn("Cannot execute requested tool: mypy\nCannot find tool")
        return -1
    # always run with config from running spack prefix
    common_mypy_args = [
        "--config-file",
        os.path.join(spack.paths.prefix, "pyproject.toml"),
        "--show-error-codes",
    ]
    mypy_arg_sets = [common_mypy_args + ["--package", "spack"]]
    if "SPACK_MYPY_CHECK_PACKAGES" in os.environ:
        mypy_arg_sets.append(
            common_mypy_args + ["--package", "packages", "--disable-error-code", "no-redef"]
        )

    returncode = 0
    for mypy_args in mypy_arg_sets:
        output = mypy_cmd(*mypy_args, fail_on_error=False, output=str)
        returncode |= mypy_cmd.returncode

        rewrite_and_print_output(output, args.root, args.initial_working_dir, args.root_relative)

    print_tool_result("mypy", returncode)
    return returncode


def _module_part(root: Path, expr: str):
    parts = expr.split(".")
    # spack.pkg is for repositories, don't try to resolve it here.
    if expr.startswith(spack.repo.PKG_MODULE_PREFIX_V1) or expr == "spack.pkg":
        return None
    while parts:
        f1 = (root / "lib" / "spack").joinpath(*parts).with_suffix(".py")
        f2 = (root / "lib" / "spack").joinpath(*parts, "__init__.py")

        if (
            f1.exists()
            # ensure case sensitive match
            and any(p.name == f"{parts[-1]}.py" for p in f1.parent.iterdir())
            or f2.exists()
        ):
            return ".".join(parts)
        parts.pop()
    return None


def _run_import_check(
    file_list: List[Path],
    *,
    fix: bool,
    root_relative: bool,
    root: Path,
    report_dir: Path,
    out=sys.stdout,
    base="develop",
    untracked=True,
    all=False,
    repo: Optional[spack.repo.Repo] = None,
):
    if sys.version_info < (3, 9):
        print("import check requires Python 3.9 or later")
        return 0

    is_use = re.compile(r"(?<!from )(?<!import )spack\.[a-zA-Z0-9_\.]+")

    exit_code = 0
    files = file_list or (
        changed_files_repo(repo, base=base, untracked=untracked, all_files=all)
        if repo
        else changed_files(root=root, base=base, untracked=untracked, all_files=all)
    )
    for file in files:
        to_add: Set[str] = set()
        to_remove: List[str] = []

        if repo:
            # repo file paths are absolute; report them relative to the repo, like the header
            pretty_path = Path(os.path.relpath(file, repo.root))
        elif root_relative:
            pretty_path = file
        else:
            pretty_path = cwd_relative(file, root, report_dir)

        try:
            with open(file, "r", encoding="utf-8") as f:
                contents = f.read()
            parsed = ast.parse(contents)
        except Exception:
            exit_code = 1
            print(f"{pretty_path}: could not parse", file=out)
            continue

        imported_modules: Set[str] = set()
        potential_redundant_imports: List[str] = []

        for node in ast.walk(parsed):
            # Clear strings to make sure usages in strings are not counted
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                node.value = ""
            elif isinstance(node, ast.Import):
                # Track `import ...` without aliases
                for name in node.names:
                    if name.asname is None:
                        imported_modules.add(name.name)

                # Track top-level imports for redundancy check
                if (
                    node.col_offset == 0
                    and len(node.names) == 1
                    and node.names[0].asname is None
                    and node.names[0].name.startswith("spack.")
                ):
                    potential_redundant_imports.append(node.names[0].name)

        # Convert back to code after clearing strings
        filtered_contents = ast.unparse(parsed)  # novermin

        # Check for redundant imports
        for module_name in potential_redundant_imports:
            usage_regex = rf"(?<!from )(?<!import ){re.escape(module_name)}(?!\w)"
            if re.search(usage_regex, filtered_contents):
                continue
            statement = f"import {module_name}"
            # redundant imports followed by a `# comment` are ignored, cause there can be
            # legitimate reason to import a module: execute module scope init code, or to deal
            # with circular imports.
            if re.search(rf"^{re.escape(statement)}$", contents, re.MULTILINE):
                to_remove.append(statement)
                exit_code = 1
                print(f"{pretty_path}: redundant import: {module_name}", file=out)

        # Check for missing imports
        for m in is_use.finditer(filtered_contents):
            module = _module_part(root, m.group(0))
            if not module or module in to_add:
                continue
            if module in imported_modules:
                continue
            to_add.add(module)
            exit_code = 1
            print(f"{pretty_path}: missing import: {module} ({m.group(0)})", file=out)

        if not fix or not to_add and not to_remove:
            continue

        with open(file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        if to_add:
            # insert missing imports before the first import, delegate ordering to isort
            for node in parsed.body:
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    first_line = node.lineno
                    break
            else:
                print(f"{pretty_path}: could not fix", file=out)
                continue
            lines.insert(first_line, "\n".join(f"import {x}" for x in to_add) + "\n")

        new_contents = "".join(lines)

        # remove redundant imports
        for statement in to_remove:
            new_contents = new_contents.replace(f"{statement}\n", "")

        with open(file, "w", encoding="utf-8") as f:
            f.write(new_contents)

    return exit_code


@tool("import", external=False)
def run_import_check(file_list, args, repo: Optional[spack.repo.Repo] = None):
    exit_code = _run_import_check(
        file_list,
        fix=args.fix,
        root_relative=args.root_relative,
        # ``root`` locates the spack modules imports are resolved against, so it stays the
        # spack root even when the files being checked live in a package repo.
        root=args.root,
        report_dir=args.initial_working_dir,
        base=args.base,
        untracked=args.untracked,
        all=args.all,
        repo=repo,
    )
    print_tool_result("import", exit_code)
    return exit_code


def print_style_header(
    file_list: List[Path], args, tools_to_run, repo: Optional[spack.repo.Repo] = None
):
    target = f"spack repository {repo.namespace}" if repo else "spack"
    tty.msg(f"Running style checks on {target}", "selected: " + ", ".join(tools_to_run))
    if file_list:
        if repo:
            # repo files are absolute; report them relative to the repo
            paths = [os.path.relpath(f, repo.root) for f in file_list]
        elif args.root_relative:
            paths = [str(f) for f in file_list]
        else:
            paths = [str(cwd_relative(f, args.root, args.initial_working_dir)) for f in file_list]
        tty.msg("Checking Files:", *paths)
    sys.stdout.flush()


def validate_toolset(arg_value):
    """Validate ``--tool`` and ``--skip`` arguments (sets of optionally comma-separated tools)."""
    tools = set(",".join(arg_value).split(","))  # allow args like 'ruff-check,mypy'
    for tool in tools:
        if tool not in tool_names:
            tty.die("Invalid tool: '%s'" % tool, "Choose from: %s" % ", ".join(tool_names))
    return tools


def missing_tools(tools_to_run: List[str]) -> List[str]:
    return [t for t in tools_to_run if not tools[t].installed]


def _bootstrap_dev_dependencies():
    import spack.bootstrap

    with spack.bootstrap.ensure_bootstrap_configuration():
        spack.bootstrap.ensure_environment_dependencies()


def style(parser, args):
    if args.spec_strings:
        if not args.files:
            tty.die("No files provided to check spec strings.")
        handler = _spec_str_fix_handler if args.fix else _spec_str_default_handler
        return _check_spec_strings(args.files, handler)

    # save initial working directory for relativizing paths later
    args.initial_working_dir = Path.cwd()

    # ensure that the config files we need actually exist in the spack prefix.
    # assertions b/c users should not ever see these errors -- they're checked in CI.
    assert (Path(spack.paths.prefix) / "pyproject.toml").is_file()

    # a package repo is looked up by namespace in the running spack's configuration, so it
    # can't be combined with a --root pointing at a different spack instance. Everything
    # about the repo -- where its files, config, and git checkout live -- comes from spack.
    if args.repo and args.root:
        tty.die("--repo and --root are mutually exclusive.")
    repo = spack.repo.PATH.get_repo(args.repo) if args.repo else None

    # validate spack root if the user provided one
    args.root = Path(args.root).resolve() if args.root else Path(spack.paths.prefix)
    spack_script = args.root / "bin" / "spack"
    if not spack_script.exists():
        tty.die("This does not look like a valid spack root.", "No such file: '%s'" % spack_script)

    def prefix_relative(path: Union[Path, str]) -> Path:
        return Path(os.path.relpath(os.path.abspath(os.path.realpath(path)), args.root))

    # core files are checked from the spack root; repo files are checked where they live
    file_list = [Path(os.path.realpath(f)) if repo else prefix_relative(f) for f in args.files]

    # process --tool and --skip arguments
    selected = set(tool_names)
    if args.tool is not None:
        selected = validate_toolset(args.tool)
    if args.skip is not None:
        selected -= validate_toolset(args.skip)
    if repo:
        # mypy type checks an importable spack, not a tree of package recipes
        selected.discard("mypy")

    if not selected:
        tty.msg("Nothing to run.")
        return

    tools_to_run = [t for t in tool_names if t in selected]
    if missing_tools(tools_to_run):
        _bootstrap_dev_dependencies()

    return_code = 0
    with working_dir(str(args.root)):
        print_style_header(file_list, args, tools_to_run, repo)
        for tool_name in tools_to_run:
            tool = tools[tool_name]
            tty.msg(f"Running {tool.name} checks")
            return_code |= tool.fun(file_list, args, repo)

    if return_code == 0:
        tty.msg(color.colorize("@*{spack style checks were clean}"))
    else:
        tty.error(color.colorize("@*{spack style found errors}"))

    return return_code
