# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
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
from collections import namedtuple
from enum import Enum
from typing import List, Optional
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import HTTPHandler, Request, build_opener

import llnl.util.filesystem as fs
import llnl.util.tty as tty
from llnl.util.lang import memoized

import spack
import spack.binary_distribution as bindist
import spack.config as cfg
import spack.environment as ev
import spack.main
import spack.mirror
import spack.paths
import spack.repo
import spack.spec
import spack.util.git
import spack.util.gpg as gpg_util
import spack.util.spack_yaml as syaml
import spack.util.url as url_util
import spack.util.web as web_util
from spack import traverse
from spack.error import SpackError
from spack.reporters import CDash, CDashConfiguration
from spack.reporters.cdash import build_stamp as cdash_build_stamp

from .formatters import get_formatter, UnknownFormatterException

__all__ = [
    "PipelineDag",
    "PipelineNode",
    "PipelineOptions",
    "PipelineType",
    "SpackCI",
    "SPACK_RESERVED_TAGS",
    "unpack_script",
    "update_env_scopes",
]


TEMP_STORAGE_MIRROR_NAME = "ci_temporary_mirror"
SPACK_RESERVED_TAGS = ["public", "protected", "notary"]
# TODO: Remove this in Spack 0.23
SHARED_PR_MIRROR_URL = "s3://spack-binaries-prs/shared_pr_mirror"

spack_gpg = spack.main.SpackCommand("gpg")
spack_compiler = spack.main.SpackCommand("compiler")

PushResult = namedtuple("PushResult", "success url")


class TemporaryDirectory:
    def __init__(self):
        self.temporary_directory = tempfile.mkdtemp()

    def __enter__(self):
        return self.temporary_directory

    def __exit__(self, exc_type, exc_value, exc_traceback):
        shutil.rmtree(self.temporary_directory)
        return False


class PipelineType(Enum):
    COPY_ONLY = 1
    spack_copy_only = 1
    PROTECTED_BRANCH = 2
    spack_protected_branch = 2
    PULL_REQUEST = 3
    spack_pull_request = 3


class PipelineOptions():
    """A container for all pipeline options that can be specified (whether
    via cli, config/yaml, or environment variables)"""
    def __init__(
            self,
            env: ev.Environment,
            print_summary: bool = True,
            output_file: Optional[str] = None,
            check_index_only: bool = False,
            run_optimizer: bool = False,
            use_dependencies: bool = False,
            broken_specs_url: Optional[str] = None,
            enable_artifacts_buildcache: bool = False,
            rebuild_index: bool = True,
            temporary_storage_url_prefix: Optional[str] = None,
            untouched_pruning_dependent_depth: Optional[int] = None,
            prune_untouched: bool = False,
            prune_up_to_date: bool = True,
            stack_name: Optional[str] = None,
            job_name: Optional[str] = None,
            pipeline_id: Optional[str] = None,
            pipeline_type: Optional[PipelineType] = None,
            require_signing: bool = False,
            artifacts_root: Optional[str] = None,
            remote_mirror: Optional[str] = None,
            shared_pr_mirror: Optional[str] = None,
            remote_mirror_override: Optional[str] = None,  # deprecated, remove in Spack 0.23
            buildcache_destination: Optional[spack.mirror.Mirror] = None,
            cdash_handler: Optional["CDashHandler"] = None,
    ):
        """
        Args:
            env: Active spack environment
            print_summary: Print a summary of the scheduled pipeline
            output_file: Path where output file should be written
            check_index_only: Only fetch the index or fetch all spec files
            run_optimizer: Run best-effort optimizer to reduce yaml size
            use_dependencies: Use "dependencies" instead of "specs" (gitlab only, deprecated)
            broken_specs_url: URL where broken specs (on develop) should be reported
            enable_artifacts_buildcache: Treat artifacts like a buildcache (deprecated)
            rebuild_index: Generate a job to rebuild mirror index after rebuilds
            temporary_storage_url_prefix: URL where binaries can be stored temporarily (deprecated)
            untouched_pruning_dependent_depth: How many parents to traverse from changed pkg specs
            prune_untouched: Prune jobs for specs that were unchanged in git history
            prune_up_to_date: Prune specs from pipeline if binary exists on the mirror
            stack_name: Name of spack stack
            job_name: Name of job running pipeline generation in CI
            pipeline_id: ID of pipeline running generation in CI
            pipeline_type: Type of pipeline running (optional)
            require_signing: Require buildcache to be signed (fail w/out signing key)
            artifacts_root: Path to location where artifacts should be stored
            remote_mirror: Mirror from spack.yaml (deprecated)
            shared_pr_mirror: Shared pr mirror url (deprecated)
            remote_mirror_override: Override the mirror in the spack environment (deprecated)
            buildcache_destination: The mirror where built binaries should be pushed
            cdash_handler: Object for communicating build information with CDash
        """
        self.env = env
        self.print_summary = print_summary
        self.output_file = output_file
        self.check_index_only = check_index_only
        self.run_optimizer = run_optimizer
        self.use_dependencies = use_dependencies
        self.broken_specs_url = broken_specs_url
        self.enable_artifacts_buildcache = enable_artifacts_buildcache
        self.rebuild_index = rebuild_index
        self.temporary_storage_url_prefix = temporary_storage_url_prefix
        self.untouched_pruning_dependent_depth = untouched_pruning_dependent_depth
        self.prune_untouched = prune_untouched
        self.prune_up_to_date = prune_up_to_date
        self.stack_name = stack_name
        self.job_name = job_name
        self.pipeline_id = pipeline_id
        self.pipeline_type = pipeline_type
        self.require_signing = require_signing
        self.artifacts_root = artifacts_root
        self.remote_mirror = remote_mirror
        self.shared_pr_mirror = shared_pr_mirror
        self.remote_mirror_override = remote_mirror_override
        self.buildcache_destination = buildcache_destination
        self.cdash_handler = cdash_handler


