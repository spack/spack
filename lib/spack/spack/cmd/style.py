# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import argparse
import ast
import linecache
import os
import re
import sys
import warnings
from itertools import zip_longest
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Set, Tuple, Union

import spack.llnl.util.tty as tty
import spack.llnl.util.tty.color as color
import spack.paths
import spack.repo
import spack.util.git
import spack.util.spack_yaml
from spack.llnl.util.filesystem import working_dir
from spack.spec_parser import NAME, VERSION_LIST, SpecTokens
from spack.tokenize import Token, TokenBase, Tokenizer
from spack.util.executable import Executable, which

description = "runs source code style checks on spack"
section = "developer"
level = "long"


LINTER_EXEMPTIONS = {
    "E501": [
        re.compile(r"(ssh|https?|ftp|file)\:"),  # URLs
        re.compile(r"([\'\"])[0-9a-fA-F]{32,}\1"),  # long hex checksums
    ],
    "F403": [
        re.compile(r"^from spack\.package import \*$"),
        re.compile(r"^from spack\.package_defs import \*$"),
    ],
    "F811": [
        # Redefinitions are okay if preceded by a @when decorator
        re.compile(r"^\s*@when\(.*\)")
    ],
}
ANSI_ESCAPE = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
ERROR_START_PATTERN = re.compile(r"^([A-Z]{1,4}[0-9]{3,4})\s+")
LOCATION_PATTERN = re.compile(r"^\s*-->\s+(.+?):(\d+):\d+")
SUMMARY_PATTERN = re.compile(r"^Found \d+ errors?")


