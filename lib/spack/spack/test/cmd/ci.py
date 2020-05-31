# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import filecmp
import os
import pytest

import spack
import spack.ci as ci
import spack.config
import spack.environment as ev
import spack.hash_types as ht
from spack.main import SpackCommand
import spack.paths as spack_paths
import spack.repo as repo
from spack.spec import Spec
from spack.util.mock_package import MockPackageMultiRepo
import spack.util.executable as exe
import spack.util.spack_yaml as syaml
import spack.util.gpg


ci_cmd = SpackCommand('ci')
env_cmd = SpackCommand('env')
mirror_cmd = SpackCommand('mirror')
gpg_cmd = SpackCommand('gpg')
install_cmd = SpackCommand('install')
buildcache_cmd = SpackCommand('buildcache')
git = exe.which('git', required=True)


def has_gpg():
    try:
        gpg = spack.util.gpg.Gpg.gpg()
    except spack.util.gpg.SpackGPGError:
        gpg = None
    return bool(gpg)


@pytest.fixture()
def env_deactivate():
    yield
    spack.environment._active_environment = None
    os.environ.pop('SPACK_ENV', None)


def set_env_var(key, val):
    os.environ[key] = val


def test_specs_staging(config):
    """Make sure we achieve the best possible staging for the following
spec DAG::

        a
       /|
      c b
        |\
        e d
          |\
          f g

In this case, we would expect 'c', 'e', 'f', and 'g' to be in the first stage,
and then 'd', 'b', and 'a' to be put in the next three stages, respectively.

"""
    default = ('build', 'link')

    mock_repo = MockPackageMultiRepo()
    g = mock_repo.add_package('g', [], [])
    f = mock_repo.add_package('f', [], [])
    e = mock_repo.add_package('e', [], [])
    d = mock_repo.add_package('d', [f, g], [default, default])
    c = mock_repo.add_package('c', [], [])
    b = mock_repo.add_package('b', [d, e], [default, default])
    mock_repo.add_package('a', [b, c], [default, default])

    with repo.swap(mock_repo):
        spec_a = Spec('a')
        spec_a.concretize()

        spec_a_label = ci.spec_deps_key_label(spec_a)[1]
        spec_b_label = ci.spec_deps_key_label(spec_a['b'])[1]
        spec_c_label = ci.spec_deps_key_label(spec_a['c'])[1]
        spec_d_label = ci.spec_deps_key_label(spec_a['d'])[1]
        spec_e_label = ci.spec_deps_key_label(spec_a['e'])[1]
        spec_f_label = ci.spec_deps_key_label(spec_a['f'])[1]
        spec_g_label = ci.spec_deps_key_label(spec_a['g'])[1]

        spec_labels, dependencies, stages = ci.stage_spec_jobs([spec_a])

        assert (len(stages) == 4)

        assert (len(stages[0]) == 4)
        assert (spec_c_label in stages[0])
        assert (spec_e_label in stages[0])
        assert (spec_f_label in stages[0])
        assert (spec_g_label in stages[0])

        assert (len(stages[1]) == 1)
        assert (spec_d_label in stages[1])

        assert (len(stages[2]) == 1)
        assert (spec_b_label in stages[2])

        assert (len(stages[3]) == 1)
        assert (spec_a_label in stages[3])


def test_ci_generate_with_env(tmpdir, mutable_mock_env_path, env_deactivate,
                              install_mockery, mock_packages):
    """Make sure we can get a .gitlab-ci.yml from an environment file
       which has the gitlab-ci, cdash, and mirrors sections."""
    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
spack:
  definitions:
    - bootstrap:
      - cmake@3.4.3
    - old-gcc-pkgs:
      - archive-files
      - callpath
      - hypre@0.2.15
  specs:
    - matrix:
      - [$old-gcc-pkgs]
  mirrors:
    some-mirror: https://my.fake.mirror
  gitlab-ci:
    bootstrap:
      - name: bootstrap
        compiler-agnostic: true
    mappings:
      - match:
          - arch=test-debian6-x86_64
        runner-attributes:
          tags:
            - donotcare
          image: donotcare
    final-stage-rebuild-index:
      image: donotcare
      tags: [donotcare]
  cdash:
    build-group: Not important
    url: https://my.fake.cdash
    project: Not used
    site: Nothing
