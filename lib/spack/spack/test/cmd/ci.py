# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import filecmp
import json
import os
import shutil
import sys

import jsonschema
import pytest

from llnl.util.filesystem import mkdirp, working_dir

import spack
import spack.binary_distribution
import spack.ci as ci
import spack.compilers as compilers
import spack.config
import spack.environment as ev
import spack.hash_types as ht
import spack.main
import spack.paths as spack_paths
import spack.repo as repo
import spack.util.gpg
import spack.util.spack_yaml as syaml
import spack.util.url as url_util
from spack.schema.buildcache_spec import schema as specfile_schema
from spack.schema.database_index import schema as db_idx_schema
from spack.schema.gitlab_ci import schema as gitlab_ci_schema
from spack.spec import CompilerSpec, Spec
from spack.util.pattern import Bunch

ci_cmd = spack.main.SpackCommand("ci")
env_cmd = spack.main.SpackCommand("env")
mirror_cmd = spack.main.SpackCommand("mirror")
gpg_cmd = spack.main.SpackCommand("gpg")
install_cmd = spack.main.SpackCommand("install")
uninstall_cmd = spack.main.SpackCommand("uninstall")
buildcache_cmd = spack.main.SpackCommand("buildcache")

pytestmark = [
    pytest.mark.skipif(sys.platform == "win32", reason="does not run on windows"),
    pytest.mark.maybeslow,
]


@pytest.fixture()
def ci_base_environment(working_env, tmpdir):
    os.environ["CI_PROJECT_DIR"] = tmpdir.strpath


@pytest.fixture(scope="function")
def mock_git_repo(git, tmpdir):
    """Create a mock git repo with two commits, the last one creating
    a .gitlab-ci.yml"""

    repo_path = tmpdir.join("mockspackrepo").strpath
    mkdirp(repo_path)

    with working_dir(repo_path):
        git("init")

        with open("README.md", "w") as f:
            f.write("# Introduction")

        with open(".gitlab-ci.yml", "w") as f:
            f.write(
                """
testjob:
    script:
        - echo "success"
            """
            )

        git("config", "--local", "user.email", "testing@spack.io")
        git("config", "--local", "user.name", "Spack Testing")

        # initial commit with README
        git("add", "README.md")
        git("-c", "commit.gpgsign=false", "commit", "-m", "initial commit")

        # second commit, adding a .gitlab-ci.yml
        git("add", ".gitlab-ci.yml")
        git("-c", "commit.gpgsign=false", "commit", "-m", "add a .gitlab-ci.yml")

        yield repo_path


def test_specs_staging(config, tmpdir):
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
    builder = repo.MockRepositoryBuilder(tmpdir)
    builder.add_package("g")
    builder.add_package("f")
    builder.add_package("e")
    builder.add_package("d", dependencies=[("f", None, None), ("g", None, None)])
    builder.add_package("c")
    builder.add_package("b", dependencies=[("d", None, None), ("e", None, None)])
    builder.add_package("a", dependencies=[("b", None, None), ("c", None, None)])

    with repo.use_repositories(builder.root):
        spec_a = Spec("a").concretized()

        spec_a_label = ci._spec_deps_key(spec_a)
        spec_b_label = ci._spec_deps_key(spec_a["b"])
        spec_c_label = ci._spec_deps_key(spec_a["c"])
        spec_d_label = ci._spec_deps_key(spec_a["d"])
        spec_e_label = ci._spec_deps_key(spec_a["e"])
        spec_f_label = ci._spec_deps_key(spec_a["f"])
        spec_g_label = ci._spec_deps_key(spec_a["g"])

        spec_labels, dependencies, stages = ci.stage_spec_jobs([spec_a])

        assert len(stages) == 4

        assert len(stages[0]) == 4
        assert spec_c_label in stages[0]
        assert spec_e_label in stages[0]
        assert spec_f_label in stages[0]
        assert spec_g_label in stages[0]

        assert len(stages[1]) == 1
        assert spec_d_label in stages[1]

        assert len(stages[2]) == 1
        assert spec_b_label in stages[2]

        assert len(stages[3]) == 1
        assert spec_a_label in stages[3]


def test_ci_generate_with_env(
    tmpdir,
    mutable_mock_env_path,
    install_mockery,
    mock_packages,
    ci_base_environment,
    mock_binary_index,
):
    """Make sure we can get a .gitlab-ci.yml from an environment file
    which has the gitlab-ci, cdash, and mirrors sections."""
    mirror_url = "https://my.fake.mirror"
    filename = str(tmpdir.join("spack.yaml"))
    with open(filename, "w") as f:
        f.write(
            """\
spack:
  definitions:
    - bootstrap:
      - cmake@3.4.3
    - old-gcc-pkgs:
      - archive-files
      - callpath
      # specify ^openblas-with-lapack to ensure that builtin.mock repo flake8
      # package (which can also provide lapack) is not chosen, as it violates
      # a package-level check which requires exactly one fetch strategy (this
      # is apparently not an issue for other tests that use it).
      - hypre@0.2.15 ^openblas-with-lapack
  specs:
    - matrix:
      - [$old-gcc-pkgs]
  mirrors:
    some-mirror: {0}
  gitlab-ci:
    bootstrap:
      - name: bootstrap
        compiler-agnostic: true
    mappings:
      - match:
          - arch=test-debian6-core2
        runner-attributes:
          tags:
            - donotcare
          image: donotcare
      - match:
          - arch=test-debian6-m1
        runner-attributes:
          tags:
            - donotcare
          image: donotcare
    service-job-attributes:
      image: donotcare
      tags: [donotcare]
  cdash:
    build-group: Not important
    url: https://my.fake.cdash
    project: Not used
    site: Nothing
""".format(
                mirror_url
            )
        )
    with tmpdir.as_cwd():
        env_cmd("create", "test", "./spack.yaml")
        outputfile = str(tmpdir.join(".gitlab-ci.yml"))

        with ev.read("test"):
            ci_cmd("generate", "--output-file", outputfile)

        with open(outputfile) as f:
            contents = f.read()
            yaml_contents = syaml.load(contents)
            found_spec = False
            for ci_key in yaml_contents.keys():
                if "(bootstrap)" in ci_key:
                    found_spec = True
                    assert "cmake" in ci_key
            assert found_spec
            assert "stages" in yaml_contents
            assert len(yaml_contents["stages"]) == 6
            assert yaml_contents["stages"][0] == "stage-0"
            assert yaml_contents["stages"][5] == "stage-rebuild-index"

            assert "rebuild-index" in yaml_contents
            rebuild_job = yaml_contents["rebuild-index"]
            expected = "spack buildcache update-index --keys --mirror-url {0}".format(mirror_url)
            assert rebuild_job["script"][0] == expected

            assert "variables" in yaml_contents
            assert "SPACK_ARTIFACTS_ROOT" in yaml_contents["variables"]
            artifacts_root = yaml_contents["variables"]["SPACK_ARTIFACTS_ROOT"]
            assert artifacts_root == "jobs_scratch_dir"


def _validate_needs_graph(yaml_contents, needs_graph, artifacts):
    for job_name, job_def in yaml_contents.items():
        for needs_def_name, needs_list in needs_graph.items():
            if job_name.startswith(needs_def_name):
                # check job needs against the expected needs definition
                j_needs = job_def["needs"]
                assert all(
                    [
                        job_needs["job"][: job_needs["job"].index("/")] in needs_list
                        for job_needs in j_needs
                    ]
                )
                assert all(
                    [nl in [n["job"][: n["job"].index("/")] for n in j_needs] for nl in needs_list]
                )
                assert all([job_needs["artifacts"] == artifacts for job_needs in j_needs])
                break


def test_ci_generate_bootstrap_gcc(
    tmpdir, working_env, mutable_mock_env_path, install_mockery, mock_packages, ci_base_environment
):
    """Test that we can bootstrap a compiler and use it as the
    compiler for a spec in the environment"""
    filename = str(tmpdir.join("spack.yaml"))
    with open(filename, "w") as f:
        f.write(
            """\
spack:
  definitions:
    - bootstrap:
      - gcc@9.5
      - gcc@9.0
  specs:
    - dyninst%gcc@9.5
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
      - match:
          - arch=test-debian6-aarch64
        runner-attributes:
          tags:
            - donotcare
"""
        )

    needs_graph = {
        "(bootstrap) conflict": [],
        "(bootstrap) gcc": ["(bootstrap) conflict"],
        "(specs) libelf": ["(bootstrap) gcc"],
        "(specs) libdwarf": ["(bootstrap) gcc", "(specs) libelf"],
        "(specs) dyninst": ["(bootstrap) gcc", "(specs) libelf", "(specs) libdwarf"],
    }

    with tmpdir.as_cwd():
        env_cmd("create", "test", "./spack.yaml")
        outputfile = str(tmpdir.join(".gitlab-ci.yml"))

        with ev.read("test"):
            ci_cmd("generate", "--output-file", outputfile)

        with open(outputfile) as f:
            contents = f.read()
            yaml_contents = syaml.load(contents)
            _validate_needs_graph(yaml_contents, needs_graph, False)


