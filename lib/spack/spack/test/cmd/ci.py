# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pytest

import llnl.util.filesystem as fs

import spack
import spack.ci as ci
import spack.environment as ev
from spack.main import SpackCommand
import spack.repo as repo
from spack.spec import Spec
from spack.test.conftest import MockPackage, MockPackageMultiRepo
import spack.util.executable as exe


ci_cmd = SpackCommand('ci')
env_cmd = SpackCommand('env')
git = exe.which('git', required=True)


pytestmark = pytest.mark.usefixtures(
    'mutable_mock_env_path', 'config', 'mutable_mock_packages')


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
    - packages: [archive-files]
  specs:
    - $packages
  mirrors:
    some-mirror: https://my.fake.mirror
  gitlab-ci:
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
        outputfile = str(tmpdir.join('.gitlab-ci.yml'))

        with ev.read('test'):
            ci_cmd('generate', '--output-file', outputfile)

        with open(outputfile) as f:
            contents = f.read()
            assert('archive-files' in contents)
            assert('stages: [stage-0' in contents)


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
