# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import copy
import os
import shutil
import urllib
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import spack.vendor.ruamel.yaml

import spack
import spack.binary_distribution
import spack.config
import spack.environment as ev
import spack.llnl.util.tty as tty
import spack.mirrors.mirror
import spack.schema
import spack.spec
import spack.util.spack_yaml as syaml
from spack.util.path import canonicalize_path, substitute_path_variables

from .common import (
    CIJobData,
    CIScriptStage,
    PipelineDag,
    PipelineOptions,
    PipelineType,
    SpackCIConfig,
    SpackCIError,
    ensure_expected_target_path,
    spec_job_names,
    write_pipeline_manifest,
)
from .generator_registry import generator

# See https://docs.gitlab.com/ee/ci/yaml/#retry for descriptions of conditions
JOB_RETRY_CONDITIONS = [
    # "always",
    "unknown_failure",
    "script_failure",
    "api_failure",
    "stuck_or_timeout_failure",
    "runner_system_failure",
    "runner_unsupported",
    "stale_schedule",
    # "job_execution_timeout",
    "archived_failure",
    "unmet_prerequisites",
    "scheduler_failure",
    "data_integrity_failure",
]
JOB_NAME_FORMAT = "{name}{@version} {/hash}"


class GitlabJob(CIJobData):
    def __init__(
        self,
        name: str,
        spec: Optional[spack.spec.Spec] = None,
        remove: bool = False,
        config: GitlabCI = None,
    ):
        """
        Args:
            name: standard job name
            spec: release spec
            remove: ``True`` if a remove job; otherwise, ``False``
            config: configuration options
        """
        super().__init__(name, spec, remove)
        self.config: GitlabCI = config

        # TODO/TBD/TLD: Should the job_id start with 0 or 1?
        self.job_id: Optional[int] = None

    def __str__(self):
        return f"GitlabJob({self.name}, {self.spec}, {self.remove})"

    def convert_artifacts_dir(self):
        """Replace the env_dir placeholder with the environment's artifacts directory.

        The only script we care about for spec jobs is the main script.

        Raises:
            AttributeError: job does not have the expected script
        """
        # skip conversions non-spec jobs
        if self.name not in spec_job_names:
            tty.debug(f"{self}: skipping script conversion")
            return

        if CIScriptStage.DURING not in self.script:
            raise AttributeError(f"{self.name} is missing the required '{CIScriptStage.DURING}'")

        def _replace_env_dir(cmd: str):
            return cmd.replace("{env_dir}", self.config.path("env_artifacts_dir", absolute=False))

        self.script[CIScriptStage.DURING] = self.script[CIScriptStage.DURING].convert(
            _replace_env_dir
        )

    def convert_target_mirror(self):
        """Replace the env_dir placeholder with the environment's artifacts directory.

        Raises:
            AttributeError: job does not have the expected script
        """
        if CIScriptStage.DURING not in self.script:
            raise AttributeError(f"{self.name} is missing the required '{CIScriptStage.DURING}'")

        target_mirror = self.config.path("buildcache_push_url")
        self.script[CIScriptStage.DURING] = self.script[CIScriptStage.DURING].convert(
            lambda cmd: cmd.replace("{index_target_mirror}", target_mirror)
        )

    def add_pipeline_tags(self):
        """Add pipeline type-specific tags."""
        if self.config.options.pipeline_type is None:
            return

        # For spack pipelines "public" and "protected" are reserved tags
        self.remove_reserved_tags()
        if self.options.pipeline_type == PipelineType.PROTECTED_BRANCH:
            self.add_tags(["protected"])
        elif self.options.pipeline_type == PipelineType.PULL_REQUEST:
            self.add_tags(["public"])

    def update_build_data(self, job_id: int, build_group: str) -> int:
        """Ensure the build job has the correct build data.

        Args:
            job_id: job number
            build_group: name of the job's CDash build group

        Returns: next build id

        Raises:
            AssertionError: job name does not match expected core name
        """
        assert self.name == "build", f"Cannot update build data for non-build {self.name} job"

        self.job_id = job_id

        self.add_pipeline_tags()
        self.convert_artifacts_dir()

        # TODO/TLD: Resume here with processing job attributes
        self.attributes["stage"] = stage
        job_name = get_job_name(release_spec, build_group)

        # TODO/TLD: add "needs" to GitlabJob
        dep_nodes = pipeline.get_dependencies(node)
        self.attributes["needs"] = [
            {"job": get_job_name(dep_node.spec, build_group), "artifacts": False}
            for dep_node in dep_nodes
        ]
        self.attributes["needs"].append(
            {"job": self.generate_job_name, "pipeline": self.generate_pipeline_id}
        )

        # TODO/TLD: move variable handling to GitlabJob
        job_vars = self.attributes["variables"]

        # Let downstream jobs know whether the spec needed rebuilding, regardless
        # whether DAG pruning was enabled or not.
        already_built = spack.binary_distribution.get_mirrors_for_spec(
            spec=release_spec, index_only=True
        )
        job_vars["SPACK_SPEC_NEEDS_REBUILD"] = "False" if already_built else "True"

        if self.options.cdash_handler:
            build_name = self.options.cdash_handler.build_name(release_spec)
            job_vars["SPACK_CDASH_BUILD_NAME"] = build_name
            build_stamp = self.options.cdash_handler.build_stamp
            job_vars["SPACK_CDASH_BUILD_STAMP"] = build_stamp

        # TODO/TLD: shouldn't this be part of instantiating/converting
        # TODO/TLD:  a build (and maybe test) GitlabJob?
        job.merge_attributes(
            {
                "when": "always",
                "paths": [
                    self.path("log_artifacts_dir", absolute=False),
                    self.path("reproduction_artifacts_dir", absolute=False),
                    self.path("test_artifacts_dir", absolute=False),
                    self.path("user_artifacts_dir", absolute=False),
                ],
            }
        )

        # TODO/TLD: Should these be part of converting a build (and test?)
        # TODO/TLD: job?
        self.attributes["stage"] = stage_name
        self.attributes["retry"] = spack.schema.merge_yaml(
            {"max": 2, "when": JOB_RETRY_CONDITIONS}, self.attributes.get("retry", {})
        )
        self.attributes["interruptible"] = True

        length_needs = len(self.attributes["needs"])
        if length_needs > self.config.max_length_needs:
            self.config.max_length_needs = length_needs
            self.config.max_needs_job = job_name

        return job_id + 1

    def update_copy_data(self, job_id: int, stage: str):
        """Ensure the copy job has the correct dependency and buildcache setting.

        Args:
            job_id: job number
            stage: name of the job stage

        Raises:
            AssertionError: job name does not match expected core name
        """
        assert self.name == "copy", f"Cannot update copy data for non-copy {self.name} job"

        self.job_id = job_id

        self.attributes["stage"] = stage
        self.attributes["dependencies"] = []

        self.attributes["needs"] = [
            {"job": self.config.generate_job_name, "pipeline": self.config.generate_pipeline_id}
        ]

        if "variables" not in self.attributes:
            self.attributes["variables"] = {}
        self.attributes["variables"].update(
            {
                "SPACK_BUILDCACHE_RELATIVE_KEYS_URL": self.config.path("relative_keys_url"),
                "SPACK_BUILDCACHE_SOURCE": self.config.pipeline_mirrors[
                    "buildcache-source"
                ].fetch_url,
                "SPACK_COPY_ONLY_DESTINATION": self.config.path("buildcache_fetch_url"),
            }
        )

    def update_noop_data(self):
        """Ensure the noop job has the appropriate data.

        Args:
            stage: name of the job stage

        Raises:
            AssertionError: job name does not match expected core name
        """
        assert self.name == "noop", f"Cannot update noop data for non-noop  {self.name} job"

        # If this job fails ignore the status and carry on
        noop_job["retry"] = 0
        noop_job["allow_failure"] = True

    def update_reindex_data(self, stage: str):
        """Ensure the reindex job has the data.

        Args:
            stage: name of the job stage

        Raises:
            AssertionError: job name does not match expected core name
        """
        assert (
            self.name == "reindex"
        ), f"Cannot update reindex data for non-reindex  {self.name} job"

        self.convert_target_mirror()

        self.attributes["stage"] = stage
        self.attributes["when"] = "always"
        self.attributes["retry"] = {
            "max": 2,
            "when": ["runner_system_failure", "stuck_or_timeout_failure", "script_failure"],
        }
        self.attributes["interruptible"] = True
        self.attributes["dependencies"] = []

    def update_signing_data(self, stage: str):
        """Ensure the signing job has the data.

        Args:
            stage: name of the job stage

        Raises:
            AssertionError: job name does not match expected core name
        """
        assert (
            self.name == "signing"
        ), f"Cannot update signing data for non-signing {self.name} job"

        self.attributes["stage"] = stage
        self.attributes["when"] = "always"
        self.attributes["retry"] = {"max": 2, "when": ["always"]}
        self.attributes["dependencies"] = []
        self.attributes["interruptible"] = True

        if "variables" not in self.attributes:
            self.attributes["variables"] = {}
        self.attributes["variables"].update(
            {
                "SPACK_BUILDCACHE_DESTINATION": self.config.path("buildcache_push_url"),
                "SPACK_BUILDCACHE_RELATIVE_SPECS_URL": self.config.path("relative_specs_url"),
                "SPACK_BUILDCACHE_RELATIVE_KEYS_URL": self.config.path("relative_keys_url"),
            }
        )


