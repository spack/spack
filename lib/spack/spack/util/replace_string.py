# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

def replace_string(file_to_patch, string_to_find, replacement_string):
    """
    replace all occourances of string_to_find with replacement_string
    in file_to_patch
    """

    os.chmod(file_to_patch, 0o777)
    with open(file_to_patch) as f:
        patched_file_contents = f.read().replace(string_to_find, replacement_string)

    with open(file_to_patch, "w") as f:
        f.write(patched_file_contents)
