# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import base64
import codecs
import copy
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import zipfile
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import HTTPHandler, Request, build_opener

import llnl.util.filesystem as fs
import llnl.util.tty as tty
from llnl.util.lang import memoized

import spack
import spack.binary_distribution as bindist
import spack.compilers as compilers
import spack.config as cfg
import spack.environment as ev
import spack.main
import spack.mirror
import spack.paths
import spack.repo
import spack.util.git
import spack.util.gpg as gpg_util
import spack.util.spack_yaml as syaml
import spack.util.url as url_util
import spack.util.web as web_util
from spack.error import SpackError
from spack.reporters import CDash, CDashConfiguration
from spack.reporters.cdash import build_stamp as cdash_build_stamp

JOB_RETRY_CONDITIONS = ["always"]

TEMP_STORAGE_MIRROR_NAME = "ci_temporary_mirror"
SPACK_RESERVED_TAGS = ["public", "protected", "notary"]
SHARED_PR_MIRROR_URL = "s3://spack-binaries-prs/shared_pr_mirror"

spack_gpg = spack.main.SpackCommand("gpg")
spack_compiler = spack.main.SpackCommand("compiler")


class TemporaryDirectory(object):
    def __init__(self):
        self.temporary_directory = tempfile.mkdtemp()

    def __enter__(self):
        return self.temporary_directory

    def __exit__(self, exc_type, exc_value, exc_traceback):
        shutil.rmtree(self.temporary_directory)
        return False


def _is_main_phase(phase_name):
    return True if phase_name == "specs" else False


def get_job_name(phase, strip_compiler, spec, osarch, build_group):
    """Given the necessary parts, format the gitlab job name

    Arguments:
        phase (str): Either 'specs' for the main phase, or the name of a
            bootstrapping phase
        strip_compiler (bool): Should compiler be stripped from job name
        spec (spack.spec.Spec): Spec job will build
        osarch: Architecture TODO: (this is a spack.spec.ArchSpec,
            but sphinx doesn't recognize the type and fails).
        build_group (str): Name of build group this job belongs to (a CDash
        notion)

    Returns: The job name
    """
    item_idx = 0
    format_str = ""
    format_args = []

    if phase:
        format_str += "({{{0}}})".format(item_idx)
        format_args.append(phase)
        item_idx += 1

    format_str += " {{{0}}}".format(item_idx)
    format_args.append(spec.name)
    item_idx += 1

    format_str += "/{{{0}}}".format(item_idx)
    format_args.append(spec.dag_hash(7))
    item_idx += 1

    format_str += " {{{0}}}".format(item_idx)
    format_args.append(spec.version)
    item_idx += 1

    if _is_main_phase(phase) is True or strip_compiler is False:
        format_str += " {{{0}}}".format(item_idx)
        format_args.append(spec.compiler)
        item_idx += 1

    format_str += " {{{0}}}".format(item_idx)
    format_args.append(osarch)
    item_idx += 1

    if build_group:
        format_str += " {{{0}}}".format(item_idx)
        format_args.append(build_group)
        item_idx += 1

    return format_str.format(*format_args)


def _remove_reserved_tags(tags):
    """Convenience function to strip reserved tags from jobs"""
    return [tag for tag in tags if tag not in SPACK_RESERVED_TAGS]


def _get_spec_string(spec):
    format_elements = ["{name}{@version}", "{%compiler}"]

    if spec.architecture:
        format_elements.append(" {arch=architecture}")

    return spec.format("".join(format_elements))


def _spec_deps_key(s):
    return "{0}/{1}".format(s.name, s.dag_hash(7))


def _add_dependency(spec_label, dep_label, deps):
    if spec_label == dep_label:
        return
    if spec_label not in deps:
        deps[spec_label] = set()
    deps[spec_label].add(dep_label)


def _get_spec_dependencies(
    specs, deps, spec_labels, check_index_only=False, mirrors_to_check=None
):
    spec_deps_obj = _compute_spec_deps(
        specs, check_index_only=check_index_only, mirrors_to_check=mirrors_to_check
    )

    if spec_deps_obj:
        dependencies = spec_deps_obj["dependencies"]
        specs = spec_deps_obj["specs"]

        for entry in specs:
            spec_labels[entry["label"]] = {
                "spec": entry["spec"],
                "needs_rebuild": entry["needs_rebuild"],
            }

        for entry in dependencies:
            _add_dependency(entry["spec"], entry["depends"], deps)


def stage_spec_jobs(specs, check_index_only=False, mirrors_to_check=None):
    """Take a set of release specs and generate a list of "stages", where the
        jobs in any stage are dependent only on jobs in previous stages.  This
        allows us to maximize build parallelism within the gitlab-ci framework.

    Arguments:
        specs (Iterable): Specs to build
        check_index_only (bool): Regardless of whether DAG pruning is enabled,
            all configured mirrors are searched to see if binaries for specs
            are up to date on those mirrors.  This flag limits that search to
            the binary cache indices on those mirrors to speed the process up,
            even though there is no garantee the index is up to date.
        mirrors_to_checK: Optional mapping giving mirrors to check instead of
            any configured mirrors.

    Returns: A tuple of information objects describing the specs, dependencies
        and stages:

        spec_labels: A dictionary mapping the spec labels which are made of
            (pkg-name/hash-prefix), to objects containing "spec" and "needs_rebuild"
            keys.  The root spec is the spec of which this spec is a dependency
            and the spec is the formatted spec string for this spec.

        deps: A dictionary where the keys should also have appeared as keys in
            the spec_labels dictionary, and the values are the set of
            dependencies for that spec.

        stages: An ordered list of sets, each of which contains all the jobs to
            built in that stage.  The jobs are expressed in the same format as
            the keys in the spec_labels and deps objects.

    """

    # The convenience method below, "_remove_satisfied_deps()", does not modify
    # the "deps" parameter.  Instead, it returns a new dictionary where only
    # dependencies which have not yet been satisfied are included in the
    # return value.
    def _remove_satisfied_deps(deps, satisfied_list):
        new_deps = {}

        for key, value in deps.items():
            new_value = set([v for v in value if v not in satisfied_list])
            if new_value:
                new_deps[key] = new_value

        return new_deps

    deps = {}
    spec_labels = {}

    _get_spec_dependencies(
        specs,
        deps,
        spec_labels,
        check_index_only=check_index_only,
        mirrors_to_check=mirrors_to_check,
    )

    # Save the original deps, as we need to return them at the end of the
    # function.  In the while loop below, the "dependencies" variable is
    # overwritten rather than being modified each time through the loop,
    # thus preserving the original value of "deps" saved here.
    dependencies = deps
    unstaged = set(spec_labels.keys())
    stages = []

    while dependencies:
        dependents = set(dependencies.keys())
        next_stage = unstaged.difference(dependents)
        stages.append(next_stage)
        unstaged.difference_update(next_stage)
        # Note that "dependencies" is a dictionary mapping each dependent
        # package to the set of not-yet-handled dependencies.  The final step
        # below removes all the dependencies that are handled by this stage.
        dependencies = _remove_satisfied_deps(dependencies, next_stage)

    if unstaged:
        stages.append(unstaged.copy())

    return spec_labels, deps, stages


def _print_staging_summary(spec_labels, dependencies, stages):
    if not stages:
        return

    tty.msg("  Staging summary ([x] means a job needs rebuilding):")
    for stage_index, stage in enumerate(stages):
        tty.msg("    stage {0} ({1} jobs):".format(stage_index, len(stage)))

        for job in sorted(stage):
            s = spec_labels[job]["spec"]
            tty.msg(
                "      [{1}] {0} -> {2}".format(
                    job, "x" if spec_labels[job]["needs_rebuild"] else " ", _get_spec_string(s)
                )
            )


def _compute_spec_deps(spec_list, check_index_only=False, mirrors_to_check=None):
    """
    Computes all the dependencies for the spec(s) and generates a JSON
    object which provides both a list of unique spec names as well as a
    comprehensive list of all the edges in the dependency graph.  For
    example, given a single spec like 'readline@7.0', this function
    generates the following JSON object:

    .. code-block:: JSON

       {
           "dependencies": [
               {
                   "depends": "readline/ip6aiun",
                   "spec": "readline/ip6aiun"
               },
               {
                   "depends": "ncurses/y43rifz",
                   "spec": "readline/ip6aiun"
               },
               {
                   "depends": "ncurses/y43rifz",
                   "spec": "readline/ip6aiun"
               },
               {
                   "depends": "pkgconf/eg355zb",
                   "spec": "ncurses/y43rifz"
               },
               {
                   "depends": "pkgconf/eg355zb",
                   "spec": "readline/ip6aiun"
               }
           ],
           "specs": [
               {
                 "spec": "readline@7.0%apple-clang@9.1.0 arch=darwin-highs...",
                 "label": "readline/ip6aiun"
               },
               {
                 "spec": "ncurses@6.1%apple-clang@9.1.0 arch=darwin-highsi...",
                 "label": "ncurses/y43rifz"
               },
               {
                 "spec": "pkgconf@1.5.4%apple-clang@9.1.0 arch=darwin-high...",
                 "label": "pkgconf/eg355zb"
               }
           ]
       }

    """
    spec_labels = {}

    specs = []
    dependencies = []

    def append_dep(s, d):
        dependencies.append({"spec": s, "depends": d})

    for spec in spec_list:
        for s in spec.traverse(deptype=all):
            if s.external:
                tty.msg("Will not stage external pkg: {0}".format(s))
                continue

            up_to_date_mirrors = bindist.get_mirrors_for_spec(
                spec=s, mirrors_to_check=mirrors_to_check, index_only=check_index_only
            )

            skey = _spec_deps_key(s)
            spec_labels[skey] = {"spec": s, "needs_rebuild": not up_to_date_mirrors}

            for d in s.dependencies(deptype=all):
                dkey = _spec_deps_key(d)
                if d.external:
                    tty.msg("Will not stage external dep: {0}".format(d))
                    continue

                append_dep(skey, dkey)

    for spec_label, spec_holder in spec_labels.items():
        specs.append(
            {
                "label": spec_label,
                "spec": spec_holder["spec"],
                "needs_rebuild": spec_holder["needs_rebuild"],
            }
        )

    deps_json_obj = {"specs": specs, "dependencies": dependencies}

    return deps_json_obj


