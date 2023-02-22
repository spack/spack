# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import json
import os
import shutil

import llnl.util.filesystem as fs
import llnl.util.tty as tty

import spack.binary_distribution as bindist
import spack.ci as spack_ci
import spack.cmd.buildcache as buildcache
import spack.config as cfg
import spack.environment as ev
import spack.hash_types as ht
import spack.mirror
import spack.util.url as url_util
import spack.util.web as web_util

description = "manage continuous integration pipelines"
section = "build"
level = "long"

SPACK_COMMAND = "spack"
MAKE_COMMAND = "make"
INSTALL_FAIL_CODE = 1


def deindent(desc):
    return desc.replace("    ", "")


def get_env_var(variable_name):
    if variable_name in os.environ:
        return os.environ.get(variable_name)
    return None


def setup_parser(subparser):
    setup_parser.parser = subparser
    subparsers = subparser.add_subparsers(help="CI sub-commands")

    # Dynamic generation of the jobs yaml from a spack environment
    generate = subparsers.add_parser(
        "generate",
        description=deindent(ci_generate.__doc__),
        help=spack.cmd.first_line(ci_generate.__doc__),
    )
    generate.add_argument(
        "--output-file",
        default=None,
        help="""pathname for the generated gitlab ci yaml file
  Path to the file where generated jobs file should
be written. Default is .gitlab-ci.yml in the root of
the repository.""",
    )
    generate.add_argument(
        "--copy-to",
        default=None,
        help="""path to additional directory for job files
  This option provides an absolute path to a directory
where the generated jobs yaml file should be copied.
Default is not to copy.""",
    )
    generate.add_argument(
        "--optimize",
        action="store_true",
        default=False,
        help="""(Experimental) optimize the gitlab yaml file for size
  Run the generated document through a series of
optimization passes designed to reduce the size
of the generated file.""",
    )
    generate.add_argument(
        "--dependencies",
        action="store_true",
        default=False,
        help="(Experimental) disable DAG scheduling; use " ' "plain" dependencies.',
    )
    generate.add_argument(
        "--buildcache-destination",
        default=None,
        help="Override the mirror configured in the environment (spack.yaml) "
        + "in order to push binaries from the generated pipeline to a "
        + "different location.",
    )
    prune_group = generate.add_mutually_exclusive_group()
    prune_group.add_argument(
        "--prune-dag",
        action="store_true",
        dest="prune_dag",
        default=True,
        help="""skip up-to-date specs
  Do not generate jobs for specs that are up-to-date
on the mirror.""",
    )
    prune_group.add_argument(
        "--no-prune-dag",
        action="store_false",
        dest="prune_dag",
        default=True,
        help="""process up-to-date specs
  Generate jobs for specs even when they are up-to-date
on the mirror.""",
    )
    generate.add_argument(
        "--check-index-only",
        action="store_true",
        dest="index_only",
        default=False,
        help="""only check spec state from buildcache indices
  Spack always checks specs against configured binary
mirrors, regardless of the DAG pruning option.
  If enabled, Spack will assume all remote buildcache
indices are up-to-date when assessing whether the spec
on the mirror, if present, is up-to-date. This has the
benefit of reducing pipeline generation time but at the
potential cost of needlessly rebuilding specs when the
indices are outdated.
  If not enabled, Spack will fetch remote spec files
directly to assess whether the spec on the mirror is
up-to-date.""",
    )
    generate.add_argument(
        "--artifacts-root",
        default=None,
        help="""path to the root of the artifacts directory
  If provided, concrete environment files (spack.yaml,
spack.lock) will be generated under this directory.
Their location will be passed to generated child jobs
through the SPACK_CONCRETE_ENVIRONMENT_PATH variable.""",
    )
    generate.set_defaults(func=ci_generate)

    # Rebuild the buildcache index associated with the mirror in the
    # active, gitlab-enabled environment.
    index = subparsers.add_parser(
        "rebuild-index",
        description=deindent(ci_reindex.__doc__),
        help=spack.cmd.first_line(ci_reindex.__doc__),
    )
    index.set_defaults(func=ci_reindex)

    # Handle steps of a ci build/rebuild
    rebuild = subparsers.add_parser(
        "rebuild",
        description=deindent(ci_rebuild.__doc__),
        help=spack.cmd.first_line(ci_rebuild.__doc__),
    )
    rebuild.add_argument(
        "-t",
        "--tests",
        action="store_true",
        default=False,
        help="""run stand-alone tests after the build""",
    )
    rebuild.add_argument(
        "--fail-fast",
        action="store_true",
        default=False,
        help="""stop stand-alone tests after the first failure""",
    )
    rebuild.set_defaults(func=ci_rebuild)

    # Facilitate reproduction of a failed CI build job
    reproduce = subparsers.add_parser(
        "reproduce-build",
        description=deindent(ci_reproduce.__doc__),
        help=spack.cmd.first_line(ci_reproduce.__doc__),
    )
    reproduce.add_argument("job_url", help="Url of job artifacts bundle")
    reproduce.add_argument(
        "--working-dir",
        help="Where to unpack artifacts",
        default=os.path.join(os.getcwd(), "ci_reproduction"),
    )

    reproduce.set_defaults(func=ci_reproduce)