class PipelineNode:
    spec: spack.spec.Spec
    parents: List[str]
    children: List[str]

    def __init__(self, spec: spack.spec.Spec):
        self.spec = spec
        self.parents = []
        self.children = []


class PipelineDag:
    """Turn a list of specs into a simple directed graph, that doesn't keep track
    of edge types."""

    @classmethod
    def key(cls, spec: spack.spec.Spec) -> str:
        return f"{spec.name}/{spec.dag_hash(7)}"

    def __init__(self, specs: List[spack.spec.Spec]) -> None:
        # Build dictionary of nodes
        self.nodes: Dict[str, PipelineNode] = {
            PipelineDag.key(s): PipelineNode(s) for s in spack.traverse.traverse_nodes(specs, deptype=all, root=True)
        }

        # Create edges
        for edge in spack.traverse.traverse_edges(specs, deptype=all, root=False, cover="edges"):
            parent_key = PipelineDag.key(edge.parent)
            child_key = PipelineDag.key(edge.spec)

            self.nodes[parent_key].children.append(child_key)
            self.nodes[child_key].parents.append(parent_key)

    def prune(self, node_key: str):
        """Remove a node from the graph, and reconnect its parents and children"""
        node = self.nodes[node_key]
        for parent in node.parents:
            self.nodes[parent].children.remove(node_key)
            self.nodes[parent].children.extend(node.children)
        for child in node.children:
            self.nodes[child].parents.remove(node_key)
            self.nodes[child].parents.extend(node.parents)
        del self.nodes[node_key]

    def traverse(self, top_down: bool=True):
        visited = set()
        level = 0

        if top_down:
            # Yields the roots first, followed by direct children of roots, followed
            # by their children and so on.
            node_list = [
                (key, node) for key, node in self.nodes.items() if len(node.parents) == 0
            ]
            while node_list:
                for key, node in node_list:
                    if key not in visited:
                        visited.add(key)
                        yield (level, (key, node))
                level += 1
                node_list = [(k, self.nodes[k]) for _, n in node_list for k in n.children]
        else:
            # Yields the leaves first, followed by nodes whose only children were
            # leaves, and so on.
            node_list = [
                (key, node) for key, node in self.nodes.items() if len(node.children) == 0
            ]
            while node_list:
                for key, node in node_list:
                    if key not in visited:
                        visited.add(key)
                        yield (level, (key, node))
                level += 1
                node_list = [
                    (k, self.nodes[k]) for _, n in node_list for k in n.parents
                    if not k in visited and all([c in visited for c in self.nodes[k].children])
                ]

    def get_dependencies(self, node: PipelineNode, transitive: bool = False):
        # TODO: handle transitive=True case
        dep_list = [self.nodes[k].spec for k in node.children]

        if not transitive:
            return dep_list

        all_deps = set()

        while dep_list:
            dep = dep_list.pop(0)
            all_deps.add(dep)
            dep_list.extend([n for n in dep.children])

        return [n.spec for n in all_deps]


def _spec_matches(spec, match_string):
    return spec.intersects(match_string)


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
    affected_pkgs = frozenset(affected_pkgs)
    env_matches = [s for s in all_concrete_specs if s.name in affected_pkgs]
    visited = set()
    dag_hash = lambda s: s.dag_hash()
    for depth, parent in traverse.traverse_nodes(
        env_matches, direction="parents", key=dag_hash, depth=True, order="breadth"
    ):
        if dependent_traverse_depth is not None and depth > dependent_traverse_depth:
            break
        affected_specs.update(parent.traverse(direction="children", visited=visited, key=dag_hash))
    return affected_specs


def prune_unaffected_specs(pipeline: PipelineDag, affected_specs: List[spack.spec.Spec]):
    """Prune any unaffected specs from the pipeline"""
    to_prune = set()
    for _, (key, node) in pipeline.traverse(top_down=True):
        if node.spec not in affected_specs:
            to_prune.add(key)

    if to_prune:
        tty.msg("Pruned the following unaffected specs:")
        for key in to_prune:
            tty.msg(f"  {key}")
            pipeline.prune(key)
    else:
        tty.msg("There were no unaffected specs.")


def prune_built_specs(pipeline, mirrors_to_check=None, check_index_only=True):
    """Prune already built specs from the pipeline"""
    # Speed up checking by first fetching binary indices from all mirrors
    try:
        bindist.BINARY_INDEX.update()
    except bindist.FetchCacheError as e:
        tty.warn(e)

    to_prune = set()
    found_on_mirrors = {}
    for _, (key, node) in pipeline.traverse(top_down=True):
        release_spec = node.spec
        up_to_date_mirrors = bindist.get_mirrors_for_spec(
            spec=release_spec, mirrors_to_check=mirrors_to_check, index_only=check_index_only
        )
        if up_to_date_mirrors:
            to_prune.add(key)
            found_on_mirrors[key] = [m["mirror_url"] for m in up_to_date_mirrors]

    if to_prune:
        tty.msg("Pruned the following already built specs:")
        for key in to_prune:
            spec_mirrors = found_on_mirrors[key]
            tty.msg(f"  {key} [{', '.join(spec_mirrors)}]")
            pipeline.prune(key)
    else:
        tty.msg("There were no already built specs.")


