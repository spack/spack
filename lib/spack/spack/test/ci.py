# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import itertools
import os
import subprocess
import sys

import pytest

import llnl.util.filesystem as fs

import spack.ci as ci
import spack.ci_needs_workaround as cinw
import spack.ci_optimization as ci_opt
import spack.config
import spack.environment as ev
import spack.error
import spack.paths as spack_paths
import spack.util.git
import spack.util.gpg
import spack.util.spack_yaml as syaml


@pytest.fixture
def repro_dir(tmp_path):
    result = tmp_path / "repro_dir"
    result.mkdir()
    with fs.working_dir(str(tmp_path)):
        yield result


def test_urlencode_string():
    assert ci._url_encode_string("Spack Test Project") == "Spack+Test+Project"


@pytest.mark.skipif(sys.platform == "win32", reason="Not supported on Windows (yet)")
def test_import_signing_key(mock_gnupghome):
    signing_key_dir = spack_paths.mock_gpg_keys_path
    signing_key_path = os.path.join(signing_key_dir, "package-signing-key")
    with open(signing_key_path) as fd:
        signing_key = fd.read()

    # Just make sure this does not raise any exceptions
    ci.import_signing_key(signing_key)


def test_configure_compilers(mutable_config):
    def assert_missing(config):
        assert (
            "install_missing_compilers" not in config
            or config["install_missing_compilers"] is False
        )

    def assert_present(config):
        assert (
            "install_missing_compilers" in config and config["install_missing_compilers"] is True
        )

    original_config = spack.config.get("config")
    assert_missing(original_config)

    ci.configure_compilers("FIND_ANY", scope="site")

    second_config = spack.config.get("config")
    assert_missing(second_config)

    ci.configure_compilers("INSTALL_MISSING")
    last_config = spack.config.get("config")
    assert_present(last_config)


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


def test_download_and_extract_artifacts(tmpdir, monkeypatch, working_env):
    os.environ.update({"GITLAB_PRIVATE_TOKEN": "faketoken"})

    url = "https://www.nosuchurlexists.itsfake/artifacts.zip"
    working_dir = os.path.join(tmpdir.strpath, "repro")
    test_artifacts_path = os.path.join(
        spack_paths.test_path, "data", "ci", "gitlab", "artifacts.zip"
    )

    with open(test_artifacts_path, "rb") as fd:
        fake_responder = FakeWebResponder(content_to_read=[fd.read()])

    monkeypatch.setattr(ci, "build_opener", lambda handler: fake_responder)

    ci.download_and_extract_artifacts(url, working_dir)

    found_zip = fs.find(working_dir, "artifacts.zip")
    assert len(found_zip) == 0

    found_install = fs.find(working_dir, "install.sh")
    assert len(found_install) == 1

    fake_responder._resp_code = 400
    with pytest.raises(spack.error.SpackError):
        ci.download_and_extract_artifacts(url, working_dir)


def test_ci_copy_stage_logs_to_artifacts_fail(tmpdir, default_mock_concretization, capfd):
    """The copy will fail because the spec is not concrete so does not have
    a package."""
    log_dir = tmpdir.join("log_dir")
    concrete_spec = default_mock_concretization("printing-package")
    ci.copy_stage_logs_to_artifacts(concrete_spec, log_dir)
    _, err = capfd.readouterr()
    assert "Unable to copy files" in err
    assert "No such file or directory" in err


def test_ci_copy_test_logs_to_artifacts_fail(tmpdir, capfd):
    log_dir = tmpdir.join("log_dir")

    ci.copy_test_logs_to_artifacts("no-such-dir", log_dir)
    _, err = capfd.readouterr()
    assert "Cannot copy test logs" in err

    stage_dir = tmpdir.join("stage_dir").strpath
    os.makedirs(stage_dir)
    ci.copy_test_logs_to_artifacts(stage_dir, log_dir)
    _, err = capfd.readouterr()
    assert "Unable to copy files" in err
    assert "No such file or directory" in err


