# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from ..ci import PipelineDag, PipelineOptions, SpackCI
from . import formatter


@formatter("gitlab")
def format_gitlab_yaml(pipeline: PipelineDag, spack_ci_ir: SpackCI, options: PipelineOptions):
    """Given a pipeline graph, job attributes, and pipeline options,
    write a pipeline that can be consumed by GitLab to the given output file.

    Arguments:
        pipeline (PipelineDAG): An already pruned graph of jobs representing all
            the specs to build
        spack_ci_ir (SpackCI): An object containing the configured attributes of
            all jobs in the pipeline
        output_file (str): Path to output file to be written
    """
    output_file = options.output_file
    all_job_names = []
    output_object = {}
    job_id = 0
    stage_id = 0

    stage_names = []

    max_length_needs = 0
    max_needs_job = ""

    for level, (spec_label, node) in pipeline.traverse(top_down=False):
        stage_id = level
        stage_name = f"stage-{level}"

        if stage_name not in stage_names:
            stage_names.append(stage_name)

        release_spec = node.spec
        release_spec_dag_hash = release_spec.dag_hash()

        job_object = spack_ci_ir["jobs"][release_spec_dag_hash]["attributes"]

        if not job_object:
            tty.warn("No match found for {0}, skipping it".format(release_spec))
            continue

        if spack_pipeline_type is not None:
            # For spack pipelines "public" and "protected" are reserved tags
            job_object["tags"] = _remove_reserved_tags(job_object.get("tags", []))
            if spack_pipeline_type == "spack_protected_branch":
                job_object["tags"].extend(["protected"])
            elif spack_pipeline_type == "spack_pull_request":
                job_object["tags"].extend(["public"])

        if "script" not in job_object:
            raise AttributeError

        def main_script_replacements(cmd):
            return cmd.replace("{env_dir}", rel_concrete_env_dir)

        job_object["script"] = _unpack_script(
            job_object["script"], op=main_script_replacements
        )

        if "before_script" in job_object:
            job_object["before_script"] = _unpack_script(job_object["before_script"])

        if "after_script" in job_object:
            job_object["after_script"] = _unpack_script(job_object["after_script"])

        job_name = get_job_name(release_spec, build_group)

        job_vars = job_object.setdefault("variables", {})
        job_vars["SPACK_JOB_SPEC_DAG_HASH"] = release_spec_dag_hash
        job_vars["SPACK_JOB_SPEC_PKG_NAME"] = release_spec.name
        job_vars["SPACK_JOB_SPEC_PKG_VERSION"] = release_spec.format("{version}")
        job_vars["SPACK_JOB_SPEC_COMPILER_NAME"] = release_spec.format("{compiler.name}")
        job_vars["SPACK_JOB_SPEC_COMPILER_VERSION"] = release_spec.format("{compiler.version}")
        job_vars["SPACK_JOB_SPEC_ARCH"] = release_spec.format("{architecture}")
        job_vars["SPACK_JOB_SPEC_VARIANTS"] = release_spec.format("{variants}")

        job_object["needs"] = []
        if spec_label in dependencies:
            if enable_artifacts_buildcache:
                # Get dependencies transitively, so they're all
                # available in the artifacts buildcache.
                dep_jobs = [d for d in release_spec.traverse(deptype="all", root=False)]
            else:
                # In this case, "needs" is only used for scheduling
                # purposes, so we only get the direct dependencies.
                dep_jobs = []
                for dep_label in dependencies[spec_label]:
                    dep_jobs.append(spec_labels[dep_label])

            job_object["needs"].extend(
                _format_job_needs(
                    dep_jobs,
                    build_group,
                    prune_dag,
                    rebuild_decisions,
                    enable_artifacts_buildcache,
                )
            )

        rebuild_spec = spec_record.rebuild

        if not rebuild_spec and not copy_only_pipeline:
            if prune_dag:
                spec_record.reason = "Pruned, up-to-date"
                continue
            else:
                # DAG pruning is disabled, force the spec to rebuild. The
                # record still contains any mirrors on which the spec
                # may have been found, so we can print them in the staging
                # summary.
                spec_record.rebuild = True
                spec_record.reason = "Scheduled, DAG pruning disabled"

        if artifacts_root:
            job_object["needs"].append(
                {"job": generate_job_name, "pipeline": "{0}".format(parent_pipeline_id)}
            )

        # Let downstream jobs know whether the spec needed rebuilding, regardless
        # whether DAG pruning was enabled or not.
        job_vars["SPACK_SPEC_NEEDS_REBUILD"] = str(rebuild_spec)

        if cdash_handler:
            cdash_handler.current_spec = release_spec
            build_name = cdash_handler.build_name
            all_job_names.append(build_name)
            job_vars["SPACK_CDASH_BUILD_NAME"] = build_name

            build_stamp = cdash_handler.build_stamp
            job_vars["SPACK_CDASH_BUILD_STAMP"] = build_stamp

        job_object["artifacts"] = spack.config.merge_yaml(
            job_object.get("artifacts", {}),
            {
                "when": "always",
                "paths": [
                    rel_job_log_dir,
                    rel_job_repro_dir,
                    rel_job_test_dir,
                    rel_user_artifacts_dir,
                ],
            },
        )

        # TODO: Remove this block in Spack 0.23
        if enable_artifacts_buildcache:
            bc_root = os.path.join(local_mirror_dir, "build_cache")
            job_object["artifacts"]["paths"].extend(
                [
                    os.path.join(bc_root, p)
                    for p in [
                        bindist.tarball_name(release_spec, ".spec.json"),
                        bindist.tarball_directory_name(release_spec),
                    ]
                ]
            )

        job_object["stage"] = stage_name
        job_object["retry"] = {"max": 2, "when": JOB_RETRY_CONDITIONS}
        job_object["interruptible"] = True

        length_needs = len(job_object["needs"])
        if length_needs > max_length_needs:
            max_length_needs = length_needs
            max_needs_job = job_name

        if not copy_only_pipeline:
            output_object[job_name] = job_object
            job_id += 1

    if print_summary:
        _print_staging_summary(spec_labels, stages, mirrors_to_check, rebuild_decisions)

    tty.debug("{0} build jobs generated in {1} stages".format(job_id, stage_id))

    if job_id > 0:
        tty.debug(
            "The max_needs_job is {0}, with {1} needs".format(max_needs_job, max_length_needs)
        )

    service_job_retries = {
        "max": 2,
        "when": ["runner_system_failure", "stuck_or_timeout_failure", "script_failure"],
    }

    if copy_only_pipeline and not config_deprecated:
        stage_names.append("copy")
        sync_job = copy.deepcopy(spack_ci_ir["jobs"]["copy"]["attributes"])
        sync_job["stage"] = "copy"
        if artifacts_root:
            sync_job["needs"] = [
                {"job": generate_job_name, "pipeline": "{0}".format(parent_pipeline_id)}
            ]

        if "variables" not in sync_job:
            sync_job["variables"] = {}

        sync_job["variables"]["SPACK_COPY_ONLY_DESTINATION"] = (
            buildcache_destination.fetch_url
            if buildcache_destination
            else remote_mirror_override or remote_mirror_url
        )

        if "buildcache-source" in pipeline_mirrors:
            buildcache_source = pipeline_mirrors["buildcache-source"].fetch_url
        else:
            # TODO: Remove this condition in Spack 0.23
            buildcache_source = os.environ.get("SPACK_SOURCE_MIRROR", None)
        sync_job["variables"]["SPACK_BUILDCACHE_SOURCE"] = buildcache_source

        output_object["copy"] = sync_job
        job_id += 1

    if job_id > 0:
        # TODO: Remove this block in Spack 0.23
        if temp_storage_url_prefix:
            # There were some rebuild jobs scheduled, so we will need to
            # schedule a job to clean up the temporary storage location
            # associated with this pipeline.
            stage_names.append("cleanup-temp-storage")
            cleanup_job = copy.deepcopy(spack_ci_ir["jobs"]["cleanup"]["attributes"])

            cleanup_job["stage"] = "cleanup-temp-storage"
            cleanup_job["when"] = "always"
            cleanup_job["retry"] = service_job_retries
            cleanup_job["interruptible"] = True

            cleanup_job["script"] = _unpack_script(
                cleanup_job["script"],
                op=lambda cmd: cmd.replace("mirror_prefix", temp_storage_url_prefix),
            )

            cleanup_job["dependencies"] = []
            output_object["cleanup"] = cleanup_job

        if (
            "script" in spack_ci_ir["jobs"]["signing"]["attributes"]
            and spack_pipeline_type == "spack_protected_branch"
        ):
            # External signing: generate a job to check and sign binary pkgs
            stage_names.append("stage-sign-pkgs")
            signing_job = spack_ci_ir["jobs"]["signing"]["attributes"]

            signing_job["script"] = _unpack_script(signing_job["script"])

            signing_job["stage"] = "stage-sign-pkgs"
            signing_job["when"] = "always"
            signing_job["retry"] = {"max": 2, "when": ["always"]}
            signing_job["interruptible"] = True
            if "variables" not in signing_job:
                signing_job["variables"] = {}
            signing_job["variables"]["SPACK_BUILDCACHE_DESTINATION"] = (
                buildcache_destination.push_url  # need the s3 url for aws s3 sync
                if buildcache_destination
                else remote_mirror_override or remote_mirror_url
            )
            signing_job["dependencies"] = []

            output_object["sign-pkgs"] = signing_job

        if rebuild_index_enabled:
            # Add a final job to regenerate the index
            stage_names.append("stage-rebuild-index")
            final_job = spack_ci_ir["jobs"]["reindex"]["attributes"]

            final_job["stage"] = "stage-rebuild-index"
            target_mirror = remote_mirror_override or remote_mirror_url
            if buildcache_destination:
                target_mirror = buildcache_destination.push_url
            final_job["script"] = _unpack_script(
                final_job["script"],
                op=lambda cmd: cmd.replace("{index_target_mirror}", target_mirror),
            )

            final_job["when"] = "always"
            final_job["retry"] = service_job_retries
            final_job["interruptible"] = True
            final_job["dependencies"] = []

            output_object["rebuild-index"] = final_job

        output_object["stages"] = stage_names

        # Capture the version of Spack used to generate the pipeline, that can be
        # passed to `git checkout` for version consistency. If we aren't in a Git
        # repository, presume we are a Spack release and use the Git tag instead.
        spack_version = spack.main.get_version()
        version_to_clone = spack.main.get_spack_commit() or f"v{spack.spack_version}"

        output_object["variables"] = {
            "SPACK_ARTIFACTS_ROOT": rel_artifacts_root,
            "SPACK_CONCRETE_ENV_DIR": rel_concrete_env_dir,
            "SPACK_VERSION": spack_version,
            "SPACK_CHECKOUT_VERSION": version_to_clone,
            # TODO: Remove this line in Spack 0.23
            "SPACK_REMOTE_MIRROR_URL": remote_mirror_url,
            "SPACK_JOB_LOG_DIR": rel_job_log_dir,
            "SPACK_JOB_REPRO_DIR": rel_job_repro_dir,
            "SPACK_JOB_TEST_DIR": rel_job_test_dir,
            # TODO: Remove this line in Spack 0.23
            "SPACK_LOCAL_MIRROR_DIR": rel_local_mirror_dir,
            "SPACK_PIPELINE_TYPE": str(spack_pipeline_type),
            "SPACK_CI_STACK_NAME": os.environ.get("SPACK_CI_STACK_NAME", "None"),
            # TODO: Remove this line in Spack 0.23
            "SPACK_CI_SHARED_PR_MIRROR_URL": shared_pr_mirror or "None",
            "SPACK_REBUILD_CHECK_UP_TO_DATE": str(prune_dag),
            "SPACK_REBUILD_EVERYTHING": str(rebuild_everything),
            "SPACK_REQUIRE_SIGNING": os.environ.get("SPACK_REQUIRE_SIGNING", "False"),
        }

        # TODO: Remove this block in Spack 0.23
        if deprecated_mirror_config and remote_mirror_override:
            (output_object["variables"]["SPACK_REMOTE_MIRROR_OVERRIDE"]) = remote_mirror_override

        spack_stack_name = os.environ.get("SPACK_CI_STACK_NAME", None)
        if spack_stack_name:
            output_object["variables"]["SPACK_CI_STACK_NAME"] = spack_stack_name

        # TODO(opadron): remove this or refactor
        if run_optimizer:
            import spack.ci_optimization as ci_opt

            output_object = ci_opt.optimizer(output_object)

        # TODO(opadron): remove this or refactor
        if use_dependencies:
            import spack.ci_needs_workaround as cinw

            output_object = cinw.needs_to_dependencies(output_object)
    else:
        # No jobs were generated
        noop_job = spack_ci_ir["jobs"]["noop"]["attributes"]
        noop_job["retry"] = service_job_retries

        if copy_only_pipeline and config_deprecated:
            tty.debug("Generating no-op job as copy-only is unsupported here.")
            noop_job["script"] = [
                'echo "copy-only pipelines are not supported with deprecated ci configs"'
            ]
            output_object = {"unsupported-copy": noop_job}
        else:
            tty.debug("No specs to rebuild, generating no-op job")
            output_object = {"no-specs-to-rebuild": noop_job}

    # Ensure the child pipeline always runs
    output_object["workflow"] = {"rules": [{"when": "always"}]}

    sorted_output = {}
    for output_key, output_value in sorted(output_object.items()):
        sorted_output[output_key] = output_value

    with open(output_file, "w") as outf:
        outf.write(syaml.dump(sorted_output, default_flow_style=True))