def _spec_matches(spec, match_string):
    return spec.intersects(match_string)


def _remove_attributes(src_dict, dest_dict):
    if "tags" in src_dict and "tags" in dest_dict:
        # For 'tags', we remove any tags that are listed for removal
        for tag in src_dict["tags"]:
            while tag in dest_dict["tags"]:
                dest_dict["tags"].remove(tag)


def _copy_attributes(attrs_list, src_dict, dest_dict):
    for runner_attr in attrs_list:
        if runner_attr in src_dict:
            if runner_attr in dest_dict and runner_attr == "tags":
                # For 'tags', we combine the lists of tags, while
                # avoiding duplicates
                for tag in src_dict[runner_attr]:
                    if tag not in dest_dict[runner_attr]:
                        dest_dict[runner_attr].append(tag)
            elif runner_attr in dest_dict and runner_attr == "variables":
                # For 'variables', we merge the dictionaries.  Any conflicts
                # (i.e. 'runner-attributes' has same variable key as the
                # higher level) we resolve by keeping the more specific
                # 'runner-attributes' version.
                for src_key, src_val in src_dict[runner_attr].items():
                    dest_dict[runner_attr][src_key] = copy.deepcopy(src_dict[runner_attr][src_key])
            else:
                dest_dict[runner_attr] = copy.deepcopy(src_dict[runner_attr])


def _find_matching_config(spec, gitlab_ci):
    runner_attributes = {}
    overridable_attrs = ["image", "tags", "variables", "before_script", "script", "after_script"]

    _copy_attributes(overridable_attrs, gitlab_ci, runner_attributes)

    matched = False
    only_first = gitlab_ci.get("match_behavior", "first") == "first"
    for ci_mapping in gitlab_ci["mappings"]:
        for match_string in ci_mapping["match"]:
            if _spec_matches(spec, match_string):
                matched = True
                if "remove-attributes" in ci_mapping:
                    _remove_attributes(ci_mapping["remove-attributes"], runner_attributes)
                if "runner-attributes" in ci_mapping:
                    _copy_attributes(
                        overridable_attrs, ci_mapping["runner-attributes"], runner_attributes
                    )
                break
        if matched and only_first:
            break

    return runner_attributes if matched else None


def _format_job_needs(
    phase_name,
    strip_compilers,
    dep_jobs,
    osname,
    build_group,
    prune_dag,
    stage_spec_dict,
    enable_artifacts_buildcache,
):
    needs_list = []
    for dep_job in dep_jobs:
        dep_spec_key = _spec_deps_key(dep_job)
        dep_spec_info = stage_spec_dict[dep_spec_key]

        if not prune_dag or dep_spec_info["needs_rebuild"]:
            needs_list.append(
                {
                    "job": get_job_name(
                        phase_name, strip_compilers, dep_job, dep_job.architecture, build_group
                    ),
                    "artifacts": enable_artifacts_buildcache,
                }
            )
    return needs_list


def get_change_revisions():
    """If this is a git repo get the revisions to use when checking
    for changed packages and spack core modules."""
    git_dir = os.path.join(spack.paths.prefix, ".git")
    if os.path.exists(git_dir) and os.path.isdir(git_dir):
        # TODO: This will only find changed packages from the last
        # TODO: commit.  While this may work for single merge commits
        # TODO: when merging the topic branch into the base, it will
        # TODO: require more thought outside of that narrow case.
        return "HEAD^", "HEAD"
    return None, None


def get_stack_changed(env_path, rev1="HEAD^", rev2="HEAD"):
    """Given an environment manifest path and two revisions to compare, return
    whether or not the stack was changed.  Returns True if the environment
    manifest changed between the provided revisions (or additionally if the
    `.gitlab-ci.yml` file itself changed).  Returns False otherwise."""
    git = spack.util.git.git()
    if git:
        with fs.working_dir(spack.paths.prefix):
            git_log = git(
                "diff",
                "--name-only",
                rev1,
                rev2,
                output=str,
                error=os.devnull,
                fail_on_error=False,
            ).strip()
            lines = [] if not git_log else re.split(r"\s+", git_log)

            for path in lines:
                if ".gitlab-ci.yml" in path or path in env_path:
                    tty.debug("env represented by {0} changed".format(env_path))
                    tty.debug("touched file: {0}".format(path))
                    return True
    return False


def compute_affected_packages(rev1="HEAD^", rev2="HEAD"):
    """Determine which packages were added, removed or changed
    between rev1 and rev2, and return the names as a set"""
    return spack.repo.get_all_package_diffs("ARC", rev1=rev1, rev2=rev2)


def get_spec_filter_list(env, affected_pkgs, dependent_traverse_depth=None):
    """Given a list of package names and an active/concretized
       environment, return the set of all concrete specs from the
       environment that could have been affected by changing the
       list of packages.

       If a ``dependent_traverse_depth`` is given, it is used to limit
       upward (in the parent direction) traversal of specs of touched
       packages.  E.g. if 1 is provided, then only direct dependents
       of touched package specs are traversed to produce specs that
       could have been affected by changing the package, while if 0 is
       provided, only the changed specs themselves are traversed. If ``None``
       is given, upward traversal of touched package specs is done all
       the way to the environment roots.  Providing a negative number
       results in no traversals at all, yielding an empty set.

    Arguments:

        env (spack.environment.Environment): Active concrete environment
        affected_pkgs (List[str]): Affected package names
        dependent_traverse_depth: Optional integer to limit dependent
            traversal, or None to disable the limit.

    Returns:

        A set of concrete specs from the active environment including
        those associated with affected packages, their dependencies and
        dependents, as well as their dependents dependencies.
    """
    affected_specs = set()
    all_concrete_specs = env.all_specs()
    tty.debug("All concrete environment specs:")
    for s in all_concrete_specs:
        tty.debug("  {0}/{1}".format(s.name, s.dag_hash()[:7]))
    env_matches = [s for s in all_concrete_specs if s.name in frozenset(affected_pkgs)]
    visited = set()
    dag_hash = lambda s: s.dag_hash()
    for match in env_matches:
        for dep_level, parent in match.traverse(direction="parents", key=dag_hash, depth=True):
            if dependent_traverse_depth is None or dep_level <= dependent_traverse_depth:
                affected_specs.update(
                    parent.traverse(direction="children", visited=visited, key=dag_hash)
                )
    return affected_specs