def _noop(x):
    return x


def unpack_script(script_section, op=_noop):
    script = []
    for cmd in script_section:
        if isinstance(cmd, list):
            for subcmd in cmd:
                script.append(op(subcmd))
        else:
            script.append(op(cmd))

    return script


class SpackCI:
    """Spack CI object used to generate intermediate representation
    used by the CI generator(s).
    """

    def __init__(self, ci_config, pipeline):
        """Given the information from the ci section of the config
        and the staged jobs, set up meta data needed for generating Spack
        CI IR.
        """

        self.ci_config = ci_config
        self.named_jobs = ["any", "build", "copy", "cleanup", "noop", "reindex", "signing"]

        self.ir = {
            "jobs": {},
            "temporary-storage-url-prefix": self.ci_config.get(
                "temporary-storage-url-prefix", None
            ),
            "enable-artifacts-buildcache": self.ci_config.get(
                "enable-artifacts-buildcache", False
            ),
            "rebuild-index": self.ci_config.get("rebuild-index", True),
            "broken-specs-url": self.ci_config.get("broken-specs-url", None),
            "broken-tests-packages": self.ci_config.get("broken-tests-packages", []),
            "target": self.ci_config.get("target", "gitlab"),
        }
        jobs = self.ir["jobs"]

        for _, (key, node) in pipeline.traverse():
            dag_hash = node.spec.dag_hash()
            jobs[dag_hash] = self.__init_job(node.spec)

        for name in self.named_jobs:
            # Skip the special named jobs
            if name not in ["any", "build"]:
                jobs[name] = self.__init_job("")

    def __init_job(self, spec):
        """Initialize job object"""
        return {"spec": spec, "attributes": {}}

    def __is_named(self, section):
        """Check if a pipeline-gen configuration section is for a named job,
        and if so return the name otherwise return none.
        """
        for _name in self.named_jobs:
            keys = ["{0}-job".format(_name), "{0}-job-remove".format(_name)]
            if any([key for key in keys if key in section]):
                return _name

        return None

    @staticmethod
    def __job_name(name, suffix=""):
        """Compute the name of a named job with appropriate suffix.
        Valid suffixes are either '-remove' or empty string or None
        """
        assert isinstance(name, str)

        jname = name
        if suffix:
            jname = "{0}-job{1}".format(name, suffix)
        else:
            jname = "{0}-job".format(name)

        return jname

    def __apply_submapping(self, dest, spec, section):
        """Apply submapping setion to the IR dict"""
        matched = False
        only_first = section.get("match_behavior", "first") == "first"

        for match_attrs in reversed(section["submapping"]):
            attrs = cfg.InternalConfigScope._process_dict_keyname_overrides(match_attrs)
            for match_string in match_attrs["match"]:
                if _spec_matches(spec, match_string):
                    matched = True
                    if "build-job-remove" in match_attrs:
                        spack.config.remove_yaml(dest, attrs["build-job-remove"])
                    if "build-job" in match_attrs:
                        spack.config.merge_yaml(dest, attrs["build-job"])
                    break
            if matched and only_first:
                break

        return dest

    # Generate IR from the configs
    def generate_ir(self):
        """Generate the IR from the Spack CI configurations."""

        jobs = self.ir["jobs"]

        # Implicit job defaults
        defaults = [
            {
                "build-job": {
                    "script": [
                        "cd {env_dir}",
                        "spack env activate --without-view .",
                        "spack ci rebuild",
                    ]
                }
            },
            {"noop-job": {"script": ['echo "All specs already up to date, nothing to rebuild."']}},
        ]

        # Job overrides
        overrides = [
            # Reindex script
            {
                "reindex-job": {
                    "script:": ["spack buildcache update-index --keys {index_target_mirror}"]
                }
            },
            # Cleanup script
            {
                "cleanup-job": {
                    "script:": ["spack -d mirror destroy {mirror_prefix}/$CI_PIPELINE_ID"]
                }
            },
            # Add signing job tags
            {"signing-job": {"tags": ["aws", "protected", "notary"]}},
            # Remove reserved tags
            {"any-job-remove": {"tags": SPACK_RESERVED_TAGS}},
        ]

        pipeline_gen = overrides + self.ci_config.get("pipeline-gen", []) + defaults

        for section in reversed(pipeline_gen):
            name = self.__is_named(section)
            has_submapping = "submapping" in section
            section = cfg.InternalConfigScope._process_dict_keyname_overrides(section)

            if name:
                remove_job_name = self.__job_name(name, suffix="-remove")
                merge_job_name = self.__job_name(name)
                do_remove = remove_job_name in section
                do_merge = merge_job_name in section

                def _apply_section(dest, src):
                    if do_remove:
                        dest = spack.config.remove_yaml(dest, src[remove_job_name])
                    if do_merge:
                        dest = copy.copy(spack.config.merge_yaml(dest, src[merge_job_name]))

                if name == "build":
                    # Apply attributes to all build jobs
                    for _, job in jobs.items():
                        if job["spec"]:
                            _apply_section(job["attributes"], section)
                elif name == "any":
                    # Apply section attributes too all jobs
                    for _, job in jobs.items():
                        _apply_section(job["attributes"], section)
                else:
                    # Create a signing job if there is script and the job hasn't
                    # been initialized yet
                    if name == "signing" and name not in jobs:
                        if "signing-job" in section:
                            if "script" not in section["signing-job"]:
                                continue
                            else:
                                jobs[name] = self.__init_job("")
                    # Apply attributes to named job
                    _apply_section(jobs[name]["attributes"], section)

            elif has_submapping:
                # Apply section jobs with specs to match
                for _, job in jobs.items():
                    if job["spec"]:
                        job["attributes"] = self.__apply_submapping(
                            job["attributes"], job["spec"], section
                        )

        for _, job in jobs.items():
            if job["spec"]:
                job["spec"] = job["spec"].name

        return self.ir


