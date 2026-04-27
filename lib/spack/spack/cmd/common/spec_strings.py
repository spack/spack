# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import ast
import os
import re
import sys
import warnings
from typing import Callable, List, Optional

import spack.llnl.util.tty as tty
import spack.util.spack_yaml
from spack.spec_parser import NAME, VERSION_LIST, SpecTokens
from spack.tokenize import Token, TokenBase, Tokenizer

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