def generate_gitlab_ci_yaml(
    env,
    print_summary,
    output_file,
    prune_dag=False,
    check_index_only=False,
    run_optimizer=False,
    use_dependencies=False,
    artifacts_root=None,
    remote_mirror_override=None,
):
    """Generate a gitlab yaml file to run a dynamic child pipeline from
        the spec matrix in the active environment.

    Arguments:
        env (spack.environment.Environment): Activated environment object
            which must contain a gitlab-ci section describing how to map
            specs to runners
        print_summary (bool): Should we print a summary of all the jobs in
            the stages in which they were placed.
        output_file (str): File path where generated file should be written
        prune_dag (bool): If True, do not generate jobs for specs already
            exist built on the mirror.
        check_index_only (bool): If True, attempt to fetch the mirror index
            and only use that to determine whether built specs on the mirror
            this mode results in faster yaml generation time). Otherwise, also
            check each spec directly by url (useful if there is no index or it
            might be out of date).
        run_optimizer (bool): If True, post-process the generated yaml to try
            try to reduce the size (attempts to collect repeated configuration
            and replace with definitions).)
        use_dependencies (bool): If true, use "dependencies" rather than "needs"
            ("needs" allows DAG scheduling).  Useful if gitlab instance cannot
            be configured to handle more than a few "needs" per job.
        artifacts_root (str): Path where artifacts like logs, environment
            files (spack.yaml, spack.lock), etc should be written.  GitLab
            requires this to be within the project directory.
        remote_mirror_override (str): Typically only needed when one spack.yaml
            is used to populate several mirrors with binaries, based on some
            criteria.  Spack protected pipelines populate different mirrors based
            on branch name, facilitated by this option.
    """
    with spack.concretize.disable_compiler_existence_check():
        with env.write_transaction():
            env.concretize()
            env.write()

    yaml_root = ev.config_dict(env.yaml)

    if "gitlab-ci" not in yaml_root:
        tty.die('Environment yaml does not have "gitlab-ci" section')

    gitlab_ci = yaml_root["gitlab-ci"]

    cdash_handler = CDashHandler(yaml_root.get("cdash")) if "cdash" in yaml_root else None
    build_group = cdash_handler.build_group if cdash_handler else None

    dependent_depth = os.environ.get("SPACK_PRUNE_UNTOUCHED_DEPENDENT_DEPTH", None)
    if dependent_depth is not None:
        try:
            dependent_depth = int(dependent_depth)
        except (TypeError, ValueError):
            tty.warn(
                "Unrecognized value ({0}) ".format(dependent_depth),
                "provide forSPACK_PRUNE_UNTOUCHED_DEPENDENT_DEPTH, ",
                "ignoring it.",
            )
            dependent_depth = None

    prune_untouched_packages = False
    spack_prune_untouched = os.environ.get("SPACK_PRUNE_UNTOUCHED", None)
    if spack_prune_untouched is not None and spack_prune_untouched.lower() == "true":
        # Requested to prune untouched packages, but assume we won't do that
        # unless we're actually in a git repo.
        rev1, rev2 = get_change_revisions()
        tty.debug("Got following revisions: rev1={0}, rev2={1}".format(rev1, rev2))
        if rev1 and rev2:
            # If the stack file itself did not change, proceed with pruning
            if not get_stack_changed(env.manifest_path, rev1, rev2):
                prune_untouched_packages = True
                affected_pkgs = compute_affected_packages(rev1, rev2)
                tty.debug("affected pkgs:")
                for p in affected_pkgs:
                    tty.debug("  {0}".format(p))
                affected_specs = get_spec_filter_list(
                    env, affected_pkgs, dependent_traverse_depth=dependent_depth
                )
                tty.debug("all affected specs:")
                for s in affected_specs:
                    tty.debug("  {0}/{1}".format(s.name, s.dag_hash()[:7]))

    # Allow overriding --prune-dag cli opt with environment variable
    prune_dag_override = os.environ.get("SPACK_PRUNE_UP_TO_DATE", None)
    if prune_dag_override is not None:
        prune_dag = True if prune_dag_override.lower() == "true" else False

    # If we are not doing any kind of pruning, we are rebuilding everything
    rebuild_everything = not prune_dag and not prune_untouched_packages

    # Downstream jobs will "need" (depend on, for both scheduling and
    # artifacts, which include spack.lock file) this pipeline generation
    # job by both name and pipeline id.  If those environment variables
    # do not exist, then maybe this is just running in a shell, in which
    # case, there is no expectation gitlab will ever run the generated
    # pipeline and those environment variables do not matter.
    generate_job_name = os.environ.get("CI_JOB_NAME", "job-does-not-exist")
    parent_pipeline_id = os.environ.get("CI_PIPELINE_ID", "pipeline-does-not-exist")

    # Values: "spack_pull_request", "spack_protected_branch", or not set
    spack_pipeline_type = os.environ.get("SPACK_PIPELINE_TYPE", None)

    if "mirrors" not in yaml_root or len(yaml_root["mirrors"].values()) < 1:
        tty.die("spack ci generate requires an env containing a mirror")

    ci_mirrors = yaml_root["mirrors"]
    mirror_urls = [url for url in ci_mirrors.values()]
    remote_mirror_url = mirror_urls[0]

    spack_buildcache_copy = os.environ.get("SPACK_COPY_BUILDCACHE", None)
    if spack_buildcache_copy:
        buildcache_copies = {}
        buildcache_copy_src_prefix = remote_mirror_override or remote_mirror_url
        buildcache_copy_dest_prefix = spack_buildcache_copy

    # Check for a list of "known broken" specs that we should not bother
    # trying to build.
    broken_specs_url = ""
    known_broken_specs_encountered = []
    if "broken-specs-url" in gitlab_ci:
        broken_specs_url = gitlab_ci["broken-specs-url"]

    enable_artifacts_buildcache = False
    if "enable-artifacts-buildcache" in gitlab_ci:
        enable_artifacts_buildcache = gitlab_ci["enable-artifacts-buildcache"]

    rebuild_index_enabled = True
    if "rebuild-index" in gitlab_ci and gitlab_ci["rebuild-index"] is False:
        rebuild_index_enabled = False

    temp_storage_url_prefix = None
    if "temporary-storage-url-prefix" in gitlab_ci:
        temp_storage_url_prefix = gitlab_ci["temporary-storage-url-prefix"]

    bootstrap_specs = []
    phases = []
    if "bootstrap" in gitlab_ci:
        for phase in gitlab_ci["bootstrap"]:
            try:
                phase_name = phase.get("name")
                strip_compilers = phase.get("compiler-agnostic")
            except AttributeError:
                phase_name = phase
                strip_compilers = False
            phases.append({"name": phase_name, "strip-compilers": strip_compilers})

            for bs in env.spec_lists[phase_name]:
                bootstrap_specs.append(
                    {"spec": bs, "phase-name": phase_name, "strip-compilers": strip_compilers}
                )

    phases.append({"name": "specs", "strip-compilers": False})

    # If a remote mirror override (alternate buildcache destination) was
    # specified, add it here in case it has already built hashes we might
    # generate.
    mirrors_to_check = None
    if remote_mirror_override:
        if spack_pipeline_type == "spack_protected_branch":
            # Overriding the main mirror in this case might result
            # in skipping jobs on a release pipeline because specs are
            # up to date in develop.  Eventually we want to notice and take
            # advantage of this by scheduling a job to copy the spec from
            # develop to the release, but until we have that, this makes
            # sure we schedule a rebuild job if the spec isn't already in
            # override mirror.
            mirrors_to_check = {"override": remote_mirror_override}

        # If we have a remote override and we want generate pipeline using
        # --check-index-only, then the override mirror needs to be added to
        # the configured mirrors when bindist.update() is run, or else we
        # won't fetch its index and include in our local cache.
        spack.mirror.add(
            spack.mirror.Mirror(remote_mirror_override, name="ci_pr_mirror"),
            cfg.default_modify_scope(),
        )

    shared_pr_mirror = None
    if spack_pipeline_type == "spack_pull_request":
        stack_name = os.environ.get("SPACK_CI_STACK_NAME", "")
        shared_pr_mirror = url_util.join(SHARED_PR_MIRROR_URL, stack_name)
        spack.mirror.add(
            spack.mirror.Mirror(shared_pr_mirror, name="ci_shared_pr_mirror"),
            cfg.default_modify_scope(),
        )

    pipeline_artifacts_dir = artifacts_root
    if not pipeline_artifacts_dir:
        proj_dir = os.environ.get("CI_PROJECT_DIR", os.getcwd())
        pipeline_artifacts_dir = os.path.join(proj_dir, "jobs_scratch_dir")

    pipeline_artifacts_dir = os.path.abspath(pipeline_artifacts_dir)
    concrete_env_dir = os.path.join(pipeline_artifacts_dir, "concrete_environment")

    # Now that we've added the mirrors we know about, they should be properly
    # reflected in the environment manifest file, so copy that into the
    # concrete environment directory, along with the spack.lock file.
    if not os.path.exists(concrete_env_dir):
        os.makedirs(concrete_env_dir)
    shutil.copyfile(env.manifest_path, os.path.join(concrete_env_dir, "spack.yaml"))
    shutil.copyfile(env.lock_path, os.path.join(concrete_env_dir, "spack.lock"))

    job_log_dir = os.path.join(pipeline_artifacts_dir, "logs")
    job_repro_dir = os.path.join(pipeline_artifacts_dir, "reproduction")
    job_test_dir = os.path.join(pipeline_artifacts_dir, "tests")
    local_mirror_dir = os.path.join(pipeline_artifacts_dir, "mirror")
    user_artifacts_dir = os.path.join(pipeline_artifacts_dir, "user_data")

    # We communicate relative paths to the downstream jobs to avoid issues in
    # situations where the CI_PROJECT_DIR varies between the pipeline
    # generation job and the rebuild jobs.  This can happen when gitlab
    # checks out the project into a runner-specific directory, for example,
    # and different runners are picked for generate and rebuild jobs.
    ci_project_dir = os.environ.get("CI_PROJECT_DIR")
    rel_artifacts_root = os.path.relpath(pipeline_artifacts_dir, ci_project_dir)
    rel_concrete_env_dir = os.path.relpath(concrete_env_dir, ci_project_dir)
    rel_job_log_dir = os.path.relpath(job_log_dir, ci_project_dir)
    rel_job_repro_dir = os.path.relpath(job_repro_dir, ci_project_dir)
    rel_job_test_dir = os.path.relpath(job_test_dir, ci_project_dir)
    rel_local_mirror_dir = os.path.join(local_mirror_dir, ci_project_dir)
    rel_user_artifacts_dir = os.path.relpath(user_artifacts_dir, ci_project_dir)

    # Speed up staging by first fetching binary indices from all mirrors
    # (including the override mirror we may have just added above).
    try:
        bindist.binary_index.update()
    except bindist.FetchCacheError as e:
        tty.error(e)

    staged_phases = {}
    try:
        for phase in phases:
            phase_name = phase["name"]
            if phase_name == "specs":
                # Anything in the "specs" of the environment are already
                # concretized by the block at the top of this method, so we
                # only need to find the concrete versions, and then avoid
                # re-concretizing them needlessly later on.
                concrete_phase_specs = [
                    concrete
                    for abstract, concrete in env.concretized_specs()
                    if abstract in env.spec_lists[phase_name]
                ]
            else:
                # Any specs lists in other definitions (but not in the
                # "specs") of the environment are not yet concretized so we
                # have to concretize them explicitly here.
                concrete_phase_specs = env.spec_lists[phase_name]
                with spack.concretize.disable_compiler_existence_check():
                    for phase_spec in concrete_phase_specs:
                        phase_spec.concretize()
            staged_phases[phase_name] = stage_spec_jobs(
                concrete_phase_specs,
                check_index_only=check_index_only,
                mirrors_to_check=mirrors_to_check,
            )
    finally:
        # Clean up remote mirror override if enabled
        if remote_mirror_override:
            spack.mirror.remove("ci_pr_mirror", cfg.default_modify_scope())
        if spack_pipeline_type == "spack_pull_request":
            spack.mirror.remove("ci_shared_pr_mirror", cfg.default_modify_scope())

    all_job_names = []
    output_object = {}
    job_id = 0
    stage_id = 0

    stage_names = []

    max_length_needs = 0
    max_needs_job = ""

    # If this is configured, spack will fail "spack ci generate" if it
    # generates any hash which exists under the broken specs url.
    broken_spec_urls = None
    if broken_specs_url:
        if broken_specs_url.startswith("http"):
            # To make checking each spec against the list faster, we require
            # a url protocol that allows us to iterate the url in advance.
            tty.msg("Cannot use an http(s) url for broken specs, ignoring")
        else:
            broken_spec_urls = web_util.list_url(broken_specs_url)

    before_script, after_script = None, None
    for phase in phases:
        phase_name = phase["name"]
        strip_compilers = phase["strip-compilers"]

        spec_labels, dependencies, stages = staged_phases[phase_name]

        for stage_jobs in stages:
            stage_name = "stage-{0}".format(stage_id)
            stage_names.append(stage_name)
            stage_id += 1

            for spec_label in stage_jobs:
                spec_record = spec_labels[spec_label]
                release_spec = spec_record["spec"]
                release_spec_dag_hash = release_spec.dag_hash()

                if prune_untouched_packages:
                    if release_spec not in affected_specs:
                        tty.debug(
                            "Pruning {0}/{1}, untouched by change.".format(
                                release_spec.name, release_spec.dag_hash()[:7]
                            )
                        )
                        spec_record["needs_rebuild"] = False
                        continue

                runner_attribs = _find_matching_config(release_spec, gitlab_ci)

                if not runner_attribs:
                    tty.warn("No match found for {0}, skipping it".format(release_spec))
                    continue

                tags = [tag for tag in runner_attribs["tags"]]

                if spack_pipeline_type is not None:
                    # For spack pipelines "public" and "protected" are reserved tags
                    tags = _remove_reserved_tags(tags)
                    if spack_pipeline_type == "spack_protected_branch":
                        tags.extend(["protected"])
                    elif spack_pipeline_type == "spack_pull_request":
                        tags.extend(["public"])

                variables = {}
                if "variables" in runner_attribs:
                    variables.update(runner_attribs["variables"])

                image_name = None
                image_entry = None
                if "image" in runner_attribs:
                    build_image = runner_attribs["image"]
                    try:
                        image_name = build_image.get("name")
                        entrypoint = build_image.get("entrypoint")
                        image_entry = [p for p in entrypoint]
                    except AttributeError:
                        image_name = build_image

                job_script = ["spack env activate --without-view ."]

                if artifacts_root:
                    job_script.insert(0, "cd {0}".format(concrete_env_dir))

                job_script.extend(["spack ci rebuild"])

                if "script" in runner_attribs:
                    job_script = [s for s in runner_attribs["script"]]

                before_script = None
                if "before_script" in runner_attribs:
                    before_script = [s for s in runner_attribs["before_script"]]

                after_script = None
                if "after_script" in runner_attribs:
                    after_script = [s for s in runner_attribs["after_script"]]

                osname = str(release_spec.architecture)
                job_name = get_job_name(
                    phase_name, strip_compilers, release_spec, osname, build_group
                )

                compiler_action = "NONE"
                if len(phases) > 1:
                    compiler_action = "FIND_ANY"
                    if _is_main_phase(phase_name):
                        compiler_action = "INSTALL_MISSING"

                job_vars = {
                    "SPACK_JOB_SPEC_DAG_HASH": release_spec_dag_hash,
                    "SPACK_JOB_SPEC_PKG_NAME": release_spec.name,
                    "SPACK_COMPILER_ACTION": compiler_action,
                }

                job_dependencies = []
                if spec_label in dependencies:
                    if enable_artifacts_buildcache:
                        # Get dependencies transitively, so they're all
                        # available in the artifacts buildcache.
                        dep_jobs = [d for d in release_spec.traverse(deptype=all, root=False)]
                    else:
                        # In this case, "needs" is only used for scheduling
                        # purposes, so we only get the direct dependencies.
                        dep_jobs = []
                        for dep_label in dependencies[spec_label]:
                            dep_jobs.append(spec_labels[dep_label]["spec"])

                    job_dependencies.extend(
                        _format_job_needs(
                            phase_name,
                            strip_compilers,
                            dep_jobs,
                            osname,
                            build_group,
                            prune_dag,
                            spec_labels,
                            enable_artifacts_buildcache,
                        )
                    )

                rebuild_spec = spec_record["needs_rebuild"]

                # This next section helps gitlab make sure the right
                # bootstrapped compiler exists in the artifacts buildcache by
                # creating an artificial dependency between this spec and its
                # compiler.  So, if we are in the main phase, and if the
                # compiler we are supposed to use is listed in any of the
                # bootstrap spec lists, then we will add more dependencies to
                # the job (that compiler and maybe it's dependencies as well).
                if _is_main_phase(phase_name):
                    spec_arch_family = release_spec.architecture.target.microarchitecture.family
                    compiler_pkg_spec = compilers.pkg_spec_for_compiler(release_spec.compiler)
                    for bs in bootstrap_specs:
                        c_spec = bs["spec"]
                        bs_arch = c_spec.architecture
                        bs_arch_family = bs_arch.target.microarchitecture.family
                        if (
                            c_spec.intersects(compiler_pkg_spec)
                            and bs_arch_family == spec_arch_family
                        ):
                            # We found the bootstrap compiler this release spec
                            # should be built with, so for DAG scheduling
                            # purposes, we will at least add the compiler spec
                            # to the jobs "needs".  But if artifact buildcache
                            # is enabled, we'll have to add all transtive deps
                            # of the compiler as well.

                            # Here we check whether the bootstrapped compiler
                            # needs to be rebuilt.  Until compilers are proper
                            # dependencies, we artificially force the spec to
                            # be rebuilt if the compiler targeted to build it
                            # needs to be rebuilt.
                            bs_specs, _, _ = staged_phases[bs["phase-name"]]
                            c_spec_key = _spec_deps_key(c_spec)
                            rbld_comp = bs_specs[c_spec_key]["needs_rebuild"]
                            rebuild_spec = rebuild_spec or rbld_comp
                            # Also update record so dependents do not fail to
                            # add this spec to their "needs"
                            spec_record["needs_rebuild"] = rebuild_spec

                            dep_jobs = [c_spec]
                            if enable_artifacts_buildcache:
                                dep_jobs = [d for d in c_spec.traverse(deptype=all)]

                            job_dependencies.extend(
                                _format_job_needs(
                                    bs["phase-name"],
                                    bs["strip-compilers"],
                                    dep_jobs,
                                    str(bs_arch),
                                    build_group,
                                    prune_dag,
                                    bs_specs,
                                    enable_artifacts_buildcache,
                                )
                            )
                        else:
                            debug_msg = "".join(
                                [
                                    "Considered compiler {0} for spec ",
                                    "{1}, but rejected it either because it was ",
                                    "not the compiler required by the spec, or ",
                                    "because the target arch families of the ",
                                    "spec and the compiler did not match",
                                ]
                            ).format(c_spec, release_spec)
                            tty.debug(debug_msg)

                if prune_dag and not rebuild_spec:
                    tty.debug(
                        "Pruning {0}/{1}, does not need rebuild.".format(
                            release_spec.name, release_spec.dag_hash()
                        )
                    )
                    continue

                if broken_spec_urls is not None and release_spec_dag_hash in broken_spec_urls:
                    known_broken_specs_encountered.append(release_spec_dag_hash)

                # Only keep track of these if we are copying rebuilt cache entries
                if spack_buildcache_copy:
                    # TODO: This assumes signed version of the spec
                    buildcache_copies[release_spec_dag_hash] = [
                        {
                            "src": url_util.join(
                                buildcache_copy_src_prefix,
                                bindist.build_cache_relative_path(),
                                bindist.tarball_name(release_spec, ".spec.json.sig"),
                            ),
                            "dest": url_util.join(
                                buildcache_copy_dest_prefix,
                                bindist.build_cache_relative_path(),
                                bindist.tarball_name(release_spec, ".spec.json.sig"),
                            ),
                        },
                        {
                            "src": url_util.join(
                                buildcache_copy_src_prefix,
                                bindist.build_cache_relative_path(),
                                bindist.tarball_path_name(release_spec, ".spack"),
                            ),
                            "dest": url_util.join(
                                buildcache_copy_dest_prefix,
                                bindist.build_cache_relative_path(),
                                bindist.tarball_path_name(release_spec, ".spack"),
                            ),
                        },
                    ]

                if artifacts_root:
                    job_dependencies.append(
                        {"job": generate_job_name, "pipeline": "{0}".format(parent_pipeline_id)}
                    )

                job_vars["SPACK_SPEC_NEEDS_REBUILD"] = str(rebuild_spec)

                if cdash_handler:
                    cdash_handler.current_spec = release_spec
                    build_name = cdash_handler.build_name
                    all_job_names.append(build_name)
                    job_vars["SPACK_CDASH_BUILD_NAME"] = build_name

                    build_stamp = cdash_handler.build_stamp
                    job_vars["SPACK_CDASH_BUILD_STAMP"] = build_stamp

                variables.update(job_vars)

                artifact_paths = [
                    rel_job_log_dir,
                    rel_job_repro_dir,
                    rel_job_test_dir,
                    rel_user_artifacts_dir,
                ]

                if enable_artifacts_buildcache:
                    bc_root = os.path.join(local_mirror_dir, "build_cache")
                    artifact_paths.extend(
                        [
                            os.path.join(bc_root, p)
                            for p in [
                                bindist.tarball_name(release_spec, ".spec.json"),
                                bindist.tarball_directory_name(release_spec),
                            ]
                        ]
                    )

                job_object = {
                    "stage": stage_name,
                    "variables": variables,
                    "script": job_script,
                    "tags": tags,
                    "artifacts": {"paths": artifact_paths, "when": "always"},
                    "needs": sorted(job_dependencies, key=lambda d: d["job"]),
                    "retry": {"max": 2, "when": JOB_RETRY_CONDITIONS},
                    "interruptible": True,
                }

                length_needs = len(job_dependencies)
                if length_needs > max_length_needs:
                    max_length_needs = length_needs
                    max_needs_job = job_name

                if before_script:
                    job_object["before_script"] = before_script

                if after_script:
                    job_object["after_script"] = after_script

                if image_name:
                    job_object["image"] = image_name
                    if image_entry is not None:
                        job_object["image"] = {"name": image_name, "entrypoint": image_entry}

                output_object[job_name] = job_object
                job_id += 1

    if print_summary:
        for phase in phases:
            phase_name = phase["name"]
            tty.msg('Stages for phase "{0}"'.format(phase_name))
            phase_stages = staged_phases[phase_name]
            _print_staging_summary(*phase_stages)

    tty.debug("{0} build jobs generated in {1} stages".format(job_id, stage_id))

    if job_id > 0:
        tty.debug(
            "The max_needs_job is {0}, with {1} needs".format(max_needs_job, max_length_needs)
        )

    # Use "all_job_names" to populate the build group for this set
    if cdash_handler and cdash_handler.auth_token:
        try:
            cdash_handler.populate_buildgroup(all_job_names)
        except (SpackError, HTTPError, URLError) as err:
            tty.warn("Problem populating buildgroup: {0}".format(err))
    else:
        tty.warn("Unable to populate buildgroup without CDash credentials")

    service_job_config = None
    if "service-job-attributes" in gitlab_ci:
        service_job_config = gitlab_ci["service-job-attributes"]

    default_attrs = [
        "image",
        "tags",
        "variables",
        "before_script",
        # 'script',
        "after_script",
    ]

    service_job_retries = {
        "max": 2,
        "when": ["runner_system_failure", "stuck_or_timeout_failure", "script_failure"],
    }

    if job_id > 0:
        if temp_storage_url_prefix:
            # There were some rebuild jobs scheduled, so we will need to
            # schedule a job to clean up the temporary storage location
            # associated with this pipeline.
            stage_names.append("cleanup-temp-storage")
            cleanup_job = {}

            if service_job_config:
                _copy_attributes(default_attrs, service_job_config, cleanup_job)

            if "tags" in cleanup_job:
                service_tags = _remove_reserved_tags(cleanup_job["tags"])
                cleanup_job["tags"] = service_tags

            cleanup_job["stage"] = "cleanup-temp-storage"
            cleanup_job["script"] = [
                "spack -d mirror destroy --mirror-url {0}/$CI_PIPELINE_ID".format(
                    temp_storage_url_prefix
                )
            ]
            cleanup_job["when"] = "always"
            cleanup_job["retry"] = service_job_retries
            cleanup_job["interruptible"] = True

            output_object["cleanup"] = cleanup_job

        if (
            "signing-job-attributes" in gitlab_ci
            and spack_pipeline_type == "spack_protected_branch"
        ):
            # External signing: generate a job to check and sign binary pkgs
            stage_names.append("stage-sign-pkgs")
            signing_job_config = gitlab_ci["signing-job-attributes"]
            signing_job = {}

            signing_job_attrs_to_copy = [
                "image",
                "tags",
                "variables",
                "before_script",
                "script",
                "after_script",
            ]

            _copy_attributes(signing_job_attrs_to_copy, signing_job_config, signing_job)

            signing_job_tags = []
            if "tags" in signing_job:
                signing_job_tags = _remove_reserved_tags(signing_job["tags"])

            for tag in ["aws", "protected", "notary"]:
                if tag not in signing_job_tags:
                    signing_job_tags.append(tag)
            signing_job["tags"] = signing_job_tags

            signing_job["stage"] = "stage-sign-pkgs"
            signing_job["when"] = "always"
            signing_job["retry"] = {"max": 2, "when": ["always"]}
            signing_job["interruptible"] = True

            output_object["sign-pkgs"] = signing_job

        if rebuild_index_enabled:
            # Add a final job to regenerate the index
            stage_names.append("stage-rebuild-index")
            final_job = {}

            if service_job_config:
                _copy_attributes(default_attrs, service_job_config, final_job)

            if "tags" in final_job:
                service_tags = _remove_reserved_tags(final_job["tags"])
                final_job["tags"] = service_tags

            index_target_mirror = mirror_urls[0]
            if remote_mirror_override:
                index_target_mirror = remote_mirror_override

            final_job["stage"] = "stage-rebuild-index"
            final_job["script"] = [
                "spack buildcache update-index --keys --mirror-url {0}".format(index_target_mirror)
            ]
            final_job["when"] = "always"
            final_job["retry"] = service_job_retries
            final_job["interruptible"] = True

            output_object["rebuild-index"] = final_job

        output_object["stages"] = stage_names

        # Capture the version of spack used to generate the pipeline, transform it
        # into a value that can be passed to "git checkout", and save it in a
        # global yaml variable
        spack_version = spack.main.get_version()
        version_to_clone = None
        v_match = re.match(r"^\d+\.\d+\.\d+$", spack_version)
        if v_match:
            version_to_clone = "v{0}".format(v_match.group(0))
        else:
            v_match = re.match(r"^[^-]+-[^-]+-([a-f\d]+)$", spack_version)
            if v_match:
                version_to_clone = v_match.group(1)
            else:
                version_to_clone = spack_version

        output_object["variables"] = {
            "SPACK_ARTIFACTS_ROOT": rel_artifacts_root,
            "SPACK_CONCRETE_ENV_DIR": rel_concrete_env_dir,
            "SPACK_VERSION": spack_version,
            "SPACK_CHECKOUT_VERSION": version_to_clone,
            "SPACK_REMOTE_MIRROR_URL": remote_mirror_url,
            "SPACK_JOB_LOG_DIR": rel_job_log_dir,
            "SPACK_JOB_REPRO_DIR": rel_job_repro_dir,
            "SPACK_JOB_TEST_DIR": rel_job_test_dir,
            "SPACK_LOCAL_MIRROR_DIR": rel_local_mirror_dir,
            "SPACK_PIPELINE_TYPE": str(spack_pipeline_type),
            "SPACK_CI_STACK_NAME": os.environ.get("SPACK_CI_STACK_NAME", "None"),
            "SPACK_CI_SHARED_PR_MIRROR_URL": shared_pr_mirror or "None",
            "SPACK_REBUILD_CHECK_UP_TO_DATE": str(prune_dag),
            "SPACK_REBUILD_EVERYTHING": str(rebuild_everything),
        }

        if remote_mirror_override:
            (output_object["variables"]["SPACK_REMOTE_MIRROR_OVERRIDE"]) = remote_mirror_override

        spack_stack_name = os.environ.get("SPACK_CI_STACK_NAME", None)
        if spack_stack_name:
            output_object["variables"]["SPACK_CI_STACK_NAME"] = spack_stack_name

        if spack_buildcache_copy:
            # Write out the file describing specs that should be copied
            copy_specs_dir = os.path.join(pipeline_artifacts_dir, "specs_to_copy")

            if not os.path.exists(copy_specs_dir):
                os.makedirs(copy_specs_dir)

            copy_specs_file = os.path.join(
                copy_specs_dir,
                "copy_{}_specs.json".format(spack_stack_name if spack_stack_name else "rebuilt"),
            )

            with open(copy_specs_file, "w") as fd:
                fd.write(json.dumps(buildcache_copies))

        sorted_output = {}
        for output_key, output_value in sorted(output_object.items()):
            sorted_output[output_key] = output_value

        # TODO(opadron): remove this or refactor
        if run_optimizer:
            import spack.ci_optimization as ci_opt

            sorted_output = ci_opt.optimizer(sorted_output)

        # TODO(opadron): remove this or refactor
        if use_dependencies:
            import spack.ci_needs_workaround as cinw

            sorted_output = cinw.needs_to_dependencies(sorted_output)
    else:
        # No jobs were generated
        tty.debug("No specs to rebuild, generating no-op job")
        noop_job = {}

        if service_job_config:
            _copy_attributes(default_attrs, service_job_config, noop_job)

        if "script" not in noop_job:
            noop_job["script"] = ['echo "All specs already up to date, nothing to rebuild."']

        noop_job["retry"] = service_job_retries

        sorted_output = {"no-specs-to-rebuild": noop_job}

    if known_broken_specs_encountered:
        tty.error("This pipeline generated hashes known to be broken on develop:")
        display_broken_spec_messages(broken_specs_url, known_broken_specs_encountered)

        if not rebuild_everything:
            sys.exit(1)

    with open(output_file, "w") as outf:
        outf.write(syaml.dump_config(sorted_output, default_flow_style=True))


