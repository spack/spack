# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import pytest

import llnl.util.tty as tty

import spack.config
import spack.monitor
import spack.spec
from spack.main import SpackCommand
from spack.monitor import SpackMonitorClient

install = SpackCommand('install')


def get_client(host, prefix="ms1", allow_fail=False, tags=None, save_local=False):
    """
    We replicate this function to not generate a global client.
    """
    cli = SpackMonitorClient(host=host, prefix=prefix, allow_fail=allow_fail,
                             tags=tags, save_local=save_local)

    # We will exit early if the monitoring service is not running, but
    # only if we aren't doing a local save
    if not save_local:
        info = cli.service_info()

        # If we allow failure, the response will be done
        if info:
            tty.debug("%s v.%s has status %s" % (
                info['id'],
                info['version'],
                info['status'])
            )
    return cli


@pytest.fixture
def mock_monitor_request(monkeypatch):
    """
    Monitor requests that are shared across tests go here
    """
    def mock_do_request(self, endpoint, *args, **kwargs):

        build = {"build_id": 1,
                 "spec_full_hash": "bpfvysmqndtmods4rmy6d6cfquwblngp",
                 "spec_name": "dttop"}

        # Service Info
        if endpoint == "":
            organization = {"name": "spack", "url": "https://github.com/spack"}
            return {"id": "spackmon", "status": "running",
                    "name": "Spack Monitor (Spackmon)",
                    "description": "The best spack monitor",
                    "organization": organization,
                    "contactUrl": "https://github.com/spack/spack-monitor/issues",
                    "documentationUrl": "https://spack-monitor.readthedocs.io",
                    "createdAt": "2021-04-09T21:54:51Z",
                    "updatedAt": "2021-05-24T15:06:46Z",
                    "environment": "test",
                    "version": "0.0.1",
                    "auth_instructions_url": "url"}

        # New Build
        elif endpoint == "builds/new/":
            return {"message": "Build get or create was successful.",
                    "data": {
                        "build_created": True,
                        "build_environment_created": True,
                        "build": build
                    },
                    "code": 201}

        # Update Build
        elif endpoint == "builds/update/":
            return {"message": "Status updated",
                    "data": {"build": build},
                    "code": 200}

        # Send Analyze Metadata
        elif endpoint == "analyze/builds/":
            return {"message": "Metadata updated",
                    "data": {"build": build},
                    "code": 200}

        # Update Build Phase
        elif endpoint == "builds/phases/update/":
            return {"message": "Phase autoconf was successfully updated.",
                    "code": 200,
                    "data": {
                        "build_phase": {
                            "id": 1,
                            "status": "SUCCESS",
                            "name": "autoconf"
                        }
                    }}

        # Update Phase Status
        elif endpoint == "phases/update/":
            return {"message": "Status updated",
                    "data": {"build": build},
                    "code": 200}

        # New Spec
        elif endpoint == "specs/new/":
            return {"message": "success",
                    "data": {
                        "full_hash": "bpfvysmqndtmods4rmy6d6cfquwblngp",
                        "name": "dttop",
                        "version": "1.0",
                        "spack_version": "0.16.0-1379-7a5351d495",
                        "specs": {
                            "dtbuild1": "btcmljubs4njhdjqt2ebd6nrtn6vsrks",
                            "dtlink1": "x4z6zv6lqi7cf6l4twz4bg7hj3rkqfmk",
                            "dtrun1": "i6inyro74p5yqigllqk5ivvwfjfsw6qz"
                        }
                    }}
        else:
            pytest.fail("bad endpoint: %s" % endpoint)
    monkeypatch.setattr(spack.monitor.SpackMonitorClient, "do_request", mock_do_request)


def test_spack_monitor_auth(mock_monitor_request):
    os.environ["SPACKMON_TOKEN"] = "xxxxxxxxxxxxxxxxx"
    os.environ["SPACKMON_USER"] = "spackuser"
    get_client(host="http://127.0.0.1")


def test_spack_monitor_without_auth(mock_monitor_request):
    get_client(host="hostname")


def test_spack_monitor_build_env(mock_monitor_request, install_mockery_mutable_config):
    monitor = get_client(host="hostname")
    assert hasattr(monitor, "build_environment")
    for key in ["host_os", "platform", "host_target", "hostname", "spack_version",
                "kernel_version"]:
        assert key in monitor.build_environment

    spec = spack.spec.Spec("dttop")
    spec.concretize()
    # Loads the build environment from the spec install folder
    monitor.load_build_environment(spec)