def test_setup_spack_repro_version(tmpdir, capfd, last_two_git_commits, monkeypatch):
    c1, c2 = last_two_git_commits
    repro_dir = os.path.join(tmpdir.strpath, "repro")
    spack_dir = os.path.join(repro_dir, "spack")
    os.makedirs(spack_dir)

    prefix_save = spack.paths.prefix
    monkeypatch.setattr(spack.paths, "prefix", "/garbage")

    ret = ci.setup_spack_repro_version(repro_dir, c2, c1)
    _, err = capfd.readouterr()

    assert not ret
    assert "Unable to find the path" in err

    monkeypatch.setattr(spack.paths, "prefix", prefix_save)
    monkeypatch.setattr(spack.util.git, "git", lambda: None)

    ret = ci.setup_spack_repro_version(repro_dir, c2, c1)
    out, err = capfd.readouterr()

    assert not ret
    assert "requires git" in err

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

    monkeypatch.setattr(spack.util.git, "git", lambda: git_cmd)

    git_cmd.check = lambda *a, **k: 1 if len(a) > 2 and a[2] == c2 else 0
    ret = ci.setup_spack_repro_version(repro_dir, c2, c1)
    _, err = capfd.readouterr()

    assert not ret
    assert "Missing commit: {0}".format(c2) in err

    git_cmd.check = lambda *a, **k: 1 if len(a) > 2 and a[2] == c1 else 0
    ret = ci.setup_spack_repro_version(repro_dir, c2, c1)
    _, err = capfd.readouterr()

    assert not ret
    assert "Missing commit: {0}".format(c1) in err

    git_cmd.check = lambda *a, **k: 1 if a[0] == "clone" else 0
    ret = ci.setup_spack_repro_version(repro_dir, c2, c1)
    _, err = capfd.readouterr()

    assert not ret
    assert "Unable to clone" in err

    git_cmd.check = lambda *a, **k: 1 if a[0] == "checkout" else 0
    ret = ci.setup_spack_repro_version(repro_dir, c2, c1)
    _, err = capfd.readouterr()

    assert not ret
    assert "Unable to checkout" in err

    git_cmd.check = lambda *a, **k: 1 if "merge" in a else 0
    ret = ci.setup_spack_repro_version(repro_dir, c2, c1)
    _, err = capfd.readouterr()

    assert not ret
    assert "Unable to merge {0}".format(c1) in err


@pytest.mark.parametrize("obj, proto", [({}, [])])
def test_ci_opt_argument_checking(obj, proto):
    """Check that matches() and subkeys() return False when `proto` is not a dict."""
    assert not ci_opt.matches(obj, proto)
    assert not ci_opt.subkeys(obj, proto)


@pytest.mark.parametrize("yaml", [{"extends": 1}])
def test_ci_opt_add_extends_non_sequence(yaml):
    """Check that add_extends() exits if 'extends' is not a sequence."""
    yaml_copy = yaml.copy()
    ci_opt.add_extends(yaml, None)
    assert yaml == yaml_copy


def test_ci_workarounds():
    fake_root_spec = "x" * 544
    fake_spack_ref = "x" * 40

    common_variables = {"SPACK_COMPILER_ACTION": "NONE", "SPACK_IS_PR_PIPELINE": "False"}

    common_before_script = [
        'git clone "https://github.com/spack/spack"',
        " && ".join(("pushd ./spack", 'git checkout "{ref}"'.format(ref=fake_spack_ref), "popd")),
        '. "./spack/share/spack/setup-env.sh"',
    ]

    def make_build_job(name, deps, stage, use_artifact_buildcache, optimize, use_dependencies):
        variables = common_variables.copy()
        variables["SPACK_JOB_SPEC_PKG_NAME"] = name

        result = {
            "stage": stage,
            "tags": ["tag-0", "tag-1"],
            "artifacts": {
                "paths": ["jobs_scratch_dir", "cdash_report", name + ".spec.json", name],
                "when": "always",
            },
            "retry": {"max": 2, "when": ["always"]},
            "after_script": ['rm -rf "./spack"'],
            "script": ["spack ci rebuild"],
            "image": {"name": "spack/centos7", "entrypoint": [""]},
        }

        if optimize:
            result["extends"] = [".c0", ".c1"]
        else:
            variables["SPACK_ROOT_SPEC"] = fake_root_spec
            result["before_script"] = common_before_script

        result["variables"] = variables

        if use_dependencies:
            result["dependencies"] = list(deps) if use_artifact_buildcache else []
        else:
            result["needs"] = [{"job": dep, "artifacts": use_artifact_buildcache} for dep in deps]

        return {name: result}

    def make_rebuild_index_job(use_artifact_buildcache, optimize, use_dependencies):
        result = {
            "stage": "stage-rebuild-index",
            "script": "spack buildcache update-index --mirror-url s3://mirror",
            "tags": ["tag-0", "tag-1"],
            "image": {"name": "spack/centos7", "entrypoint": [""]},
            "after_script": ['rm -rf "./spack"'],
        }

        if optimize:
            result["extends"] = ".c0"
        else:
            result["before_script"] = common_before_script

        return {"rebuild-index": result}

    def make_factored_jobs(optimize):
        return (
            {
                ".c0": {"before_script": common_before_script},
                ".c1": {"variables": {"SPACK_ROOT_SPEC": fake_root_spec}},
            }
            if optimize
            else {}
        )

    def make_stage_list(num_build_stages):
        return {
            "stages": (
                ["-".join(("stage", str(i))) for i in range(num_build_stages)]
                + ["stage-rebuild-index"]
            )
        }

    def make_yaml_obj(use_artifact_buildcache, optimize, use_dependencies):
        result = {}

        result.update(
            make_build_job(
                "pkg-a", [], "stage-0", use_artifact_buildcache, optimize, use_dependencies
            )
        )

        result.update(
            make_build_job(
                "pkg-b", ["pkg-a"], "stage-1", use_artifact_buildcache, optimize, use_dependencies
            )
        )

        result.update(
            make_build_job(
                "pkg-c",
                ["pkg-a", "pkg-b"],
                "stage-2",
                use_artifact_buildcache,
                optimize,
                use_dependencies,
            )
        )

        result.update(make_rebuild_index_job(use_artifact_buildcache, optimize, use_dependencies))

        result.update(make_factored_jobs(optimize))

        result.update(make_stage_list(3))

        return result

    # test every combination of:
    #     use artifact buildcache: true or false
    #     run optimization pass: true or false
    #     convert needs to dependencies: true or false
    for use_ab in (False, True):
        original = make_yaml_obj(
            use_artifact_buildcache=use_ab, optimize=False, use_dependencies=False
        )

        for opt, deps in itertools.product(*(((False, True),) * 2)):
            # neither optimizing nor converting needs->dependencies
            if not (opt or deps):
                # therefore, nothing to test
                continue

            predicted = make_yaml_obj(
                use_artifact_buildcache=use_ab, optimize=opt, use_dependencies=deps
            )

            actual = original.copy()
            if opt:
                actual = ci_opt.optimizer(actual)
            if deps:
                actual = cinw.needs_to_dependencies(actual)

            predicted = syaml.dump_config(ci_opt.sort_yaml_obj(predicted), default_flow_style=True)
            actual = syaml.dump_config(ci_opt.sort_yaml_obj(actual), default_flow_style=True)

            assert predicted == actual


