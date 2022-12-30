# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.path as lup


def test_sanitze_file_path(tmpdir):
    """Test filtering illegal characters out of potential file paths"""
    # *nix illegal files characters are '/' and none others
    illegal_file_path = str(tmpdir) + "//" + "abcdefghi.txt"
    if is_windows:
        # Windows has a larger set of illegal characters
        illegal_file_path = os.path.join(tmpdir, 'a<b>cd?e:f"g|h*i.txt')
    real_path = lup.sanitize_file_path(illegal_file_path)
    assert real_path == os.path.join(str(tmpdir), "abcdefghi.txt")