def test_spack_monitor_basic_auth(mock_monitor_request):
    monitor = get_client(host="hostname")

    # Headers should be empty
    assert not monitor.headers
    monitor.set_basic_auth("spackuser", "password")
    assert "Authorization" in monitor.headers
    assert monitor.headers['Authorization'].startswith("Basic")


def test_spack_monitor_new_configuration(mock_monitor_request, install_mockery):
    monitor = get_client(host="hostname")
    spec = spack.spec.Spec("dttop")
    spec.concretize()
    response = monitor.new_configuration([spec])

    # The response is a lookup of specs
    assert "dttop" in response


def test_spack_monitor_new_build(mock_monitor_request, install_mockery_mutable_config,
                                 install_mockery):
    monitor = get_client(host="hostname")
    spec = spack.spec.Spec("dttop")
    spec.concretize()
    response = monitor.new_build(spec)
    assert "message" in response and "data" in response and "code" in response
    assert response['code'] == 201
    # We should be able to get a build id
    monitor.get_build_id(spec)


def test_spack_monitor_update_build(mock_monitor_request, install_mockery,
                                    install_mockery_mutable_config):
    monitor = get_client(host="hostname")
    spec = spack.spec.Spec("dttop")
    spec.concretize()
    response = monitor.update_build(spec, status="SUCCESS")
    assert "message" in response and "data" in response and "code" in response
    assert response['code'] == 200


def test_spack_monitor_fail_task(mock_monitor_request, install_mockery,
                                 install_mockery_mutable_config):
    monitor = get_client(host="hostname")
    spec = spack.spec.Spec("dttop")
    spec.concretize()
    response = monitor.fail_task(spec)
    assert "message" in response and "data" in response and "code" in response
    assert response['code'] == 200


def test_spack_monitor_send_analyze_metadata(monkeypatch, mock_monitor_request,
                                             install_mockery,
                                             install_mockery_mutable_config):

    def buildid(*args, **kwargs):
        return 1
    monkeypatch.setattr(spack.monitor.SpackMonitorClient, "get_build_id", buildid)
    monitor = get_client(host="hostname")
    spec = spack.spec.Spec("dttop")
    spec.concretize()
    response = monitor.send_analyze_metadata(spec.package, metadata={"boop": "beep"})
    assert "message" in response and "data" in response and "code" in response
    assert response['code'] == 200


def test_spack_monitor_send_phase(mock_monitor_request, install_mockery,
                                  install_mockery_mutable_config):

    monitor = get_client(host="hostname")

    def get_build_id(*args, **kwargs):
        return 1

    spec = spack.spec.Spec("dttop")
    spec.concretize()
    response = monitor.send_phase(spec.package, "autoconf",
                                  spec.package.install_log_path,
                                  "SUCCESS")
    assert "message" in response and "data" in response and "code" in response
    assert response['code'] == 200


def test_spack_monitor_info(mock_monitor_request):
    os.environ["SPACKMON_TOKEN"] = "xxxxxxxxxxxxxxxxx"
    os.environ["SPACKMON_USER"] = "spackuser"
    monitor = get_client(host="http://127.0.0.1")
    info = monitor.service_info()

    for key in ['id', 'status', 'name', 'description', 'organization',
                'contactUrl', 'documentationUrl', 'createdAt', 'updatedAt',
                'environment', 'version', 'auth_instructions_url']:
        assert key in info


@pytest.fixture(scope='session')
def test_install_monitor_save_local(install_mockery_mutable_config,
                                    mock_fetch, tmpdir_factory):
    """
    Mock installing and saving monitor results to file.
    """
    reports_dir = tmpdir_factory.mktemp('reports')
    spack.config.set('config:monitor_dir', str(reports_dir))
    out = install('--monitor', '--monitor-save-local', 'dttop')
    assert "Successfully installed dttop" in out

    # The reports directory should not be empty (timestamped folders)
    assert os.listdir(str(reports_dir))

    # Get the spec name
    spec = spack.spec.Spec("dttop")
    spec.concretize()
    full_hash = spec.full_hash()

    # Ensure we have monitor results saved
    for dirname in os.listdir(str(reports_dir)):
        dated_dir = os.path.join(str(reports_dir), dirname)
        build_metadata = "build-metadata-%s.json" % full_hash
        assert build_metadata in os.listdir(dated_dir)
        spec_file = "spec-dttop-%s-config.json" % spec.version
        assert spec_file in os.listdir(dated_dir)

    spack.config.set('config:monitor_dir', "~/.spack/reports/monitor")