def test_get_spec_filter_list(mutable_mock_env_path, config, mutable_mock_repo):
    """Test that given an active environment and list of touched pkgs,
    we get the right list of possibly-changed env specs"""
    e1 = ev.create("test")
    e1.add("mpileaks")
    e1.add("hypre")
    e1.concretize()

    """
    Concretizing the above environment results in the following graphs:

    mpileaks -> mpich (provides mpi virtual dep of mpileaks)
             -> callpath -> dyninst -> libelf
                                    -> libdwarf -> libelf
                         -> mpich (provides mpi dep of callpath)

    hypre -> openblas-with-lapack (provides lapack and blas virtual deps of hypre)
    """

    touched = ["libdwarf"]

    # Make sure we return the correct set of possibly affected specs,
    # given a dependent traversal depth and the fact that the touched
    # package is libdwarf.  Passing traversal depth of None or something
    # equal to or larger than the greatest depth in the graph are
    # equivalent and result in traversal of all specs from the touched
    # package to the root.  Passing negative traversal depth results in
    # no spec traversals.  Passing any other number yields differing
    # numbers of possibly affected specs.

    full_set = set(["mpileaks", "mpich", "callpath", "dyninst", "libdwarf", "libelf"])
    empty_set = set([])
    depth_2_set = set(["mpich", "callpath", "dyninst", "libdwarf", "libelf"])
    depth_1_set = set(["dyninst", "libdwarf", "libelf"])
    depth_0_set = set(["libdwarf", "libelf"])

    expectations = {
        None: full_set,
        3: full_set,
        100: full_set,
        -1: empty_set,
        0: depth_0_set,
        1: depth_1_set,
        2: depth_2_set,
    }

    for key, val in expectations.items():
        affected_specs = ci.get_spec_filter_list(e1, touched, dependent_traverse_depth=key)
        affected_pkg_names = set([s.name for s in affected_specs])
        print(f"{key}: {affected_pkg_names}")
        assert affected_pkg_names == val


@pytest.mark.regression("29947")
def test_affected_specs_on_first_concretization(mutable_mock_env_path, mock_packages, config):
    e = ev.create("first_concretization")
    e.add("mpileaks~shared")
    e.add("mpileaks+shared")
    e.concretize()

    affected_specs = spack.ci.get_spec_filter_list(e, ["callpath"])
    mpileaks_specs = [s for s in affected_specs if s.name == "mpileaks"]
    assert len(mpileaks_specs) == 2, e.all_specs()


@pytest.mark.skipif(
    sys.platform == "win32", reason="Reliance on bash script not supported on Windows"
)
def test_ci_process_command(repro_dir):
    result = ci.process_command("help", commands=[], repro_dir=str(repro_dir))
    help_sh = repro_dir / "help.sh"
    assert help_sh.exists() and not result


