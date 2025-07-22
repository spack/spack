# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from typing import List

from spack.util.executable import Executable, which


def compile_c_and_execute(
    source_file: str, include_flags: List[str], link_flags: List[str]
) -> str:
    """Compile a C source file with the given include and link flags, execute the resulting binary,
    and return its output as a string. Used in package tests."""
    cc = which("cc", required=True)
    flags = include_flags
    flags.extend([source_file])
    cc("-c", *flags)
    name = os.path.splitext(os.path.basename(source_file))[0]
    cc("-o", "check", "%s.o" % name, *link_flags)

    check = Executable("./check")
    return check(output=str)


def compare_output(current_output: str, blessed_output: str) -> None:
    """Compare blessed and current output of executables. Used in package tests."""
    if not (current_output == blessed_output):
        print("Produced output does not match expected output.")
        print("Expected output:")
        print("-" * 80)
        print(blessed_output)
        print("-" * 80)
        print("Produced output:")
        print("-" * 80)
        print(current_output)
        print("-" * 80)
        raise RuntimeError("Ouput check failed.", "See spack_output.log for details")


def compare_output_file(current_output: str, blessed_output_file: str) -> None:
    """Same as above, but when the blessed output is given as a file. Used in package tests."""
    with open(blessed_output_file, "r", encoding="utf-8") as f:
        blessed_output = f.read()

    compare_output(current_output, blessed_output)
