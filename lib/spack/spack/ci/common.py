# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import copy
import json
import os
import time
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlencode
from urllib.request import HTTPHandler, Request, build_opener

import llnl.util.filesystem as fs
import llnl.util.tty as tty
from llnl.util.lang import memoized

import spack.binary_distribution as bindist
import spack.config as cfg
import spack.deptypes as dt
import spack.environment as ev
import spack.spec
import spack.util.spack_yaml as syaml
import spack.util.url as url_util
from spack.reporters import CDash, CDashConfiguration
from spack.reporters.cdash import build_stamp as cdash_build_stamp

SPACK_RESERVED_TAGS = ["public", "protected", "notary"]


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


def _spec_matches(spec, match_string):
    return spec.intersects(match_string)


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


def update_env_scopes(env_manifest_path: str, cli_scopes: List[str]) -> None:
    """Add any config scopes from cli_scopes which aren't already included in the
    environment, by reading the yaml, adding the missing includes, and writing the
    updated yaml back to the same location.
    """
    with open(env_manifest_path, "r") as env_fd:
        env_yaml_root = syaml.load(env_fd)

    # Add config scopes to environment
    env_includes = env_yaml_root["spack"].get("include", [])
    include_scopes: List[str] = []
    for scope in cli_scopes:
        if scope not in include_scopes and scope not in env_includes:
            include_scopes.insert(0, scope)
    env_includes.extend(include_scopes)
    env_yaml_root["spack"]["include"] = env_includes

    with open(env_manifest_path, "w") as fd:
        fd.write(syaml.dump_config(env_yaml_root, default_flow_style=False))


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

    def build_name(self, spec: Optional[spack.spec.Spec] = None) -> str:
        """Returns the CDash build name.

        A name will be generated if the `spec` is provided,
        otherwise, the value will be retrieved from the environment
        through the `SPACK_CDASH_BUILD_NAME` variable.

        Returns: (str) given spec's CDash build name."""
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

        build_name = os.environ.get("SPACK_CDASH_BUILD_NAME", "None")
        tty.debug("Using CDash build name ({0}) from the environment".format(build_name))
        return build_name

    @property  # type: ignore
    def build_stamp(self):
        """Returns the CDash build stamp.

        The one defined by SPACK_CDASH_BUILD_STAMP environment variable
        is preferred due to the representation of timestamps; otherwise,
        one will be built.

        Returns: (str) CDash build stamp from env or newly generated one"""
        build_stamp = os.environ.get("SPACK_CDASH_BUILD_STAMP", None)
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


class PipelineType(Enum):
    COPY_ONLY = 1
    spack_copy_only = 1
    PROTECTED_BRANCH = 2
    spack_protected_branch = 2
    PULL_REQUEST = 3
    spack_pull_request = 3


class PipelineOptions:
    """A container for all pipeline options that can be specified (whether
    via cli, config/yaml, or environment variables)"""

    def __init__(
        self,
        env: ev.Environment,
        artifacts_root: str = "jobs_scratch_dir",
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
        prune_external: bool = True,
        stack_name: Optional[str] = None,
        pipeline_type: Optional[PipelineType] = None,
        require_signing: bool = False,
        remote_mirror_url: Optional[str] = None,  # remove n Spack 0.23
        shared_pr_mirror: Optional[str] = None,  # remove in Spack 0.23
        remote_mirror_override: Optional[str] = None,  # deprecated, remove in Spack 0.23
        copy_yaml_to: Optional[str] = None,  # deprecated, remove in Spack 0.23
        buildcache_destination: Optional[spack.mirror.Mirror] = None,
        cdash_handler: Optional["CDashHandler"] = None,
    ):
        """
        Args:
            env: Active spack environment
            artifacts_root: Path to location where artifacts should be stored
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
            prune_external: Prune specs from pipeline if they are external
            stack_name: Name of spack stack
            pipeline_type: Type of pipeline running (optional)
            require_signing: Require buildcache to be signed (fail w/out signing key)
            remote_mirror_url: Mirror from spack.yaml (deprecated)
            shared_pr_mirror: Shared pr mirror url (deprecated)
            remote_mirror_override: Override the mirror in the spack environment (deprecated)
            copy_yaml_to: Path where generated yaml should be copied to
            buildcache_destination: The mirror where built binaries should be pushed
            cdash_handler: Object for communicating build information with CDash
        """
        self.env = env
        self.artifacts_root = artifacts_root
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
        self.prune_external = prune_external
        self.stack_name = stack_name
        self.pipeline_type = pipeline_type
        self.require_signing = require_signing
        self.remote_mirror_url = remote_mirror_url
        self.shared_pr_mirror = shared_pr_mirror
        self.remote_mirror_override = remote_mirror_override
        self.copy_yaml_to = copy_yaml_to
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


class PruningResults:
    filterDescriptions: Tuple[str, ...]
    filterResults: Dict[str, List[bool]]

    def __init__(self, descriptions: Tuple[str, ...], results: Dict[str, List[bool]]):
        self.filterDescriptions = descriptions
        self.filterResults = results

    def get_filter_result_for_description(self, key: str, description: str) -> bool:
        filterIndex = self.filterDescriptions.index(description)
        return self.filterResults[key][filterIndex]


class PipelineDag:
    """Turn a list of specs into a simple directed graph, that doesn't keep track
    of edge types."""

    @classmethod
    def key(cls, spec: spack.spec.Spec) -> str:
        return f"{spec.name}/{spec.dag_hash(7)}"

    def __init__(self, specs: List[spack.spec.Spec]) -> None:
        # Build dictionary of nodes
        self.nodes: Dict[str, PipelineNode] = {
            PipelineDag.key(s): PipelineNode(s)
            for s in spack.traverse.traverse_nodes(specs, deptype=dt.ALL_TYPES, root=True)
        }

        # Create edges
        for edge in spack.traverse.traverse_edges(
            specs, deptype=dt.ALL_TYPES, root=False, cover="edges"
        ):
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

    def traverse(self, top_down: bool = True):
        visited = set()
        level = 0

        if top_down:
            # Yields the roots first, followed by direct children of roots, followed
            # by their children and so on.
            node_list = [(key, node) for key, node in self.nodes.items() if len(node.parents) == 0]
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
                    (k, self.nodes[k])
                    for _, n in node_list
                    for k in n.parents
                    if k not in visited and all([c in visited for c in self.nodes[k].children])
                ]

    def get_dependencies(self, node: PipelineNode, transitive: bool = False):
        dep_list = [self.nodes[k] for k in node.children]

        if not transitive:
            return [d.spec for d in dep_list]

        all_deps = set()

        while dep_list:
            dep_node = dep_list.pop(0)
            all_deps.add(dep_node.spec)
            dep_list.extend([self.nodes[k] for k in dep_node.children])

        return all_deps


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
    def generate_ir(self) -> Dict[Any, Any]:
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