def test_ci_generate_bootstrap_artifacts_buildcache(
    tmpdir, working_env, mutable_mock_env_path, install_mockery, mock_packages, ci_base_environment
):
    """Test that we can bootstrap a compiler when artifacts buildcache
    is turned on"""
    filename = str(tmpdir.join("spack.yaml"))
    with open(filename, "w") as f:
        f.write(
            """\
spack:
  definitions:
    - bootstrap:
      - gcc@9.5
  specs:
    - dyninst%gcc@9.5
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
      - match:
          - arch=test-debian6-aarch64
        runner-attributes:
          tags:
            - donotcare
    enable-artifacts-buildcache: True
"""
        )

    needs_graph = {
        "(bootstrap) conflict": [],
        "(bootstrap) gcc": ["(bootstrap) conflict"],
        "(specs) libelf": ["(bootstrap) gcc", "(bootstrap) conflict"],
        "(specs) libdwarf": ["(bootstrap) gcc", "(bootstrap) conflict", "(specs) libelf"],
        "(specs) dyninst": [
            "(bootstrap) gcc",
            "(bootstrap) conflict",
            "(specs) libelf",
            "(specs) libdwarf",
        ],
    }

    with tmpdir.as_cwd():
        env_cmd("create", "test", "./spack.yaml")
        outputfile = str(tmpdir.join(".gitlab-ci.yml"))

        with ev.read("test"):
            ci_cmd("generate", "--output-file", outputfile)

        with open(outputfile) as f:
            contents = f.read()
            yaml_contents = syaml.load(contents)
            _validate_needs_graph(yaml_contents, needs_graph, True)


def test_ci_generate_with_env_missing_section(
    tmpdir,
    working_env,
    mutable_mock_env_path,
    install_mockery,
    mock_packages,
    ci_base_environment,
    mock_binary_index,
):
    """Make sure we get a reasonable message if we omit gitlab-ci section"""
    filename = str(tmpdir.join("spack.yaml"))
    with open(filename, "w") as f:
        f.write(
            """\
spack:
  specs:
    - archive-files
  mirrors:
    some-mirror: https://my.fake.mirror
"""
        )

    expect_out = 'Error: Environment yaml does not have "gitlab-ci" section'

    with tmpdir.as_cwd():
        env_cmd("create", "test", "./spack.yaml")

        with ev.read("test"):
            output = ci_cmd("generate", fail_on_error=False, output=str)
            assert expect_out in output


def test_ci_generate_with_cdash_token(
    tmpdir,
    mutable_mock_env_path,
    install_mockery,
    mock_packages,
    ci_base_environment,
    mock_binary_index,
):
    """Make sure we it doesn't break if we configure cdash"""
    os.environ.update({"SPACK_CDASH_AUTH_TOKEN": "notreallyatokenbutshouldnotmatter"})
    filename = str(tmpdir.join("spack.yaml"))
    with open(filename, "w") as f:
        f.write(
            """\
spack:
  specs:
    - archive-files
  mirrors:
    some-mirror: https://my.fake.mirror
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
"""
        )

    with tmpdir.as_cwd():
        env_cmd("create", "test", "./spack.yaml")

        with ev.read("test"):
            copy_to_file = str(tmpdir.join("backup-ci.yml"))
            output = ci_cmd("generate", "--copy-to", copy_to_file, output=str)
            # That fake token should still have resulted in being unable to
            # register build group with cdash, but the workload should
            # still have been generated.
            expect = "Problem populating buildgroup"
            assert expect in output

            dir_contents = os.listdir(tmpdir.strpath)

            assert "backup-ci.yml" in dir_contents

            orig_file = str(tmpdir.join(".gitlab-ci.yml"))

            assert filecmp.cmp(orig_file, copy_to_file) is True


def test_ci_generate_with_custom_scripts(
    tmpdir,
    working_env,
    mutable_mock_env_path,
    install_mockery,
    mock_packages,
    monkeypatch,
    ci_base_environment,
    mock_binary_index,
):
    """Test use of user-provided scripts"""
    filename = str(tmpdir.join("spack.yaml"))
    with open(filename, "w") as f:
        f.write(
            """\
spack:
  specs:
    - archive-files
  mirrors:
    some-mirror: https://my.fake.mirror
  gitlab-ci:
    mappings:
      - match:
          - archive-files
        runner-attributes:
          tags:
            - donotcare
          variables:
            ONE: plain-string-value
            TWO: ${INTERP_ON_BUILD}
          before_script:
            - mkdir /some/path
            - pushd /some/path
            - git clone ${SPACK_REPO}
            - cd spack
            - git checkout ${SPACK_REF}
            - popd
          script:
            - spack -d ci rebuild
          after_script:
            - rm -rf /some/path/spack
"""
        )

    with tmpdir.as_cwd():
        env_cmd("create", "test", "./spack.yaml")
        outputfile = str(tmpdir.join(".gitlab-ci.yml"))

        with ev.read("test"):
            monkeypatch.setattr(spack.main, "get_version", lambda: "0.15.3")
            ci_cmd("generate", "--output-file", outputfile)

            with open(outputfile) as f:
                contents = f.read()
                yaml_contents = syaml.load(contents)

                found_it = False

                assert "variables" in yaml_contents
                global_vars = yaml_contents["variables"]
                assert "SPACK_VERSION" in global_vars
                assert global_vars["SPACK_VERSION"] == "0.15.3"
                assert "SPACK_CHECKOUT_VERSION" in global_vars
                assert global_vars["SPACK_CHECKOUT_VERSION"] == "v0.15.3"

                for ci_key in yaml_contents.keys():
                    ci_obj = yaml_contents[ci_key]
                    if "archive-files" in ci_key:
                        # Ensure we have variables, possibly interpolated
                        assert "variables" in ci_obj
                        var_d = ci_obj["variables"]
                        assert "ONE" in var_d
                        assert var_d["ONE"] == "plain-string-value"
                        assert "TWO" in var_d
                        assert var_d["TWO"] == "${INTERP_ON_BUILD}"

                        # Ensure we have scripts verbatim
                        assert "before_script" in ci_obj
                        before_script = ci_obj["before_script"]
                        assert before_script[0] == "mkdir /some/path"
                        assert before_script[1] == "pushd /some/path"
                        assert before_script[2] == "git clone ${SPACK_REPO}"
                        assert before_script[3] == "cd spack"
                        assert before_script[4] == "git checkout ${SPACK_REF}"
                        assert before_script[5] == "popd"

                        assert "script" in ci_obj
                        assert ci_obj["script"][0] == "spack -d ci rebuild"

                        assert "after_script" in ci_obj
                        after_script = ci_obj["after_script"][0]
                        assert after_script == "rm -rf /some/path/spack"

                        found_it = True

            assert found_it


def test_ci_generate_pkg_with_deps(
    tmpdir, working_env, mutable_mock_env_path, install_mockery, mock_packages, ci_base_environment
):
    """Test pipeline generation for a package w/ dependencies"""
    filename = str(tmpdir.join("spack.yaml"))
    with open(filename, "w") as f:
        f.write(
            """\
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
"""
        )

    with tmpdir.as_cwd():
        env_cmd("create", "test", "./spack.yaml")
        outputfile = str(tmpdir.join(".gitlab-ci.yml"))

        with ev.read("test"):
            ci_cmd("generate", "--output-file", outputfile)

        with open(outputfile) as f:
            contents = f.read()
            yaml_contents = syaml.load(contents)
            found = []
            for ci_key in yaml_contents.keys():
                ci_obj = yaml_contents[ci_key]
                if "dependency-install" in ci_key:
                    assert "stage" in ci_obj
                    assert ci_obj["stage"] == "stage-0"
                    found.append("dependency-install")
                if "flatten-deps" in ci_key:
                    assert "stage" in ci_obj
                    assert ci_obj["stage"] == "stage-1"
                    found.append("flatten-deps")

            assert "flatten-deps" in found
            assert "dependency-install" in found


