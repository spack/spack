# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pytest

import llnl.util.filesystem as fs

import spack
import spack.ci as ci
import spack.config
import spack.environment as ev
import spack.util.gpg as gpg_util
from spack.main import SpackCommand
import spack.paths as spack_paths
import spack.repo as repo
from spack.spec import Spec
from spack.test.conftest import MockPackage, MockPackageMultiRepo
import spack.util.executable as exe
import spack.util.spack_yaml as syaml


ci_cmd = SpackCommand('ci')
env_cmd = SpackCommand('env')
mirror_cmd = SpackCommand('mirror')
git = exe.which('git', required=True)


@pytest.fixture(scope='function')
def testing_gpg_directory(tmpdir):
    old_gpg_path = gpg_util.GNUPGHOME
    gpg_util.GNUPGHOME = str(tmpdir.join('gpg'))
    yield
    gpg_util.GNUPGHOME = old_gpg_path


@pytest.fixture()
def env_deactivate():
    yield
    spack.environment._active_environment = None
    os.environ.pop('SPACK_ENV', None)


def initialize_new_repo(repo_path, initial_commit=False):
    if not os.path.exists(repo_path):
        os.makedirs(repo_path)

    with fs.working_dir(repo_path):
        init_args = ['init', '.']
        # if not initial_commit:
        #     init_args.append('--bare')

        git(*init_args)

        if initial_commit:
            readme_contents = "This is the project README\n"
            readme_path = os.path.join(repo_path, 'README.md')
            with open(readme_path, 'w') as fd:
                fd.write(readme_contents)
            git('add', '.')
            git('commit', '-m', 'Project initial commit')


def get_repo_status(repo_path):
    with fs.working_dir(repo_path):
        output = git('rev-parse', '--abbrev-ref', 'HEAD', output=str)
        current_branch = output.split()[0]

        output = git('rev-parse', 'HEAD', output=str)
        current_sha = output.split()[0]

        return current_branch, current_sha


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

    g = MockPackage('g', [], [])
    f = MockPackage('f', [], [])
    e = MockPackage('e', [], [])
    d = MockPackage('d', [f, g], [default, default])
    c = MockPackage('c', [], [])
    b = MockPackage('b', [d, e], [default, default])
    a = MockPackage('a', [b, c], [default, default])

    mock_repo = MockPackageMultiRepo([a, b, c, d, e, f, g])

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
            print(yaml_contents)
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


def test_ci_rebuild_basic(tmpdir, mutable_mock_env_path, env_deactivate,
                          install_mockery, mock_packages,
                          testing_gpg_directory):
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


def test_ci_pushyaml(tmpdir):
    fake_yaml_contents = """generate ci jobs:
  script:
    - "./share/spack/qa/gitlab/generate-gitlab-ci-yml.sh"
  tags:
    - "spack-pre-ci"
  artifacts:
    paths:
      - ci-generation
    when: always
 """
    local_repo_path = tmpdir.join('local_repo')
    initialize_new_repo(local_repo_path.strpath, True)

    remote_repo_path = tmpdir.join('remote_repo')
    initialize_new_repo(remote_repo_path.strpath)

    current_branch, current_sha = get_repo_status(local_repo_path.strpath)

    print('local repo info: {0}, {1}'.format(current_branch, current_sha))

    local_jobs_yaml = local_repo_path.join('.gitlab-ci.yml')
    with local_jobs_yaml.open('w') as f:
        f.write(fake_yaml_contents)

    pushyaml_args = [
        'pushyaml',
        '--downstream-repo', remote_repo_path.strpath,
        '--branch-name', current_branch,
        '--commit-sha', current_sha,
    ]

    with fs.working_dir(local_repo_path.strpath):
        ci_cmd(*pushyaml_args)

    with fs.working_dir(remote_repo_path.strpath):
        branch_to_checkout = 'multi-ci-{0}'.format(current_branch)
        git('checkout', branch_to_checkout)
        with open('.gitlab-ci.yml') as fd:
            pushed_contents = fd.read()
            assert pushed_contents == fake_yaml_contents