class GitlabCI(SpackCIConfig):
    """Gitlab-specific CI configuration and options handler."""

    @classmethod
    def from_config(cls, config: SpackCIConfig, options: PipelineOptions) -> "GitlabCI":
        return cls(config.ci_config, options)

    def __init__(self, ci_config: Dict[str, Any], options: PipelineOptions):
        super().__init__(ci_config)

        self.generate_job_name: str = os.environ.get("CI_JOB_NAME", "job-does-not-exist")
        self.generate_pipeline_id: str = os.environ.get(
            "CI_PIPELINE_ID", "pipeline-does-not-exist"
        )
        self.pipeline_mirrors = spack.mirrors.mirror.MirrorCollection(binary=True)
        self.rebuild_everything = not options.prune_up_to_date and not options.prune_untouched

        self.options: PipelineOptions = options
        self.stages: List[List[str]] = []
        self.stage_names: List[str] = []
        self.output_jobs: List[Tuple(str, GitlabJob)] = []

        self._path: Dict[str, str] = {}
        self._add_paths()

        self.max_length_needs = 0
        self.max_needs_job = ""

    def _add_paths(self):
        """Add relevant CI paths."""
        ci_project_dir = os.environ.get("CI_PROJECT_DIR") or os.getcwd()

        artifacts_root = self.options.artifacts_root
        if artifacts_root.startswith(ci_project_dir):
            artifacts_root = os.path.relpath(artifacts_root, ci_project_dir)

        pipeline_artifacts_dir = os.path.join(ci_project_dir, artifacts_root)

        self._path["ci_project_dir"] = ci_project_dir
        self._path["relative_artifacts_root"] = artifacts_root

        self._path["pipeline_artifacts_dir"] = pipeline_artifacts_dir
        self._path["env_artifacts_dir"] = os.path.join(
            pipeline_artifacts_dir, "concrete_environment"
        )
        self._path["log_artifacts_dir"] = os.path.join(pipeline_artifacts_dir, "logs")
        self._path["reproduction_artifacts_dir"] = os.path.join(
            pipeline_artifacts_dir, "reproduction"
        )
        self._path["test_artifacts_dir"] = os.path.join(pipeline_artifacts_dir, "tests")
        self._path["user_artifacts_dir"] = os.path.join(pipeline_artifacts_dir, "user_data")

        output_file = self.options.output_file or ".gitlab-ci.yml"
        self._path["output_file"] = os.path.abspath(output_file)

        # TODO/TLD: Make  sure the buildcache_destination fetch+push urls used in proper locations
        self._path["buildcache_fetch_url"] = self.options.buildcache_destination.fetch_url
        self._path["buildcache_push_url"] = self.options.buildcache_destination.push_url
        self._path["relative_keys_url"] = spack.binary_distribution.buildcache_relative_keys_url()

    def customize_jobs(self):
        """Convert each CIJobData instance into a GitlabJob instance."""
        gitlab_jobs: Dict[str, List[CIJobData]] = {}
        for name, jobs in self.jobs.items():
            gitlab_jobs[name] = [GitlabJob(job.name, job.spec, job.remove, self) for job in jobs]
        self.jobs = gitlab_jobs

    def add_copy_stage(self, job_id: int) -> int:
        """Add the copy stage, used by copy-only pipelines, and update its data.

        Returns: next job id

        Raises:
            AssertionError: the default core job is missing
            SpackCIError:
                the required buildcache-source pipeline mirror is missing
        """
        job = self.job("copy")
        assert job, "The default core copy job is required."

        if "buildcache-source" not in self.pipeline_mirrors:
            raise SpackCIError("Copy-only pipelines require a mirror named 'buildcache-source'")

        stage = "copy"
        job.update_copy_data(job_id, stage)

        self.stage_names.append(stage)
        self.output_jobs.append((stage, job))
        return job_id + 1

    def add_no_specs_stage(self):
        """Add the no specs stage and update its data.

        Raises:
            AssertionError: the default core job is missing
        """
        job = self.job("noop")
        assert job, "The default core noop job is required."

        job.update_noop_data()
        return

    def add_rebuild_index_stage(self):
        """Add the rebuild index stage and update its job data.

        Raises:
            AssertionError: the default core job is missing
        """
        job = self.job("reindex")
        assert job, "The default core reindex job is required."

        stage = "stage-rebuild-index"
        job.update_reindex_data(stage)

        self.stage_names.append(stage)
        self.output_jobs.append(("rebuild-index", job))
        return

    def add_signing_stage(self):
        """Add the external signing stage, updating the job data accordingly.

        Raises:
            AssertionError: the default core job is missing
        """
        job = self.job("signing")
        assert job, "The default core signing job is required."

        if not (
            job.has_script(CIScriptStage.DURING)
            and self.options.pipeline_type == PipelineType.PROTECTED_BRANCH
        ):
            return

        stage = "stage-sign-pkgs"
        self.stage_names.append(stage)
        job.update_signing_data(stage)

        self.output_jobs.append(("sign-pkgs", job))
        return

    def copy_env_artifacts(self):
        """Copy the environment manifest and lock files to the environment
        artifacts directory."""
        env_artifacts_dir = self.path("env_artifacts_dir")
        if not os.path.exists(env_artifacts_dir):
            os.makedirs(env_artifacts_dir)

        self.copy_manifest_file()

        shutil.copyfile(
            self.options.env.lock_path, os.path.join(env_artifacts_dir, ev.lockfile_name)
        )

    def copy_manifest_file(self):
        """Copy the manifest file to the artifacts directory.

        Raises:
            spack.config.ConfigSectionError: top level is not 'spack'
        """
        env_artifacts_dir = self.path("env_artifacts_dir")
        with open(self.options.env.manifest_path, "r", encoding="utf-8") as fin, open(
            os.path.join(os.path.join(env_artifacts_dir, ev.manifest_name)), "w", encoding="utf-8"
        ) as fout:
            data = syaml.load(fin)
            if "spack" not in data:
                raise spack.config.ConfigSectionError(
                    'Missing top level "spack" section in environment'
                )

            def _rewrite_include(path, orig_root, new_root):
                expanded_path = substitute_path_variables(path)

                # Skip non-local paths
                parsed = urllib.parse.urlparse(expanded_path)
                file_schemes = ["", "file"]
                if parsed.scheme not in file_schemes:
                    return path

                if os.path.isabs(expanded_path):
                    return path
                abs_path = canonicalize_path(path, orig_root)
                return os.path.relpath(abs_path, start=new_root)

            # If there are no includes, just copy
            if "include" in data["spack"]:
                includes = data["spack"]["include"]
                # If there are includes in the config, then we need to fix the relative paths
                # to be relative from the concrete env dir used by downstream pipelines
                env_root_path = os.path.dirname(os.path.abspath(self.options.env.manifest_path))
                fixed_includes = []
                for inc in includes:
                    if isinstance(inc, dict):
                        inc["path"] = _rewrite_include(
                            inc["path"], env_root_path, env_artifacts_dir
                        )
                    else:
                        inc = _rewrite_include(inc, env_root_path, env_artifacts_dir)

                    fixed_includes.append(inc)

                data["spack"]["include"] = fixed_includes

            syaml.dump(data, fout)

    def path(self, name: str, absolute: bool = True) -> str:
        """Return the named path.

        Relative paths are used by downstream jobs to avoid issues in situations
        where the CI_PROJECT_DIR varies between the pipeline generation job and
        the rebuild jobs.  This can happen when gitlab checks out the project
        into a runner-specific directory, for example, and different runners are
        picked for generate and rebuild jobs.

        Args:
            name: name/key of the path
            absolute: ``True`` for the absolute directory; ``False`` for the
                path relative to CI_PROJECT_DIR

        Returns: named path

        Raises:
            ValueError: unknown name/key
        """
        if name not in self._path:
            raise ValueError(f"'{name}' is not a known directory")

        path = self._path[name]
        if absolute:
            return path

        return os.path.relpath(path, self._path["ci_project_dir"])

    def process_spec_stages(self, job_id: int, pipeline: PipelineDag) -> int:
        """Process pipeline specs.

        Assumes default pipeline build (and test) jobs have been created for
        each spec.

        Arguments:
            pipeline: pruned graph of jobs representing all of the specs to build
        Returns: next job id
        """
        build_group = (
            self.options.cdash_handler.build_group if self.options.cdash_handler else None
        )

        for level, node in pipeline.traverse_nodes(direction="parents"):
            stage_id = level
            if len(self.stages) == stage_id:
                self.stages.append([])

            self.stages[stage_id].append(node.spec)
            stage_name = f"stage-{level}"

            if stage_name not in self.stage_names:
                self.stage_names.append(stage_name)

            release_spec = node.spec
            release_spec_dag_hash = release_spec.dag_hash()

            # TODO/TLD: Replace with custom jobs processing
            # TODO/TLD: need to process build and test?
            job = self.job("build", node.spec)
            if not job:
                tty.warn(f"No match found for {release_spec}, skipping it")
                continue

            job_id = job.update_build_data(job_id, build_group)
            output_object[job_name] = job_object

        return job_id


