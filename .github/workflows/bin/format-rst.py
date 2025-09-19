#!/usr/bin/env python3
# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""This script formats reStructuredText files to ensure one sentence per line and no trailing
whitespace. It exits with a non-zero status if any files were modified."""

import difflib
import importlib
import io
import json
import os
import re
import subprocess
import sys
from typing import List

import black
from docutils import nodes
from docutils.core import publish_doctree
from docutils.parsers.rst import Directive, directives
from ruamel.yaml import YAML

from spack.vendor import jsonschema

import spack.schema

#: Map Spack config sections to their corresponding JSON schema
SECTION_AND_SCHEMA = [
    # The first property's key is the config section name
    (next(iter(m.schema["properties"])), m.schema)
    # Dynamically load all modules in spack.schema to be future-proof
    for m in (
        importlib.import_module(f"spack.schema.{f[:-3]}")
        for f in os.listdir(os.path.dirname(spack.schema.__file__))
        if f.endswith(".py") and f != "__init__.py"
    )
    if hasattr(m, "schema") and len(m.schema.get("properties", {})) == 1
]

assert SECTION_AND_SCHEMA, "no schemas found"

END_OF_SENTENCE = re.compile(
    r"""
(
  (?:
    (?<!\b(?:e\.g|i\.e))  # e.g. and i.e. are not sentence endings
    \.|\?|!|\?!           # end of sentence punctuation
  )
  (?:\*{0,2})             # optionally match **bold.** and *italic.* at the end of sentence.
  ['")\]]?                # optionally match closing quotes and parentheses
)
\s+                       # at least one blank after punctuation
(?=[A-Z0-9:`*'"(\[])      # likely start of a new sentence
""",
    re.VERBOSE,
)
DOCUTILS_SETTING = {"report_level": 5, "raw_enabled": False, "file_insertion_enabled": False}


def _warning(msg: str) -> str:
    return f"\033[33mwarning:\033[0m {msg}"


class Warning:
    def __init__(self, path: str, line: int, message: str) -> None:
        self.path = path
        self.line = line
        self.message = message

    def __str__(self) -> str:
        return _warning(f"{self.path}:{self.line}: {self.message}")


class CodeBlockWarning(Warning):
    def __init__(self, path: str, line: int, message: str, diff: str):
        super().__init__(path, line, f"{message}\n{diff}")

    def __str__(self) -> str:
        return _warning(f"{self.path}:{self.line}: {self.message}")


class ValidationWarning(Warning):
    pass


class SphinxCodeBlock(Directive):
    """Defines a code-block directive with the options Sphinx supports."""

    has_content = True
    optional_arguments = 1  # language
    required_arguments = 0
    option_spec = {
        "force": directives.unchanged,
        "linenos": directives.unchanged,
        "dedent": directives.unchanged,
        "lineno-start": directives.unchanged,
        "emphasize-lines": directives.unchanged,
        "caption": directives.unchanged,
        "class": directives.unchanged,
        "name": directives.unchanged,
    }

    def run(self) -> List[nodes.Node]:
        # Produce a literal block with block.attributes["language"] set.
        language = self.arguments[0] if self.arguments else "python"
        literal = nodes.literal_block("\n".join(self.content), "\n".join(self.content))
        literal["language"] = language
        return [literal]


directives.register_directive("code-block", SphinxCodeBlock)


class ParagraphInfo:
    lineno: int
    end_lineno: int
    src: str
    lines: List[str]

    def __init__(self, line: int, src: str) -> None:
        self.lineno = line
        self.src = src
        self.lines = src.splitlines()
        self.end_lineno = line + len(self.lines) - 1


def _is_node_in_table(node: nodes.Node) -> bool:
    """Check if a node is inside a table by walking up the parent chain."""
    while node.parent:
        node = node.parent
        if isinstance(node, nodes.table):
            return True
    return False


def _validate_schema(data: object) -> None:
    if not isinstance(data, dict):
        return
    for section, schema in SECTION_AND_SCHEMA:
        if section in data:
            jsonschema.validate(data, schema)


def _format_code_blocks(document: nodes.document, path: str) -> List[Warning]:
    """Try to parse and format Python, YAML, and JSON code blocks. This does *not* update the
    sources, but collects issues for later reporting. Returns a list of warnings."""
    issues: List[Warning] = []
    for code_block in document.findall(nodes.literal_block):
        language = code_block.attributes.get("language", "")
        if language not in ("python", "yaml", "json"):
            continue
        original = code_block.astext()
        line = code_block.line if code_block.line else 0
        possible_config_data = None

        try:
            if language == "python":
                formatted = black.format_str(original, mode=black.FileMode(line_length=99))
            elif language == "yaml":
                yaml = YAML(pure=True)
                yaml.width = 10000  # do not wrap lines
                yaml.preserve_quotes = True  # do not force particular quotes
                buf = io.BytesIO()
                possible_config_data = yaml.load(original)
                yaml.dump(possible_config_data, buf)
                formatted = buf.getvalue().decode("utf-8")
            elif language == "json":
                formatted = json.dumps(json.loads(original), indent=2)
            else:
                assert False
        except Exception as e:
            issues.append(Warning(path, line, f"formatting failed: {e}: {original!r}"))
            continue

        try:
            _validate_schema(possible_config_data)
        except jsonschema.ValidationError as e:
            issues.append(ValidationWarning(path, line, f"schema validation failed: {e.message}"))

        if formatted == original:
            continue
        diff = "\n".join(
            difflib.unified_diff(
                original.splitlines(),
                formatted.splitlines(),
                lineterm="",
                fromfile=f"{path}:{line} (original)",
                tofile=f"{path}:{line} (suggested, NOT required)",
            )
        )
        if diff:
            issues.append(CodeBlockWarning(path, line, "formatting suggested:", diff))
    return issues


def _format_paragraphs(document: nodes.document, path: str, src_lines: List[str]) -> bool:
    """Format paragraphs in the document. Returns True if ``src_lines`` was modified."""

    paragraphs = [
        ParagraphInfo(line=p.line, src=p.rawsource)
        for p in document.findall(nodes.paragraph)
        if p.line is not None and p.rawsource and not _is_node_in_table(p)
    ]

    # Work from bottom to top to avoid messing up line numbers
    paragraphs.sort(key=lambda p: p.lineno, reverse=True)
    modified = False

    for p in paragraphs:
        # docutils does not give us the column offset, so we'll find it ourselves.
        col_offset = src_lines[p.lineno - 1].rfind(p.lines[0])
        assert col_offset >= 0, f"{path}:{p.lineno}: rst parsing error."
        prefix = lambda i: " " * col_offset if i > 0 else src_lines[p.lineno - 1][:col_offset]

        # Defensive check to ensure the source paragraph matches the docutils paragraph
        for i, line in enumerate(p.lines):
            line_lhs = f"{prefix(i)}{line}"
            line_rhs = src_lines[p.lineno - 1 + i].rstrip()  # docutils trims trailing whitespace
            assert line_lhs == line_rhs, f"{path}:{p.lineno + i}: rst parsing error."

        # Replace current newlines with whitespace, and then split sentences.
        new_paragraph_src = END_OF_SENTENCE.sub(r"\1\n", p.src.replace("\n", " "))
        new_paragraph_lines = [
            f"{prefix(i)}{line.lstrip()}" for i, line in enumerate(new_paragraph_src.splitlines())
        ]

        if new_paragraph_lines != src_lines[p.lineno - 1 : p.end_lineno]:
            modified = True
            src_lines[p.lineno - 1 : p.end_lineno] = new_paragraph_lines

    return modified


def reformat_rst_file(path: str, warnings: List[Warning]) -> bool:
    """Reformat a reStructuredText file "in-place". Returns True if modified, False otherwise."""
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()

    src_lines = src.splitlines()
    document: nodes.document = publish_doctree(src, settings_overrides=DOCUTILS_SETTING)

    warnings.extend(_format_code_blocks(document, path))

    if not _format_paragraphs(document, path, src_lines):
        return False

    with open(f"{path}.tmp", "w", encoding="utf-8") as f:
        f.write("\n".join(src_lines))
        f.write("\n")
    os.rename(f"{path}.tmp", path)
    print(f"Fixed reStructuredText formatting: {path}", flush=True)
    return True


def main(*files: str) -> None:
    modified = False
    warnings: List[Warning] = []
    for f in files:
        modified |= reformat_rst_file(f, warnings)

    if modified:
        subprocess.run(["git", "--no-pager", "diff", "--color=always", "--", *files])

    for warning in sorted(warnings, key=lambda w: isinstance(w, ValidationWarning)):
        print(warning, flush=True, file=sys.stderr)

    if warnings:
        print(
            _warning(f"completed with {len(warnings)} potential issues"),
            flush=True,
            file=sys.stderr,
        )
    sys.exit(1 if modified else 0)


if __name__ == "__main__":
    main(*sys.argv[1:])