def _url_encode_string(input_string):
    encoded_keyval = urlencode({"donotcare": input_string})
    eq_idx = encoded_keyval.find("=") + 1
    encoded_value = encoded_keyval[eq_idx:]
    return encoded_value


def import_signing_key(base64_signing_key):
    """Given Base64-encoded gpg key, decode and import it to use for
        signing packages.

    Arguments:
        base64_signing_key (str): A gpg key including the secret key,
            armor-exported and base64 encoded, so it can be stored in a
            gitlab CI variable.  For an example of how to generate such
            a key, see:

        https://github.com/spack/spack-infrastructure/blob/main/gitlab-docker/files/gen-key
    """
    if not base64_signing_key:
        tty.warn("No key found for signing/verifying packages")
        return

    tty.debug("ci.import_signing_key() will attempt to import a key")

    # This command has the side-effect of creating the directory referred
    # to as GNUPGHOME in setup_environment()
    list_output = spack_gpg("list", output=str)

    tty.debug("spack gpg list:")
    tty.debug(list_output)

    decoded_key = base64.b64decode(base64_signing_key)
    if isinstance(decoded_key, bytes):
        decoded_key = decoded_key.decode("utf8")

    with TemporaryDirectory() as tmpdir:
        sign_key_path = os.path.join(tmpdir, "signing_key")
        with open(sign_key_path, "w") as fd:
            fd.write(decoded_key)

        key_import_output = spack_gpg("trust", sign_key_path, output=str)
        tty.debug("spack gpg trust {0}".format(sign_key_path))
        tty.debug(key_import_output)

    # Now print the keys we have for verifying and signing
    trusted_keys_output = spack_gpg("list", "--trusted", output=str)
    signing_keys_output = spack_gpg("list", "--signing", output=str)

    tty.debug("spack gpg list --trusted")
    tty.debug(trusted_keys_output)
    tty.debug("spack gpg list --signing")
    tty.debug(signing_keys_output)