def ci_generate(args):
    """Generate jobs file from a CI-aware spack file.

    If you want to report the results on CDash, you will need to set
    the SPACK_CDASH_AUTH_TOKEN before invoking this command. The
    value must be the CDash authorization token needed to create a
    build group and register all generated jobs under it."""
    env = spack.cmd.require_active_env(cmd_name="ci generate")

    output_file = args.output_file
    copy_yaml_to = args.copy_to
    run_optimizer = args.optimize
    use_dependencies = args.dependencies
    prune_dag = args.prune_dag
    index_only = args.index_only
    artifacts_root = args.artifacts_root
    buildcache_destination = args.buildcache_destination

    if not output_file:
        output_file = os.path.abspath(".gitlab-ci.yml")
    else:
        output_file_path = os.path.abspath(output_file)
        gen_ci_dir = os.path.dirname(output_file_path)
        if not os.path.exists(gen_ci_dir):
            os.makedirs(gen_ci_dir)

    # Generate the jobs
    spack_ci.generate_gitlab_ci_yaml(
        env,
        True,
        output_file,
        prune_dag=prune_dag,
        check_index_only=index_only,
        run_optimizer=run_optimizer,
        use_dependencies=use_dependencies,
        artifacts_root=artifacts_root,
        remote_mirror_override=buildcache_destination,
    )

    if copy_yaml_to:
        copy_to_dir = os.path.dirname(copy_yaml_to)
        if not os.path.exists(copy_to_dir):
            os.makedirs(copy_to_dir)
        shutil.copyfile(output_file, copy_yaml_to)


def ci_reindex(args):
    """Rebuild the buildcache index for the remote mirror.

    Use the active, gitlab-enabled environment to rebuild the buildcache
    index for the associated mirror."""
    env = spack.cmd.require_active_env(cmd_name="ci rebuild-index")
    yaml_root = ev.config_dict(env.yaml)

    if "mirrors" not in yaml_root or len(yaml_root["mirrors"].values()) < 1:
        tty.die("spack ci rebuild-index requires an env containing a mirror")

    ci_mirrors = yaml_root["mirrors"]
    mirror_urls = [url for url in ci_mirrors.values()]
    remote_mirror_url = mirror_urls[0]
    mirror = spack.mirror.Mirror(remote_mirror_url)

    buildcache.update_index(mirror, update_keys=True)