""")
    with tmpdir.as_cwd():
        env_cmd('create', 'test', './spack.yaml')
        outputfile = str(tmpdir.join('.gitlab-ci.yml'))

        with ev.read('test'):
            ci_cmd('generate', '--output-file', outputfile)

        with open(outputfile) as f:
            contents = f.read()
            yaml_contents = syaml.load(contents)
            found_spec = False
            for ci_key in yaml_contents.keys():
                if '(bootstrap)' in ci_key:
                    found_spec = True
                    assert('cmake' in ci_key)
            assert(found_spec)
            assert('stages' in yaml_contents)
            assert(len(yaml_contents['stages']) == 6)
            assert(yaml_contents['stages'][0] == 'stage-0')
            assert(yaml_contents['stages'][5] == 'stage-rebuild-index')


def _validate_needs_graph(yaml_contents, needs_graph, artifacts):
    for job_name, job_def in yaml_contents.items():
        for needs_def_name, needs_list in needs_graph.items():
            if job_name.startswith(needs_def_name):
                # check job needs against the expected needs definition
                assert all([job_needs['job'][:job_needs['job'].index('/')]
                           in needs_list for job_needs in job_def['needs']])
                assert all([job_needs['artifacts'] == artifacts
                           for job_needs in job_def['needs']])
                break


def test_ci_generate_bootstrap_gcc(tmpdir, mutable_mock_env_path,
                                   env_deactivate, install_mockery,
                                   mock_packages):
    """Test that we can bootstrap a compiler and use it as the
    compiler for a spec in the environment"""
    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
spack:
  definitions:
    - bootstrap:
      - gcc@3.0
  specs:
    - dyninst%gcc@3.0
  mirrors:
    some-mirror: https://my.fake.mirror
  gitlab-ci:
    bootstrap:
      - name: bootstrap
        compiler-agnostic: true
    mappings:
      - match:
          - arch=test-debian6-x86_64
        runner-attributes:
          tags:
            - donotcare
""")

    needs_graph = {
        '(bootstrap) conflict': [],
        '(bootstrap) gcc': [
            '(bootstrap) conflict',
        ],
        '(specs) libelf': [
            '(bootstrap) gcc',
        ],
        '(specs) libdwarf': [
            '(bootstrap) gcc',
            '(specs) libelf',
        ],
        '(specs) dyninst': [
            '(bootstrap) gcc',
            '(specs) libelf',
            '(specs) libdwarf',
        ],
    }

    with tmpdir.as_cwd():
        env_cmd('create', 'test', './spack.yaml')
        outputfile = str(tmpdir.join('.gitlab-ci.yml'))

        with ev.read('test'):
            ci_cmd('generate', '--output-file', outputfile)

        with open(outputfile) as f:
            contents = f.read()
            yaml_contents = syaml.load(contents)
            _validate_needs_graph(yaml_contents, needs_graph, False)


def test_ci_generate_bootstrap_artifacts_buildcache(tmpdir,
                                                    mutable_mock_env_path,
                                                    env_deactivate,
                                                    install_mockery,
                                                    mock_packages):
    """Test that we can bootstrap a compiler when artifacts buildcache
    is turned on"""
    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
spack:
  definitions:
    - bootstrap:
      - gcc@3.0
  specs:
    - dyninst%gcc@3.0
  mirrors:
    some-mirror: https://my.fake.mirror
  gitlab-ci:
    bootstrap:
      - name: bootstrap
        compiler-agnostic: true
    mappings:
      - match:
          - arch=test-debian6-x86_64
        runner-attributes:
          tags:
            - donotcare
    enable-artifacts-buildcache: True
""")

    needs_graph = {
        '(bootstrap) conflict': [],
        '(bootstrap) gcc': [
            '(bootstrap) conflict',
        ],
        '(specs) libelf': [
            '(bootstrap) gcc',
            '(bootstrap) conflict',
        ],
        '(specs) libdwarf': [
            '(bootstrap) gcc',
            '(bootstrap) conflict',
            '(specs) libelf',
        ],
        '(specs) dyninst': [
            '(bootstrap) gcc',
            '(bootstrap) conflict',
            '(specs) libelf',
            '(specs) libdwarf',
        ],
    }

    with tmpdir.as_cwd():
        env_cmd('create', 'test', './spack.yaml')
        outputfile = str(tmpdir.join('.gitlab-ci.yml'))

        with ev.read('test'):
            ci_cmd('generate', '--output-file', outputfile)

        with open(outputfile) as f:
            contents = f.read()
            yaml_contents = syaml.load(contents)
            _validate_needs_graph(yaml_contents, needs_graph, True)


def test_ci_generate_with_env_missing_section(tmpdir, mutable_mock_env_path,
                                              env_deactivate, install_mockery,
                                              mock_packages):
    """Make sure we get a reasonable message if we omit gitlab-ci section"""
    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
spack:
  specs:
    - archive-files
  mirrors:
    some-mirror: https://my.fake.mirror
""")

    expect_out = 'Error: Environment yaml does not have "gitlab-ci" section'

    with tmpdir.as_cwd():
        env_cmd('create', 'test', './spack.yaml')

        with ev.read('test'):
            output = ci_cmd('generate', fail_on_error=False, output=str)
            assert(expect_out in output)


