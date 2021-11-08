# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import collections
import itertools as it
import json
import os

import pytest

import llnl.util.filesystem as fs

import spack.ci as ci
import spack.ci_needs_workaround as cinw
import spack.ci_optimization as ci_opt
import spack.config as cfg
import spack.environment as ev
import spack.error
import spack.main as spack_main
import spack.paths as spack_paths
import spack.spec as spec
import spack.util.gpg
import spack.util.spack_yaml as syaml

try:
    # dynamically import to keep vermin from complaining
    collections_abc = __import__('collections.abc')
except ImportError:
    collections_abc = collections


@pytest.fixture
def tmp_scope():
    """Creates a temporary configuration scope"""
    base_name = 'internal-testing-scope'
    current_overrides = set(
        x.name for x in
        cfg.config.matching_scopes(r'^{0}'.format(base_name)))

    num_overrides = 0
    scope_name = base_name
    while scope_name in current_overrides:
        scope_name = '{0}{1}'.format(base_name, num_overrides)
        num_overrides += 1

    with cfg.override(cfg.InternalConfigScope(scope_name)):
        yield scope_name


def test_urlencode_string():
    s = 'Spack Test Project'

    s_enc = ci.url_encode_string(s)

    assert(s_enc == 'Spack+Test+Project')


def test_import_signing_key(mock_gnupghome):
    signing_key_dir = spack_paths.mock_gpg_keys_path
    signing_key_path = os.path.join(signing_key_dir, 'package-signing-key')
    with open(signing_key_path) as fd:
        signing_key = fd.read()

    # Just make sure this does not raise any exceptions
    ci.import_signing_key(signing_key)


def test_configure_compilers(mutable_config):

    def assert_missing(config):
        assert('install_missing_compilers' not in config or
               config['install_missing_compilers'] is False)

    def assert_present(config):
        assert('install_missing_compilers' in config and
               config['install_missing_compilers'] is True)

    original_config = cfg.get('config')
    assert_missing(original_config)

    ci.configure_compilers('FIND_ANY', scope='site')

    second_config = cfg.get('config')
    assert_missing(second_config)

    ci.configure_compilers('INSTALL_MISSING')
    last_config = cfg.get('config')
    assert_present(last_config)


def test_get_concrete_specs(config, mutable_mock_env_path, mock_packages):
    e = ev.create('test1')
    e.add('dyninst')
    e.concretize()

    dyninst_hash = None
    hash_dict = {}

    with e as active_env:
        for s in active_env.all_specs():
            hash_dict[s.name] = s.build_hash()
            if s.name == 'dyninst':
                dyninst_hash = s.build_hash()

        assert(dyninst_hash)

        dep_builds = 'libdwarf;libelf'
        spec_map = ci.get_concrete_specs(
            active_env, dyninst_hash, 'dyninst', dep_builds, 'NONE')
        assert('root' in spec_map and 'deps' in spec_map)

        concrete_root = spec_map['root']
        assert(concrete_root.build_hash() == dyninst_hash)

        concrete_deps = spec_map['deps']
        for key, obj in concrete_deps.items():
            assert(obj.build_hash() == hash_dict[key])

        s = spec.Spec('dyninst')
        print('nonconc spec name: {0}'.format(s.name))

        spec_map = ci.get_concrete_specs(
            active_env, s.name, s.name, dep_builds, 'FIND_ANY')

        assert('root' in spec_map and 'deps' in spec_map)


class FakeWebResponder(object):
    def __init__(self, response_code=200, content_to_read=[]):
        self._resp_code = response_code
        self._content = content_to_read
        self._read = [False for c in content_to_read]

    def open(self, request):
        return self

    def getcode(self):
        return self._resp_code

    def read(self, length=None):

        if len(self._content) <= 0:
            return None

        if not self._read[-1]:
            return_content = self._content[-1]
            if length:
                self._read[-1] = True
            else:
                self._read.pop()
                self._content.pop()
            return return_content

        self._read.pop()
        self._content.pop()
        return None