def test_ci_generate_for_pr_pipeline(
    tmpdir,
    working_env,
    mutable_mock_env_path,
    install_mockery,
    mock_packages,
    monkeypatch,
    ci_base_environment,
):
    """Test that PR pipelines do not include a final stage job for
    rebuilding the mirror index, even if that job is specifically
    configured"""
    os.environ.update(
        {"SPACK_PIPELINE_TYPE": "spack_pull_request", "SPACK_PR_BRANCH": "fake-test-branch"}
    )
    filename = str(tmpdir.join("spack.yaml"))
    with open(filename, "w") as f:
        f.write(
            """\
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
    service-job-attributes:
      image: donotcare
      tags: [donotcare]
    rebuild-index: False
"""
        )

    monkeypatch.setattr(spack.ci, "SHARED_PR_MIRROR_URL", "https://fake.shared.pr.mirror")

    with tmpdir.as_cwd():
        env_cmd("create", "test", "./spack.yaml")
        outputfile = str(tmpdir.join(".gitlab-ci.yml"))

        with ev.read("test"):
            ci_cmd("generate", "--output-file", outputfile)

        with open(outputfile) as f:
            contents = f.read()
            yaml_contents = syaml.load(contents)

            assert "rebuild-index" not in yaml_contents

            assert "variables" in yaml_contents
            pipeline_vars = yaml_contents["variables"]
            assert "SPACK_PIPELINE_TYPE" in pipeline_vars
            assert pipeline_vars["SPACK_PIPELINE_TYPE"] == "spack_pull_request"


def test_ci_generate_with_external_pkg(
    tmpdir,
    working_env,
    mutable_mock_env_path,
    install_mockery,
    mock_packages,
    monkeypatch,
    ci_base_environment,
):
    """Make sure we do not generate jobs for external pkgs"""
    filename = str(tmpdir.join("spack.yaml"))
    with open(filename, "w") as f:
        f.write(
            """\
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
"""
        )

    with tmpdir.as_cwd():
        env_cmd("create", "test", "./spack.yaml")
        outputfile = str(tmpdir.join(".gitlab-ci.yml"))

        with ev.read("test"):
            ci_cmd("generate", "--output-file", outputfile)

        with open(outputfile) as f:
            yaml_contents = syaml.load(f)

        # Check that the "externaltool" package was not erroneously staged
        assert not any("externaltool" in key for key in yaml_contents)


def test_ci_rebuild_missing_config(tmpdir, working_env, mutable_mock_env_path):
    spack_yaml_contents = """
spack:
  specs:
    - archive-files
"""

    filename = str(tmpdir.join("spack.yaml"))
    with open(filename, "w") as f:
        f.write(spack_yaml_contents)

    with tmpdir.as_cwd():
        env_cmd("create", "test", "./spack.yaml")
        env_cmd("activate", "--without-view", "--sh", "test")
        out = ci_cmd("rebuild", fail_on_error=False)
        assert "env containing gitlab-ci" in out

        env_cmd("deactivate")


def _signing_key():
    signing_key_dir = spack_paths.mock_gpg_keys_path
    signing_key_path = os.path.join(signing_key_dir, "package-signing-key")
    with open(signing_key_path) as fd:
        key = fd.read()
    return key


def create_rebuild_env(tmpdir, pkg_name, broken_tests=False):
    working_dir = tmpdir.join("working_dir")

    log_dir = os.path.join(working_dir.strpath, "logs")
    repro_dir = os.path.join(working_dir.strpath, "repro")
    test_dir = os.path.join(working_dir.strpath, "test")
    env_dir = working_dir.join("concrete_env")

    mirror_dir = working_dir.join("mirror")
    mirror_url = url_util.path_to_file_url(mirror_dir.strpath)

    broken_specs_path = os.path.join(working_dir.strpath, "naughty-list")
    broken_specs_url = url_util.path_to_file_url(broken_specs_path)
    temp_storage_url = "file:///path/to/per/pipeline/storage"

    broken_tests_packages = [pkg_name] if broken_tests else []

    ci_job_url = "https://some.domain/group/project/-/jobs/42"
    ci_pipeline_url = "https://some.domain/group/project/-/pipelines/7"

    spack_yaml_contents = """
spack:
  definitions:
    - packages: [{0}]
  specs:
    - $packages
  mirrors:
    test-mirror: {1}
  gitlab-ci:
    broken-specs-url: {2}
    broken-tests-packages: {3}
    temporary-storage-url-prefix: {4}
    mappings:
     - match:
         - {0}
       runner-attributes:
         tags:
           - donotcare
         image: donotcare
  cdash:
    build-group: Not important
    url: https://my.fake.cdash
    project: Not used
    site: Nothing
""".format(
        pkg_name, mirror_url, broken_specs_url, broken_tests_packages, temp_storage_url
    )

    filename = str(tmpdir.join("spack.yaml"))
    with open(filename, "w") as f:
        f.write(spack_yaml_contents)

    with tmpdir.as_cwd():
        env_cmd("create", "test", "./spack.yaml")
        with ev.read("test") as env:
            with env.write_transaction():
                env.concretize()
                env.write()

            if not os.path.exists(env_dir.strpath):
                os.makedirs(env_dir.strpath)

            shutil.copyfile(env.manifest_path, os.path.join(env_dir.strpath, "spack.yaml"))
            shutil.copyfile(env.lock_path, os.path.join(env_dir.strpath, "spack.lock"))

            root_spec_dag_hash = None

            for h, s in env.specs_by_hash.items():
                if s.name == pkg_name:
                    root_spec_dag_hash = h

            assert root_spec_dag_hash

    return Bunch(
        broken_spec_file=os.path.join(broken_specs_path, root_spec_dag_hash),
        ci_job_url=ci_job_url,
        ci_pipeline_url=ci_pipeline_url,
        env_dir=env_dir,
        log_dir=log_dir,
        mirror_dir=mirror_dir,
        mirror_url=mirror_url,
        repro_dir=repro_dir,
        root_spec_dag_hash=root_spec_dag_hash,
        test_dir=test_dir,
        working_dir=working_dir,
    )


def activate_rebuild_env(tmpdir, pkg_name, rebuild_env):
    env_cmd("activate", "--without-view", "--sh", "-d", ".")

    # Create environment variables as gitlab would do it
    os.environ.update(
        {
            "SPACK_ARTIFACTS_ROOT": rebuild_env.working_dir.strpath,
            "SPACK_JOB_LOG_DIR": rebuild_env.log_dir,
            "SPACK_JOB_REPRO_DIR": rebuild_env.repro_dir,
            "SPACK_JOB_TEST_DIR": rebuild_env.test_dir,
            "SPACK_LOCAL_MIRROR_DIR": rebuild_env.mirror_dir.strpath,
            "SPACK_CONCRETE_ENV_DIR": rebuild_env.env_dir.strpath,
            "CI_PIPELINE_ID": "7192",
            "SPACK_SIGNING_KEY": _signing_key(),
            "SPACK_JOB_SPEC_DAG_HASH": rebuild_env.root_spec_dag_hash,
            "SPACK_JOB_SPEC_PKG_NAME": pkg_name,
            "SPACK_COMPILER_ACTION": "NONE",
            "SPACK_CDASH_BUILD_NAME": "(specs) {0}".format(pkg_name),
            "SPACK_REMOTE_MIRROR_URL": rebuild_env.mirror_url,
            "SPACK_PIPELINE_TYPE": "spack_protected_branch",
            "CI_JOB_URL": rebuild_env.ci_job_url,
            "CI_PIPELINE_URL": rebuild_env.ci_pipeline_url,
            "CI_PROJECT_DIR": tmpdir.join("ci-project").strpath,
        }
    )


@pytest.mark.parametrize("broken_tests", [True, False])
def test_ci_rebuild_mock_success(
    tmpdir,
    config,
    working_env,
    mutable_mock_env_path,
    install_mockery,
    mock_gnupghome,
    mock_stage,
    mock_fetch,
    mock_binary_index,
    monkeypatch,
    broken_tests,
):
    pkg_name = "archive-files"
    rebuild_env = create_rebuild_env(tmpdir, pkg_name, broken_tests)

    monkeypatch.setattr(spack.cmd.ci, "SPACK_COMMAND", "echo")
    monkeypatch.setattr(spack.cmd.ci, "MAKE_COMMAND", "echo")

    with rebuild_env.env_dir.as_cwd():
        activate_rebuild_env(tmpdir, pkg_name, rebuild_env)

        out = ci_cmd("rebuild", "--tests", fail_on_error=False)

        # We didn"t really run the build so build output file(s) are missing
        assert "Unable to copy files" in out
        assert "No such file or directory" in out

        if broken_tests:
            # We generate a skipped tests report in this case
            assert "Unable to run stand-alone tests" in out
        else:
            # No installation means no package to test and no test log to copy
            assert "Cannot copy test logs" in out


