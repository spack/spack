# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import llnl.util.filesystem as fs
import spack.main
import os


containerize = spack.main.SpackCommand('containerize')


def test_output(tmpdir):
    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
spack:
  # add package specs to the `specs` list
  specs:
    - callpath
  container:
    format: docker
    base:
      image: "ubuntu:18.04"
      spack: "develop"
    strip: true
""")
    containerize('-f', filename, '-r', 'recipe')
    assert os.path.exists(os.path.join('.', 'recipe'))


def test_command(configuration_dir, capsys):
    with capsys.disabled():
        with fs.working_dir(configuration_dir):
            output = containerize()
    assert 'FROM spack/ubuntu-bionic' in output