def write_pipeline_manifest(specs, src_prefix, dest_prefix, output_file):
    """Write out the file describing specs that should be copied"""
    buildcache_copies = {}

    for release_spec in specs:
        release_spec_dag_hash = release_spec.dag_hash()
        # TODO: This assumes signed version of the spec
        buildcache_copies[release_spec_dag_hash] = [
            {
                "src": url_util.join(
                    src_prefix,
                    bindist.build_cache_relative_path(),
                    bindist.tarball_name(release_spec, ".spec.json.sig"),
                ),
                "dest": url_util.join(
                    dest_prefix,
                    bindist.build_cache_relative_path(),
                    bindist.tarball_name(release_spec, ".spec.json.sig"),
                ),
            },
            {
                "src": url_util.join(
                    src_prefix,
                    bindist.build_cache_relative_path(),
                    bindist.tarball_path_name(release_spec, ".spack"),
                ),
                "dest": url_util.join(
                    dest_prefix,
                    bindist.build_cache_relative_path(),
                    bindist.tarball_path_name(release_spec, ".spack"),
                ),
            },
        ]

    target_dir = os.path.dirname(output_file)

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    with open(output_file, "w") as fd:
        fd.write(json.dumps(buildcache_copies))


def check_for_broken_specs(pipeline_specs, broken_specs_url):
    """Check the pipeline specs against the list of known broken specs and return
        True if there were any matches, False otherwise."""
    if broken_specs_url.startswith("http"):
        # To make checking each spec against the list faster, we require
        # a url protocol that allows us to iterate the url in advance.
        tty.msg("Cannot use an http(s) url for broken specs, ignoring")
        return False
    else:
        broken_spec_urls = web_util.list_url(broken_specs_url)

        if broken_spec_urls is None:
            return False

        known_broken_specs_encountered = []
        for release_spec in pipeline_specs:
            release_spec_dag_hash = release_spec.dag_hash()
            if release_spec_dag_hash in broken_spec_urls:
                known_broken_specs_encountered.append(release_spec_dag_hash)

        if known_broken_specs_encountered:
            tty.error("This pipeline generated hashes known to be broken on develop:")
            display_broken_spec_messages(broken_specs_url, known_broken_specs_encountered)
            return True


def collect_pipeline_options(
        args: spack.main.SpackArgumentParser,
        env: ev.Environment,
    ) -> PipelineOptions:
    """Gather pipeline options from cli args, spack environment, and
    os environment variables """
    options = PipelineOptions(env)

    """
            env: ev.Environment,
            print_summary: bool = False,
            output_file: Optional[str] = None,
            check_index_only: bool = False,
            run_optimizer: bool = False,
            use_dependencies: bool = False,
            broken_specs_url: Optional[str] = None,
            enable_artifacts_buildcache: bool = False,
            rebuild_index: bool = True,
            temporary_storage_url_prefix: Optional[str] = None,
            untouched_pruning_dependent_depth: Optional[int] = None,
            prune_untouched: bool = False,
            prune_up_to_date: bool = True,
            stack_name: Optional[str] = None,
            job_name: Optional[str] = None,
            pipeline_id: Optional[str] = None,
            pipeline_type: Optional[PipelineType] = None,
            require_signing: bool = False,
            artifacts_root: Optional[str] = None,
            remote_mirror: Optional[str] = None,
            shared_pr_mirror: Optional[str] = None,
            remote_mirror_override: Optional[str] = None,  # deprecated, remove in Spack 0.23
            buildcache_destination: Optional[spack.mirror.Mirror] = None,
            cdash_handler: Optional["CDashHandler"] = None,
    """

    options.output_file = args.output_file
    options.run_optimizer = args.optimize
    options.use_dependencies = args.dependencies
    options.prune_up_to_date = args.prune_dag
    options.check_index_only = args.index_only
    options.artifacts_root = args.artifacts_root
    options.remote_mirror_override = args.buildcache_destination

    ci_config = cfg.get("ci")

    cdash_config = cfg.get("cdash")
    if "build-group" in cdash_config:
        options.cdash_handler = CDashHandler(cdash_config)

    dependent_depth = os.environ.get("SPACK_PRUNE_UNTOUCHED_DEPENDENT_DEPTH", None)
    if dependent_depth is not None:
        try:
            options.untouched_pruning_dependent_depth = int(dependent_depth)
        except (TypeError, ValueError):
            tty.warn(
                f"Unrecognized value ({dependent_depth}) "
                "provided for SPACK_PRUNE_UNTOUCHED_DEPENDENT_DEPTH, "
                "ignoring it."
            )

    spack_prune_untouched = os.environ.get("SPACK_PRUNE_UNTOUCHED", None)
    options.prune_untouched = spack_prune_untouched is not None and spack_prune_untouched.lower() == "true"

    # Allow overriding --prune-dag cli opt with environment variable
    prune_dag_override = os.environ.get("SPACK_PRUNE_UP_TO_DATE", None)
    if prune_dag_override is not None:
        options.prune_up_to_date = True if prune_dag_override.lower() == "true" else False

    options.stack_name = os.environ.get("SPACK_CI_STACK_NAME", None)
    options.require_signing = os.environ.get("SPACK_REQUIRE_SIGNING", False)
    options.job_name = os.environ.get("CI_JOB_NAME", "job-does-not-exist")
    options.pipeline_id = os.environ.get("CI_PIPELINE_ID", "pipeline-does-not-exist")

    # Get the type of pipeline, which is optional
    spack_pipeline_type = os.environ.get("SPACK_PIPELINE_TYPE", None)
    if spack_pipeline_type:
        try:
            options.pipeline_type = PipelineType[spack_pipeline_type]
        except KeyError:
            options.pipeline_type = None

    if "broken-specs-url" in ci_config:
        options.broken_specs_url = ci_config["broken-specs-url"]

    if "enable-artifacts-buildcache" in ci_config:
        tty.warn("Support for enable-artifacts-buildcache will be removed in Spack 0.23")
        options.enable_artifacts_buildcache = ci_config["enable-artifacts-buildcache"]

    if "rebuild-index" in ci_config and ci_config["rebuild-index"] is False:
        options.rebuild_index = False

    if "temporary-storage-url-prefix" in ci_config:
        tty.warn("Support for temporary-storage-url-prefix will be removed in Spack 0.23")
        options.temporary_storage_url_prefix = ci_config["temporary-storage-url-prefix"]

    return options


