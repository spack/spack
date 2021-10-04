# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import llnl.util.filesystem as fs

import spack.main

containerize = spack.main.SpackCommand('containerize')


def test_command(default_config, container_config_dir, capsys):
    with capsys.disabled():
        with fs.working_dir(container_config_dir):
            output = containerize()
    assert 'FROM spack/ubuntu-bionic' in output