def test_ci_generate_with_cdash_token(tmpdir, mutable_mock_env_path,
                                      env_deactivate, install_mockery,
                                      mock_packages):
    """Make sure we it doesn't break if we configure cdash"""
    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
spack:
  specs:
    - archive-files
  mirrors:
    some-mirror: https://my.fake.mirror
  gitlab-ci:
    enable-artifacts-buildcache: True
    enable-debug-messages: True
    mappings:
      - match:
          - archive-files
        runner-attributes:
          tags:
            - donotcare
          image: donotcare
  cdash:
    build-group: Not important
    url: https://my.fake.cdash
    project: Not used
    site: Nothing
""")

    with tmpdir.as_cwd():
        env_cmd('create', 'test', './spack.yaml')

        with ev.read('test'):
            fake_token = 'notreallyatokenbutshouldnotmatter'
            os.environ['SPACK_CDASH_AUTH_TOKEN'] = fake_token
            copy_to_file = str(tmpdir.join('backup-ci.yml'))
            output = ci_cmd('generate', '--copy-to', copy_to_file, output=str)
            # That fake token should still have resulted in being unable to
            # register build group with cdash, but the workload should
            # still have been generated.
            expect = 'Problem populating buildgroup'
            assert(expect in output)

            dir_contents = os.listdir(tmpdir.strpath)

            print(dir_contents)

            assert('backup-ci.yml' in dir_contents)

            orig_file = str(tmpdir.join('.gitlab-ci.yml'))

            assert(filecmp.cmp(orig_file, copy_to_file) is True)


def test_ci_generate_pkg_with_deps(tmpdir, mutable_mock_env_path,
                                   env_deactivate, install_mockery,
                                   mock_packages):
    """Test pipeline generation for a package w/ dependencies"""
    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
spack:
  specs:
    - flatten-deps
  mirrors:
    some-mirror: https://my.fake.mirror
  gitlab-ci:
    enable-artifacts-buildcache: True
    mappings:
      - match:
          - flatten-deps
        runner-attributes:
          tags:
            - donotcare
      - match:
          - dependency-install
        runner-attributes:
          tags:
            - donotcare
""")

    with tmpdir.as_cwd():
        env_cmd('create', 'test', './spack.yaml')
        outputfile = str(tmpdir.join('.gitlab-ci.yml'))

        with ev.read('test'):
            ci_cmd('generate', '--output-file', outputfile)

        with open(outputfile) as f:
            contents = f.read()
            print('generated contents: ')
            print(contents)
            yaml_contents = syaml.load(contents)
            found = []
            for ci_key in yaml_contents.keys():
                ci_obj = yaml_contents[ci_key]
                if 'dependency-install' in ci_key:
                    assert('stage' in ci_obj)
                    assert(ci_obj['stage'] == 'stage-0')
                    found.append('dependency-install')
                if 'flatten-deps' in ci_key:
                    assert('stage' in ci_obj)
                    assert(ci_obj['stage'] == 'stage-1')
                    found.append('flatten-deps')

            assert('flatten-deps' in found)
            assert('dependency-install' in found)


def test_ci_generate_for_pr_pipeline(tmpdir, mutable_mock_env_path,
                                     env_deactivate, install_mockery,
                                     mock_packages):
    """Test that PR pipelines do not include a final stage job for
    rebuilding the mirror index, even if that job is specifically
    configured"""
    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
spack:
  specs:
    - flatten-deps
  mirrors:
    some-mirror: https://my.fake.mirror
  gitlab-ci:
    enable-artifacts-buildcache: True
    mappings:
      - match:
          - flatten-deps
        runner-attributes:
          tags:
            - donotcare
      - match:
          - dependency-install
        runner-attributes:
          tags:
            - donotcare
    final-stage-rebuild-index:
      image: donotcare
      tags: [donotcare]