def update_env_scopes(env_manifest_path: str, cli_scopes: List[str]) -> None:
    """Add any config scopes from cli_scopes which aren't already included in the
    environment, by reading the yaml, adding the missing includes, and writing the
    updated yaml back to the same location.
    """
    with open(env_manifest_path, "r") as env_fd:
        env_yaml_root = syaml.load(env_fd)

    # Add config scopes to environment
    env_includes = env_yaml_root["spack"].get("include", [])
    include_scopes = []
    for scope in cli_scopes:
        if scope not in include_scopes and scope not in env_includes:
            include_scopes.insert(0, scope)
    env_includes.extend(include_scopes)
    env_yaml_root["spack"]["include"] = env_includes

    with open(env_manifest_path, "w") as fd:
        fd.write(syaml.dump_config(env_yaml_root, default_flow_style=False))


def generate_pipeline(env: ev.Environment, args: spack.main.SpackArgumentParser) -> None:
    """Generate a gitlab yaml file to run a dynamic child pipeline from
        the spec matrix in the active environment.

    Arguments:
        env (spack.environment.Environment): Activated environment object
            which must contain a gitlab-ci section describing attributes for
            all jobs
        args: (spack.main.SpackArgumentParser): Parsed arguments from the command
            line.
    """
    with spack.concretize.disable_compiler_existence_check():
        with env.write_transaction():
            env.concretize()
            env.write()

    yaml_root = env.manifest[ev.TOP_LEVEL_KEY]

    options = collect_pipeline_options(args, env)
    options.environment = env

    # Get the joined "ci" config with all of the current scopes resolved
    ci_config = cfg.get("ci")
    if not ci_config:
        tty.die("Environment yaml must have `ci` config section in order to generate a pipeline.")

    # Get the target platform we should generate a pipeline for
    ci_target = ci_config.get("target", "gitlab")
    try:
        target_formatter = get_formatter(ci_target)
    except UnknownFormatterException:
        tty.die(f"Spack CI module cannot generate a pipeline for format {ci_target}")

    # If we are not doing any kind of pruning, we are rebuilding everything
    rebuild_everything = not options.prune_up_to_date and not options.prune_untouched

    pipeline_mirrors = spack.mirror.MirrorCollection(binary=True)
    deprecated_mirror_config = False
    if "buildcache-destination" in pipeline_mirrors:
        if options.remote_mirror_override:
            tty.die(
                "Using the deprecated --buildcache-destination cli option and "
                "having a mirror named 'buildcache-destination' at the same time "
                "is not allowed"
            )
        options.buildcache_destination = pipeline_mirrors["buildcache-destination"]
    else:
        deprecated_mirror_config = True
        # TODO: This will be an error in Spack 0.23

    # TODO: Remove this block in spack 0.23
    if deprecated_mirror_config:
        if "mirrors" not in yaml_root or len(yaml_root["mirrors"].values()) < 1:
            tty.die("spack ci generate requires an env containing a mirror")

        ci_mirrors = yaml_root["mirrors"]
        mirror_urls = [url for url in ci_mirrors.values()]
        options.remote_mirror_url = mirror_urls[0]

    # If a remote mirror override (alternate buildcache destination) was
    # specified, add it here in case it has already built hashes we might
    # generate.
    # TODO: Remove this block in Spack 0.23
    mirrors_to_check = None
    if deprecated_mirror_config and options.remote_mirror_override:
        if options.pipeline_type == PipelineType.PROTECTED_BRANCH:
            # Overriding the main mirror in this case might result
            # in skipping jobs on a release pipeline because specs are
            # up to date in develop.  Eventually we want to notice and take
            # advantage of this by scheduling a job to copy the spec from
            # develop to the release, but until we have that, this makes
            # sure we schedule a rebuild job if the spec isn't already in
            # override mirror.
            mirrors_to_check = {"override": options.remote_mirror_override}

        # If we have a remote override and we want generate pipeline using
        # --check-index-only, then the override mirror needs to be added to
        # the configured mirrors when bindist.update() is run, or else we
        # won't fetch its index and include in our local cache.
        spack.mirror.add(
            spack.mirror.Mirror(options.remote_mirror_override, name="ci_pr_mirror"),
            cfg.default_modify_scope(),
        )

    # TODO: Remove this block in Spack 0.23
    if deprecated_mirror_config and options.pipeline_type == PipelineType.PULL_REQUEST:
        stack_name = options.stack_name if options.stack_name else ""
        options.shared_pr_mirror = url_util.join(SHARED_PR_MIRROR_URL, stack_name)
        spack.mirror.add(
            spack.mirror.Mirror(options.shared_pr_mirror, name="ci_shared_pr_mirror"),
            cfg.default_modify_scope(),
        )

    # Build a pipeline from the specs in the concrete environment
    pipeline = PipelineDag(
        [
            concrete
            for abstract, concrete in env.concretized_specs()
            if abstract in env.spec_lists["specs"]
        ]
    )

    # Possibly prune specs that were unaffected by the change
    if options.prune_untouched:
        # If we don't have two revisions to compare, or if either the spack.yaml
        # associated with the active env or the .gitlab-ci.yml files changed
        # between the provided revisions, then don't do any "untouched spec"
        # pruning.  Otherwise, list the names of all packages touched between
        # rev1 and rev2, and prune from the pipeline any node whose spec has a
        # packagen name not in that list.
        rev1, rev2 = get_change_revisions()
        tty.debug("Got following revisions: rev1={0}, rev2={1}".format(rev1, rev2))
        if rev1 and rev2:
            # If the stack file itself did not change, proceed with pruning
            if not get_stack_changed(env.manifest_path, rev1, rev2):
                affected_pkgs = compute_affected_packages(rev1, rev2)
                tty.debug("affected pkgs:")
                for p in affected_pkgs:
                    tty.debug("  {0}".format(p))
                affected_specs = get_spec_filter_list(
                    env, affected_pkgs, dependent_traverse_depth=options.untouched_pruning_dependent_depth
                )
                tty.msg(f"dependent_traverse_depth={options.untouched_pruning_dependent_depth}, affected specs:")
                for s in affected_specs:
                    tty.msg(f"  {PipelineDag.key(s)}")

                prune_unaffected_specs(pipeline, affected_specs)

    # Possibly prune specs that are already built on some configured mirror
    if options.prune_up_to_date:
        prune_built_specs(pipeline, mirrors_to_check, options.check_index_only)

    # List all specs remaining after any pruning
    pipeline_specs = [n.spec for _, (k, n) in pipeline.traverse(top_down=True)]

    # FIXME: This block needs detangling, these bits are all involved:
    #     - here we write manifest file for stack pipeline
    #     - gitlab passes manifest files from multiple stack pipelines
    #           as artifacts to a single job, so files names can collide
    #     - in protected-publish, where "spack buildcache sync --manifest" happens
    spack_buildcache_copy = os.environ.get("SPACK_COPY_BUILDCACHE", None)
    if spack_buildcache_copy:
        buildcache_copy_dest_prefix = spack_buildcache_copy
        buildcache_copy_src_prefix = (
            options.buildcache_destination.fetch_url
            if options.buildcache_destination
            else options.remote_mirror_override or options.remote_mirror_url
        )

        if options.pipeline_type == PipelineType.COPY_ONLY:
            manifest_specs = [s for _, s in env.concretized_specs()]
        else:
            manifest_specs = pipeline_specs

        pipeline_artifacts_dir = os.path.abspath(options.artifacts_root)
        copy_specs_dir = os.path.join(pipeline_artifacts_dir, "specs_to_copy")
        copy_specs_file = os.path.join(
            copy_specs_dir,
            "copy_{}_specs.json".format(options.stack_name if options.stack_name else "rebuilt"),
        )

        write_pipeline_manifest(manifest_specs, buildcache_copy_src_prefix, buildcache_copy_dest_prefix, copy_specs_file)

    # If this is configured, spack will fail "spack ci generate" if it
    # generates any hash which exists under the broken specs url.
    if options.broken_specs_url and not options.pipeline_type == PipelineType.COPY_ONLY:
        broken = check_for_broken_specs(pipeline_specs, options.broken_specs_url)
        if broken and not rebuild_everything:
            sys.exit(1)

    spack_ci = SpackCI(ci_config, pipeline)
    spack_ci_ir = spack_ci.generate_ir()

    # Format the pipeline using the formatter specified in the environment
    target_formatter(pipeline, spack_ci_ir, options)

    # Clean up remote mirror override if enabled
    # TODO: Remove this block in Spack 0.23
    if deprecated_mirror_config:
        if options.remote_mirror_override:
            spack.mirror.remove("ci_pr_mirror", cfg.default_modify_scope())
        if options.pipeline_type == PipelineType.PULL_REQUEST:
            spack.mirror.remove("ci_shared_pr_mirror", cfg.default_modify_scope())

    # Use all unpruned specs to populate the build group for this set
    if options.cdash_handler and options.cdash_handler.auth_token:
        try:
            options.cdash_handler.populate_buildgroup([
                options.cdash_handler.build_name(s) for s in pipeline_specs
            ])
        except (SpackError, HTTPError, URLError) as err:
            tty.warn("Problem populating buildgroup: {0}".format(err))
    else:
        tty.warn("Unable to populate buildgroup without CDash credentials")


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