@pytest.mark.skip(reason="fails intermittently and covered by gitlab ci")
def test_ci_rebuild(
    tmpdir,
    working_env,
    mutable_mock_env_path,
    install_mockery,
    mock_packages,
    monkeypatch,
    mock_gnupghome,
    mock_fetch,
    ci_base_environment,
    mock_binary_index,
):
    pkg_name = "archive-files"
    rebuild_env = create_rebuild_env(tmpdir, pkg_name)

    # Create job directories to be removed before processing (for coverage)
    os.makedirs(rebuild_env.log_dir)
    os.makedirs(rebuild_env.repro_dir)
    os.makedirs(rebuild_env.test_dir)

    with rebuild_env.env_dir.as_cwd():
        activate_rebuild_env(tmpdir, pkg_name, rebuild_env)

        ci_cmd("rebuild", "--tests", fail_on_error=False)

    monkeypatch.setattr(spack.cmd.ci, "SPACK_COMMAND", "notcommand")
    monkeypatch.setattr(spack.cmd.ci, "MAKE_COMMAND", "notcommand")
    monkeypatch.setattr(spack.cmd.ci, "INSTALL_FAIL_CODE", 127)

    with rebuild_env.env_dir.as_cwd():
        activate_rebuild_env(tmpdir, pkg_name, rebuild_env)

        expected_repro_files = [
            "install.sh",
            "root.json",
            "archive-files.json",
            "spack.yaml",
            "spack.lock",
        ]
        repro_files = os.listdir(rebuild_env.repro_dir)
        assert all([f in repro_files for f in expected_repro_files])

        install_script_path = os.path.join(rebuild_env.repro_dir, "install.sh")
        install_line = None
        with open(install_script_path) as fd:
            for line in fd:
                if line.startswith('"notcommand"'):
                    install_line = line

        assert install_line

        def mystrip(s):
            return s.strip('"').rstrip("\n").rstrip('"')

        install_parts = [mystrip(s) for s in install_line.split(" ")]

        assert "--keep-stage" in install_parts
        assert "--no-check-signature" not in install_parts
        assert "-f" in install_parts
        flag_index = install_parts.index("-f")
        assert "archive-files.json" in install_parts[flag_index + 1]

        with open(rebuild_env.broken_spec_file) as fd:
            broken_spec_content = fd.read()
            assert rebuild_env.ci_job_url in broken_spec_content
            assert rebuild_env.ci_pipeline_url in broken_spec_content

        # Ensure also produce CDash output for skipped (or notrun) tests
        test_files = os.listdir(rebuild_env.test_dir)
        with open(os.path.join(rebuild_env.test_dir, test_files[0]), "r") as f:
            have = False
            for line in f:
                if "notrun" in line:
                    have = True
                    break
            assert have

        env_cmd("deactivate")


def test_ci_nothing_to_rebuild(
    tmpdir,
    working_env,
    mutable_mock_env_path,
    install_mockery,
    mock_packages,
    monkeypatch,
    mock_fetch,
    ci_base_environment,
    mock_binary_index,
):
    working_dir = tmpdir.join("working_dir")

    mirror_dir = working_dir.join("mirror")
    mirror_url = "file://{0}".format(mirror_dir.strpath)

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
""".format(
        mirror_url
    )

    install_cmd("archive-files")
    buildcache_cmd("create", "-a", "-f", "-u", "--mirror-url", mirror_url, "archive-files")

    filename = str(tmpdir.join("spack.yaml"))
    with open(filename, "w") as f:
        f.write(spack_yaml_contents)

    with tmpdir.as_cwd():
        env_cmd("create", "test", "./spack.yaml")
        with ev.read("test") as env:
            env.concretize()
            root_spec_dag_hash = None

            for h, s in env.specs_by_hash.items():
                if s.name == "archive-files":
                    root_spec_dag_hash = h

            # Create environment variables as gitlab would do it
            os.environ.update(
                {
                    "SPACK_ARTIFACTS_ROOT": working_dir.strpath,
                    "SPACK_JOB_LOG_DIR": "log_dir",
                    "SPACK_JOB_REPRO_DIR": "repro_dir",
                    "SPACK_JOB_TEST_DIR": "test_dir",
                    "SPACK_LOCAL_MIRROR_DIR": mirror_dir.strpath,
                    "SPACK_CONCRETE_ENV_DIR": tmpdir.strpath,
                    "SPACK_JOB_SPEC_DAG_HASH": root_spec_dag_hash,
                    "SPACK_JOB_SPEC_PKG_NAME": "archive-files",
                    "SPACK_COMPILER_ACTION": "NONE",
                    "SPACK_REMOTE_MIRROR_URL": mirror_url,
                }
            )

            def fake_dl_method(spec, *args, **kwargs):
                print("fake download buildcache {0}".format(spec.name))

            monkeypatch.setattr(spack.binary_distribution, "download_single_spec", fake_dl_method)

            ci_out = ci_cmd("rebuild", output=str)

            assert "No need to rebuild archive-files" in ci_out
            assert "fake download buildcache archive-files" in ci_out

            env_cmd("deactivate")


def test_ci_generate_mirror_override(
    tmpdir,
    mutable_mock_env_path,
    install_mockery_mutable_config,
    mock_packages,
    mock_fetch,
    mock_stage,
    mock_binary_index,
    ci_base_environment,
):
    """Ensure that protected pipelines using --buildcache-destination do not
    skip building specs that are not in the override mirror when they are
    found in the main mirror."""
    os.environ.update({"SPACK_PIPELINE_TYPE": "spack_protected_branch"})

    working_dir = tmpdir.join("working_dir")

    mirror_dir = working_dir.join("mirror")
    mirror_url = "file://{0}".format(mirror_dir.strpath)

    spack_yaml_contents = """
spack:
 definitions:
   - packages: [patchelf]
 specs:
   - $packages
 mirrors:
   test-mirror: {0}
 gitlab-ci:
   mappings:
     - match:
         - patchelf
       runner-attributes:
         tags:
           - donotcare
         image: donotcare
   service-job-attributes:
     tags:
       - nonbuildtag
     image: basicimage
""".format(
        mirror_url
    )

    filename = str(tmpdir.join("spack.yaml"))
    with open(filename, "w") as f:
        f.write(spack_yaml_contents)

    with tmpdir.as_cwd():
        env_cmd("create", "test", "./spack.yaml")
        first_ci_yaml = str(tmpdir.join(".gitlab-ci-1.yml"))
        second_ci_yaml = str(tmpdir.join(".gitlab-ci-2.yml"))
        with ev.read("test"):
            install_cmd()
            buildcache_cmd("create", "-u", "--mirror-url", mirror_url, "patchelf")
            buildcache_cmd("update-index", "--mirror-url", mirror_url, output=str)

            # This generate should not trigger a rebuild of patchelf, since it's in
            # the main mirror referenced in the environment.
            ci_cmd("generate", "--check-index-only", "--output-file", first_ci_yaml)

            # Because we used a mirror override (--buildcache-destination) on a
            # spack protected pipeline, we expect to only look in the override
            # mirror for the spec, and thus the patchelf job should be generated in
            # this pipeline
            ci_cmd(
                "generate",
                "--check-index-only",
                "--output-file",
                second_ci_yaml,
                "--buildcache-destination",
                "file:///mirror/not/exist",
            )

        with open(first_ci_yaml) as fd1:
            first_yaml = fd1.read()
            assert "no-specs-to-rebuild" in first_yaml

        with open(second_ci_yaml) as fd2:
            second_yaml = fd2.read()
            assert "no-specs-to-rebuild" not in second_yaml


@pytest.mark.disable_clean_stage_check
def test_push_mirror_contents(
    tmpdir,
    mutable_mock_env_path,
    install_mockery_mutable_config,
    mock_packages,
    mock_fetch,
    mock_stage,
    mock_gnupghome,
    ci_base_environment,
    mock_binary_index,
):
    working_dir = tmpdir.join("working_dir")

    mirror_dir = working_dir.join("mirror")
    mirror_url = url_util.path_to_file_url(mirror_dir.strpath)

    ci.import_signing_key(_signing_key())

    spack_yaml_contents = """
spack:
 definitions:
   - packages: [patchelf]
 specs:
   - $packages
 mirrors:
   test-mirror: {0}
 gitlab-ci:
   enable-artifacts-buildcache: True
   mappings:
     - match:
         - patchelf
       runner-attributes:
         tags:
           - donotcare
         image: donotcare
   service-job-attributes:
     tags:
       - nonbuildtag
     image: basicimage
