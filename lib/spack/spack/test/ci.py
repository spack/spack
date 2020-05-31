# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pytest
from six.moves.urllib.error import URLError

import spack.ci as ci
import spack.main as spack_main
import spack.config as cfg
import spack.paths as spack_paths
import spack.spec as spec
import spack.util.web as web_util
import spack.util.gpg


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


def has_gpg():
    try:
        gpg = spack.util.gpg.Gpg.gpg()
    except spack.util.gpg.SpackGPGError:
        gpg = None
    return bool(gpg)


@pytest.mark.skipif(not has_gpg(), reason='This test requires gpg')
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


def test_get_concrete_specs(config, mock_packages):
    root_spec = (
        'eJztkk1uwyAQhfc5BbuuYjWObSKuUlURYP5aDBjjBPv0RU7iRI6qpKuqUtnxzZvRwHud'
        'YxSt1oCMyuVoBdI5MN8paxDYZK/ZbkLYU3kqAuA0Dtz6BgGtTB8XdG87BCgzwXbwXArY'
        'CxYQiLtqXxUTpLZxSjN/mWlwwxAQlJ7v8wpFtsvK1UXSOUyTjvRKB2Um7LBPhZD0l1md'
        'xJ7VCATfszOiXGOR9np7vwDn7lCMS8SXQNf3RCtyBTVzzNTMUMXmfWrFeR+UngEAEncS'
        'ASjKwZcid7ERNldthBxjX46mMD2PsJnlYXDs2rye3l+vroOkJJ54SXgZPklLRQmx61sm'
        'cgKNVFRO0qlpf2pojq1Ro7OG56MY+Bgc1PkIo/WkaT8OVcrDYuvZkJdtBl/+XCZ+NQBJ'
        'oKg1h6X/VdXRoyE2OWeH6lCXZdHGrauUZAWFw/YJ/0/39OefN3F4Kle3cXjYsF684ZqG'
        'Tbap/uPwbRx+YPStIQ8bvgA7G6YE'
    )

    dep_builds = 'diffutils;libiconv'
    spec_map = ci.get_concrete_specs(root_spec, 'bzip2', dep_builds, 'NONE')

    assert('root' in spec_map and 'deps' in spec_map)

    nonconc_root_spec = 'archive-files'
    dep_builds = ''
    spec_map = ci.get_concrete_specs(
        nonconc_root_spec, 'archive-files', dep_builds, 'FIND_ANY')

    assert('root' in spec_map and 'deps' in spec_map)
    assert('archive-files' in spec_map)


def test_register_cdash_build():
    build_name = 'Some pkg'
    base_url = 'http://cdash.fake.org'
    project = 'spack'
    site = 'spacktests'
    track = 'Experimental'

    with pytest.raises(URLError):
        ci.register_cdash_build(build_name, base_url, project, site, track)


def test_relate_cdash_builds(config, mock_packages):
    root_spec = (
        'eJztkk1uwyAQhfc5BbuuYjWObSKuUlURYP5aDBjjBPv0RU7iRI6qpKuqUtnxzZvRwHud'
        'YxSt1oCMyuVoBdI5MN8paxDYZK/ZbkLYU3kqAuA0Dtz6BgGtTB8XdG87BCgzwXbwXArY'
        'CxYQiLtqXxUTpLZxSjN/mWlwwxAQlJ7v8wpFtsvK1UXSOUyTjvRKB2Um7LBPhZD0l1md'
        'xJ7VCATfszOiXGOR9np7vwDn7lCMS8SXQNf3RCtyBTVzzNTMUMXmfWrFeR+UngEAEncS'
        'ASjKwZcid7ERNldthBxjX46mMD2PsJnlYXDs2rye3l+vroOkJJ54SXgZPklLRQmx61sm'
        'cgKNVFRO0qlpf2pojq1Ro7OG56MY+Bgc1PkIo/WkaT8OVcrDYuvZkJdtBl/+XCZ+NQBJ'
        'oKg1h6X/VdXRoyE2OWeH6lCXZdHGrauUZAWFw/YJ/0/39OefN3F4Kle3cXjYsF684ZqG'
        'Tbap/uPwbRx+YPStIQ8bvgA7G6YE'
    )

    dep_builds = 'diffutils;libiconv'
    spec_map = ci.get_concrete_specs(root_spec, 'bzip2', dep_builds, 'NONE')
    cdash_api_url = 'http://cdash.fake.org'
    job_build_id = '42'
    cdash_project = 'spack'
    cdashids_mirror_url = 'https://my.fake.mirror'

    with pytest.raises(web_util.SpackWebError):
        ci.relate_cdash_builds(spec_map, cdash_api_url, job_build_id,
                               cdash_project, cdashids_mirror_url)

    # Just make sure passing None for build id doesn't throw exceptions
    ci.relate_cdash_builds(spec_map, cdash_api_url, None, cdash_project,
                           cdashids_mirror_url)


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
