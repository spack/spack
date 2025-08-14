#!/usr/bin/env python3
# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""This script formats reStructuredText files to ensure one sentence per line and no trailing
whitespace. It exits with a non-zero status if any files were modified."""

import os
import re
import subprocess
import sys
from typing import List

from docutils import nodes
from docutils.core import publish_doctree

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


def reformat_rst_file(path: str) -> bool:
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()

    src_lines = src.splitlines()
    document: nodes.document = publish_doctree(src, settings_overrides=DOCUTILS_SETTING)
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

    if not modified:
        return False

    with open(f"{path}.tmp", "w", encoding="utf-8") as f:
        f.write("\n".join(src_lines))
        f.write("\n")
    os.rename(f"{path}.tmp", path)
    print(f"Fixed reStructuredText formatting: {path}", flush=True)
    return True


if __name__ == "__main__":
    modified = False
    for f in sys.argv[1:]:
        modified |= reformat_rst_file(f)
    if modified:
        subprocess.run(["git", "--no-pager", "diff", "--color=always", "--", *sys.argv[1:]])
    sys.exit(1 if modified else 0)