""".format(
        mirror_url
    )

    filename = str(tmpdir.join("spack.yaml"))
    with open(filename, "w") as f:
        f.write(spack_yaml_contents)

    with tmpdir.as_cwd():
        env_cmd("create", "test", "./spack.yaml")
        with ev.read("test") as env:
            concrete_spec = Spec("patchelf").concretized()
            spec_json = concrete_spec.to_json(hash=ht.dag_hash)
            json_path = str(tmpdir.join("spec.json"))
            with open(json_path, "w") as ypfd:
                ypfd.write(spec_json)

            install_cmd("--add", "--keep-stage", json_path)

            # env, spec, json_path, mirror_url, build_id, sign_binaries
            ci.push_mirror_contents(env, json_path, mirror_url, True)

            buildcache_path = os.path.join(mirror_dir.strpath, "build_cache")

            # Now test the --prune-dag (default) option of spack ci generate
            mirror_cmd("add", "test-ci", mirror_url)

            outputfile_pruned = str(tmpdir.join("pruned_pipeline.yml"))
            ci_cmd("generate", "--output-file", outputfile_pruned)

            with open(outputfile_pruned) as f:
                contents = f.read()
                yaml_contents = syaml.load(contents)
                assert "no-specs-to-rebuild" in yaml_contents
                # Make sure there are no other spec jobs or rebuild-index
                assert len(yaml_contents.keys()) == 1
                the_elt = yaml_contents["no-specs-to-rebuild"]
                assert "tags" in the_elt
                assert "nonbuildtag" in the_elt["tags"]
                assert "image" in the_elt
                assert the_elt["image"] == "basicimage"

            outputfile_not_pruned = str(tmpdir.join("unpruned_pipeline.yml"))
            ci_cmd("generate", "--no-prune-dag", "--output-file", outputfile_not_pruned)

            # Test the --no-prune-dag option of spack ci generate
            with open(outputfile_not_pruned) as f:
                contents = f.read()
                yaml_contents = syaml.load(contents)

                found_spec_job = False

                for ci_key in yaml_contents.keys():
                    if "(specs) patchelf" in ci_key:
                        the_elt = yaml_contents[ci_key]
                        assert "variables" in the_elt
                        job_vars = the_elt["variables"]
                        assert "SPACK_SPEC_NEEDS_REBUILD" in job_vars
                        assert job_vars["SPACK_SPEC_NEEDS_REBUILD"] == "False"
                        found_spec_job = True

                assert found_spec_job

            mirror_cmd("rm", "test-ci")

            # Test generating buildcache index while we have bin mirror
            buildcache_cmd("update-index", "--mirror-url", mirror_url)
            index_path = os.path.join(buildcache_path, "index.json")
            with open(index_path) as idx_fd:
                index_object = json.load(idx_fd)
                jsonschema.validate(index_object, db_idx_schema)

            # Now that index is regenerated, validate "buildcache list" output
            buildcache_list_output = buildcache_cmd("list", output=str)
            assert "patchelf" in buildcache_list_output
            # Also test buildcache_spec schema
            bc_files_list = os.listdir(buildcache_path)
            for file_name in bc_files_list:
                if file_name.endswith(".spec.json.sig"):
                    spec_json_path = os.path.join(buildcache_path, file_name)
                    with open(spec_json_path) as json_fd:
                        json_object = Spec.extract_json_from_clearsig(json_fd.read())
                        jsonschema.validate(json_object, specfile_schema)

            logs_dir = working_dir.join("logs_dir")
            if not os.path.exists(logs_dir.strpath):
                os.makedirs(logs_dir.strpath)

            ci.copy_stage_logs_to_artifacts(concrete_spec, logs_dir.strpath)

            logs_dir_list = os.listdir(logs_dir.strpath)

            assert "spack-build-out.txt" in logs_dir_list

            # Also just make sure that if something goes wrong with the
            # stage logs copy, no exception is thrown
            ci.copy_stage_logs_to_artifacts(concrete_spec, None)
            ci.copy_stage_logs_to_artifacts(None, logs_dir.strpath)

            dl_dir = working_dir.join("download_dir")
            if not os.path.exists(dl_dir.strpath):
                os.makedirs(dl_dir.strpath)
            buildcache_cmd("download", "--spec-file", json_path, "--path", dl_dir.strpath)
            dl_dir_list = os.listdir(dl_dir.strpath)

            assert len(dl_dir_list) == 2


def test_push_mirror_contents_exceptions(monkeypatch, capsys):
    def failing_access(*args, **kwargs):
        raise Exception("Error: Access Denied")

    monkeypatch.setattr(spack.ci, "_push_mirror_contents", failing_access)

    # Input doesn't matter, as wwe are faking exceptional output
    url = "fakejunk"
    ci.push_mirror_contents(None, None, url, None)

    captured = capsys.readouterr()
    std_out = captured[0]
    expect_msg = "Permission problem writing to {0}".format(url)

    assert expect_msg in std_out


@pytest.mark.parametrize("match_behavior", ["first", "merge"])
def test_ci_generate_override_runner_attrs(
    tmpdir,
    mutable_mock_env_path,
    install_mockery,
    mock_packages,
    monkeypatch,
    ci_base_environment,
    match_behavior,
):
    """Test that we get the behavior we want with respect to the provision
    of runner attributes like tags, variables, and scripts, both when we
    inherit them from the top level, as well as when we override one or
    more at the runner level"""
    filename = str(tmpdir.join("spack.yaml"))
    with open(filename, "w") as f:
        f.write(
            """\
spack:
  specs:
    - flatten-deps
    - a
  mirrors:
    some-mirror: https://my.fake.mirror
  gitlab-ci:
    tags:
      - toplevel
      - toplevel2
    variables:
      ONE: toplevelvarone
      TWO: toplevelvartwo
    before_script:
      - pre step one
      - pre step two
    script:
      - main step
    after_script:
      - post step one
    match_behavior: {0}
    mappings:
      - match:
          - flatten-deps
        runner-attributes:
          tags:
            - specific-one
          variables:
            THREE: specificvarthree
      - match:
          - dependency-install
      - match:
          - a
        remove-attributes:
          tags:
            - toplevel2
        runner-attributes:
          tags:
            - specific-a
          variables:
            ONE: specificvarone
            TWO: specificvartwo
          before_script:
            - custom pre step one
          script:
            - custom main step
          after_script:
            - custom post step one
      - match:
          - a
        runner-attributes:
          tags:
            - specific-a-2
    service-job-attributes:
      image: donotcare
      tags: [donotcare]