def get_job_name(spec: spack.spec.Spec, build_group: Optional[str] = None) -> str:
    """Given a spec and possibly a build group, return the job name. If the
    resulting name is longer than 255 characters, it will be truncated.

    Arguments:
        spec: Spec job will build
        build_group: Name of build group this job belongs to (a CDash notion)

    Returns: The job name
    """
    job_name = spec.format(JOB_NAME_FORMAT)

    if build_group:
        job_name = f"{job_name} {build_group}"

    return job_name[:255]


# TODO/TLD: refactor this
def maybe_generate_manifest(pipeline: PipelineDag, options: PipelineOptions, manifest_path):
    # TODO: Consider including only hashes of rebuilt specs in the manifest,
    # instead of full source and destination urls.  Also, consider renaming
    # the variable that controls whether or not to write the manifest from
    # "SPACK_COPY_BUILDCACHE" to "SPACK_WRITE_PIPELINE_MANIFEST" or similar.
    spack_buildcache_copy = os.environ.get("SPACK_COPY_BUILDCACHE", None)
    if spack_buildcache_copy:
        buildcache_copy_src_prefix = options.buildcache_destination.fetch_url
        buildcache_copy_dest_prefix = spack_buildcache_copy

        if options.pipeline_type == PipelineType.COPY_ONLY:
            manifest_specs = [s for s in options.env.all_specs() if not s.external]
        else:
            manifest_specs = [n.spec for _, n in pipeline.traverse_nodes(direction="children")]

        write_pipeline_manifest(
            manifest_specs, buildcache_copy_src_prefix, buildcache_copy_dest_prefix, manifest_path
        )