def ci_rebuild(args):
    """Rebuild a spec if it is not on the remote mirror.

    Check a single spec against the remote mirror, and rebuild it from
    source if the mirror does not contain the hash."""
    env = spack.cmd.require_active_env(cmd_name="ci rebuild")

    # Make sure the environment is "gitlab-enabled", or else there's nothing
    # to do.
    yaml_root = ev.config_dict(env.yaml)
    gitlab_ci = yaml_root["gitlab-ci"] if "gitlab-ci" in yaml_root else None
    if not gitlab_ci:
        tty.die("spack ci rebuild requires an env containing gitlab-ci cfg")

    tty.msg(
        "SPACK_BUILDCACHE_DESTINATION={0}".format(
            os.environ.get("SPACK_BUILDCACHE_DESTINATION", None)
        )
    )

    # Grab the environment variables we need.  These either come from the
    # pipeline generation step ("spack ci generate"), where they were written
    # out as variables, or else provided by GitLab itself.
    pipeline_artifacts_dir = get_env_var("SPACK_ARTIFACTS_ROOT")
    job_log_dir = get_env_var("SPACK_JOB_LOG_DIR")
    job_test_dir = get_env_var("SPACK_JOB_TEST_DIR")
    repro_dir = get_env_var("SPACK_JOB_REPRO_DIR")
    local_mirror_dir = get_env_var("SPACK_LOCAL_MIRROR_DIR")
    concrete_env_dir = get_env_var("SPACK_CONCRETE_ENV_DIR")
    ci_pipeline_id = get_env_var("CI_PIPELINE_ID")
    ci_job_name = get_env_var("CI_JOB_NAME")
    signing_key = get_env_var("SPACK_SIGNING_KEY")
    job_spec_pkg_name = get_env_var("SPACK_JOB_SPEC_PKG_NAME")
    job_spec_dag_hash = get_env_var("SPACK_JOB_SPEC_DAG_HASH")
    compiler_action = get_env_var("SPACK_COMPILER_ACTION")
    spack_pipeline_type = get_env_var("SPACK_PIPELINE_TYPE")
    remote_mirror_override = get_env_var("SPACK_REMOTE_MIRROR_OVERRIDE")
    remote_mirror_url = get_env_var("SPACK_REMOTE_MIRROR_URL")
    spack_ci_stack_name = get_env_var("SPACK_CI_STACK_NAME")
    shared_pr_mirror_url = get_env_var("SPACK_CI_SHARED_PR_MIRROR_URL")
    rebuild_everything = get_env_var("SPACK_REBUILD_EVERYTHING")

    # Construct absolute paths relative to current $CI_PROJECT_DIR
    ci_project_dir = get_env_var("CI_PROJECT_DIR")
    pipeline_artifacts_dir = os.path.join(ci_project_dir, pipeline_artifacts_dir)
    job_log_dir = os.path.join(ci_project_dir, job_log_dir)
    job_test_dir = os.path.join(ci_project_dir, job_test_dir)
    repro_dir = os.path.join(ci_project_dir, repro_dir)
    local_mirror_dir = os.path.join(ci_project_dir, local_mirror_dir)
    concrete_env_dir = os.path.join(ci_project_dir, concrete_env_dir)

    # Debug print some of the key environment variables we should have received
    tty.debug("pipeline_artifacts_dir = {0}".format(pipeline_artifacts_dir))
    tty.debug("remote_mirror_url = {0}".format(remote_mirror_url))
    tty.debug("job_spec_pkg_name = {0}".format(job_spec_pkg_name))
    tty.debug("compiler_action = {0}".format(compiler_action))

    # Query the environment manifest to find out whether we're reporting to a
    # CDash instance, and if so, gather some information from the manifest to
    # support that task.
    cdash_handler = spack_ci.CDashHandler(yaml_root.get("cdash")) if "cdash" in yaml_root else None
    if cdash_handler:
        tty.debug("cdash url = {0}".format(cdash_handler.url))
        tty.debug("cdash project = {0}".format(cdash_handler.project))
        tty.debug("cdash project_enc = {0}".format(cdash_handler.project_enc))
        tty.debug("cdash build_name = {0}".format(cdash_handler.build_name))
        tty.debug("cdash build_stamp = {0}".format(cdash_handler.build_stamp))
        tty.debug("cdash site = {0}".format(cdash_handler.site))
        tty.debug("cdash build_group = {0}".format(cdash_handler.build_group))

    # Is this a pipeline run on a spack PR or a merge to develop?  It might
    # be neither, e.g. a pipeline run on some environment repository.
    spack_is_pr_pipeline = spack_pipeline_type == "spack_pull_request"
    spack_is_develop_pipeline = spack_pipeline_type == "spack_protected_branch"

    tty.debug(
        "Pipeline type - PR: {0}, develop: {1}".format(
            spack_is_pr_pipeline, spack_is_develop_pipeline
        )
    )

    full_rebuild = True if rebuild_everything and rebuild_everything.lower() == "true" else False

    # If no override url exists, then just push binary package to the
    # normal remote mirror url.
    buildcache_mirror_url = remote_mirror_override or remote_mirror_url

    # Figure out what is our temporary storage mirror: Is it artifacts
    # buildcache?  Or temporary-storage-url-prefix?  In some cases we need to
    # force something or pipelines might not have a way to propagate build
    # artifacts from upstream to downstream jobs.
    pipeline_mirror_url = None

    temp_storage_url_prefix = None
    if "temporary-storage-url-prefix" in gitlab_ci:
        temp_storage_url_prefix = gitlab_ci["temporary-storage-url-prefix"]
        pipeline_mirror_url = url_util.join(temp_storage_url_prefix, ci_pipeline_id)

    enable_artifacts_mirror = False
    if "enable-artifacts-buildcache" in gitlab_ci:
        enable_artifacts_mirror = gitlab_ci["enable-artifacts-buildcache"]
        if enable_artifacts_mirror or (
            spack_is_pr_pipeline and not enable_artifacts_mirror and not temp_storage_url_prefix
        ):
            # If you explicitly enabled the artifacts buildcache feature, or
            # if this is a PR pipeline but you did not enable either of the
            # per-pipeline temporary storage features, we force the use of
            # artifacts buildcache.  Otherwise jobs will not have binary
            # dependencies from previous stages available since we do not
            # allow pushing binaries to the remote mirror during PR pipelines.
            enable_artifacts_mirror = True
            pipeline_mirror_url = url_util.path_to_file_url(local_mirror_dir)
            mirror_msg = "artifact buildcache enabled, mirror url: {0}".format(pipeline_mirror_url)
            tty.debug(mirror_msg)

    # Get the concrete spec to be built by this job.
    try:
        job_spec = env.get_one_by_hash(job_spec_dag_hash)
    except AssertionError:
        tty.die("Could not find environment spec with hash {0}".format(job_spec_dag_hash))

    job_spec_json_file = "{0}.json".format(job_spec_pkg_name)
    job_spec_json_path = os.path.join(repro_dir, job_spec_json_file)

    # To provide logs, cdash reports, etc for developer download/perusal,
    # these things have to be put into artifacts.  This means downstream
    # jobs that "need" this job will get those artifacts too.  So here we
    # need to clean out the artifacts we may have got from upstream jobs.

    cdash_report_dir = os.path.join(pipeline_artifacts_dir, "cdash_report")
    if os.path.exists(cdash_report_dir):
        shutil.rmtree(cdash_report_dir)

    if os.path.exists(job_log_dir):
        shutil.rmtree(job_log_dir)

    if os.path.exists(job_test_dir):
        shutil.rmtree(job_test_dir)

    if os.path.exists(repro_dir):
        shutil.rmtree(repro_dir)

    # Now that we removed them if they existed, create the directories we
    # need for storing artifacts.  The cdash_report directory will be
    # created internally if needed.
    os.makedirs(job_log_dir)
    os.makedirs(job_test_dir)
    os.makedirs(repro_dir)

    # Copy the concrete environment files to the repro directory so we can
    # expose them as artifacts and not conflict with the concrete environment
    # files we got as artifacts from the upstream pipeline generation job.
    # Try to cast a slightly wider net too, and hopefully get the generated
    # pipeline yaml.  If we miss it, the user will still be able to go to the
    # pipeline generation job and get it from there.
    target_dirs = [concrete_env_dir, pipeline_artifacts_dir]

    for dir_to_list in target_dirs:
        for file_name in os.listdir(dir_to_list):
            src_file = os.path.join(dir_to_list, file_name)
            if os.path.isfile(src_file):
                dst_file = os.path.join(repro_dir, file_name)
                shutil.copyfile(src_file, dst_file)

    # If signing key was provided via "SPACK_SIGNING_KEY", then try to
    # import it.
    if signing_key:
        spack_ci.import_signing_key(signing_key)

    # Depending on the specifics of this job, we might need to turn on the
    # "config:install_missing compilers" option (to build this job spec
    # with a bootstrapped compiler), or possibly run "spack compiler find"
    # (to build a bootstrap compiler or one of its deps in a
    # compiler-agnostic way), or maybe do nothing at all (to build a spec
    # using a compiler already installed on the target system).
    spack_ci.configure_compilers(compiler_action)

    # Write this job's spec json into the reproduction directory, and it will
    # also be used in the generated "spack install" command to install the spec
    tty.debug("job concrete spec path: {0}".format(job_spec_json_path))
    with open(job_spec_json_path, "w") as fd:
        fd.write(job_spec.to_json(hash=ht.dag_hash))

    # Write some other details to aid in reproduction into an artifact
    repro_file = os.path.join(repro_dir, "repro.json")
    repro_details = {
        "job_name": ci_job_name,
        "job_spec_json": job_spec_json_file,
        "ci_project_dir": ci_project_dir,
    }
    with open(repro_file, "w") as fd:
        fd.write(json.dumps(repro_details))

    # Write information about spack into an artifact in the repro dir
    spack_info = spack_ci.get_spack_info()
    spack_info_file = os.path.join(repro_dir, "spack_info.txt")
    with open(spack_info_file, "wb") as fd:
        fd.write(b"\n")
        fd.write(spack_info.encode("utf8"))
        fd.write(b"\n")

    pipeline_mirrors = []

    # If we decided there should be a temporary storage mechanism, add that
    # mirror now so it's used when we check for a hash match already
    # built for this spec.
    if pipeline_mirror_url:
        mirror = spack.mirror.Mirror(pipeline_mirror_url, name=spack_ci.TEMP_STORAGE_MIRROR_NAME)
        spack.mirror.add(mirror, cfg.default_modify_scope())
        pipeline_mirrors.append(pipeline_mirror_url)

    # Check configured mirrors for a built spec with a matching hash
    mirrors_to_check = None
    if remote_mirror_override:
        if spack_pipeline_type == "spack_protected_branch":
            # Passing "mirrors_to_check" below means we *only* look in the override
            # mirror to see if we should skip building, which is what we want.
            mirrors_to_check = {"override": remote_mirror_override}

            # Adding this mirror to the list of configured mirrors means dependencies
            # could be installed from either the override mirror or any other configured
            # mirror (e.g. remote_mirror_url which is defined in the environment or
            # pipeline_mirror_url), which is also what we want.
            spack.mirror.add(
                spack.mirror.Mirror(remote_mirror_override, name="mirror_override"),
                cfg.default_modify_scope(),
            )
        pipeline_mirrors.append(remote_mirror_override)

    if spack_pipeline_type == "spack_pull_request":
        if shared_pr_mirror_url != "None":
            pipeline_mirrors.append(shared_pr_mirror_url)

    matches = (
        None
        if full_rebuild
        else bindist.get_mirrors_for_spec(
            job_spec, mirrors_to_check=mirrors_to_check, index_only=False
        )
    )

    if matches:
        # Got a hash match on at least one configured mirror.  All
        # matches represent the fully up-to-date spec, so should all be
        # equivalent.  If artifacts mirror is enabled, we just pick one
        # of the matches and download the buildcache files from there to
        # the artifacts, so they're available to be used by dependent
        # jobs in subsequent stages.
        tty.msg("No need to rebuild {0}, found hash match at: ".format(job_spec_pkg_name))
        for match in matches:
            tty.msg("    {0}".format(match["mirror_url"]))
        if enable_artifacts_mirror:
            matching_mirror = matches[0]["mirror_url"]
            build_cache_dir = os.path.join(local_mirror_dir, "build_cache")
            tty.debug("Getting {0} buildcache from {1}".format(job_spec_pkg_name, matching_mirror))
            tty.debug("Downloading to {0}".format(build_cache_dir))
            bindist.download_single_spec(job_spec, build_cache_dir, mirror_url=matching_mirror)

        # Now we are done and successful
        return 0

    # Before beginning the install, if this is a "rebuild everything" pipeline, we
    # only want to keep the mirror being used by the current pipeline as it's binary
    # package destination.  This ensures that the when we rebuild everything, we only
    # consume binary dependencies built in this pipeline.
    if full_rebuild:
        spack_ci.remove_other_mirrors(pipeline_mirrors, cfg.default_modify_scope())

    # No hash match anywhere means we need to rebuild spec

    # Start with spack arguments
    spack_cmd = [SPACK_COMMAND, "--color=always", "--backtrace", "--verbose"]

    config = cfg.get("config")
    if not config["verify_ssl"]:
        spack_cmd.append("-k")

    install_args = []

    can_verify = spack_ci.can_verify_binaries()
    verify_binaries = can_verify and spack_is_pr_pipeline is False
    if not verify_binaries:
        install_args.append("--no-check-signature")

    slash_hash = "/{}".format(job_spec.dag_hash())

    # Arguments when installing dependencies from cache
    deps_install_args = install_args

    # Arguments when installing the root from sources
    root_install_args = install_args + [
        "--keep-stage",
        "--only=package",
        "--use-buildcache=package:never,dependencies:only",
    ]
    if cdash_handler:
        # Add additional arguments to `spack install` for CDash reporting.
        root_install_args.extend(cdash_handler.args())
    root_install_args.append(slash_hash)

    # ["x", "y"] -> "'x' 'y'"
    args_to_string = lambda args: " ".join("'{}'".format(arg) for arg in args)

    commands = [
        # apparently there's a race when spack bootstraps? do it up front once
        [SPACK_COMMAND, "-e", env.path, "bootstrap", "now"],
        [
            SPACK_COMMAND,
            "-e",
            env.path,
            "env",
            "depfile",
            "-o",
            "Makefile",
            "--use-buildcache=package:never,dependencies:only",
            slash_hash,  # limit to spec we're building
        ],
        [
            # --output-sync requires GNU make 4.x.
            # Old make errors when you pass it a flag it doesn't recognize,
            # but it doesn't error or warn when you set unrecognized flags in
            # this variable.
            "export",
            "GNUMAKEFLAGS=--output-sync=recurse",
        ],
        [
            MAKE_COMMAND,
            "SPACK={}".format(args_to_string(spack_cmd)),
            "SPACK_COLOR=always",
            "SPACK_INSTALL_FLAGS={}".format(args_to_string(deps_install_args)),
            "-j$(nproc)",
            "install-deps/{}".format(job_spec.format("{name}-{version}-{hash}")),
        ],
        spack_cmd + ["install"] + root_install_args,
    ]

    tty.debug("Installing {0} from source".format(job_spec.name))
    install_exit_code = spack_ci.process_command("install", commands, repro_dir)

    # Now do the post-install tasks
    tty.debug("spack install exited {0}".format(install_exit_code))

    # If a spec fails to build in a spack develop pipeline, we add it to a
    # list of known broken hashes.  This allows spack PR pipelines to
    # avoid wasting compute cycles attempting to build those hashes.
    if install_exit_code == INSTALL_FAIL_CODE and spack_is_develop_pipeline:
        tty.debug("Install failed on develop")
        if "broken-specs-url" in gitlab_ci:
            broken_specs_url = gitlab_ci["broken-specs-url"]
            dev_fail_hash = job_spec.dag_hash()
            broken_spec_path = url_util.join(broken_specs_url, dev_fail_hash)
            tty.msg("Reporting broken develop build as: {0}".format(broken_spec_path))
            spack_ci.write_broken_spec(
                broken_spec_path,
                job_spec_pkg_name,
                spack_ci_stack_name,
                get_env_var("CI_JOB_URL"),
                get_env_var("CI_PIPELINE_URL"),
                job_spec.to_dict(hash=ht.dag_hash),
            )

    # We generated the "spack install ..." command to "--keep-stage", copy
    # any logs from the staging directory to artifacts now
    spack_ci.copy_stage_logs_to_artifacts(job_spec, job_log_dir)

    # If the installation succeeded and we're running stand-alone tests for
    # the package, run them and copy the output. Failures of any kind should
    # *not* terminate the build process or preclude creating the build cache.
    broken_tests = (
        "broken-tests-packages" in gitlab_ci
        and job_spec.name in gitlab_ci["broken-tests-packages"]
    )
    reports_dir = fs.join_path(os.getcwd(), "cdash_report")
    if args.tests and broken_tests:
        tty.warn(
            "Unable to run stand-alone tests since listed in "
            "gitlab-ci's 'broken-tests-packages'"
        )
        if cdash_handler:
            msg = "Package is listed in gitlab-ci's broken-tests-packages"
            cdash_handler.report_skipped(job_spec, reports_dir, reason=msg)
            cdash_handler.copy_test_results(reports_dir, job_test_dir)
    elif args.tests:
        if install_exit_code == 0:
            try:
                # First ensure we will use a reasonable test stage directory
                stage_root = os.path.dirname(str(job_spec.package.stage.path))
                test_stage = fs.join_path(stage_root, "spack-standalone-tests")
                tty.debug("Configuring test_stage to {0}".format(test_stage))
                config_test_path = "config:test_stage:{0}".format(test_stage)
                cfg.add(config_test_path, scope=cfg.default_modify_scope())

                # Run the tests, resorting to junit results if not using cdash
                log_file = (
                    None if cdash_handler else fs.join_path(test_stage, "ci-test-results.xml")
                )
                spack_ci.run_standalone_tests(
                    cdash=cdash_handler,
                    job_spec=job_spec,
                    fail_fast=args.fail_fast,
                    log_file=log_file,
                    repro_dir=repro_dir,
                )

            except Exception as err:
                # If there is any error, just print a warning.
                msg = "Error processing stand-alone tests: {0}".format(str(err))
                tty.warn(msg)

            finally:
                # Copy the test log/results files
                spack_ci.copy_test_logs_to_artifacts(test_stage, job_test_dir)
                if cdash_handler:
                    cdash_handler.copy_test_results(reports_dir, job_test_dir)
                elif log_file:
                    spack_ci.copy_files_to_artifacts(log_file, job_test_dir)
                else:
                    tty.warn("No recognized test results reporting option")

        else:
            tty.warn("Unable to run stand-alone tests due to unsuccessful " "installation")
            if cdash_handler:
                msg = "Failed to install the package"
                cdash_handler.report_skipped(job_spec, reports_dir, reason=msg)
                cdash_handler.copy_test_results(reports_dir, job_test_dir)

    # If the install succeeded, create a buildcache entry for this job spec
    # and push it to one or more mirrors.  If the install did not succeed,
    # print out some instructions on how to reproduce this build failure
    # outside of the pipeline environment.
    if install_exit_code == 0:
        if buildcache_mirror_url or pipeline_mirror_url:
            spack_ci.create_buildcache(
                env=env,
                buildcache_mirror_url=buildcache_mirror_url,
                pipeline_mirror_url=pipeline_mirror_url,
                pr_pipeline=spack_is_pr_pipeline,
                json_path=job_spec_json_path,
            )

        # If this is a develop pipeline, check if the spec that we just built is
        # on the broken-specs list. If so, remove it.
        if spack_is_develop_pipeline and "broken-specs-url" in gitlab_ci:
            broken_specs_url = gitlab_ci["broken-specs-url"]
            just_built_hash = job_spec.dag_hash()
            broken_spec_path = url_util.join(broken_specs_url, just_built_hash)
            if web_util.url_exists(broken_spec_path):
                tty.msg("Removing {0} from the list of broken specs".format(broken_spec_path))
                try:
                    web_util.remove_url(broken_spec_path)
                except Exception as err:
                    # If there is an S3 error (e.g., access denied or connection
                    # error), the first non boto-specific class in the exception
                    # hierarchy is Exception.  Just print a warning and return.
                    msg = "Error removing {0} from broken specs list: {1}"
                    tty.warn(msg.format(broken_spec_path, err))

    else:
        tty.debug("spack install exited non-zero, will not create buildcache")

        api_root_url = get_env_var("CI_API_V4_URL")
        ci_project_id = get_env_var("CI_PROJECT_ID")
        ci_job_id = get_env_var("CI_JOB_ID")

        repro_job_url = "{0}/projects/{1}/jobs/{2}/artifacts".format(
            api_root_url, ci_project_id, ci_job_id
        )

        # Control characters cause this to be printed in blue so it stands out
        reproduce_msg = """

\033[34mTo reproduce this build locally, run:

    spack ci reproduce-build {0} [--working-dir <dir>]

If this project does not have public pipelines, you will need to first:

    export GITLAB_PRIVATE_TOKEN=<generated_token>

... then follow the printed instructions.\033[0;0m

""".format(
            repro_job_url
        )

        print(reproduce_msg)

    # Tie job success/failure to the success/failure of building the spec
    return install_exit_code


def ci_reproduce(args):
    """Generate instructions for reproducing the spec rebuild job.

    Artifacts of the provided gitlab pipeline rebuild job's URL will be
    used to derive instructions for reproducing the build locally."""
    job_url = args.job_url
    work_dir = args.working_dir

    return spack_ci.reproduce_ci_job(job_url, work_dir)


def ci(parser, args):
    if args.func:
        return args.func(args)