def can_sign_binaries():
    """Utility method to determine if this spack instance is capable of
    signing binary packages.  This is currently only possible if the
    spack gpg keystore contains exactly one secret key."""
    return len(gpg_util.signing_keys()) == 1


def can_verify_binaries():
    """Utility method to determin if this spack instance is capable (at
    least in theory) of verifying signed binaries."""
    return len(gpg_util.public_keys()) >= 1


def configure_compilers(compiler_action, scope=None):
    """Depending on the compiler_action parameter, either turn on the
        install_missing_compilers config option, or find spack compilers,
        or do nothing.  This is used from rebuild jobs in bootstrapping
        pipelines, where in the bootsrapping phase we would pass
        FIND_ANY in case of compiler-agnostic bootstrapping, while in the
        spec building phase we would pass INSTALL_MISSING in order to get
        spack to use the compiler which was built in the previous phase and
        is now sitting in the binary mirror.

    Arguments:
        compiler_action (str): 'FIND_ANY', 'INSTALL_MISSING' have meanings
            described above.  Any other value essentially results in a no-op.
        scope (spack.config.ConfigScope): Optional.  The scope in which to look for
            compilers, in case 'FIND_ANY' was provided.
    """
    if compiler_action == "INSTALL_MISSING":
        tty.debug("Make sure bootstrapped compiler will be installed")
        config = cfg.get("config")
        config["install_missing_compilers"] = True
        cfg.set("config", config)
    elif compiler_action == "FIND_ANY":
        tty.debug("Just find any available compiler")
        find_args = ["find"]
        if scope:
            find_args.extend(["--scope", scope])
        output = spack_compiler(*find_args)
        tty.debug("spack compiler find")
        tty.debug(output)
        output = spack_compiler("list")
        tty.debug("spack compiler list")
        tty.debug(output)
    else:
        tty.debug("No compiler action to be taken")

    return None


