# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.container.writers as writers


def test_manifest(minimal_configuration):
    writer = writers.create(minimal_configuration)
    manifest_str = writer.manifest
    for line in manifest_str.split('\n'):
        assert 'echo' in line


def test_build_and_run_images(minimal_configuration):
    writer = writers.create(minimal_configuration)

    # Test the output of run property
    run = writer.run
    assert run.image == 'ubuntu:18.04'

    # Test the output of the build property
    build = writer.build
    assert build.image == 'spack/ubuntu-bionic'
    assert build.tag == 'latest'


def test_packages(minimal_configuration):
    # In this minimal configuration we don't have packages
    writer = writers.create(minimal_configuration)
    assert writer.os_packages is None

    # If we add them a list should be returned
    pkgs = ['libgomp1']
    minimal_configuration['spack']['container']['os_packages'] = pkgs
    writer = writers.create(minimal_configuration)
    p = writer.os_packages
    assert p.update
    assert p.install
    assert p.clean
    assert p.list == pkgs


def test_ensure_render_works(minimal_configuration):
    # Here we just want to ensure that nothing is raised
    writer = writers.create(minimal_configuration)
    writer()


def test_strip_is_set_from_config(minimal_configuration):
    writer = writers.create(minimal_configuration)
    assert writer.strip is True

    minimal_configuration['spack']['container']['strip'] = False
    writer = writers.create(minimal_configuration)
    assert writer.strip is False


def test_extra_instructions_is_set_from_config(minimal_configuration):
    writer = writers.create(minimal_configuration)
    assert writer.extra_instructions == (None, None)

    test_line = 'RUN echo Hello world!'
    e = minimal_configuration['spack']['container']
    e['extra_instructions'] = {}
    e['extra_instructions']['build'] = test_line
    writer = writers.create(minimal_configuration)
    assert writer.extra_instructions == (test_line, None)

    e['extra_instructions']['final'] = test_line
    del e['extra_instructions']['build']
    writer = writers.create(minimal_configuration)
    assert writer.extra_instructions == (None, test_line)