@pytest.mark.skipif(
    sys.platform == "win32", reason="Reliance on bash script not supported on Windows"
)
def test_ci_process_command_fail(repro_dir, monkeypatch):
    msg = "subprocess wait exception"

    def _fail(self, args):
        raise RuntimeError(msg)

    monkeypatch.setattr(subprocess.Popen, "__init__", _fail)
    with pytest.raises(RuntimeError, match=msg):
        ci.process_command("help", [], str(repro_dir))


def test_ci_create_buildcache(tmpdir, working_env, config, mock_packages, monkeypatch):
    # Monkeypatching ci method tested elsewhere to reduce number of methods
    # that would need to be patched here.
    monkeypatch.setattr(spack.ci, "push_mirror_contents", lambda a, b, c, d: None)

    args = {
        "env": None,
        "buildcache_mirror_url": "file://fake-url",
        "pipeline_mirror_url": "file://fake-url",
    }
    ci.create_buildcache(**args)


def test_ci_run_standalone_tests_missing_requirements(
    tmpdir, working_env, default_mock_concretization, capfd
):
    """This test case checks for failing prerequisite checks."""
    ci.run_standalone_tests()
    err = capfd.readouterr()[1]
    assert "Job spec is required" in err

    args = {"job_spec": default_mock_concretization("printing-package")}
    ci.run_standalone_tests(**args)
    err = capfd.readouterr()[1]
    assert "Reproduction directory is required" in err


@pytest.mark.skipif(
    sys.platform == "win32", reason="Reliance on bash script not supported on Windows"
)
def test_ci_run_standalone_tests_not_installed_junit(
    tmp_path, repro_dir, working_env, default_mock_concretization, mock_test_stage, capfd
):
    log_file = tmp_path / "junit.xml"
    args = {
        "log_file": str(log_file),
        "job_spec": default_mock_concretization("printing-package"),
        "repro_dir": str(repro_dir),
        "fail_fast": True,
    }

    ci.run_standalone_tests(**args)
    err = capfd.readouterr()[1]
    assert "No installed packages" in err
    assert os.path.getsize(log_file) > 0


@pytest.mark.skipif(
    sys.platform == "win32", reason="Reliance on bash script not supported on Windows"
)
def test_ci_run_standalone_tests_not_installed_cdash(
    tmp_path, repro_dir, working_env, default_mock_concretization, mock_test_stage, capfd
):
    """Test run_standalone_tests with cdash and related options."""
    log_file = tmp_path / "junit.xml"
    args = {
        "log_file": str(log_file),
        "job_spec": default_mock_concretization("printing-package"),
        "repro_dir": str(repro_dir),
    }

    # Cover when CDash handler provided (with the log file as well)
    ci_cdash = {
        "url": "file://fake",
        "build-group": "fake-group",
        "project": "ci-unit-testing",
        "site": "fake-site",
    }
    os.environ["SPACK_CDASH_BUILD_NAME"] = "ci-test-build"
    os.environ["SPACK_CDASH_BUILD_STAMP"] = "ci-test-build-stamp"
    os.environ["CI_RUNNER_DESCRIPTION"] = "test-runner"
    handler = ci.CDashHandler(ci_cdash)
    args["cdash"] = handler
    ci.run_standalone_tests(**args)
    out = capfd.readouterr()[0]
    # CDash *and* log file output means log file ignored
    assert "xml option is ignored" in out
    assert "0 passed of 0" in out

    # copy test results (though none)
    artifacts_dir = tmp_path / "artifacts"
    artifacts_dir.mkdir()
    handler.copy_test_results(str(tmp_path), str(artifacts_dir))
    err = capfd.readouterr()[1]
    assert "Unable to copy files" in err
    assert "No such file or directory" in err


def test_ci_skipped_report(tmpdir, mock_packages, config):
    """Test explicit skipping of report as well as CI's 'package' arg."""
    pkg = "trivial-smoke-test"
    spec = spack.spec.Spec(pkg).concretized()
    ci_cdash = {
        "url": "file://fake",
        "build-group": "fake-group",
        "project": "ci-unit-testing",
        "site": "fake-site",
    }
    os.environ["SPACK_CDASH_BUILD_NAME"] = "fake-test-build"
    os.environ["SPACK_CDASH_BUILD_STAMP"] = "ci-test-build-stamp"
    os.environ["CI_RUNNER_DESCRIPTION"] = "test-runner"
    handler = ci.CDashHandler(ci_cdash)
    reason = "Testing skip"
    handler.report_skipped(spec, tmpdir.strpath, reason=reason)

    report = fs.join_path(tmpdir, "{0}_Testing.xml".format(pkg))
    expected = "Skipped {0} package".format(pkg)
    with open(report, "r") as f:
        have = [0, 0]
        for line in f:
            if expected in line:
                have[0] += 1
            elif reason in line:
                have[1] += 1
        assert all(count == 1 for count in have)