""")

    with tmpdir.as_cwd():
        env_cmd('create', 'test', './spack.yaml')
        outputfile = str(tmpdir.join('.gitlab-ci.yml'))

        with ev.read('test'):
            os.environ['SPACK_IS_PR_PIPELINE'] = 'True'
            ci_cmd('generate', '--output-file', outputfile)

        with open(outputfile) as f:
            contents = f.read()
            print('generated contents: ')
            print(contents)
            yaml_contents = syaml.load(contents)

            assert('rebuild-index' not in yaml_contents)


def test_ci_generate_with_external_pkg(tmpdir, mutable_mock_env_path,
                                       env_deactivate, install_mockery,
                                       mock_packages):
    """Make sure we do not generate jobs for external pkgs"""
    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
spack:
  specs:
    - archive-files
    - externaltest
  mirrors:
    some-mirror: https://my.fake.mirror
  gitlab-ci:
    mappings:
      - match:
          - archive-files
          - externaltest
        runner-attributes:
          tags:
            - donotcare
          image: donotcare
""")

    with tmpdir.as_cwd():
        env_cmd('create', 'test', './spack.yaml')
        outputfile = str(tmpdir.join('.gitlab-ci.yml'))

        with ev.read('test'):
            ci_cmd('generate', '--output-file', outputfile)

        with open(outputfile) as f:
            contents = f.read()
            print('generated contents: ')
            print(contents)
            yaml_contents = syaml.load(contents)
            for ci_key in yaml_contents.keys():
                if 'externaltool' in ci_key:
                    print('Erroneously staged "externaltool" pkg')
                    assert(False)


def test_ci_generate_debug_with_custom_spack(tmpdir, mutable_mock_env_path,
                                             env_deactivate, install_mockery,
                                             mock_packages):
    """Make sure we generate cloning of spack in job script if needed"""
    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
spack:
  specs:
    - archive-files
  mirrors:
    some-mirror: https://my.fake.mirror
  gitlab-ci:
    enable-artifacts-buildcache: True
    enable-debug-messages: True
    mappings:
      - match:
          - archive-files
        runner-attributes:
          tags:
            - donotcare
          image: donotcare
""")

    with tmpdir.as_cwd():
        env_cmd('create', 'test', './spack.yaml')
        outfile = str(tmpdir.join('.gitlab-ci.yml'))

        with ev.read('test'):
            spack_repo = 'https://github.com/usera/spack.git'
            spack_ref = 'custom-branch'
            expected_clone_str = 'git clone "{0}"'.format(spack_repo)

            ci_cmd('generate', '--output-file', outfile, '--spack-repo',
                   spack_repo, '--spack-ref', spack_ref)

            with open(outfile) as f:
                contents = f.read()
                yaml_contents = syaml.load(contents)
                for ci_key in yaml_contents.keys():
                    if '(specs)' in ci_key:
                        next_job = yaml_contents[ci_key]
                        print(next_job)
                        assert('before_script' in next_job)
                        before_script = next_job['before_script']
                        for step in before_script:
                            if expected_clone_str in step:
                                break
                        else:
                            msg = 'job "{0}" did not clone spack repo'.format(
                                ci_key)
                            print(msg)
                            assert(False)

                        assert('script' in next_job)
                        script = next_job['script']
                        for step in script:
                            if 'spack -d ci rebuild' in step:
                                break
                        else:
                            msg = 'job {0} missing rebuild command'.format(
                                ci_key)
                            print(msg)
                            assert(False)


def test_ci_rebuild_basic(tmpdir, mutable_mock_env_path, env_deactivate,
                          install_mockery, mock_packages,
                          mock_gnupghome):
    working_dir = tmpdir.join('working_dir')

    mirror_dir = working_dir.join('mirror')
    mirror_url = 'file://{0}'.format(mirror_dir.strpath)

    signing_key_dir = spack_paths.mock_gpg_keys_path
    signing_key_path = os.path.join(signing_key_dir, 'package-signing-key')
    with open(signing_key_path) as fd:
        signing_key = fd.read()

    spack_yaml_contents = """
spack:
 definitions:
   - packages: [archive-files]
 specs:
   - $packages
 mirrors:
   test-mirror: {0}
 gitlab-ci:
   enable-artifacts-buildcache: True
   mappings:
     - match:
         - archive-files
       runner-attributes:
         tags:
           - donotcare
         image: donotcare
 cdash:
   build-group: Not important
   url: https://my.fake.cdash
   project: Not used
   site: Nothing