def grouper(iterable: Iterable[Any], n: int, fillvalue=None):
    """Collect data into fixed-length chunks or blocks"""
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    for group in zip_longest(*args, fillvalue=fillvalue):
        yield filter(None, group)


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

    git = spack.util.git.git(required=True)

    # ensure base is in the repo
    base_sha = git(
        "rev-parse", "--quiet", "--verify", "--revs-only", base, fail_on_error=False, output=str
    )
    if git.returncode != 0:
        tty.die(
            "This repository does not have a '%s' revision." % base,
            "spack style needs this branch to determine which files changed.",
            "Ensure that '%s' exists, or specify files to check explicitly." % base,
        )

    range = "{0}...".format(base_sha.strip())

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
        "-a", "--all", action="store_true", help="check all files, not just changed files"
    )
    subparser.add_argument(
        "-r",
        "--root-relative",
        action="store_true",
        default=False,
        help="print root-relative paths (default: cwd-relative)",
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
        help="format automatically if possible (e.g., with isort, black)",
    )
    subparser.add_argument(
        "--root", action="store", default=None, help="style check a different spack instance"
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


def cwd_relative(path: Path, root: Union[Path, str], initial_working_dir: Path) -> Path:
    """Translate prefix-relative path to current working directory-relative."""
    if path.is_absolute():
        return path
    return Path(os.path.relpath((root / path), initial_working_dir))


def rewrite_and_print_output(
    output,
    root,
    working_dir,
    root_relative,
    re_obj=re.compile(r"^(.+):([0-9]+):"),
    replacement=r"{0}:{1}:",
):
    """rewrite output with <file>:<line>: format to respect path args"""

    # print results relative to current working directory
    def translate(match):
        return replacement.format(
            cwd_relative(Path(match.group(1)), root, working_dir), *list(match.groups()[1:])
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


def print_style_header(file_list, args, tools_to_run):
    tty.msg("Running style checks on spack", "selected: " + ", ".join(tools_to_run))
    # translate modified paths to cwd_relative if needed
    paths = file_list
    if not args.root_relative:
        paths = [cwd_relative(filename, args.root, args.initial_working_dir) for filename in paths]
    tty.msg("Modified files", *[str(x) for x in paths])
    sys.stdout.flush()


def print_tool_header(tool: str):
    sys.stdout.flush()
    tty.msg("Running %s checks" % tool)
    sys.stdout.flush()


def print_tool_result(tool, returncode):
    if returncode == 0:
        color.cprint("  @g{%s checks were clean}" % tool)
    else:
        color.cprint("  @r{%s found errors}" % tool)


def _handle_special_linter_exemptions(
    output: str, root: Path, original_returncode: int
) -> Tuple[str, int]:
    """Process ruff output to exempt our specific patterns
    
    Ruff does not have the capacity to exempt certain occurances
    of a linter violation the way flake8 does, so we do it as a
    post processing step instead of during lint time.
    """
    if not output:
        return output, original_returncode

    filtered_lines = []
    current_block = []
    current_err_code = None
    current_is_exempt = False
    real_errors_count = 0

    for line in output.splitlines():
        clean_line = ANSI_ESCAPE.sub("", line)

        match_start = ERROR_START_PATTERN.match(clean_line)
        if match_start:
            if current_block and not current_is_exempt:
                filtered_lines.extend(current_block)
                real_errors_count += 1

            current_block = [line]
            current_err_code = match_start.group(1)
            current_is_exempt = False
            continue

        match_loc = LOCATION_PATTERN.match(clean_line)
        if match_loc and current_block:
            current_block.append(line)

            if current_err_code in LINTER_EXEMPTIONS:
                filepath, line_num = match_loc.groups()
                abs_fp = Path(filepath) if os.path.isabs(filepath) else (root / filepath)
                line_idx = int(line_num)
                linecache.checkcache(str(abs_fp))

                lines_to_check = [linecache.getline(str(abs_fp), line_idx)]
                if line_idx > 1:
                    lines_to_check.append(linecache.getline(str(abs_fp), line_idx - 1))

                patterns = LINTER_EXEMPTIONS[current_err_code]
                if any(p.search(text) for text in lines_to_check for p in patterns):
                    current_is_exempt = True
            continue

        if SUMMARY_PATTERN.match(clean_line):
            if current_block and not current_is_exempt:
                filtered_lines.extend(current_block)
                real_errors_count += 1
            current_block = []

            if real_errors_count > 0:
                msg = f"Found {real_errors_count} error{'s' if real_errors_count > 1 else ''}."
                filtered_lines.append(color.colorize(f"@*r{{{msg}}}"))
            continue

        if current_block:
            current_block.append(line)
        else:
            filtered_lines.append(line)

    if current_block and not current_is_exempt:
        filtered_lines.extend(current_block)
        real_errors_count += 1

    new_output = "\n".join(filtered_lines) + ("\n" if filtered_lines else "")
    new_rc = original_returncode if real_errors_count > 0 else 0
    return new_output, new_rc


@tool("ruff-check", cmd="ruff")
def ruff_check(file_list, args, repo: Optional[spack.repo.Repo] = None):
    """Run the ruff-check command. Handles config and non generic ruff argument logic"""
    cmd_args = ["--config", os.path.join(spack.paths.prefix, "pyproject.toml"), "--quiet"]
    if args.fix:
        cmd_args += ["--fix", "--no-unsafe-fixes"]
    else:
        cmd_args += ["--no-fix"]
    return run_ruff(
        file_list, "check", cmd_args, args.root, args.initial_working_dir, args.root_relative
    )


@tool("ruff-format", cmd="ruff")
def ruff_format(file_list, args, repo: Optional[spack.repo.Repo] = None):
    """Run the ruff format command"""
    cmd_args = ["--config", os.path.join(spack.paths.prefix, "pyproject.toml"), "--quiet"]
    if not args.fix:
        cmd_args += ["--check", "--diff"]
    return run_ruff(
        file_list, "format", cmd_args, args.root, args.initial_working_dir, args.root_relative
    )


def run_ruff(
    file_list: List[Path],
    cmd: str,
    args: List[str],
    root: Path,
    working_dir: Path,
    root_relative: bool,
):
    """Run the ruff tool"""
    ruff_cmd = tools[f"ruff-{cmd}"].executable
    if not ruff_cmd:
        tty.warn("Cannot execute requested tool: ruff\nCannot find tool")
        return -1

    if color.get_color_when():
        args += ("--color", "auto")
    pat = re.compile("would reformat +(.*)")
    replacement = "would reformat {0}"
    returncode = 0

    for chunk in grouper(file_list, 100):
        packed_args = (cmd,) + (*args,) + tuple([str(x) for x in chunk])
        output = ruff_cmd(*packed_args, fail_on_error=False, output=str, error=str)
        chunk_returncode = ruff_cmd.returncode
        if cmd == "check" and output:
            output, chunk_returncode = _handle_special_linter_exemptions(
                output, root, chunk_returncode
            )

        returncode |= chunk_returncode
        rewrite_and_print_output(output, root, working_dir, root_relative, pat, replacement)

    print_tool_result(f"ruff-{cmd}", returncode)
    return returncode


@tool("mypy")
def run_mypy(file_list, args):
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
    mypy_arg_sets = [common_mypy_args + ["--package", "spack", "--package", "llnl"]]
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
    working_dir: Path,
    out=sys.stdout,
):
    if sys.version_info < (3, 9):
        print("import check requires Python 3.9 or later")
        return 0

    is_use = re.compile(r"(?<!from )(?<!import )spack\.[a-zA-Z0-9_\.]+")

    exit_code = 0

    for file in file_list:
        to_add: Set[str] = set()
        to_remove: List[str] = []

        pretty_path = file if root_relative else cwd_relative(file, root, working_dir)

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
def run_import_check(file_list, args):
    exit_code = _run_import_check(
        file_list,
        fix=args.fix,
        root_relative=args.root_relative,
        root=args.root,
        working_dir=args.initial_working_dir,
    )
    print_tool_result("import", exit_code)
    return exit_code


def validate_toolset(arg_value):
    """Validate ``--tool`` and ``--skip`` arguments (sets of optionally comma-separated tools)."""
    tools = set(",".join(arg_value).split(","))  # allow args like 'isort,flake8'
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


IS_PROBABLY_COMPILER = re.compile(r"%[a-zA-Z_][a-zA-Z0-9\-]")


class _LegacySpecTokens(TokenBase):
    """Reconstructs the tokens for previous specs, so we can reuse code to rotate them"""

    # Dependency
    START_EDGE_PROPERTIES = r"(?:\^\[)"
    END_EDGE_PROPERTIES = r"(?:\])"
    DEPENDENCY = r"(?:\^)"
    # Version
    VERSION_HASH_PAIR = SpecTokens.VERSION_HASH_PAIR.regex
    GIT_VERSION = SpecTokens.GIT_VERSION.regex
    VERSION = SpecTokens.VERSION.regex
    # Variants
    PROPAGATED_BOOL_VARIANT = SpecTokens.PROPAGATED_BOOL_VARIANT.regex
    BOOL_VARIANT = SpecTokens.BOOL_VARIANT.regex
    PROPAGATED_KEY_VALUE_PAIR = SpecTokens.PROPAGATED_KEY_VALUE_PAIR.regex
    KEY_VALUE_PAIR = SpecTokens.KEY_VALUE_PAIR.regex
    # Compilers
    COMPILER_AND_VERSION = rf"(?:%\s*(?:{NAME})(?:[\s]*)@\s*(?:{VERSION_LIST}))"
    COMPILER = rf"(?:%\s*(?:{NAME}))"
    # FILENAME
    FILENAME = SpecTokens.FILENAME.regex
    # Package name
    FULLY_QUALIFIED_PACKAGE_NAME = SpecTokens.FULLY_QUALIFIED_PACKAGE_NAME.regex
    UNQUALIFIED_PACKAGE_NAME = SpecTokens.UNQUALIFIED_PACKAGE_NAME.regex
    # DAG hash
    DAG_HASH = SpecTokens.DAG_HASH.regex
    # White spaces
    WS = SpecTokens.WS.regex
    # Unexpected character(s)
    UNEXPECTED = SpecTokens.UNEXPECTED.regex


def _spec_str_reorder_compiler(idx: int, blocks: List[List[Token]]) -> None:
    # only move the compiler to the back if it exists and is not already at the end
    if not 0 <= idx < len(blocks) - 1:
        return
    # if there's only whitespace after the compiler, don't move it
    if all(token.kind == _LegacySpecTokens.WS for block in blocks[idx + 1 :] for token in block):
        return
    # rotate left and always add at least one WS token between compiler and previous token
    compiler_block = blocks.pop(idx)
    if compiler_block[0].kind != _LegacySpecTokens.WS:
        compiler_block.insert(0, Token(_LegacySpecTokens.WS, " "))
    # delete the WS tokens from the new first block if it was at the very start, to prevent leading
    # WS tokens.
    while idx == 0 and blocks[0][0].kind == _LegacySpecTokens.WS:
        blocks[0].pop(0)
    blocks.append(compiler_block)


def _spec_str_format(spec_str: str) -> Optional[str]:
    """Given any string, try to parse as spec string, and rotate the compiler token to the end
    of each spec instance. Returns the formatted string if it was changed, otherwise None."""
    # We parse blocks of tokens that include leading whitespace, and move the compiler block to
    # the end when we hit a dependency ^... or the end of a string.
    # [@3.1][ +foo][ +bar][ %gcc@3.1][ +baz]
    # [@3.1][ +foo][ +bar][ +baz][ %gcc@3.1]

    current_block: List[Token] = []
    blocks: List[List[Token]] = []
    compiler_block_idx = -1
    in_edge_attr = False

    legacy_tokenizer = Tokenizer(_LegacySpecTokens)

    for token in legacy_tokenizer.tokenize(spec_str):
        if token.kind == _LegacySpecTokens.UNEXPECTED:
            # parsing error, we cannot fix this string.
            return None
        elif token.kind in (_LegacySpecTokens.COMPILER, _LegacySpecTokens.COMPILER_AND_VERSION):
            # multiple compilers are not supported in Spack v0.x, so early return
            if compiler_block_idx != -1:
                return None
            current_block.append(token)
            blocks.append(current_block)
            current_block = []
            compiler_block_idx = len(blocks) - 1
        elif token.kind in (
            _LegacySpecTokens.START_EDGE_PROPERTIES,
            _LegacySpecTokens.DEPENDENCY,
            _LegacySpecTokens.UNQUALIFIED_PACKAGE_NAME,
            _LegacySpecTokens.FULLY_QUALIFIED_PACKAGE_NAME,
        ):
            _spec_str_reorder_compiler(compiler_block_idx, blocks)
            compiler_block_idx = -1
            if token.kind == _LegacySpecTokens.START_EDGE_PROPERTIES:
                in_edge_attr = True
            current_block.append(token)
            blocks.append(current_block)
            current_block = []
        elif token.kind == _LegacySpecTokens.END_EDGE_PROPERTIES:
            in_edge_attr = False
            current_block.append(token)
            blocks.append(current_block)
            current_block = []
        elif in_edge_attr:
            current_block.append(token)
        elif token.kind in (
            _LegacySpecTokens.VERSION_HASH_PAIR,
            _LegacySpecTokens.GIT_VERSION,
            _LegacySpecTokens.VERSION,
            _LegacySpecTokens.PROPAGATED_BOOL_VARIANT,
            _LegacySpecTokens.BOOL_VARIANT,
            _LegacySpecTokens.PROPAGATED_KEY_VALUE_PAIR,
            _LegacySpecTokens.KEY_VALUE_PAIR,
            _LegacySpecTokens.DAG_HASH,
        ):
            current_block.append(token)
            blocks.append(current_block)
            current_block = []
        elif token.kind == _LegacySpecTokens.WS:
            current_block.append(token)
        else:
            raise ValueError(f"unexpected token {token}")

    if current_block:
        blocks.append(current_block)
    _spec_str_reorder_compiler(compiler_block_idx, blocks)

    new_spec_str = "".join(token.value for block in blocks for token in block)
    return new_spec_str if spec_str != new_spec_str else None


SpecStrHandler = Callable[[str, int, int, str, str], None]


def _spec_str_default_handler(path: str, line: int, col: int, old: str, new: str):
    """A SpecStrHandler that prints formatted spec strings and their locations."""
    print(f"{path}:{line}:{col}: `{old}` -> `{new}`")


def _spec_str_fix_handler(path: str, line: int, col: int, old: str, new: str):
    """A SpecStrHandler that updates formatted spec strings in files."""
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    new_line = lines[line - 1].replace(old, new)
    if new_line == lines[line - 1]:
        tty.warn(f"{path}:{line}:{col}: could not apply fix: `{old}` -> `{new}`")
        return
    lines[line - 1] = new_line
    print(f"{path}:{line}:{col}: fixed `{old}` -> `{new}`")
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)