def _push_mirror_contents(input_spec, sign_binaries, mirror_url):
    """Unchecked version of the public API, for easier mocking"""
    unsigned = not sign_binaries
    tty.debug("Creating buildcache ({0})".format("unsigned" if unsigned else "signed"))
    push_url = spack.mirror.Mirror.from_url(mirror_url).push_url
    return bindist.push(input_spec, push_url, bindist.PushOptions(force=True, unsigned=unsigned))


def push_mirror_contents(input_spec: spack.spec.Spec, mirror_url, sign_binaries):
    """Push one or more binary packages to the mirror.

    Arguments:

        input_spec(spack.spec.Spec): Installed spec to push
        mirror_url (str): Base url of target mirror
        sign_binaries (bool): If True, spack will attempt to sign binary
            package before pushing.
    """
    try:
        return _push_mirror_contents(input_spec, sign_binaries, mirror_url)
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
            return False
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
        msg = ("Unable to copy files ({0}) to artifacts {1} due to " "exception: {2}").format(
            src, artifacts_dir, str(err)
        )
        tty.warn(msg)


def copy_stage_logs_to_artifacts(job_spec: spack.spec.Spec, job_log_dir: str) -> None:
    """Copy selected build stage file(s) to the given artifacts directory

    Looks for build logs in the stage directory of the given
    job_spec, and attempts to copy the files into the directory given
    by job_log_dir.

    Args:
        job_spec: spec associated with spack install log
        job_log_dir: path into which build log should be copied
    """
    tty.debug("job spec: {0}".format(job_spec))
    if not job_spec:
        msg = "Cannot copy stage logs: job spec ({0}) is required"
        tty.error(msg.format(job_spec))
        return

    try:
        pkg_cls = spack.repo.PATH.get_pkg_class(job_spec.name)
        job_pkg = pkg_cls(job_spec)
        tty.debug("job package: {0}".format(job_pkg))
    except AssertionError:
        msg = "Cannot copy stage logs: job spec ({0}) must be concrete"
        tty.error(msg.format(job_spec))
        return

    stage_dir = job_pkg.stage.path
    tty.debug("stage dir: {0}".format(stage_dir))
    for file in [job_pkg.log_path, job_pkg.env_mods_path, *job_pkg.builder.archive_files]:
        copy_files_to_artifacts(file, job_log_dir)


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