""".format(mirror_url)

    print('spack.yaml:\n{0}\n'.format(spack_yaml_contents))

    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write(spack_yaml_contents)

    with tmpdir.as_cwd():
        env_cmd('create', 'test', './spack.yaml')
        with ev.read('test'):
            root_spec = ('eJyNjsGOwyAMRO/5Ct96alRFFK34ldUqcohJ6BJAQFHUry9Nk66'
                         'UXNY3v5mxJ3qSojoDBjnqTGelDUVRQZlMIWpnBZya+nJa0Mv1Fg'
                         'G8waRcmAQkimkHWxcF9NRptHyVEoaBkoD5i7ecLVC6yZd/YTtpc'
                         'SIBg5Tr/mnA6mt9qTZL9CiLr7trk7StJyd/F81jKGoqoe2gVAaH'
                         '0uT7ZwPeH9A875HaA9MfidHdHxgxjgJuTGVtIrvfHGtynjkGyzi'
                         'xRrkHy94t1lftvv1n4AkVK3kQ')

            # Create environment variables as gitlab would do it
            set_env_var('CI_PROJECT_DIR', working_dir.strpath)
            set_env_var('SPACK_SIGNING_KEY', signing_key)
            set_env_var('SPACK_ROOT_SPEC', root_spec)
            set_env_var('SPACK_JOB_SPEC_PKG_NAME', 'archive-files')
            set_env_var('SPACK_COMPILER_ACTION', 'NONE')
            set_env_var('SPACK_CDASH_BUILD_NAME', '(specs) archive-files')
            set_env_var('SPACK_RELATED_BUILDS_CDASH', '')

            rebuild_output = ci_cmd(
                'rebuild', fail_on_error=False, output=str)

            print(rebuild_output)


@pytest.mark.disable_clean_stage_check
@pytest.mark.skipif(not has_gpg(), reason='This test requires gpg')
def test_push_mirror_contents(tmpdir, mutable_mock_env_path, env_deactivate,
                              install_mockery, mock_packages, mock_fetch,
                              mock_stage, mock_gnupghome):
    working_dir = tmpdir.join('working_dir')

    mirror_dir = working_dir.join('mirror')
    mirror_url = 'file://{0}'.format(mirror_dir.strpath)

    signing_key_dir = spack_paths.mock_gpg_keys_path
    signing_key_path = os.path.join(signing_key_dir, 'package-signing-key')
    with open(signing_key_path) as fd:
        signing_key = fd.read()

    ci.import_signing_key(signing_key)

    spack_yaml_contents = """
spack:
 definitions:
   - packages: [patchelf]
 specs:
   - $packages
 mirrors:
   test-mirror: {0}
""".format(mirror_url)

    print('spack.yaml:\n{0}\n'.format(spack_yaml_contents))

    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write(spack_yaml_contents)

    with tmpdir.as_cwd():
        env_cmd('create', 'test', './spack.yaml')
        with ev.read('test') as env:
            spec_map = ci.get_concrete_specs(
                'patchelf', 'patchelf', '', 'FIND_ANY')
            concrete_spec = spec_map['patchelf']
            spec_yaml = concrete_spec.to_yaml(hash=ht.build_hash)
            yaml_path = str(tmpdir.join('spec.yaml'))
            with open(yaml_path, 'w') as ypfd:
                ypfd.write(spec_yaml)

            install_cmd('--keep-stage', yaml_path)

            # env, spec, yaml_path, mirror_url, build_id
            ci.push_mirror_contents(
                env, concrete_spec, yaml_path, mirror_url, '42')

            buildcache_list_output = buildcache_cmd('list', output=str)

            assert('patchelf' in buildcache_list_output)

            logs_dir = working_dir.join('logs_dir')
            if not os.path.exists(logs_dir.strpath):
                os.makedirs(logs_dir.strpath)

            ci.copy_stage_logs_to_artifacts(concrete_spec, logs_dir.strpath)

            logs_dir_list = os.listdir(logs_dir.strpath)

            assert('spack-build-env.txt' in logs_dir_list)
            assert('spack-build-out.txt' in logs_dir_list)

            # Also just make sure that if something goes wrong with the
            # stage logs copy, no exception is thrown
            ci.copy_stage_logs_to_artifacts(None, logs_dir.strpath)

            dl_dir = working_dir.join('download_dir')
            if not os.path.exists(dl_dir.strpath):
                os.makedirs(dl_dir.strpath)

            buildcache_cmd('download', '--spec-yaml', yaml_path, '--path',
                           dl_dir.strpath, '--require-cdashid')

            dl_dir_list = os.listdir(dl_dir.strpath)

            assert(len(dl_dir_list) == 3)
