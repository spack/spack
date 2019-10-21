# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest
import os
import subprocess

from spack.main import SpackCommand
from spack.stage import Stage
import spack.environment as ev
import spack.config

mirror = SpackCommand('mirror')
env = SpackCommand('env')
add = SpackCommand('add')
concretize = SpackCommand('concretize')
fetch = SpackCommand('fetch')


@pytest.mark.disable_clean_stage_check
@pytest.mark.regression('8083')
def test_regression_8083(tmpdir, capfd, mock_packages, mock_fetch, config):
    with capfd.disabled():
        output = mirror('create', '-d', str(tmpdir), 'externaltool')
    assert 'Skipping' in output
    assert 'as it is an external spec' in output


@pytest.mark.regression('12345')
def test_mirror_from_env(tmpdir, mock_packages, mock_fetch, config,
                         mutable_mock_env_path):
    mirror_dir = str(tmpdir)
    env_name = 'test'

    env('create', env_name)
    with ev.read(env_name):
        add('trivial-install-test-package')
        add('git-test')
        concretize()
        with spack.config.override('config:checksum', False):
            mirror('create', '-d', mirror_dir)

    e = ev.read(env_name)
    assert set(os.listdir(mirror_dir)) == set([s.name for s in e.user_specs])
    for spec in e.specs_by_hash.values():
        mirror_res = os.listdir(os.path.join(mirror_dir, spec.name))
        expected = ['%s.tar.gz' % spec.format('{name}-{version}')]
        assert mirror_res == expected


@pytest.mark.disable_clean_stage_check
@pytest.mark.regression('12710')
@pytest.mark.parametrize('new_working_path', [
    # mirror paths should be relative to the yaml file they
    # are added to, NOT the spack working directory, so
    # the test should pass with a variety of working paths
    '.',
    '..',
    '../..',
    '../../..',
])
@pytest.mark.parametrize('mirror_prefix', [
    # relative mirror paths should be handled whether
    # the file:// prefix is used or not (to match absolute
    # path handling)
    'file://', ''])
@pytest.mark.parametrize('add_method', [
    # add spack mirrors using config.set or mirror cmd directly
    # or writing the mirror path to a file (relative to the yaml file
    # itself)
    'set',
    'direct',
    'file',
])
def test_mirror_paths(tmpdir, capfd, mock_packages, mock_archive,
                      new_working_path, mirror_prefix, add_method):
    # handle mirrors added via relative paths

    with tmpdir.as_cwd():
        with Stage('spack-mirror-test') as stage:
            mirror_root = os.path.join(stage.path, 'test-mirror')
            # use relative path here:
            mirror_path = mirror_prefix + os.path.relpath(mirror_root)

            if add_method == 'set':
                # register mirror with spack config
                mirrors = {'spack-mirror-test': mirror_path}
                spack.config.set('mirrors', mirrors)
                with spack.config.override('config:checksum', False):
                    mirror('create', '-d', mirror_root, 'libdwarf')
            elif add_method == 'direct':
                try:
                    subprocess.call("spack mirror remove spack-mirror-test",
                                    shell=True)
                except subprocess.CalledProcessError:
                    pass
                # can't use use SpackCommand mirror() because we need a custom
                # temporary scope
                # TODO: don't use subprocess, especially with shell=True
                # no additional failures were observed with this approach--if
                # it is the same code path, we could just remove this
                tmp_scope = str(tmpdir)
                subprocess.call("spack -C {tmp_scope} mirror add "
                                "spack-mirror-test {mirror_path}".format(
                                    tmp_scope=tmp_scope,
                                    mirror_path=mirror_path),
                                shell=True)
                subprocess.call("spack -C {tmp_scope} mirror create "
                                " -d {mirror_root} libdwarf".format(
                                    tmp_scope=tmp_scope,
                                    mirror_root=mirror_root),
                                shell=True)
            elif add_method == 'file':
                try:
                    subprocess.call("spack mirror remove spack-mirror-test",
                                    shell=True)
                except subprocess.CalledProcessError:
                    pass
                # write a path relative to the mirrors.yaml file created
                # in tmp scope
                tmp_scope = str(tmpdir)
                tmp_mirror_file = os.path.join(tmp_scope, 'mirrors.yaml')
                rel_path = os.path.relpath(mirror_root, tmp_mirror_file)
                with open(tmp_mirror_file, 'w') as mirror_file:
                    mirror_file.write("""\
mirrors:
   spack-mirror-test: {rel_path}\n""".format(
                        rel_path=rel_path))
                subprocess.call("spack -C {tmp_scope} mirror create "
                                " -d {mirror_root} libdwarf".format(
                                    tmp_scope=tmp_scope,
                                    mirror_root=mirror_root),
                                shell=True)

            # ensure robustness relative to different
            # spack working paths
            os.chdir(new_working_path)

            if add_method != 'set':
                # prevent cache retrieval circumventing the detection
                # of issues with fetch on relative path
                subprocess.call('spack clean -a', shell=True)
                output = subprocess.check_output("spack -C {tmp_scope} "
                                                 "fetch -n libdwarf".format(
                                                     tmp_scope=tmp_scope),
                                                 shell=True).decode('utf-8')
            else:
                with capfd.disabled():
                    output = fetch('-n', 'libdwarf')

            for fetch_line in output.split('==>'):
                if mirror_root.split(os.sep)[-2] in fetch_line:
                    # various possible markers of fetch failure
                    # from relative mirror path
                    for bad_entry in ['curl', '503', 'error', 'failed']:
                        assert bad_entry not in fetch_line
                else:
                    # an http fetch line would mean local mirror fetches
                    # ultimately failed
                    assert 'http' not in fetch_line
                    # using the cache is cheating for this test
                    if 'failed' not in fetch_line:
                        assert 'cache' not in fetch_line