def _push_mirror_contents(env, specfile_path, sign_binaries, mirror_url):
    """Unchecked version of the public API, for easier mocking"""
    unsigned = not sign_binaries
    tty.debug("Creating buildcache ({0})".format("unsigned" if unsigned else "signed"))
    hashes = env.all_hashes() if env else None
    matches = spack.store.specfile_matches(specfile_path, hashes=hashes)
    push_url = spack.mirror.Mirror.from_url(mirror_url).push_url
    kwargs = {"force": True, "allow_root": True, "unsigned": unsigned}
    bindist.push(matches, push_url, include_root=True, include_dependencies=False, **kwargs)


def push_mirror_contents(env, specfile_path, mirror_url, sign_binaries):
    """Push one or more binary packages to the mirror.

    Arguments:

        env (spack.environment.Environment): Optional environment.  If
            provided, it is used to make sure binary package to push
            exists in the environment.
        specfile_path (str): Path to spec.json corresponding to built pkg
            to push.
        mirror_url (str): Base url of target mirror
        sign_binaries (bool): If True, spack will attempt to sign binary
            package before pushing.
    """
    try:
        _push_mirror_contents(env, specfile_path, sign_binaries, mirror_url)
    except Exception as inst:
        # If the mirror we're pushing to is on S3 and there's some
        # permissions problem, for example, we can't just target
        # that exception type here, since users of the
        # `spack ci rebuild' may not need or want any dependency
        # on boto3.  So we use the first non-boto exception type
        # in the heirarchy:
        #     boto3.exceptions.S3UploadFailedError
        #     boto3.exceptions.Boto3Error
        #     Exception
        #     BaseException
        #     object
        err_msg = "Error msg: {0}".format(inst)
        if any(x in err_msg for x in ["Access Denied", "InvalidAccessKeyId"]):
            tty.msg("Permission problem writing to {0}".format(mirror_url))
            tty.msg(err_msg)
        else:
            raise inst


def remove_other_mirrors(mirrors_to_keep, scope=None):
    """Remove all mirrors from the given config scope, the exceptions being
    any listed in in mirrors_to_keep, which is a list of mirror urls.
    """
    mirrors_to_remove = []
    for name, mirror_url in spack.config.get("mirrors", scope=scope).items():
        if mirror_url not in mirrors_to_keep:
            mirrors_to_remove.append(name)

    for mirror_name in mirrors_to_remove:
        spack.mirror.remove(mirror_name, scope)


def copy_files_to_artifacts(src, artifacts_dir):
    """
    Copy file(s) to the given artifacts directory

    Parameters:
        src (str): the glob-friendly path expression for the file(s) to copy
        artifacts_dir (str): the destination directory
    """
    try:
        fs.copy(src, artifacts_dir)
    except Exception as err:
        tty.warn(f"Unable to copy files ({src}) to artifacts {artifacts_dir} due to: {err}")


def copy_stage_logs_to_artifacts(job_spec, job_log_dir):
    """Copy selected build stage file(s) to the given artifacts directory

    Looks for spack-build-out.txt in the stage directory of the given
    job_spec, and attempts to copy the file into the directory given
    by job_log_dir.

    Parameters:
        job_spec (spack.spec.Spec): spec associated with spack install log
        job_log_dir (str): path into which build log should be copied
    """
    tty.debug("job spec: {0}".format(job_spec))
    if not job_spec:
        msg = "Cannot copy stage logs: job spec ({0}) is required"
        tty.error(msg.format(job_spec))
        return

    try:
        pkg_cls = spack.repo.path.get_pkg_class(job_spec.name)
        job_pkg = pkg_cls(job_spec)
        tty.debug("job package: {0}".format(job_pkg))
    except AssertionError:
        msg = "Cannot copy stage logs: job spec ({0}) must be concrete"
        tty.error(msg.format(job_spec))
        return

    stage_dir = job_pkg.stage.path
    tty.debug("stage dir: {0}".format(stage_dir))
    build_out_src = os.path.join(stage_dir, "spack-build-out.txt")
    copy_files_to_artifacts(build_out_src, job_log_dir)


def copy_test_logs_to_artifacts(test_stage, job_test_dir):
    """
    Copy test log file(s) to the given artifacts directory

    Parameters:
        test_stage (str): test stage path
        job_test_dir (str): the destination artifacts test directory
    """
    tty.debug("test stage: {0}".format(test_stage))
    if not os.path.exists(test_stage):
        msg = "Cannot copy test logs: job test stage ({0}) does not exist"
        tty.error(msg.format(test_stage))
        return

    copy_files_to_artifacts(os.path.join(test_stage, "*", "*.txt"), job_test_dir)


def download_and_extract_artifacts(url, work_dir):
    """Look for gitlab artifacts.zip at the given url, and attempt to download
        and extract the contents into the given work_dir

    Arguments:

        url (str): Complete url to artifacts.zip file
        work_dir (str): Path to destination where artifacts should be extracted
    """
    tty.msg("Fetching artifacts from: {0}\n".format(url))

    headers = {"Content-Type": "application/zip"}

    token = os.environ.get("GITLAB_PRIVATE_TOKEN", None)
    if token:
        headers["PRIVATE-TOKEN"] = token

    opener = build_opener(HTTPHandler)

    request = Request(url, headers=headers)
    request.get_method = lambda: "GET"

    response = opener.open(request)
    response_code = response.getcode()

    if response_code != 200:
        msg = "Error response code ({0}) in reproduce_ci_job".format(response_code)
        raise SpackError(msg)

    artifacts_zip_path = os.path.join(work_dir, "artifacts.zip")

    if not os.path.exists(work_dir):
        os.makedirs(work_dir)

    with open(artifacts_zip_path, "wb") as out_file:
        shutil.copyfileobj(response, out_file)

    zip_file = zipfile.ZipFile(artifacts_zip_path)
    zip_file.extractall(work_dir)
    zip_file.close()

    os.remove(artifacts_zip_path)


def get_spack_info():
    """If spack is running from a git repo, return the most recent git log
    entry, otherwise, return a string containing the spack version."""
    git_path = os.path.join(spack.paths.prefix, ".git")
    if os.path.exists(git_path):
        git = spack.util.git.git()
        if git:
            with fs.working_dir(spack.paths.prefix):
                git_log = git("log", "-1", output=str, error=os.devnull, fail_on_error=False)

            return git_log

    return "no git repo, use spack {0}".format(spack.spack_version)


def setup_spack_repro_version(repro_dir, checkout_commit, merge_commit=None):
    """Look in the local spack clone to find the checkout_commit, and if
        provided, the merge_commit given as arguments.  If those commits can
        be found locally, then clone spack and attempt to recreate a merge
        commit with the same parent commits as tested in gitlab.  This looks
        something like 1) git clone repo && cd repo 2) git checkout
        <checkout_commit> 3) git merge <merge_commit>.  If there is no
        merge_commit provided, then skip step (3).

    Arguments:

        repro_dir (str): Location where spack should be cloned
        checkout_commit (str): SHA of PR branch commit
        merge_commit (str): SHA of target branch parent

    Returns: True if git repo state was successfully recreated, or False
        otherwise.
    """
    # figure out the path to the spack git version being used for the
    # reproduction
    print("checkout_commit: {0}".format(checkout_commit))
    print("merge_commit: {0}".format(merge_commit))

    dot_git_path = os.path.join(spack.paths.prefix, ".git")
    if not os.path.exists(dot_git_path):
        tty.error("Unable to find the path to your local spack clone")
        return False

    spack_git_path = spack.paths.prefix

    git = spack.util.git.git()
    if not git:
        tty.error("reproduction of pipeline job requires git")
        return False

    # Check if we can find the tested commits in your local spack repo
    with fs.working_dir(spack_git_path):
        git("log", "-1", checkout_commit, output=str, error=os.devnull, fail_on_error=False)

        if git.returncode != 0:
            tty.error("Missing commit: {0}".format(checkout_commit))
            return False

        if merge_commit:
            git("log", "-1", merge_commit, output=str, error=os.devnull, fail_on_error=False)

            if git.returncode != 0:
                tty.error("Missing commit: {0}".format(merge_commit))
                return False

    # Next attempt to clone your local spack repo into the repro dir
    with fs.working_dir(repro_dir):
        clone_out = git(
            "clone", spack_git_path, "spack", output=str, error=os.devnull, fail_on_error=False
        )

        if git.returncode != 0:
            tty.error("Unable to clone your local spack repo:")
            tty.msg(clone_out)
            return False

    # Finally, attempt to put the cloned repo into the same state used during
    # the pipeline build job
    repro_spack_path = os.path.join(repro_dir, "spack")
    with fs.working_dir(repro_spack_path):
        co_out = git(
            "checkout", checkout_commit, output=str, error=os.devnull, fail_on_error=False
        )

        if git.returncode != 0:
            tty.error("Unable to checkout {0}".format(checkout_commit))
            tty.msg(co_out)
            return False

        if merge_commit:
            merge_out = git(
                "-c",
                "user.name=cirepro",
                "-c",
                "user.email=user@email.org",
                "merge",
                "--no-edit",
                merge_commit,
                output=str,
                error=os.devnull,
                fail_on_error=False,
            )

            if git.returncode != 0:
                tty.error("Unable to merge {0}".format(merge_commit))
                tty.msg(merge_out)
                return False

    return True


