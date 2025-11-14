# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re
import sys

import pytest

from spack.llnl.util.tty.colify import colify, colify_table

# table as 3 rows x 6 columns
lorem_table = [
    ["There", "are", "many", "variations", "of", "passages"],
    ["of", "Lorem", "Ipsum", "available", "but", "many"],
    ["have", "suffered", "alteration", "in", "some", "form"],
]

# width of each column in above table
lorem_table_col_starts = [0, 7, 17, 29, 41, 47]

# table in a single list
lorem_words = lorem_table[0] + lorem_table[1] + lorem_table[2]


@pytest.mark.parametrize("console_cols", [10, 20, 40, 60, 80, 100, 120])
def test_fixed_column_table(console_cols, capfd):
    "ensure output is a fixed table regardless of size"
    colify_table(lorem_table, output=sys.stdout, console_cols=console_cols)
    output, _ = capfd.readouterr()

    # 3 rows
    assert output.strip().count("\n") == 2

    # right spacing
    lines = output.strip().split("\n")
    for line in lines:
        assert [line[w - 1] for w in lorem_table_col_starts[1:]] == [" "] * 5

    # same data
    stripped_lines = [re.sub(r"\s+", " ", line.strip()) for line in lines]
    assert stripped_lines == [" ".join(row) for row in lorem_table]


@pytest.mark.parametrize(
    "console_cols,expected_rows,expected_cols",
    [
        (10, 18, 1),
        (20, 18, 1),
        (40, 5, 4),
        (60, 3, 6),
        (80, 2, 9),
        (100, 2, 9),
        (120, 2, 9),
        (140, 1, 18),
    ],
)
def test_variable_width_columns(console_cols, expected_rows, expected_cols, capfd):
    colify(lorem_words, tty=True, output=sys.stdout, console_cols=console_cols)
    output, _ = capfd.readouterr()

    print(output)
    # expected rows
    assert output.strip().count("\n") == expected_rows - 1

    # right cols
    lines = output.strip().split("\n")
    assert all(len(re.split(r"\s+", line)) <= expected_cols for line in lines)

    # padding between columns
    rows = [re.split(r"\s+", line) for line in lines]
    cols = list(zip(*rows))

    max_col_widths = [max(len(s) for s in col) for col in cols]
    col_start = 0
    for w in max_col_widths:
        col_start += w + 2  # plus padding

        # verify that every column boundary is at max width + padding
        assert all(
            [
                line[col_start - 1] == " " and line[col_start] != " "
                for line in lines
                if col_start < len(line)
            ]
        )