@pytest.mark.maybeslow
def test_register_cdash_build(monkeypatch):
    build_name = 'Some pkg'
    base_url = 'http://cdash.fake.org'
    project = 'spack'
    site = 'spacktests'
    track = 'Experimental'

    response_obj = {
        'buildid': 42
    }

    fake_responder = FakeWebResponder(
        content_to_read=[json.dumps(response_obj)])
    monkeypatch.setattr(ci, 'build_opener', lambda handler: fake_responder)
    build_id, build_stamp = ci.register_cdash_build(
        build_name, base_url, project, site, track)

    assert(build_id == 42)


def test_relate_cdash_builds(config, mutable_mock_env_path, mock_packages,
                             monkeypatch, capfd):
    e = ev.create('test1')
    e.add('dyninst')
    e.concretize()

    dyninst_hash = None
    hash_dict = {}

    with e as active_env:
        for s in active_env.all_specs():
            hash_dict[s.name] = s.build_hash()
            if s.name == 'dyninst':
                dyninst_hash = s.build_hash()

        assert(dyninst_hash)

        dep_builds = 'libdwarf;libelf'
        spec_map = ci.get_concrete_specs(
            active_env, dyninst_hash, 'dyninst', dep_builds, 'NONE')
        assert('root' in spec_map and 'deps' in spec_map)

        cdash_api_url = 'http://cdash.fake.org'
        job_build_id = '42'
        cdash_project = 'spack'
        cdashids_mirror_url = 'https://my.fake.mirror'

        dep_cdash_ids = {
            'libdwarf': 1,
            'libelf': 2
        }

        monkeypatch.setattr(ci, 'read_cdashid_from_mirror',
                            lambda s, u: dep_cdash_ids.pop(s.name))

        fake_responder = FakeWebResponder(
            content_to_read=['libdwarf', 'libelf'])
        monkeypatch.setattr(ci, 'build_opener', lambda handler: fake_responder)

        ci.relate_cdash_builds(spec_map, cdash_api_url, job_build_id,
                               cdash_project, [cdashids_mirror_url])

        assert(not dep_cdash_ids)

        dep_cdash_ids = {
            'libdwarf': 1,
            'libelf': 2
        }

        fake_responder._resp_code = 400
        ci.relate_cdash_builds(spec_map, cdash_api_url, job_build_id,
                               cdash_project, [cdashids_mirror_url])
        out, err = capfd.readouterr()
        assert('Warning: Relate builds' in err)
        assert('failed' in err)

        dep_cdash_ids = {}

        # Just make sure passing None for build id doesn't result in any
        # calls to "read_cdashid_from_mirror"
        ci.relate_cdash_builds(spec_map, cdash_api_url, None, cdash_project,
                               [cdashids_mirror_url])


def test_read_write_cdash_ids(config, tmp_scope, tmpdir, mock_packages):
    working_dir = tmpdir.join('working_dir')
    mirror_dir = working_dir.join('mirror')
    mirror_url = 'file://{0}'.format(mirror_dir.strpath)

    mirror_cmd = spack_main.SpackCommand('mirror')
    mirror_cmd('add', '--scope', tmp_scope, 'test_mirror', mirror_url)

    mock_spec = spec.Spec('archive-files').concretized()
    orig_cdashid = '42'

    ci.write_cdashid_to_mirror(orig_cdashid, mock_spec, mirror_url)

    # Now read it back
    read_cdashid = ci.read_cdashid_from_mirror(mock_spec, mirror_url)

    assert(str(read_cdashid) == orig_cdashid)