""".format(
                match_behavior
            )
        )

    with tmpdir.as_cwd():
        env_cmd("create", "test", "./spack.yaml")
        outputfile = str(tmpdir.join(".gitlab-ci.yml"))

        with ev.read("test"):
            monkeypatch.setattr(spack.main, "get_version", lambda: "0.15.3-416-12ad69eb1")
            ci_cmd("generate", "--output-file", outputfile)

        with open(outputfile) as f:
            contents = f.read()
            yaml_contents = syaml.load(contents)

            assert "variables" in yaml_contents
            global_vars = yaml_contents["variables"]
            assert "SPACK_VERSION" in global_vars
            assert global_vars["SPACK_VERSION"] == "0.15.3-416-12ad69eb1"
            assert "SPACK_CHECKOUT_VERSION" in global_vars
            assert global_vars["SPACK_CHECKOUT_VERSION"] == "12ad69eb1"

            for ci_key in yaml_contents.keys():
                if "(specs) b" in ci_key:
                    assert False
                if "(specs) a" in ci_key:
                    # Make sure a's attributes override variables, and all the
                    # scripts.  Also, make sure the 'toplevel' tag doesn't
                    # appear twice, but that a's specific extra tag does appear
                    the_elt = yaml_contents[ci_key]
                    assert the_elt["variables"]["ONE"] == "specificvarone"
                    assert the_elt["variables"]["TWO"] == "specificvartwo"
                    assert "THREE" not in the_elt["variables"]
                    assert len(the_elt["tags"]) == (2 if match_behavior == "first" else 3)
                    assert "specific-a" in the_elt["tags"]
                    if match_behavior == "merge":
                        assert "specific-a-2" in the_elt["tags"]
                    assert "toplevel" in the_elt["tags"]
                    assert "toplevel2" not in the_elt["tags"]
                    assert len(the_elt["before_script"]) == 1
                    assert the_elt["before_script"][0] == "custom pre step one"
                    assert len(the_elt["script"]) == 1
                    assert the_elt["script"][0] == "custom main step"
                    assert len(the_elt["after_script"]) == 1
                    assert the_elt["after_script"][0] == "custom post step one"
                if "(specs) dependency-install" in ci_key:
                    # Since the dependency-install match omits any
                    # runner-attributes, make sure it inherited all the
                    # top-level attributes.
                    the_elt = yaml_contents[ci_key]
                    assert the_elt["variables"]["ONE"] == "toplevelvarone"
                    assert the_elt["variables"]["TWO"] == "toplevelvartwo"
                    assert "THREE" not in the_elt["variables"]
                    assert len(the_elt["tags"]) == 2
                    assert "toplevel" in the_elt["tags"]
                    assert "toplevel2" in the_elt["tags"]
                    assert len(the_elt["before_script"]) == 2
                    assert the_elt["before_script"][0] == "pre step one"
                    assert the_elt["before_script"][1] == "pre step two"
                    assert len(the_elt["script"]) == 1
                    assert the_elt["script"][0] == "main step"
                    assert len(the_elt["after_script"]) == 1
                    assert the_elt["after_script"][0] == "post step one"
                if "(specs) flatten-deps" in ci_key:
                    # The flatten-deps match specifies that we keep the two
                    # top level variables, but add a third specifc one.  It
                    # also adds a custom tag which should be combined with
                    # the top-level tag.
                    the_elt = yaml_contents[ci_key]
                    assert the_elt["variables"]["ONE"] == "toplevelvarone"
                    assert the_elt["variables"]["TWO"] == "toplevelvartwo"
                    assert the_elt["variables"]["THREE"] == "specificvarthree"
                    assert len(the_elt["tags"]) == 3
                    assert "specific-one" in the_elt["tags"]
                    assert "toplevel" in the_elt["tags"]
                    assert "toplevel2" in the_elt["tags"]
                    assert len(the_elt["before_script"]) == 2
                    assert the_elt["before_script"][0] == "pre step one"
                    assert the_elt["before_script"][1] == "pre step two"
                    assert len(the_elt["script"]) == 1
                    assert the_elt["script"][0] == "main step"
                    assert len(the_elt["after_script"]) == 1
                    assert the_elt["after_script"][0] == "post step one"


def test_ci_generate_with_workarounds(
    tmpdir, mutable_mock_env_path, install_mockery, mock_packages, monkeypatch, ci_base_environment
):
    """Make sure the post-processing cli workarounds do what they should"""
    filename = str(tmpdir.join("spack.yaml"))
    with open(filename, "w") as f:
        f.write(
            """\
spack:
  specs:
    - callpath%gcc@9.5
  mirrors:
    some-mirror: https://my.fake.mirror
  gitlab-ci:
    mappings:
      - match: ['%gcc@9.5']
        runner-attributes:
          tags:
            - donotcare
          image: donotcare
    enable-artifacts-buildcache: true
"""
        )

    with tmpdir.as_cwd():
        env_cmd("create", "test", "./spack.yaml")
        outputfile = str(tmpdir.join(".gitlab-ci.yml"))

        with ev.read("test"):
            ci_cmd("generate", "--output-file", outputfile, "--dependencies")

            with open(outputfile) as f:
                contents = f.read()
                yaml_contents = syaml.load(contents)

                found_one = False

                for ci_key in yaml_contents.keys():
                    if ci_key.startswith("(specs) "):
                        found_one = True
                        job_obj = yaml_contents[ci_key]
                        assert "needs" not in job_obj
                        assert "dependencies" in job_obj

                assert found_one is True


@pytest.mark.disable_clean_stage_check
def test_ci_rebuild_index(
    tmpdir,
    working_env,
    mutable_mock_env_path,
    install_mockery,
    mock_packages,
    mock_fetch,
    mock_stage,
):
    working_dir = tmpdir.join("working_dir")

    mirror_dir = working_dir.join("mirror")
    mirror_url = "file://{0}".format(mirror_dir.strpath)

    spack_yaml_contents = """
spack:
 specs:
   - callpath
 mirrors:
   test-mirror: {0}
 gitlab-ci:
   mappings:
     - match:
         - patchelf
       runner-attributes:
         tags:
           - donotcare
         image: donotcare
""".format(
        mirror_url
    )

    filename = str(tmpdir.join("spack.yaml"))
    with open(filename, "w") as f:
        f.write(spack_yaml_contents)

    with tmpdir.as_cwd():
        env_cmd("create", "test", "./spack.yaml")
        with ev.read("test"):
            concrete_spec = Spec("callpath").concretized()
            spec_json = concrete_spec.to_json(hash=ht.dag_hash)
            json_path = str(tmpdir.join("spec.json"))
            with open(json_path, "w") as ypfd:
                ypfd.write(spec_json)

            install_cmd("--add", "--keep-stage", "-f", json_path)
            buildcache_cmd("create", "-u", "-a", "-f", "--mirror-url", mirror_url, "callpath")
            ci_cmd("rebuild-index")

            buildcache_path = os.path.join(mirror_dir.strpath, "build_cache")
            index_path = os.path.join(buildcache_path, "index.json")
            with open(index_path) as idx_fd:
                index_object = json.load(idx_fd)
                jsonschema.validate(index_object, db_idx_schema)


def test_ci_generate_bootstrap_prune_dag(
    install_mockery_mutable_config,
    mock_packages,
    mock_fetch,
    mock_archive,
    mutable_config,
    monkeypatch,
    tmpdir,
    mutable_mock_env_path,
    ci_base_environment,
):
    """Test compiler bootstrapping with DAG pruning.  Specifically, make
    sure that if we detect the bootstrapped compiler needs to be rebuilt,
    we ensure the spec we want to build with that compiler is scheduled
    for rebuild as well."""

    # Create a temp mirror directory for buildcache usage
    mirror_dir = tmpdir.join("mirror_dir")
    mirror_url = "file://{0}".format(mirror_dir.strpath)

    # Install a compiler, because we want to put it in a buildcache
    install_cmd("gcc@12.2.0%gcc@10.2.1")

    # Put installed compiler in the buildcache
    buildcache_cmd("create", "-u", "-a", "-f", "-d", mirror_dir.strpath, "gcc@12.2.0%gcc@10.2.1")

    # Now uninstall the compiler
    uninstall_cmd("-y", "gcc@12.2.0%gcc@10.2.1")

    monkeypatch.setattr(spack.concretize.Concretizer, "check_for_compiler_existence", False)
    spack.config.set("config:install_missing_compilers", True)
    assert CompilerSpec("gcc@12.2.0") not in compilers.all_compiler_specs()

    # Configure the mirror where we put that buildcache w/ the compiler
    mirror_cmd("add", "test-mirror", mirror_url)

    install_cmd("--no-check-signature", "b%gcc@12.2.0")

    # Put spec built with installed compiler in the buildcache
    buildcache_cmd("create", "-u", "-a", "-f", "-d", mirror_dir.strpath, "b%gcc@12.2.0")

    # Now uninstall the spec
    uninstall_cmd("-y", "b%gcc@12.2.0")

    filename = str(tmpdir.join("spack.yaml"))
    with open(filename, "w") as f:
        f.write(
            """\
spack:
  definitions:
    - bootstrap:
      - gcc@12.2.0%gcc@10.2.1
  specs:
    - b%gcc@12.2.0
  mirrors:
    atestm: {0}
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
      - match:
          - arch=test-debian6-core2
        runner-attributes:
          tags:
            - meh
      - match:
          - arch=test-debian6-aarch64
        runner-attributes:
          tags:
            - donotcare
      - match:
          - arch=test-debian6-m1
        runner-attributes:
          tags:
            - meh