@generator("gitlab")
def generate_gitlab_yaml(pipeline: PipelineDag, spack_ci: SpackCIConfig, options: PipelineOptions):
    """Given a pipeline graph, job attributes, and pipeline options,
    write a pipeline that can be consumed by GitLab to the given output file.

    Arguments:
        pipeline: An already pruned graph of jobs representing all the specs to build
        spack_ci: An object containing the configured attributes of all jobs in the pipeline
        options: An object containing all the pipeline options gathered from yaml, env, etc...
    """
    # Convert to gitlab-specific CI manager and jobs
    gitlab_ci = GitlabCI.from_config(spack_ci, options)
    gitlab_ci.customize_jobs()

    # Ensure directory of output file exists
    # Now that we've added the mirrors we know about, they should be properly
    # reflected in the environment manifest file, so copy that into the
    # concrete environment artifacts directory, along with the spack.lock file.
    gitlab_ci.copy_env_artifacts()

    # TODO/TLD: can't job_id be derived from the number of actual (build) jobs?
    # TODO/TLD: how does the introduction of test jobs affect this, eg, +1?
    job_id = 0

    # TODO/TLD: can't stage_id be returned from processing build [& test] jobs?
    stage_id = 0
    stages: List[List] = []

    # TODO/TLD: Switch this to process the jobs as GitlabJob's
    # spack_ci_ir = spack_ci.generate_ir()
    spack_ci_ir = gitlab_ci.generate_ir()

    # TODO/TLD: RESUME HERRE wrt processing specs
    if not options.pipeline_type == PipelineType.COPY_ONLY:
        job_id = gitlab_ci.process_spec_stages(job_id, pipeline)
        tty.debug(f"{job_id} build jobs generated in {stage_id} stages")

    if job_id > 0:
        tty.debug(
            f"The max_needs_job is {gitlab_ci.max_needs_job}, with {gitlab_ci.max_length_needs} needs"
        )

    # In some cases, pipeline generation should write a manifest.  Currently
    # the only purpose is to specify a list of sources and destinations for
    # everything that should be copied.
    distinguish_stack = options.stack_name if options.stack_name else "rebuilt"
    manifest_path = os.path.join(
        gitlab_ci.path("pipeline_artifacts_dir"),
        "specs_to_copy",
        f"copy_{distinguish_stack}_specs.json",
    )
    maybe_generate_manifest(pipeline, options, manifest_path)

    relative_specs_url = spack.binary_distribution.buildcache_relative_specs_url()

    if options.pipeline_type == PipelineType.COPY_ONLY:
        job_id = gitlab_ci.add_copy_stage(job_id)

    # TODO/TLD: Is this similar to pre-refactor check?
    # TODO/TLD: Seems like there should be a separate copy-only process
    # TODO/TLD:   that adds the signing stage, etc. instead of this stuff.
    # TODO/TLD:   Even then is the rebuild-index relevant to copy only?
    if job_id == 0:
        # No jobs were generated
        tty.debug("No specs to rebuild, generating no-op job")

        gitlab_ci.add_no_specs_stage()
        output_object = {"no-specs-to-rebuild": noop_job}

    else:
        gitlab_ci.add_signing_stage()

        if options.rebuild_index:
            gitlab_ci.add_rebuild_index_stage()

        output_object["stages"] = gitlab_ci.stage_names

        # Capture the version of Spack used to generate the pipeline, that can be
        # passed to `git checkout` for version consistency. If we aren't in a Git
        # repository, presume we are a Spack release and use the Git tag instead.
        spack_version = spack.get_version()
        version_to_clone = spack.get_spack_commit() or f"v{spack.spack_version}"

        output_object["variables"] = {
            "SPACK_ARTIFACTS_ROOT": gitlab_ci.path("artifacts_root"),
            "SPACK_CONCRETE_ENV_DIR": gitlab_ci.path("env_artifacts_dir", absolute=False),
            "SPACK_VERSION": spack_version,
            "SPACK_CHECKOUT_VERSION": version_to_clone,
            "SPACK_JOB_LOG_DIR": gitlab_ci.path("log_artifacts_dir", absolute=False),
            "SPACK_JOB_REPRO_DIR": gitlab_ci.path("reproduction_artifacts_dir"),
            "SPACK_JOB_TEST_DIR": gitlab_ci.path("test_artifacts_dir", absolute=False),
            "SPACK_PIPELINE_TYPE": options.pipeline_type.name if options.pipeline_type else "None",
            "SPACK_CI_STACK_NAME": os.environ.get("SPACK_CI_STACK_NAME", "None"),
            "SPACK_REBUILD_CHECK_UP_TO_DATE": str(options.prune_up_to_date),
            "SPACK_REBUILD_EVERYTHING": str(gitlab_ci.rebuild_everything),
            "SPACK_REQUIRE_SIGNING": str(options.require_signing),
        }
        output_object["variables"].update(
            dict([(v, os.environ[v]) for v in options.forward_variables if v in os.environ])
        )

        if options.stack_name:
            output_object["variables"]["SPACK_CI_STACK_NAME"] = options.stack_name

        output_vars = output_object["variables"]
        for item, val in output_vars.items():
            output_vars[item] = ensure_expected_target_path(val)

    # Ensure the child pipeline always runs
    output_object["workflow"] = {"rules": [{"when": "always"}]}

    sorted_output = {}
    for output_key, output_value in sorted(output_object.items()):
        sorted_output[output_key] = output_value

    # Minimize yaml output size through use of anchors
    syaml.anchorify(sorted_output)

    # Write the output file
    output_file = Path(gitlab_ci.path("output_file"))
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        spack.vendor.ruamel.yaml.YAML().dump(sorted_output, f)