def _spec_str_ast(path: str, tree: ast.AST, handler: SpecStrHandler) -> None:
    """Walk the AST of a Python file and apply handler to formatted spec strings."""
    for node in ast.walk(tree):
        if sys.version_info >= (3, 8):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                current_str = node.value
            else:
                continue
        elif isinstance(node, ast.Str):
            current_str = node.s
        else:
            continue
        if not IS_PROBABLY_COMPILER.search(current_str):
            continue
        new = _spec_str_format(current_str)
        if new is not None:
            handler(path, node.lineno, node.col_offset, current_str, new)


def _spec_str_json_and_yaml(path: str, data: dict, handler: SpecStrHandler) -> None:
    """Walk a YAML or JSON data structure and apply handler to formatted spec strings."""
    queue = [data]
    seen = set()

    while queue:
        current = queue.pop(0)
        if id(current) in seen:
            continue
        seen.add(id(current))
        if isinstance(current, dict):
            queue.extend(current.values())
            queue.extend(current.keys())
        elif isinstance(current, list):
            queue.extend(current)
        elif isinstance(current, str) and IS_PROBABLY_COMPILER.search(current):
            new = _spec_str_format(current)
            if new is not None:
                mark = getattr(current, "_start_mark", None)
                if mark:
                    line, col = mark.line + 1, mark.column + 1
                else:
                    line, col = 0, 0
                handler(path, line, col, current, new)