""".format(
                mirror_url
            )
        )

    # Without this monkeypatch, pipeline generation process would think that
    # nothing in the environment needs rebuilding.  With the monkeypatch, the
    # process sees the compiler as needing a rebuild, which should then result
    # in the specs built with that compiler needing a rebuild too.
    def fake_get_mirrors_for_spec(spec=None, mirrors_to_check=None, index_only=False):
        if spec.name == "gcc":
            return []
        else:
            return [{"spec": spec, "mirror_url": mirror_url}]

    with tmpdir.as_cwd():
        env_cmd("create", "test", "./spack.yaml")
        outputfile = str(tmpdir.join(".gitlab-ci.yml"))

        with ev.read("test"):
            ci_cmd("generate", "--output-file", outputfile)

            with open(outputfile) as of:
                yaml_contents = of.read()
                original_yaml_contents = syaml.load(yaml_contents)

            # without the monkeypatch, everything appears up to date and no
            # rebuild jobs are generated.
            assert original_yaml_contents
            assert "no-specs-to-rebuild" in original_yaml_contents

            monkeypatch.setattr(
                spack.binary_distribution, "get_mirrors_for_spec", fake_get_mirrors_for_spec
            )

            ci_cmd("generate", "--output-file", outputfile)

            with open(outputfile) as of:
                yaml_contents = of.read()
                new_yaml_contents = syaml.load(yaml_contents)

            assert new_yaml_contents

            # This 'needs' graph reflects that even though specs 'a' and 'b' do
            # not otherwise need to be rebuilt (thanks to DAG pruning), they
            # both end up in the generated pipeline because the compiler they
            # depend on is bootstrapped, and *does* need to be rebuilt.
            needs_graph = {"(bootstrap) gcc": [], "(specs) b": ["(bootstrap) gcc"]}

            _validate_needs_graph(new_yaml_contents, needs_graph, False)


def test_ci_get_stack_changed(mock_git_repo, monkeypatch):
    """Test that we can detect the change to .gitlab-ci.yml in a
    mock spack git repo."""
    monkeypatch.setattr(spack.paths, "prefix", mock_git_repo)
    assert ci.get_stack_changed("/no/such/env/path") is True


def test_ci_generate_prune_untouched(
    tmpdir, mutable_mock_env_path, install_mockery, mock_packages, ci_base_environment, monkeypatch
):
    """Test pipeline generation with pruning works to eliminate
    specs that were not affected by a change"""
    os.environ.update({"SPACK_PRUNE_UNTOUCHED": "TRUE"})  # enables pruning of untouched specs
    mirror_url = "https://my.fake.mirror"
    filename = str(tmpdir.join("spack.yaml"))
    with open(filename, "w") as f:
        f.write(
            """\
spack:
  specs:
    - archive-files
    - callpath
  mirrors:
    some-mirror: {0}
  gitlab-ci:
    mappings:
      - match:
          - arch=test-debian6-core2
        runner-attributes:
          tags:
            - donotcare
          image: donotcare
""".format(
                mirror_url
            )
        )

    # Dependency graph rooted at callpath
    # callpath -> dyninst -> libelf
    #                     -> libdwarf -> libelf
    #          -> mpich

    with tmpdir.as_cwd():
        env_cmd("create", "test", "./spack.yaml")
        outputfile = str(tmpdir.join(".gitlab-ci.yml"))

        def fake_compute_affected(r1=None, r2=None):
            return ["libdwarf"]

        def fake_stack_changed(env_path, rev1="HEAD^", rev2="HEAD"):
            return False

        env_hashes = {}

        with ev.read("test") as active_env:
            monkeypatch.setattr(ci, "compute_affected_packages", fake_compute_affected)
            monkeypatch.setattr(ci, "get_stack_changed", fake_stack_changed)

            active_env.concretize()

            for s in active_env.all_specs():
                env_hashes[s.name] = s.dag_hash()

            ci_cmd("generate", "--output-file", outputfile)

        with open(outputfile) as f:
            contents = f.read()
            print(contents)
            yaml_contents = syaml.load(contents)

            generated_hashes = []

            for ci_key in yaml_contents.keys():
                if ci_key.startswith("(specs)"):
                    generated_hashes.append(
                        yaml_contents[ci_key]["variables"]["SPACK_JOB_SPEC_DAG_HASH"]
                    )

            assert env_hashes["archive-files"] not in generated_hashes
            for spec_name in ["callpath", "dyninst", "mpich", "libdwarf", "libelf"]:
                assert env_hashes[spec_name] in generated_hashes


def test_ci_generate_prune_env_vars(
    tmpdir, mutable_mock_env_path, install_mockery, mock_packages, ci_base_environment, monkeypatch
):
    """Make sure environment variables controlling untouched spec
    pruning behave as expected."""
    os.environ.update(
        {
            "SPACK_PRUNE_UNTOUCHED": "TRUE",  # enables pruning of untouched specs
        }
    )
    filename = str(tmpdir.join("spack.yaml"))
    with open(filename, "w") as f:
        f.write(
            """\
spack:
  specs:
    - libelf
  gitlab-ci:
    mappings:
      - match:
          - arch=test-debian6-core2
        runner-attributes:
          tags:
            - donotcare
          image: donotcare
"""
        )

    with tmpdir.as_cwd():
        env_cmd("create", "test", "./spack.yaml")

        def fake_compute_affected(r1=None, r2=None):
            return ["libdwarf"]

        def fake_stack_changed(env_path, rev1="HEAD^", rev2="HEAD"):
            return False

        expected_depth_param = None

        def check_get_spec_filter_list(env, affected_pkgs, dependent_traverse_depth=None):
            assert dependent_traverse_depth == expected_depth_param
            return set()

        monkeypatch.setattr(ci, "compute_affected_packages", fake_compute_affected)
        monkeypatch.setattr(ci, "get_stack_changed", fake_stack_changed)
        monkeypatch.setattr(ci, "get_spec_filter_list", check_get_spec_filter_list)

        expectations = {"-1": -1, "0": 0, "True": None}

        for key, val in expectations.items():
            with ev.read("test"):
                os.environ.update({"SPACK_PRUNE_UNTOUCHED_DEPENDENT_DEPTH": key})
                expected_depth_param = val
                # Leaving out the mirror in the spack.yaml above means the
                # pipeline generation command will fail, pretty much immediately.
                # But for this test, we only care how the environment variables
                # for pruning are handled, the faster the better.  So allow the
                # spack command to fail.
                ci_cmd("generate", fail_on_error=False)


def test_ci_subcommands_without_mirror(
    tmpdir,
    mutable_mock_env_path,
    mock_packages,
    install_mockery,
    ci_base_environment,
    mock_binary_index,
):
    """Make sure we catch if there is not a mirror and report an error"""
    filename = str(tmpdir.join("spack.yaml"))
    with open(filename, "w") as f:
        f.write(
            """\
spack:
  specs:
    - archive-files
  gitlab-ci:
    mappings:
      - match:
          - archive-files
        runner-attributes:
          tags:
            - donotcare
          image: donotcare
"""
        )

    with tmpdir.as_cwd():
        env_cmd("create", "test", "./spack.yaml")
        outputfile = str(tmpdir.join(".gitlab-ci.yml"))

        with ev.read("test"):
            # Check the 'generate' subcommand
            output = ci_cmd(
                "generate", "--output-file", outputfile, output=str, fail_on_error=False
            )
            ex = "spack ci generate requires an env containing a mirror"
            assert ex in output

            # Also check the 'rebuild-index' subcommand
            output = ci_cmd("rebuild-index", output=str, fail_on_error=False)
            ex = "spack ci rebuild-index requires an env containing a mirror"
            assert ex in output


def test_ensure_only_one_temporary_storage():
    """Make sure 'gitlab-ci' section of env does not allow specification of
    both 'enable-artifacts-buildcache' and 'temporary-storage-url-prefix'."""
    gitlab_ci_template = """
  gitlab-ci:
    {0}
    mappings:
      - match:
          - notcheckedhere
        runner-attributes:
          tags:
            - donotcare
"""

    enable_artifacts = "enable-artifacts-buildcache: True"
    temp_storage = "temporary-storage-url-prefix: file:///temp/mirror"
    specify_both = """{0}
    {1}
""".format(
        enable_artifacts, temp_storage
    )
    specify_neither = ""

    # User can specify "enable-artifacts-buildcache" (boolean)
    yaml_obj = syaml.load(gitlab_ci_template.format(enable_artifacts))
    jsonschema.validate(yaml_obj, gitlab_ci_schema)

    # User can also specify "temporary-storage-url-prefix" (string)
    yaml_obj = syaml.load(gitlab_ci_template.format(temp_storage))
    jsonschema.validate(yaml_obj, gitlab_ci_schema)

    # However, specifying both should fail to validate
    yaml_obj = syaml.load(gitlab_ci_template.format(specify_both))
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(yaml_obj, gitlab_ci_schema)

    # Specifying neither should be fine too, as neither of these properties
    # should be required
    yaml_obj = syaml.load(gitlab_ci_template.format(specify_neither))
    jsonschema.validate(yaml_obj, gitlab_ci_schema)


def test_ci_generate_temp_storage_url(
    tmpdir,
    mutable_mock_env_path,
    install_mockery,
    mock_packages,
    monkeypatch,
    ci_base_environment,
    mock_binary_index,
):
    """Verify correct behavior when using temporary-storage-url-prefix"""
    filename = str(tmpdir.join("spack.yaml"))
    with open(filename, "w") as f:
        f.write(
            """\
spack:
  specs:
    - archive-files
  mirrors:
    some-mirror: https://my.fake.mirror
  gitlab-ci:
    temporary-storage-url-prefix: file:///work/temp/mirror
    mappings:
      - match:
          - archive-files
        runner-attributes:
          tags:
            - donotcare
          image: donotcare