def reproduce_ci_job(url, work_dir):
    """Given a url to gitlab artifacts.zip from a failed 'spack ci rebuild' job,
    attempt to setup an environment in which the failure can be reproduced
    locally.  This entails the following:

    First download and extract artifacts.  Then look through those artifacts
    to glean some information needed for the reproduer (e.g. one of the
    artifacts contains information about the version of spack tested by
    gitlab, another is the generated pipeline yaml containing details
    of the job like the docker image used to run it).  The output of this
    function is a set of printed instructions for running docker and then
    commands to run to reproduce the build once inside the container.
    """
    download_and_extract_artifacts(url, work_dir)

    lock_file = fs.find(work_dir, "spack.lock")[0]
    repro_lock_dir = os.path.dirname(lock_file)

    tty.debug("Found lock file in: {0}".format(repro_lock_dir))

    yaml_files = fs.find(work_dir, ["*.yaml", "*.yml"])

    tty.debug("yaml files:")
    for yaml_file in yaml_files:
        tty.debug("  {0}".format(yaml_file))

    pipeline_yaml = None

    # Try to find the dynamically generated pipeline yaml file in the
    # reproducer.  If the user did not put it in the artifacts root,
    # but rather somewhere else and exported it as an artifact from
    # that location, we won't be able to find it.
    for yf in yaml_files:
        with open(yf) as y_fd:
            yaml_obj = syaml.load(y_fd)
            if "variables" in yaml_obj and "stages" in yaml_obj:
                pipeline_yaml = yaml_obj

    if pipeline_yaml:
        tty.debug("\n{0} is likely your pipeline file".format(yf))

    relative_concrete_env_dir = pipeline_yaml["variables"]["SPACK_CONCRETE_ENV_DIR"]
    tty.debug("Relative environment path used by cloud job: {0}".format(relative_concrete_env_dir))

    # Using the relative concrete environment path found in the generated
    # pipeline variable above, copy the spack environment files so they'll
    # be found in the same location as when the job ran in the cloud.
    concrete_env_dir = os.path.join(work_dir, relative_concrete_env_dir)
    os.makedirs(concrete_env_dir, exist_ok=True)
    copy_lock_path = os.path.join(concrete_env_dir, "spack.lock")
    orig_yaml_path = os.path.join(repro_lock_dir, "spack.yaml")
    copy_yaml_path = os.path.join(concrete_env_dir, "spack.yaml")
    shutil.copyfile(lock_file, copy_lock_path)
    shutil.copyfile(orig_yaml_path, copy_yaml_path)

    # Find the install script in the unzipped artifacts and make it executable
    install_script = fs.find(work_dir, "install.sh")[0]
    st = os.stat(install_script)
    os.chmod(install_script, st.st_mode | stat.S_IEXEC)

    # Find the repro details file.  This just includes some values we wrote
    # during `spack ci rebuild` to make reproduction easier.  E.g. the job
    # name is written here so we can easily find the configuration of the
    # job from the generated pipeline file.
    repro_file = fs.find(work_dir, "repro.json")[0]
    repro_details = None
    with open(repro_file) as fd:
        repro_details = json.load(fd)

    repro_dir = os.path.dirname(repro_file)
    rel_repro_dir = repro_dir.replace(work_dir, "").lstrip(os.path.sep)

    # Find the spack info text file that should contain the git log
    # of the HEAD commit used during the CI build
    spack_info_file = fs.find(work_dir, "spack_info.txt")[0]
    with open(spack_info_file) as fd:
        spack_info = fd.read()

    # Access the specific job configuration
    job_name = repro_details["job_name"]
    job_yaml = None

    if job_name in pipeline_yaml:
        job_yaml = pipeline_yaml[job_name]

    if job_yaml:
        tty.debug("Found job:")
        tty.debug(job_yaml)

    job_image = None
    setup_result = False
    if "image" in job_yaml:
        job_image_elt = job_yaml["image"]
        if "name" in job_image_elt:
            job_image = job_image_elt["name"]
        else:
            job_image = job_image_elt
        tty.msg("Job ran with the following image: {0}".format(job_image))

        # Because we found this job was run with a docker image, so we will try
        # to print a "docker run" command that bind-mounts the directory where
        # we extracted the artifacts.

        # Destination of bind-mounted reproduction directory.  It makes for a
        # more faithful reproducer if everything appears to run in the same
        # absolute path used during the CI build.
        mount_as_dir = "/work"
        if repro_details:
            mount_as_dir = repro_details["ci_project_dir"]
            mounted_repro_dir = os.path.join(mount_as_dir, rel_repro_dir)
            mounted_env_dir = os.path.join(mount_as_dir, relative_concrete_env_dir)

        # We will also try to clone spack from your local checkout and
        # reproduce the state present during the CI build, and put that into
        # the bind-mounted reproducer directory.

        # Regular expressions for parsing that HEAD commit.  If the pipeline
        # was on the gitlab spack mirror, it will have been a merge commit made by
        # gitub and pushed by the sync script.  If the pipeline was run on some
        # environment repo, then the tested spack commit will likely have been
        # a regular commit.
        commit_1 = None
        commit_2 = None
        commit_regex = re.compile(r"commit\s+([^\s]+)")
        merge_commit_regex = re.compile(r"Merge\s+([^\s]+)\s+into\s+([^\s]+)")

        # Try the more specific merge commit regex first
        m = merge_commit_regex.search(spack_info)
        if m:
            # This was a merge commit and we captured the parents
            commit_1 = m.group(1)
            commit_2 = m.group(2)
        else:
            # Not a merge commit, just get the commit sha
            m = commit_regex.search(spack_info)
            if m:
                commit_1 = m.group(1)

        setup_result = False
        if commit_1:
            if commit_2:
                setup_result = setup_spack_repro_version(work_dir, commit_2, merge_commit=commit_1)
            else:
                setup_result = setup_spack_repro_version(work_dir, commit_1)

        if not setup_result:
            setup_msg = """
        This can happen if the spack you are using to run this command is not a git
        repo, or if it is a git repo, but it does not have the commits needed to
        recreate the tested merge commit.  If you are trying to reproduce a spack
        PR pipeline job failure, try fetching the latest develop commits from
        mainline spack and make sure you have the most recent commit of the PR
        branch in your local spack repo.  Then run this command again.
        Alternatively, you can also manually clone spack if you know the version
        you want to test.
            """
            tty.error(
                "Failed to automatically setup the tested version of spack "
                "in your local reproduction directory."
            )
            print(setup_msg)

    # In cases where CI build was run on a shell runner, it might be useful
    # to see what tags were applied to the job so the user knows what shell
    # runner was used.  But in that case in general, we cannot do nearly as
    # much to set up the reproducer.
    job_tags = None
    if "tags" in job_yaml:
        job_tags = job_yaml["tags"]
        tty.msg("Job ran with the following tags: {0}".format(job_tags))

    inst_list = []

    # Finally, print out some instructions to reproduce the build
    if job_image:
        inst_list.append("\nRun the following command:\n\n")
        inst_list.append(
            "    $ docker run --rm -v {0}:{1} -ti {2}\n".format(work_dir, mount_as_dir, job_image)
        )
        inst_list.append("\nOnce inside the container:\n\n")
    else:
        inst_list.append("\nOnce on the tagged runner:\n\n")

    if not setup_result:
        inst_list.append("    - Clone spack and acquire tested commit\n")
        inst_list.append("{0}".format(spack_info))
        spack_root = "<spack-clone-path>"
    else:
        spack_root = "{0}/spack".format(mount_as_dir)

    inst_list.append("    - Activate the environment\n\n")
    inst_list.append("        $ source {0}/share/spack/setup-env.sh\n".format(spack_root))
    inst_list.append(
        "        $ spack env activate --without-view {0}\n\n".format(
            mounted_env_dir if job_image else repro_dir
        )
    )
    inst_list.append("    - Run the install script\n\n")
    inst_list.append(
        "        $ {0}\n".format(
            os.path.join(mounted_repro_dir, "install.sh") if job_image else install_script
        )
    )

    print("".join(inst_list))


def process_command(name, commands, repro_dir):
    """
    Create a script for and run the command. Copy the script to the
    reproducibility directory.

    Arguments:
        name (str): name of the command being processed
        commands (list): list of arguments for single command or list of lists of
            arguments for multiple commands. No shell escape is performed.
        repro_dir (str): Job reproducibility directory

    Returns: the exit code from processing the command
    """
    tty.debug("spack {0} arguments: {1}".format(name, commands))

    if len(commands) == 0 or isinstance(commands[0], str):
        commands = [commands]

    # Create a string [command 1] && [command 2] && ... && [command n] with commands
    # quoted using double quotes.
    args_to_string = lambda args: " ".join('"{}"'.format(arg) for arg in args)
    full_command = " && ".join(map(args_to_string, commands))

    # Write the command to a shell script
    script = "{0}.sh".format(name)
    with open(script, "w") as fd:
        fd.write("#!/bin/sh\n\n")
        fd.write("\n# spack {0} command\n".format(name))
        fd.write(full_command)
        fd.write("\n")

    st = os.stat(script)
    os.chmod(script, st.st_mode | stat.S_IEXEC)

    copy_path = os.path.join(repro_dir, script)
    shutil.copyfile(script, copy_path)

    # Run the generated install.sh shell script as if it were being run in
    # a login shell.
    try:
        cmd_process = subprocess.Popen(["/bin/sh", "./{0}".format(script)])
        cmd_process.wait()
        exit_code = cmd_process.returncode
    except (ValueError, subprocess.CalledProcessError, OSError) as err:
        tty.error("Encountered error running {0} script".format(name))
        tty.error(err)
        exit_code = 1

    tty.debug("spack {0} exited {1}".format(name, exit_code))
    return exit_code