def reproduce_ci_job(url, work_dir, autostart, gpg_url, runtime):
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
    work_dir = os.path.realpath(work_dir)
    download_and_extract_artifacts(url, work_dir)

    gpg_path = None
    if gpg_url:
        gpg_path = web_util.fetch_url_text(gpg_url, dest_dir=os.path.join(work_dir, "_pgp"))
        rel_gpg_path = gpg_path.replace(work_dir, "").lstrip(os.path.sep)

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
        mounted_workdir = "/reproducer"
        if repro_details:
            mount_as_dir = repro_details["ci_project_dir"]
            mounted_repro_dir = os.path.join(mount_as_dir, rel_repro_dir)
            mounted_env_dir = os.path.join(mount_as_dir, relative_concrete_env_dir)
            if gpg_path:
                mounted_gpg_path = os.path.join(mounted_workdir, rel_gpg_path)

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

    entrypoint_script = [
        ["git", "config", "--global", "--add", "safe.directory", mount_as_dir],
        [".", os.path.join(mount_as_dir if job_image else work_dir, "share/spack/setup-env.sh")],
        ["spack", "gpg", "trust", mounted_gpg_path if job_image else gpg_path] if gpg_path else [],
        ["spack", "env", "activate", mounted_env_dir if job_image else repro_dir],
        [os.path.join(mounted_repro_dir, "install.sh") if job_image else install_script],
    ]

    inst_list = []
    # Finally, print out some instructions to reproduce the build
    if job_image:
        # Allow interactive
        entrypoint_script.extend(
            [
                [
                    "echo",
                    "Re-run install script using:\n\t{0}".format(
                        os.path.join(mounted_repro_dir, "install.sh")
                        if job_image
                        else install_script
                    ),
                ],
                # Allow interactive
                ["exec", "$@"],
            ]
        )
        process_command(
            "entrypoint", entrypoint_script, work_dir, run=False, exit_on_failure=False
        )

        docker_command = [
            [
                runtime,
                "run",
                "-i",
                "-t",
                "--rm",
                "--name",
                "spack_reproducer",
                "-v",
                ":".join([work_dir, mounted_workdir, "Z"]),
                "-v",
                ":".join(
                    [
                        os.path.join(work_dir, "jobs_scratch_dir"),
                        os.path.join(mount_as_dir, "jobs_scratch_dir"),
                        "Z",
                    ]
                ),
                "-v",
                ":".join([os.path.join(work_dir, "spack"), mount_as_dir, "Z"]),
                "--entrypoint",
                os.path.join(mounted_workdir, "entrypoint.sh"),
                job_image,
                "bash",
            ]
        ]
        autostart = autostart and setup_result
        process_command("start", docker_command, work_dir, run=autostart)

        if not autostart:
            inst_list.append("\nTo run the docker reproducer:\n\n")
            inst_list.extend(
                [
                    "    - Start the docker container install",
                    "       $ {0}/start.sh".format(work_dir),
                ]
            )
    else:
        process_command("reproducer", entrypoint_script, work_dir, run=False)

        inst_list.append("\nOnce on the tagged runner:\n\n")
        inst_list.extent(
            ["    - Run the reproducer script", "       $ {0}/reproducer.sh".format(work_dir)]
        )

    if not setup_result:
        inst_list.append("\n    - Clone spack and acquire tested commit")
        inst_list.append("\n        {0}\n".format(spack_info))
        inst_list.append("\n")
        inst_list.append("\n        Path to clone spack: {0}/spack\n\n".format(work_dir))

    tty.msg("".join(inst_list))