"""
        )

    with tmpdir.as_cwd():
        env_cmd("create", "test", "./spack.yaml")
        outputfile = str(tmpdir.join(".gitlab-ci.yml"))

        with ev.read("test"):
            ci_cmd("generate", "--output-file", outputfile)

            with open(outputfile) as of:
                pipeline_doc = syaml.load(of.read())

                assert "cleanup" in pipeline_doc
                cleanup_job = pipeline_doc["cleanup"]

                assert "script" in cleanup_job
                cleanup_task = cleanup_job["script"][0]

                assert cleanup_task.startswith("spack -d mirror destroy")

                assert "stages" in pipeline_doc
                stages = pipeline_doc["stages"]

                # Cleanup job should be 2nd to last, just before rebuild-index
                assert "stage" in cleanup_job
                assert cleanup_job["stage"] == stages[-2]


def test_ci_generate_read_broken_specs_url(
    tmpdir, mutable_mock_env_path, install_mockery, mock_packages, monkeypatch, ci_base_environment
):
    """Verify that `broken-specs-url` works as intended"""
    spec_a = Spec("a")
    spec_a.concretize()
    a_dag_hash = spec_a.dag_hash()

    spec_flattendeps = Spec("flatten-deps")
    spec_flattendeps.concretize()
    flattendeps_dag_hash = spec_flattendeps.dag_hash()

    broken_specs_url = "file://{0}".format(tmpdir.strpath)

    # Mark 'a' as broken (but not 'flatten-deps')
    broken_spec_a_url = "{0}/{1}".format(broken_specs_url, a_dag_hash)
    job_stack = "job_stack"
    a_job_url = "a_job_url"
    ci.write_broken_spec(
        broken_spec_a_url, spec_a.name, job_stack, a_job_url, "pipeline_url", spec_a.to_dict()
    )

    # Test that `spack ci generate` notices this broken spec and fails.
    filename = str(tmpdir.join("spack.yaml"))
    with open(filename, "w") as f:
        f.write(
            """\
spack:
  specs:
    - flatten-deps
    - a
  mirrors:
    some-mirror: https://my.fake.mirror
  gitlab-ci:
    broken-specs-url: "{0}"
    mappings:
      - match:
          - a
          - flatten-deps
          - b
          - dependency-install
        runner-attributes:
          tags:
            - donotcare
          image: donotcare
""".format(
                broken_specs_url
            )
        )

    with tmpdir.as_cwd():
        env_cmd("create", "test", "./spack.yaml")
        with ev.read("test"):
            # Check output of the 'generate' subcommand
            output = ci_cmd("generate", output=str, fail_on_error=False)
            assert "known to be broken" in output

            expected = "{0}/{1} (in stack {2}) was reported broken here: {3}".format(
                spec_a.name, a_dag_hash[:7], job_stack, a_job_url
            )
            assert expected in output

            not_expected = "flatten-deps/{0} (in stack".format(flattendeps_dag_hash[:7])
            assert not_expected not in output


def test_ci_generate_external_signing_job(
    tmpdir, mutable_mock_env_path, install_mockery, mock_packages, monkeypatch, ci_base_environment
):
    """Verify that in external signing mode: 1) each rebuild jobs includes
    the location where the binary hash information is written and 2) we
    properly generate a final signing job in the pipeline."""
    os.environ.update({"SPACK_PIPELINE_TYPE": "spack_protected_branch"})
    filename = str(tmpdir.join("spack.yaml"))
    with open(filename, "w") as f:
        f.write(
            """\
spack:
  specs:
    - archive-files
  mirrors:
    some-mirror: https://my.fake.mirror
  gitlab-ci:
    temporary-storage-url-prefix: file:///work/temp/mirror
    mappings:
      - match:
          - archive-files
        runner-attributes:
          tags:
            - donotcare
          image: donotcare
    signing-job-attributes:
      tags:
        - nonbuildtag
        - secretrunner
      image:
        name: customdockerimage
        entrypoint: []
      variables:
        IMPORTANT_INFO: avalue
      script:
        - echo hello
"""
        )

    with tmpdir.as_cwd():
        env_cmd("create", "test", "./spack.yaml")
        outputfile = str(tmpdir.join(".gitlab-ci.yml"))

        with ev.read("test"):
            ci_cmd("generate", "--output-file", outputfile)

        with open(outputfile) as of:
            pipeline_doc = syaml.load(of.read())

            assert "sign-pkgs" in pipeline_doc
            signing_job = pipeline_doc["sign-pkgs"]
            assert "tags" in signing_job
            signing_job_tags = signing_job["tags"]
            for expected_tag in ["notary", "protected", "aws"]:
                assert expected_tag in signing_job_tags


def test_ci_reproduce(
    tmpdir,
    mutable_mock_env_path,
    install_mockery,
    mock_packages,
    monkeypatch,
    last_two_git_commits,
    ci_base_environment,
    mock_binary_index,
):
    working_dir = tmpdir.join("repro_dir")
    image_name = "org/image:tag"

    spack_yaml_contents = """
spack:
 definitions:
   - packages: [archive-files]
 specs:
   - $packages
 mirrors:
   test-mirror: file:///some/fake/mirror
 gitlab-ci:
   mappings:
     - match:
         - archive-files
       runner-attributes:
         tags:
           - donotcare
         image: {0}
""".format(
        image_name
    )

    filename = str(tmpdir.join("spack.yaml"))
    with open(filename, "w") as f:
        f.write(spack_yaml_contents)

    with tmpdir.as_cwd():
        env_cmd("create", "test", "./spack.yaml")
        with ev.read("test") as env:
            with env.write_transaction():
                env.concretize()
                env.write()

            if not os.path.exists(working_dir.strpath):
                os.makedirs(working_dir.strpath)

            shutil.copyfile(env.manifest_path, os.path.join(working_dir.strpath, "spack.yaml"))
            shutil.copyfile(env.lock_path, os.path.join(working_dir.strpath, "spack.lock"))

            job_spec = None

            for h, s in env.specs_by_hash.items():
                if s.name == "archive-files":
                    job_spec = s

            job_spec_json_path = os.path.join(working_dir.strpath, "archivefiles.json")
            with open(job_spec_json_path, "w") as fd:
                fd.write(job_spec.to_json(hash=ht.dag_hash))

            artifacts_root = os.path.join(working_dir.strpath, "scratch_dir")
            pipeline_path = os.path.join(artifacts_root, "pipeline.yml")

            ci_cmd("generate", "--output-file", pipeline_path, "--artifacts-root", artifacts_root)

            target_name = spack.platforms.test.Test.default
            job_name = ci.get_job_name(
                "specs", False, job_spec, "test-debian6-%s" % target_name, None
            )

            repro_file = os.path.join(working_dir.strpath, "repro.json")
            repro_details = {
                "job_name": job_name,
                "job_spec_json": "archivefiles.json",
                "ci_project_dir": working_dir.strpath,
            }
            with open(repro_file, "w") as fd:
                fd.write(json.dumps(repro_details))

            install_script = os.path.join(working_dir.strpath, "install.sh")
            with open(install_script, "w") as fd:
                fd.write("#!/bin/bash\n\n#fake install\nspack install blah\n")

            spack_info_file = os.path.join(working_dir.strpath, "spack_info.txt")
            with open(spack_info_file, "w") as fd:
                fd.write(
                    "\nMerge {0} into {1}\n\n".format(
                        last_two_git_commits[1], last_two_git_commits[0]
                    )
                )

    def fake_download_and_extract_artifacts(url, work_dir):
        pass

    monkeypatch.setattr(ci, "download_and_extract_artifacts", fake_download_and_extract_artifacts)
    rep_out = ci_cmd(
        "reproduce-build",
        "https://some.domain/api/v1/projects/1/jobs/2/artifacts",
        "--working-dir",
        working_dir.strpath,
        output=str,
    )
    expect_out = "docker run --rm -v {0}:{0} -ti {1}".format(working_dir.strpath, image_name)

    assert expect_out in rep_out


@pytest.mark.parametrize(
    "subcmd", [(""), ("generate"), ("rebuild-index"), ("rebuild"), ("reproduce-build")]
)
def test_ci_help(subcmd, capsys):
    """Make sure `spack ci` --help describes the (sub)command help."""
    out = spack.main.SpackCommand("ci", subprocess=True)(subcmd, "--help")

    usage = "usage: spack ci {0}{1}[".format(subcmd, " " if subcmd else "")
    assert usage in out


def test_cmd_first_line():
    """Explicitly test first_line since not picked up in test_ci_help."""
    first = "This is a test."
    doc = """{0}

    Is there more to be said?""".format(
        first
    )

    assert spack.cmd.first_line(doc) == first