def create_buildcache(**kwargs):
    """Create the buildcache at the provided mirror(s).

    Arguments:
       kwargs (dict): dictionary of arguments used to create the buildcache

    List of recognized keys:

    * "env" (spack.environment.Environment): the active environment
    * "buildcache_mirror_url" (str or None): URL for the buildcache mirror
    * "pipeline_mirror_url" (str or None): URL for the pipeline mirror
    * "pr_pipeline" (bool): True if the CI job is for a PR
    * "json_path" (str): path the the spec's JSON file
    """
    env = kwargs.get("env")
    buildcache_mirror_url = kwargs.get("buildcache_mirror_url")
    pipeline_mirror_url = kwargs.get("pipeline_mirror_url")
    pr_pipeline = kwargs.get("pr_pipeline")
    json_path = kwargs.get("json_path")

    sign_binaries = pr_pipeline is False and can_sign_binaries()

    # Create buildcache in either the main remote mirror, or in the
    # per-PR mirror, if this is a PR pipeline
    if buildcache_mirror_url:
        push_mirror_contents(env, json_path, buildcache_mirror_url, sign_binaries)

    # Create another copy of that buildcache in the per-pipeline
    # temporary storage mirror (this is only done if either
    # artifacts buildcache is enabled or a temporary storage url
    # prefix is set)
    if pipeline_mirror_url:
        push_mirror_contents(env, json_path, pipeline_mirror_url, sign_binaries)


def write_broken_spec(url, pkg_name, stack_name, job_url, pipeline_url, spec_dict):
    """Given a url to write to and the details of the failed job, write an entry
    in the broken specs list.
    """
    tmpdir = tempfile.mkdtemp()
    file_path = os.path.join(tmpdir, "broken.txt")

    broken_spec_details = {
        "broken-spec": {
            "job-name": pkg_name,
            "job-stack": stack_name,
            "job-url": job_url,
            "pipeline-url": pipeline_url,
            "concrete-spec-dict": spec_dict,
        }
    }

    try:
        with open(file_path, "w") as fd:
            fd.write(syaml.dump(broken_spec_details))
        web_util.push_to_url(
            file_path, url, keep_original=False, extra_args={"ContentType": "text/plain"}
        )
    except Exception as err:
        # If there is an S3 error (e.g., access denied or connection
        # error), the first non boto-specific class in the exception
        # hierarchy is Exception.  Just print a warning and return
        msg = "Error writing to broken specs list {0}: {1}".format(url, err)
        tty.warn(msg)
    finally:
        shutil.rmtree(tmpdir)


def read_broken_spec(broken_spec_url):
    """Read data from broken specs file located at the url, return as a yaml
    object.
    """
    try:
        _, _, fs = web_util.read_from_url(broken_spec_url)
    except (URLError, web_util.SpackWebError, HTTPError):
        tty.warn("Unable to read broken spec from {0}".format(broken_spec_url))
        return None

    broken_spec_contents = codecs.getreader("utf-8")(fs).read()
    return syaml.load(broken_spec_contents)


def display_broken_spec_messages(base_url, hashes):
    """Fetch the broken spec file for each of the hashes under the base_url and
    print a message with some details about each one.
    """
    broken_specs = [(h, read_broken_spec(url_util.join(base_url, h))) for h in hashes]
    for spec_hash, broken_spec in [tup for tup in broken_specs if tup[1]]:
        details = broken_spec["broken-spec"]
        if "job-name" in details:
            item_name = "{0}/{1}".format(details["job-name"], spec_hash[:7])
        else:
            item_name = spec_hash

        if "job-stack" in details:
            item_name = "{0} (in stack {1})".format(item_name, details["job-stack"])

        msg = "  {0} was reported broken here: {1}".format(item_name, details["job-url"])
        tty.msg(msg)


def run_standalone_tests(**kwargs):
    """Run stand-alone tests on the current spec.

    Arguments:
       kwargs (dict): dictionary of arguments used to run the tests

    List of recognized keys:

    * "cdash" (CDashHandler): (optional) cdash handler instance
    * "fail_fast" (bool): (optional) terminate tests after the first failure
    * "log_file" (str): (optional) test log file name if NOT CDash reporting
    * "job_spec" (Spec): spec that was built
    * "repro_dir" (str): reproduction directory
    """
    cdash = kwargs.get("cdash")
    fail_fast = kwargs.get("fail_fast")
    log_file = kwargs.get("log_file")

    if cdash and log_file:
        tty.msg("The test log file {0} option is ignored with CDash reporting".format(log_file))
        log_file = None

    # Error out but do NOT terminate if there are missing required arguments.
    job_spec = kwargs.get("job_spec")
    if not job_spec:
        tty.error("Job spec is required to run stand-alone tests")
        return

    repro_dir = kwargs.get("repro_dir")
    if not repro_dir:
        tty.error("Reproduction directory is required for stand-alone tests")
        return

    test_args = ["spack", "--color=always", "--backtrace", "--verbose", "test", "run"]
    if fail_fast:
        test_args.append("--fail-fast")

    if cdash:
        test_args.extend(cdash.args())
    else:
        test_args.extend(["--log-format", "junit"])
        if log_file:
            test_args.extend(["--log-file", log_file])
    test_args.append(job_spec.name)

    tty.debug("Running {0} stand-alone tests".format(job_spec.name))
    exit_code = process_command("test", test_args, repro_dir)

    tty.debug("spack test exited {0}".format(exit_code))


class CDashHandler(object):
    """
    Class for managing CDash data and processing.
    """

    def __init__(self, ci_cdash):
        # start with the gitlab ci configuration
        self.url = ci_cdash.get("url")
        self.build_group = ci_cdash.get("build-group")
        self.project = ci_cdash.get("project")
        self.site = ci_cdash.get("site")

        # grab the authorization token when available
        self.auth_token = os.environ.get("SPACK_CDASH_AUTH_TOKEN")
        if self.auth_token:
            tty.verbose("Using CDash auth token from environment")

        # append runner description to the site if available
        runner = os.environ.get("CI_RUNNER_DESCRIPTION")
        if runner:
            self.site += " ({0})".format(runner)

        # track current spec, if any
        self.current_spec = None

    def args(self):
        return [
            "--cdash-upload-url",
            self.upload_url,
            "--cdash-build",
            self.build_name,
            "--cdash-site",
            self.site,
            "--cdash-buildstamp",
            self.build_stamp,
        ]

    @property  # type: ignore
    def build_name(self):
        """Returns the CDash build name.

        A name will be generated if the `current_spec` property is set;
        otherwise, the value will be retrieved from the environment
        through the `SPACK_CDASH_BUILD_NAME` variable.

        Returns: (str) current spec's CDash build name."""
        spec = self.current_spec
        if spec:
            build_name = "{0}@{1}%{2} hash={3} arch={4} ({5})".format(
                spec.name,
                spec.version,
                spec.compiler,
                spec.dag_hash(),
                spec.architecture,
                self.build_group,
            )
            tty.verbose(
                "Generated CDash build name ({0}) from the {1}".format(build_name, spec.name)
            )
            return build_name

        build_name = os.environ.get("SPACK_CDASH_BUILD_NAME")
        tty.verbose("Using CDash build name ({0}) from the environment".format(build_name))
        return build_name

    @property  # type: ignore
    def build_stamp(self):
        """Returns the CDash build stamp.

        The one defined by SPACK_CDASH_BUILD_STAMP environment variable
        is preferred due to the representation of timestamps; otherwise,
        one will be built.

        Returns: (str) current CDash build stamp"""
        build_stamp = os.environ.get("SPACK_CDASH_BUILD_STAMP")
        if build_stamp:
            tty.verbose("Using build stamp ({0}) from the environment".format(build_stamp))
            return build_stamp

        build_stamp = cdash_build_stamp(self.build_group, time.time())
        tty.verbose("Generated new build stamp ({0})".format(build_stamp))
        return build_stamp

    @property  # type: ignore
    @memoized
    def project_enc(self):
        tty.debug("Encoding project ({0}): {1})".format(type(self.project), self.project))
        encode = urlencode({"project": self.project})
        index = encode.find("=") + 1
        return encode[index:]

    @property
    def upload_url(self):
        url_format = "{0}/submit.php?project={1}"
        return url_format.format(self.url, self.project_enc)

    def copy_test_results(self, source, dest):
        """Copy test results to artifacts directory."""
        reports = fs.join_path(source, "*_Test*.xml")
        copy_files_to_artifacts(reports, dest)

    def create_buildgroup(self, opener, headers, url, group_name, group_type):
        data = {"newbuildgroup": group_name, "project": self.project, "type": group_type}

        enc_data = json.dumps(data).encode("utf-8")

        request = Request(url, data=enc_data, headers=headers)

        response = opener.open(request)
        response_code = response.getcode()

        if response_code not in [200, 201]:
            msg = "Creating buildgroup failed (response code = {0})".format(response_code)
            tty.warn(msg)
            return None

        response_text = response.read()
        response_json = json.loads(response_text)
        build_group_id = response_json["id"]

        return build_group_id

    def populate_buildgroup(self, job_names):
        url = "{0}/api/v1/buildgroup.php".format(self.url)

        headers = {
            "Authorization": "Bearer {0}".format(self.auth_token),
            "Content-Type": "application/json",
        }

        opener = build_opener(HTTPHandler)

        parent_group_id = self.create_buildgroup(opener, headers, url, self.build_group, "Daily")
        group_id = self.create_buildgroup(
            opener, headers, url, "Latest {0}".format(self.build_group), "Latest"
        )

        if not parent_group_id or not group_id:
            msg = "Failed to create or retrieve buildgroups for {0}".format(self.build_group)
            tty.warn(msg)
            return

        data = {
            "dynamiclist": [
                {"match": name, "parentgroupid": parent_group_id, "site": self.site}
                for name in job_names
            ]
        }

        enc_data = json.dumps(data).encode("utf-8")

        request = Request(url, data=enc_data, headers=headers)
        request.get_method = lambda: "PUT"

        response = opener.open(request)
        response_code = response.getcode()

        if response_code != 200:
            msg = "Error response code ({0}) in populate_buildgroup".format(response_code)
            tty.warn(msg)

    def report_skipped(self, spec, directory_name, reason):
        configuration = CDashConfiguration(
            upload_url=self.upload_url,
            packages=[spec.name],
            build=self.build_name,
            site=self.site,
            buildstamp=self.build_stamp,
            track=None,
        )
        reporter = CDash(configuration=configuration)
        reporter.test_skipped_report(directory_name, spec, reason)