def test_download_and_extract_artifacts(tmpdir, monkeypatch):
    os.environ['GITLAB_PRIVATE_TOKEN'] = 'faketoken'

    url = 'https://www.nosuchurlexists.itsfake/artifacts.zip'
    working_dir = os.path.join(tmpdir.strpath, 'repro')
    test_artifacts_path = os.path.join(
        spack_paths.test_path, 'data', 'ci', 'gitlab', 'artifacts.zip')

    with open(test_artifacts_path, 'rb') as fd:
        fake_responder = FakeWebResponder(content_to_read=[fd.read()])

    monkeypatch.setattr(ci, 'build_opener', lambda handler: fake_responder)

    ci.download_and_extract_artifacts(url, working_dir)

    found_zip = fs.find(working_dir, 'artifacts.zip')
    assert(len(found_zip) == 0)

    found_install = fs.find(working_dir, 'install.sh')
    assert(len(found_install) == 1)

    fake_responder._resp_code = 400
    with pytest.raises(spack.error.SpackError):
        ci.download_and_extract_artifacts(url, working_dir)


def test_setup_spack_repro_version(tmpdir, capfd, last_two_git_commits,
                                   monkeypatch):
    c1, c2 = last_two_git_commits
    repro_dir = os.path.join(tmpdir.strpath, 'repro')
    spack_dir = os.path.join(repro_dir, 'spack')
    os.makedirs(spack_dir)

    prefix_save = spack.paths.prefix
    monkeypatch.setattr(spack.paths, 'prefix', '/garbage')

    ret = ci.setup_spack_repro_version(repro_dir, c2, c1)
    out, err = capfd.readouterr()

    assert(not ret)
    assert('Unable to find the path' in err)

    monkeypatch.setattr(spack.paths, 'prefix', prefix_save)

    monkeypatch.setattr(spack.util.executable, 'which', lambda cmd: None)

    ret = ci.setup_spack_repro_version(repro_dir, c2, c1)
    out, err = capfd.readouterr()

    assert(not ret)
    assert('requires git' in err)

    class mock_git_cmd(object):
        def __init__(self, *args, **kwargs):
            self.returncode = 0
            self.check = None

        def __call__(self, *args, **kwargs):
            if self.check:
                self.returncode = self.check(*args, **kwargs)
            else:
                self.returncode = 0

    git_cmd = mock_git_cmd()

    monkeypatch.setattr(spack.util.executable, 'which', lambda cmd: git_cmd)

    git_cmd.check = lambda *a, **k: 1 if len(a) > 2 and a[2] == c2 else 0
    ret = ci.setup_spack_repro_version(repro_dir, c2, c1)
    out, err = capfd.readouterr()

    assert(not ret)
    assert('Missing commit: {0}'.format(c2) in err)

    git_cmd.check = lambda *a, **k: 1 if len(a) > 2 and a[2] == c1 else 0
    ret = ci.setup_spack_repro_version(repro_dir, c2, c1)
    out, err = capfd.readouterr()

    assert(not ret)
    assert('Missing commit: {0}'.format(c1) in err)

    git_cmd.check = lambda *a, **k: 1 if a[0] == 'clone' else 0
    ret = ci.setup_spack_repro_version(repro_dir, c2, c1)
    out, err = capfd.readouterr()

    assert(not ret)
    assert('Unable to clone' in err)

    git_cmd.check = lambda *a, **k: 1 if a[0] == 'checkout' else 0
    ret = ci.setup_spack_repro_version(repro_dir, c2, c1)
    out, err = capfd.readouterr()

    assert(not ret)
    assert('Unable to checkout' in err)

    git_cmd.check = lambda *a, **k: 1 if 'merge' in a else 0
    ret = ci.setup_spack_repro_version(repro_dir, c2, c1)
    out, err = capfd.readouterr()

    assert(not ret)
    assert('Unable to merge {0}'.format(c1) in err)


