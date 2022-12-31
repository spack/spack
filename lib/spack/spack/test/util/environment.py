# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.util.environment import dump_environment


def test_dump_environment(working_env, tmpdir):
    test_paths = "/a:/b/x:/b/c"
    os.environ["TEST_ENV_VAR"] = test_paths
    dumpfile_path = str(tmpdir.join("envdump.txt"))
    dump_environment(dumpfile_path)
    with open(dumpfile_path, "r") as dumpfile:
        assert "TEST_ENV_VAR={0}; export TEST_ENV_VAR\n".format(test_paths) in list(dumpfile)