def process_command(name, commands, repro_dir, run=True, exit_on_failure=True):
    """
    Create a script for and run the command. Copy the script to the
    reproducibility directory.

    Arguments:
        name (str): name of the command being processed
        commands (list): list of arguments for single command or list of lists of
            arguments for multiple commands. No shell escape is performed.
        repro_dir (str): Job reproducibility directory
        run (bool): Run the script and return the exit code if True

    Returns: the exit code from processing the command
    """
    tty.debug("spack {0} arguments: {1}".format(name, commands))

    if len(commands) == 0 or isinstance(commands[0], str):
        commands = [commands]

    # Create a string [command 1] && [command 2] && ... && [command n] with commands
    # quoted using double quotes.
    args_to_string = lambda args: " ".join('"{}"'.format(arg) for arg in args)
    full_command = " \n ".join(map(args_to_string, commands))

    # Write the command to a shell script
    script = "{0}.sh".format(name)
    with open(script, "w") as fd:
        fd.write("#!/bin/sh\n\n")
        fd.write("\n# spack {0} command\n".format(name))
        if exit_on_failure:
            fd.write("set -e\n")
        if os.environ.get("SPACK_VERBOSE_SCRIPT"):
            fd.write("set -x\n")
        fd.write(full_command)
        fd.write("\n")

    st = os.stat(script)
    os.chmod(script, st.st_mode | stat.S_IEXEC)

    copy_path = os.path.join(repro_dir, script)
    shutil.copyfile(script, copy_path)
    st = os.stat(copy_path)
    os.chmod(copy_path, st.st_mode | stat.S_IEXEC)

    # Run the generated install.sh shell script as if it were being run in
    # a login shell.
    exit_code = None
    if run:
        try:
            cmd_process = subprocess.Popen(["/bin/sh", "./{0}".format(script)])
            cmd_process.wait()
            exit_code = cmd_process.returncode
        except (ValueError, subprocess.CalledProcessError, OSError) as err:
            tty.error("Encountered error running {0} script".format(name))
            tty.error(err)
            exit_code = 1

        tty.debug("spack {0} exited {1}".format(name, exit_code))
    else:
        # Delete the script, it is copied to the destination dir
        os.remove(script)

    return exit_code


def create_buildcache(
    input_spec: spack.spec.Spec, *, destination_mirror_urls: List[str], sign_binaries: bool = False
) -> List[PushResult]:
    """Create the buildcache at the provided mirror(s).

    Arguments:
        input_spec: Installed spec to package and push
        destination_mirror_urls: List of urls to push to
        sign_binaries: Whether or not to sign buildcache entry

    Returns: A list of PushResults, indicating success or failure.
    """
    results = []

    for mirror_url in destination_mirror_urls:
        results.append(
            PushResult(
                success=push_mirror_contents(input_spec, mirror_url, sign_binaries), url=mirror_url
            )
        )

    return results


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


class CDashHandler:
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

    def build_name(self, spec: spack.spec.Spec = None) -> str:
        """Returns the CDash build name.

        A name will be generated if the `spec` is provided,
        otherwise, the value will be retrieved from the environment
        through the `SPACK_CDASH_BUILD_NAME` variable.

        Returns: (str) current spec's CDash build name."""
        if spec:
            build_name = "{0}@{1}%{2} hash={3} arch={4} ({5})".format(
                spec.name,
                spec.version,
                spec.compiler,
                spec.dag_hash(),
                spec.architecture,
                self.build_group,
            )
            tty.debug(
                "Generated CDash build name ({0}) from the {1}".format(build_name, spec.name)
            )
            return build_name

        build_name = os.environ.get("SPACK_CDASH_BUILD_NAME")
        tty.debug("Using CDash build name ({0}) from the environment".format(build_name))
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
            tty.debug("Using build stamp ({0}) from the environment".format(build_stamp))
            return build_stamp

        build_stamp = cdash_build_stamp(self.build_group, time.time())
        tty.debug("Generated new build stamp ({0})".format(build_stamp))
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

    def report_skipped(self, spec: spack.spec.Spec, report_dir: str, reason: Optional[str]):
        """Explicitly report skipping testing of a spec (e.g., it's CI
        configuration identifies it as known to have broken tests or
        the CI installation failed).

        Args:
            spec: spec being tested
            report_dir: directory where the report will be written
            reason: reason the test is being skipped
        """
        configuration = CDashConfiguration(
            upload_url=self.upload_url,
            packages=[spec.name],
            build=self.build_name,
            site=self.site,
            buildstamp=self.build_stamp,
            track=None,
        )
        reporter = CDash(configuration=configuration)
        reporter.test_skipped_report(report_dir, spec, reason)