def test_ci_workarounds():
    fake_root_spec = 'x' * 544
    fake_spack_ref = 'x' * 40

    common_variables = {
        'SPACK_COMPILER_ACTION': 'NONE',
        'SPACK_IS_PR_PIPELINE': 'False',
    }

    common_before_script = [
        'git clone "https://github.com/spack/spack"',
        ' && '.join((
            'pushd ./spack',
            'git checkout "{ref}"'.format(ref=fake_spack_ref),
            'popd')),
        '. "./spack/share/spack/setup-env.sh"'
    ]

    def make_build_job(name, deps, stage, use_artifact_buildcache, optimize,
                       use_dependencies):
        variables = common_variables.copy()
        variables['SPACK_JOB_SPEC_PKG_NAME'] = name

        result = {
            'stage': stage,
            'tags': ['tag-0', 'tag-1'],
            'artifacts': {
                'paths': [
                    'jobs_scratch_dir',
                    'cdash_report',
                    name + '.spec.json',
                    name + '.cdashid',
                    name
                ],
                'when': 'always'
            },
            'retry': {'max': 2, 'when': ['always']},
            'after_script': ['rm -rf "./spack"'],
            'script': ['spack ci rebuild'],
            'image': {'name': 'spack/centos7', 'entrypoint': ['']}
        }

        if optimize:
            result['extends'] = ['.c0', '.c1']
        else:
            variables['SPACK_ROOT_SPEC'] = fake_root_spec
            result['before_script'] = common_before_script

        result['variables'] = variables

        if use_dependencies:
            result['dependencies'] = (
                list(deps) if use_artifact_buildcache
                else [])
        else:
            result['needs'] = [
                {'job': dep, 'artifacts': use_artifact_buildcache}
                for dep in deps]

        return {name: result}

    def make_rebuild_index_job(
            use_artifact_buildcache, optimize, use_dependencies):

        result = {
            'stage': 'stage-rebuild-index',
            'script': 'spack buildcache update-index -d s3://mirror',
            'tags': ['tag-0', 'tag-1'],
            'image': {'name': 'spack/centos7', 'entrypoint': ['']},
            'after_script': ['rm -rf "./spack"'],
        }

        if optimize:
            result['extends'] = '.c0'
        else:
            result['before_script'] = common_before_script

        return {'rebuild-index': result}

    def make_factored_jobs(optimize):
        return {
            '.c0': {'before_script': common_before_script},
            '.c1': {'variables': {'SPACK_ROOT_SPEC': fake_root_spec}}
        } if optimize else {}

    def make_stage_list(num_build_stages):
        return {
            'stages': (
                ['-'.join(('stage', str(i))) for i in range(num_build_stages)]
                + ['stage-rebuild-index'])}

    def make_yaml_obj(use_artifact_buildcache, optimize, use_dependencies):
        result = {}

        result.update(make_build_job(
            'pkg-a', [], 'stage-0', use_artifact_buildcache, optimize,
            use_dependencies))

        result.update(make_build_job(
            'pkg-b', ['pkg-a'], 'stage-1', use_artifact_buildcache, optimize,
            use_dependencies))

        result.update(make_build_job(
            'pkg-c', ['pkg-a', 'pkg-b'], 'stage-2', use_artifact_buildcache,
            optimize, use_dependencies))

        result.update(make_rebuild_index_job(
            use_artifact_buildcache, optimize, use_dependencies))

        result.update(make_factored_jobs(optimize))

        result.update(make_stage_list(3))

        return result

    # test every combination of:
    #     use artifact buildcache: true or false
    #     run optimization pass: true or false
    #     convert needs to dependencies: true or false
    for use_ab in (False, True):
        original = make_yaml_obj(
            use_artifact_buildcache=use_ab,
            optimize=False,
            use_dependencies=False)

        for opt, deps in it.product(*(((False, True),) * 2)):
            # neither optimizing nor converting needs->dependencies
            if not (opt or deps):
                # therefore, nothing to test
                continue

            predicted = make_yaml_obj(
                use_artifact_buildcache=use_ab,
                optimize=opt,
                use_dependencies=deps)

            actual = original.copy()
            if opt:
                actual = ci_opt.optimizer(actual)
            if deps:
                actual = cinw.needs_to_dependencies(actual)

            predicted = syaml.dump_config(
                ci_opt.sort_yaml_obj(predicted), default_flow_style=True)
            actual = syaml.dump_config(
                ci_opt.sort_yaml_obj(actual), default_flow_style=True)

            assert(predicted == actual)