def _check_spec_strings(
    paths: List[str], handler: SpecStrHandler = _spec_str_default_handler
) -> None:
    """Open Python, JSON and YAML files, and format their string literals that look like spec
    strings. A handler is called for each formatting, which can be used to print or apply fixes."""
    for path in paths:
        is_json_or_yaml = path.endswith(".json") or path.endswith(".yaml") or path.endswith(".yml")
        is_python = path.endswith(".py")
        if not is_json_or_yaml and not is_python:
            continue

        try:
            with open(path, "r", encoding="utf-8") as f:
                # skip files that are likely too large to be user code or config
                if os.fstat(f.fileno()).st_size > 1024 * 1024:
                    warnings.warn(f"skipping {path}: too large.")
                    continue
                if is_json_or_yaml:
                    _spec_str_json_and_yaml(path, spack.util.spack_yaml.load_config(f), handler)
                elif is_python:
                    _spec_str_ast(path, ast.parse(f.read()), handler)
        except (OSError, spack.util.spack_yaml.SpackYAMLError, SyntaxError, ValueError):
            warnings.warn(f"skipping {path}")
            continue


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

    # validate spack root if the user provided one
    args.root = Path(args.root).resolve() if args.root else Path(spack.paths.prefix)
    spack_script = args.root / "bin" / "spack"
    if not spack_script.exists():
        tty.die("This does not look like a valid spack root.", "No such file: '%s'" % spack_script)

    def prefix_relative(path: Union[Path, str]) -> Path:
        return Path(os.path.relpath(os.path.abspath(path), args.root))

    file_list = [prefix_relative(file) for file in args.files]

    # process --tool and --skip arguments
    selected = set(tool_names)
    if args.tool is not None:
        selected = validate_toolset(args.tool)
    if args.skip is not None:
        selected -= validate_toolset(args.skip)

    if not selected:
        tty.msg("Nothing to run.")
        return

    tools_to_run = [t for t in tool_names if t in selected]
    if missing_tools(tools_to_run):
        _bootstrap_dev_dependencies()

    return_code = 0
    with working_dir(str(args.root)):
        if not file_list:
            file_list = changed_files(args.base, args.untracked, args.all)
        print_style_header(file_list, args, tools_to_run)
        for tool_name in tools_to_run:
            tool = tools[tool_name]
            print_tool_header(tool_name)
            return_code |= tool.fun(file_list, args)
    if return_code == 0:
        tty.msg(color.colorize("@*{spack style checks were clean}"))
    else:
        tty.error(color.colorize("@*{spack style found errors}"))

    return return_code
