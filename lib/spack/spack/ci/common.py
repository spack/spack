# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import copy
import enum
import errno
import glob
import gzip
import json
import os
import re
import shutil
import sys
import time
from collections import deque
from itertools import chain
from typing import Any, Callable, Dict, Generator, List, Optional, Set, Tuple, Union
from urllib.parse import quote, urlencode, urlparse
from urllib.request import Request

import spack.binary_distribution
import spack.config as cfg
import spack.deptypes as dt
import spack.environment as ev
import spack.error
import spack.llnl.util.filesystem as fs
import spack.llnl.util.tty as tty
import spack.mirrors.mirror
import spack.schema
import spack.spec
import spack.util.compression as compression
import spack.util.web as web_util
from spack import traverse
from spack.llnl.util.lang import memoized
from spack.reporters import CDash, CDashConfiguration
from spack.reporters.cdash import SPACK_CDASH_TIMEOUT
from spack.reporters.cdash import build_stamp as cdash_build_stamp
from spack.url_buildcache import get_url_buildcache_class

IS_WINDOWS = sys.platform == "win32"
SPACK_RESERVED_TAGS = ["public", "protected", "notary"]

# this exists purely for testing purposes
_urlopen = web_util.urlopen

#: Names of the core CI jobs, which are those not dependent on a specs
core_job_names = ["cleanup", "copy", "noop", "reindex", "signing"]

#: Names of all jobs that can have a spec
spec_job_names = ["build", "test"]

#: Names of all possible named jobs
all_job_names = ["any"] + spec_job_names + core_job_names

#: default job settings
default_job_settings = {
    "build-job": {
        "script": ["cd {env_dir}", "spack env activate --without-view .", "spack ci rebuild"]
    },
    "noop-job": {"script": ['echo "All specs already up-to-date, nothing to rebuild."']},
}

#: Override job settings
override_job_settings = {
    "any-job-remove": {"tags": SPACK_RESERVED_TAGS},
    "cleanup-job": {"script": ["spack -d mirror destroy {mirror_prefix}/$CI_PIPELINE_ID"]},
    "reindex-job": {"script": ["spack buildcache update-index --keys {index_target_mirror}"]},
    "signing-job": {"tags": ["aws", "protected", "notary"]},
}


def copy_gzipped(glob_or_path: str, dest: str) -> None:
    """Copy all of the files in the source glob/path to the destination.

    Args:
        glob_or_path: path to file to test
        dest: destination path to copy to
    """

    files = glob.glob(glob_or_path)
    if not files:
        raise OSError(f"No such file or directory: '{glob_or_path}'", errno.ENOENT)
    if len(files) > 1 and not os.path.isdir(dest):
        raise ValueError(
            f"'{glob_or_path}' matches multiple files but '{dest}' is not a directory"
        )

    def is_gzipped(path):
        with open(path, "rb") as fd:
            return compression.GZipFileType().matches_magic(fd)

    for src in files:
        if is_gzipped(src):
            fs.copy(src, dest)
        else:
            # Compress and copy in one step
            src_name = os.path.basename(src)
            if os.path.isdir(dest):
                zipped = os.path.join(dest, f"{src_name}.gz")
            elif not dest.endswith(".gz"):
                zipped = f"{dest}.gz"
            else:
                zipped = dest

            with open(src, "rb") as fin, gzip.open(zipped, "wb") as fout:
                shutil.copyfileobj(fin, fout)


def copy_files_to_artifacts(
    src: str, artifacts_dir: str, *, compress_artifacts: bool = False
) -> None:
    """
    Copy file(s) to the given artifacts directory

    Args:
        src (str): the glob-friendly path expression for the file(s) to copy
        artifacts_dir (str): the destination directory
        compress_artifacts (bool): option to compress copied artifacts using Gzip
    """
    try:

        if compress_artifacts:
            copy_gzipped(src, artifacts_dir)
        else:
            fs.copy(src, artifacts_dir)
    except Exception as err:
        tty.warn(
            (
                f"Unable to copy files ({src}) to artifacts {artifacts_dir} due to "
                f"exception: {str(err)}"
            )
        )


def win_quote(quote_str: str) -> str:
    if IS_WINDOWS:
        quote_str = f'"{quote_str}"'
    return quote_str


def _spec_matches(spec, match_string):
    return spec.intersects(match_string)


def ensure_expected_target_path(path: str) -> str:
    """Returns passed paths with all Windows path separators exchanged
    for posix separators

    TODO (johnwparent): Refactor config + cli read/write to deal only in posix style paths
    """
    if path:
        return path.replace("\\", "/")
    return path


def write_pipeline_manifest(specs, src_prefix, dest_prefix, output_file):
    """Write out the file describing specs that should be copied"""
    buildcache_copies = {}

    for release_spec in specs:
        release_spec_dag_hash = release_spec.dag_hash()
        cache_class = get_url_buildcache_class(
            layout_version=spack.binary_distribution.CURRENT_BUILD_CACHE_LAYOUT_VERSION
        )
        buildcache_copies[release_spec_dag_hash] = {
            "src": cache_class.get_manifest_url(release_spec, src_prefix),
            "dest": cache_class.get_manifest_url(release_spec, dest_prefix),
        }

    target_dir = os.path.dirname(output_file)

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    with open(output_file, "w", encoding="utf-8") as fd:
        fd.write(json.dumps(buildcache_copies))


class CIScriptStage(enum.Enum):
    """Script stages."""

    #: Script for setting up the job
    BEFORE = "before_script"

    #: Script that runs the job
    DURING = "script"

    #: Script that runs after the job
    AFTER = "after_script"


class CIScript:
    """Job script."""

    def __init__(self, contents: List[Union[str, List[str]]]):
        """
        Instantiate the CI script

        Args:
            contents: the script's contents
        """
        self.contents = contents

    def convert(self, converter: Optional[Callable[[str], str]]) -> List[str]:
        """Return the optionally converted commands

        Args:
            converter: optional function that takes a string and returns a string
        """
        if converter and not callable(converter):
            raise ValueError(
                f"Expected {converter} to be a conversion function, not {type(converter)}."
            )

        def _noop(line: str) -> str:
            return line

        convert = converter or _noop

        script = []
        for cmd in self.contents:
            if isinstance(cmd, list):
                for subcmd in cmd:
                    script.append(convert(subcmd))
            else:
                script.append(convert(cmd))

        return script


class CIDynamicMap:
    """Dynamic mapping options."""

    def __init__(self, mapping: Dict[str, Any]):
        # Ensure additional properties readily available when needed
        self.mapping = mapping

        self.name: Optional[str] = mapping.get("name")
        self.endpoint: Optional[str] = mapping.get("endpoint")
        self.header: Dict[str, Any] = mapping.get("header", {})

        self.require: List[str] = mapping.get("require", [])
        self.allow: List[str] = mapping.get("allow", [])
        self.ignore: List[str] = mapping.get("ignore", [])

    @property
    def allowed(self) -> List[str]:
        return sorted(set(self.allow + self.require))

    @property
    def ignored(self) -> List[str]:
        return sorted(set(self.ignore))

    @property
    def required(self) -> List[str]:
        return sorted(set(self.require))

    def endpoint_url(self) -> str:
        return str(urlparse(self.endpoint))

    def request_header(self) -> Dict[str, str]:
        header = {"User-Agent": web_util.SPACK_USER_AGENT}
        header.update(self.header)

        # Expand header environment variables, ie. if tokens are passed
        for value in header.values():
            value = os.path.expandvars(value)

        return header

    def clean_config_attrs(self, query: str) -> Optional[Dict[str, Any]]:
        """Build the clean configuration attributes for the spec query.

        Args:
           query: the spec query

        Returns: resulting clean configuration attributes
        """
        request = Request(
            self.endpoint_url().replace(query=query).geturl(),
            headers=self.request_header(),
            method="GET",
        )

        try:
            response = _urlopen(request)
            config = json.load(response)
        except Exception as e:
            # For now just ignore any errors from dynamic mapping and continue
            # This is still experimental, and failures should not stop CI
            # from running normally
            tty.warn(f"Failed to fetch dynamic mapping for query:\n\t{query}: {e}")
            return None

        # Strip ignore keys
        if self.ignored:
            for key in self.ignored:
                if key in config:
                    config.pop(key)

        # Only keep allowed keys
        clean_config = {}
        if self.allowed:
            for key in self.allowed:
                if key in config:
                    clean_config[key] = config[key]
        else:
            clean_config = config

        # Verify all of the required keys are present
        if self.required:
            missing_keys = []
            for key in self.required:
                if key not in clean_config.keys():
                    missing_keys.append(key)

            if missing_keys:
                tty.warn(f"Response missing required keys: {missing_keys}")

        return clean_config

    def skip(self) -> bool:
        """Returns ``True`` if the section should be skipped; else ``False``."""
        skip_mapping = os.environ.get("SPACK_CI_SKIP_DYNAMIC_MAPPING")
        return self.name and skip_mapping and re.match(skip_mapping, self.name)


class CIJobData:
    """Job data for a given job name (and spec)."""

    def __init__(
        self,
        name: str,
        level: int = 0,
        release_spec: Optional[spack.spec.Spec] = None,
        remove: bool = False,
    ):
        """
        Args:
            name: standard job name
            release_spec: release spec
            remove: ``True`` if a remove job; otherwise, ``False``
        """
        self.name: str = name
        self.spec: Optional[spack.spec.Spec] = release_spec
        self.hash: str = release_spec.dag_hash() if release_spec else ""
        self.remove: bool = remove
        self.job_name = f"{self.name}-job{'-remove' if self.remove else ''}"

        self.tags: List[str] = []
        self.attributes: Dict[str, Union[str, int]] = {}

        self.script: Dict[CIScriptStage, CIScript] = {}
        if self.job_name in default_job_settings:
            for key, value in default_job_settings[self.job_name].items():
                try:
                    self.script[CIScriptStage(key)] = CIScript(value)
                except KeyError:
                    try:
                        setattr(self, key, value)
                    except Exception as e:
                        tty.error(f"Failed to set {key} attribute with {value}: {str(e)}")

        if release_spec:
            job_vars = {
                "SPACK_JOB_SPEC_DAG_HASH": release_spec.dag_hash(),
                "SPACK_JOB_SPEC_PKG_NAME": release_spec.name,
                "SPACK_JOB_SPEC_PKG_VERSION": release_spec.format("{version}"),
                "SPACK_JOB_SPEC_COMPILER_NAME": release_spec.format("{compiler.name}"),
                "SPACK_JOB_SPEC_COMPILER_VERSION": release_spec.format("{compiler.version}"),
                "SPACK_JOB_SPEC_ARCH": release_spec.format("{architecture}"),
                "SPACK_JOB_SPEC_VARIANTS": release_spec.format("{variants}"),
            }
            self.attributes["variables"] = job_vars

    def __str__(self) -> str:
        return f"CIJob({self.job_name}, spec={self.spec})"

    def remove_reserved_tags(self):
        for tag in SPACK_RESERVED_TAGS:
            try:
                self.tags.remove(tag)
            except ValueError:
                # value is not in the list
                pass

    def spec_query(self) -> Optional[str]:
        """Return the job's spec query."""
        if not self.spec:
            return None

        query = (
            "{SPACK_JOB_SPEC_PKG_NAME}@{SPACK_JOB_SPEC_PKG_VERSION}"
            # The preceding spaces are required (ref. https://github.com/spack/spack-gantry/blob/develop/docs/api.md#allocation)
            " {SPACK_JOB_SPEC_VARIANTS}"
            " arch={SPACK_JOB_SPEC_ARCH}"
            "%{SPACK_JOB_SPEC_COMPILER_NAME}@{SPACK_JOB_SPEC_COMPILER_VERSION}"
        ).format_map(self.attributes["variables"])
        return f"spec={quote(query)}"

    def merge_attributes(self, attrs: Dict[str, Any]):
        """Merge the attributes into those of the job

        Args:
            attrs: attributes to be removed
        """
        # TODO/TBD: Should the result be optionally or always copied?
        self.attributes = copy.copy(spack.schema.merge_yaml(self.attributes, attrs))

    def remove_attributes(self, attrs: Dict[str, Any]):
        """Remove the attributes from the job

        Args:
            attrs: attributes to be removed
        """
        self.attributes = spack.config.remove_yaml(self.attributes, attrs)

    def update_attributes(self, section: Dict[str, Any]):
        """Update the job attributes with the attribute data for the job's name.

        The attributes will be removed if this is a ``remove`` job; otherwise,
        they will be merged.

        Args:
            section: section possibly containing relevant job attributes
        """
        if self.job_name not in section:
            return

        attrs = section[self.job_name]

        if self.remove:
            self.remove_attributes(attrs)
        else:
            self.merge_attributes(attrs)

    def update_submapping_attributes(self, section: Dict[str, Any]):
        """Update attributes with relevant submapping data.

        Args:
            section: section possibly containing relevant job attributes
        """
        if "submapping" not in section or self.name not in spec_job_names:
            return

        # Assumes the attributes are job name-specific.
        matched = False
        only_first = section.get("match_behavior", "first") == "first"

        for match_attrs in reversed(section["submapping"]):
            section = cfg.InternalConfigScope._process_dict_keyname_overrides(match_attrs)
            for match_string in match_attrs["match"]:
                if _spec_matches(self.spec, match_string):
                    matched = True

                    # Assumes only update if the remove property values match
                    job_names = ["build-job", "test-job"]

                    for name in job_names:
                        section_name = f"{name}-remove" if self.remove else name
                        if section_name in match_attrs:
                            self.update_attributes(section[section_name])
                    break

            if matched and only_first:
                break

    # TODO/TLD: Fix this since removed converters
    def to_dict(self, converters: Dict[str, Callable]) -> Dict[str, Any]:
        data: Dict[str, Any] = {"spec": self.spec, "attributes": self.attributes, "scripts": []}
        # TODO/TLD: double-check this
        for stage in self.script:
            data["scripts"][str(stage)] = self.script[stage].convert(converters[stage])
        return data


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
            self.site += f" ({runner})"

    def args(self):
        return [
            "--cdash-upload-url",
            win_quote(self.upload_url),
            "--cdash-build",
            win_quote(self.build_name()),
            "--cdash-site",
            win_quote(self.site),
            "--cdash-buildstamp",
            win_quote(self.build_stamp),
        ]

    def build_name(self, spec: Optional[spack.spec.Spec] = None) -> Optional[str]:
        """Returns the CDash build name.

        A name will be generated if the ``spec`` is provided,
        otherwise, the value will be retrieved from the environment
        through the ``SPACK_CDASH_BUILD_NAME`` variable

        Returns: given spec's CDash build name
        """
        if spec:
            spec_str = spec.format("{name}{@version}{%compiler} hash={hash} arch={architecture}")
            build_name = f"{spec_str} ({self.build_group})"
            tty.debug(f"Generated CDash build name ({build_name}) from the {spec.name}")
            return build_name

        env_build_name = os.environ.get("SPACK_CDASH_BUILD_NAME")
        tty.debug(f"Using CDash build name ({env_build_name}) from the environment")
        return env_build_name

    @property  # type: ignore
    def build_stamp(self):
        """Returns the CDash build stamp.

        The one defined by SPACK_CDASH_BUILD_STAMP environment variable
        is preferred due to the representation of timestamps; otherwise,
        one will be built.

        Returns: (str) current CDash build stamp"""
        build_stamp = os.environ.get("SPACK_CDASH_BUILD_STAMP")
        if build_stamp:
            tty.debug(f"Using build stamp ({build_stamp}) from the environment")
            return build_stamp

        build_stamp = cdash_build_stamp(self.build_group, time.time())
        tty.debug(f"Generated new build stamp ({build_stamp})")
        return build_stamp

    @property  # type: ignore
    @memoized
    def project_enc(self):
        tty.debug(f"Encoding project ({type(self.project)}): {self.project})")
        encode = urlencode({"project": self.project})
        index = encode.find("=") + 1
        return encode[index:]

    @property
    def upload_url(self):
        url_format = f"{self.url}/submit.php?project={self.project_enc}"
        return url_format

    def copy_test_results(self, source, dest):
        """Copy test results to artifacts directory."""
        reports = fs.join_path(source, "*_Test*.xml")
        copy_files_to_artifacts(reports, dest)

    def create_buildgroup(self):
        """Create the CDash buildgroup if it does not already exist."""
        headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json",
        }
        data = {"newbuildgroup": self.build_group, "project": self.project, "type": "Daily"}
        enc_data = json.dumps(data).encode("utf-8")
        request = Request(f"{self.url}/api/v1/buildgroup.php", data=enc_data, headers=headers)

        response_text = None
        group_id = None

        try:
            response_text = _urlopen(request, timeout=SPACK_CDASH_TIMEOUT).read()
        except OSError as e:
            tty.warn(f"Failed to create CDash buildgroup: {e}")

        if response_text:
            try:
                response_json = json.loads(response_text)
                group_id = response_json["id"]
            except (json.JSONDecodeError, KeyError) as e:
                tty.warn(f"Failed to parse CDash response: {e}")

        if not group_id:
            tty.warn(f"Failed to create or retrieve buildgroup for {self.build_group}")

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
            build=self.build_name(),
            site=self.site,
            buildstamp=self.build_stamp,
            track=None,
        )
        reporter = CDash(configuration=configuration)
        reporter.test_skipped_report(report_dir, spec, reason)


class PipelineType(enum.Enum):
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
        buildcache_destination: spack.mirrors.mirror.Mirror,
        artifacts_root: str = "jobs_scratch_dir",
        print_summary: bool = True,
        output_file: Optional[str] = None,
        check_index_only: bool = False,
        broken_specs_url: Optional[str] = None,
        rebuild_index: bool = True,
        untouched_pruning_dependent_depth: Optional[int] = None,
        prune_untouched: bool = False,
        prune_up_to_date: bool = True,
        prune_unaffected: bool = True,
        prune_external: bool = True,
        stack_name: Optional[str] = None,
        pipeline_type: Optional[PipelineType] = None,
        require_signing: bool = False,
        cdash_handler: Optional["CDashHandler"] = None,
    ):
        """
        Args:
            env: Active spack environment
            buildcache_destination: The mirror where built binaries should be pushed
            artifacts_root: Path to location where artifacts should be stored
            print_summary: Print a summary of the scheduled pipeline
            output_file: Path where output file should be written
            check_index_only: Only fetch the index or fetch all spec files
            broken_specs_url: URL where broken specs (on develop) should be reported
            rebuild_index: Generate a job to rebuild mirror index after rebuilds
            untouched_pruning_dependent_depth: How many parents to traverse from changed pkg specs
            prune_untouched: Prune jobs for specs that were unchanged in git history
            prune_up_to_date: Prune specs from pipeline if binary exists on the mirror
            prune_external: Prune specs from pipeline if they are external
            stack_name: Name of spack stack
            pipeline_type: Type of pipeline running (optional)
            require_signing: Require buildcache to be signed (fail w/out signing key)
            cdash_handler: Object for communicating build information with CDash
        """
        self.env = env
        self.buildcache_destination = buildcache_destination
        self.artifacts_root = artifacts_root
        self.print_summary = print_summary
        self.output_file = output_file
        self.check_index_only = check_index_only
        self.broken_specs_url = broken_specs_url
        self.rebuild_index = rebuild_index
        self.untouched_pruning_dependent_depth = untouched_pruning_dependent_depth
        self.prune_untouched = prune_untouched
        self.prune_up_to_date = prune_up_to_date
        self.prune_unaffected = prune_unaffected
        self.prune_external = prune_external
        self.stack_name = stack_name
        self.pipeline_type = pipeline_type
        self.require_signing = require_signing
        self.cdash_handler = cdash_handler
        self.forward_variables: List[str] = []


class PipelineNode:
    spec: spack.spec.Spec
    parents: Set[str]
    children: Set[str]

    def __init__(self, spec: spack.spec.Spec):
        self.spec = spec
        self.parents = set()
        self.children = set()

    @property
    def key(self):
        """Return key of the stored spec"""
        return PipelineDag.key(self.spec)


class PipelineDag:
    """Turn a list of specs into a simple directed graph, that doesn't keep track
    of edge types."""

    @classmethod
    def key(cls, spec: spack.spec.Spec) -> str:
        return spec.dag_hash()

    def __init__(self, specs: List[spack.spec.Spec]) -> None:
        # Build dictionary of nodes
        self.nodes: Dict[str, PipelineNode] = {
            PipelineDag.key(s): PipelineNode(s)
            for s in traverse.traverse_nodes(specs, deptype=dt.ALL_TYPES, root=True)
        }

        # Create edges
        for edge in traverse.traverse_edges(
            specs, deptype=dt.ALL_TYPES, root=False, cover="edges"
        ):
            parent_key = PipelineDag.key(edge.parent)
            child_key = PipelineDag.key(edge.spec)

            self.nodes[parent_key].children.add(child_key)
            self.nodes[child_key].parents.add(parent_key)

    def prune(self, node_key: str):
        """Remove a node from the graph, and reconnect its parents and children"""
        node = self.nodes[node_key]
        for parent in node.parents:
            self.nodes[parent].children.remove(node_key)
            self.nodes[parent].children |= node.children
        for child in node.children:
            self.nodes[child].parents.remove(node_key)
            self.nodes[child].parents |= node.parents
        del self.nodes[node_key]

    def traverse_nodes(
        self, direction: str = "children"
    ) -> Generator[Tuple[int, PipelineNode], None, None]:
        """Yields (depth, node) from the pipeline graph.  Traversal is topologically
        ordered from the roots if ``direction`` is ``children``, or from the leaves
        if ``direction`` is ``parents``. The yielded depth is the length of the
        longest path from the starting point to the yielded node."""
        if direction == "children":
            get_in_edges = lambda node: node.parents
            get_out_edges = lambda node: node.children
        else:
            get_in_edges = lambda node: node.children
            get_out_edges = lambda node: node.parents

        sort_key = lambda k: self.nodes[k].spec.name

        out_edges = {k: sorted(get_out_edges(n), key=sort_key) for k, n in self.nodes.items()}
        num_in_edges = {k: len(get_in_edges(n)) for k, n in self.nodes.items()}

        # Populate a queue with all the nodes that have no incoming edges
        nodes = deque(
            sorted(
                [(0, key) for key in self.nodes.keys() if num_in_edges[key] == 0],
                key=lambda item: item[1],
            )
        )

        while nodes:
            # Remove the next node, n, from the queue and yield it
            depth, n_key = nodes.pop()
            yield (depth, self.nodes[n_key])

            # Remove an in-edge from every node, m, pointed to by an
            # out-edge from n.  If any of those nodes are left with
            # 0 remaining in-edges, add them to the queue.
            for m in out_edges[n_key]:
                num_in_edges[m] -= 1
                if num_in_edges[m] == 0:
                    nodes.appendleft((depth + 1, m))

    def get_dependencies(self, node: PipelineNode) -> List[PipelineNode]:
        """Returns a list of nodes corresponding to the direct dependencies
        of the given node."""
        return [self.nodes[k] for k in node.children]


class SpackCIConfig:
    """Spack CI object used to generate intermediate representation
    used by the CI generator(s).
    """

    def __init__(self, ci_config: Dict[str, Any]):
        """Given the information from the ci section of the config
        and the staged jobs, set up meta data needed for generating Spack
        CI IR.
        """
        # Retain the original ci_config for generator-specific customizations
        self.ci_config = ci_config

        self.broken_specs_url: Optional[str] = ci_config.get("broken-specs-url", None)
        self.broken_tests: List[str] = ci_config.get("broken-tests-packages", [])
        self.rebuild_index: bool = ci_config.get("rebuild-index", True)

        self.pipeline_gen: List[Dict[str, Dict]] = ci_config.get("pipeline-gen", [])

        self.add_tests = "test-job" in self.pipeline_gen

        # Prep for each possible job type
        self.jobs: Dict[str, List[CIJobData]] = {}
        for name in all_job_names:
            self.jobs[name] = []

        # Add each core job along with its defaults
        for name in core_job_names:
            tty.debug(f"TLD: SpackCIConfig: instantiating '{name}' job")
            self.jobs[name] = [CIJobData(name)]

    # Create jobs for all the pipeline specs
    def init_pipeline_jobs(self, pipeline: PipelineDag):
        names = ["build"]
        if self.add_tests:
            names.append("test")

        for level, node in pipeline.traverse_nodes():
            for i, name in enumerate(names):
                self.jobs[name].append(CIJobData(name, level + i, node.spec))

    def job(self, name: str, spec: Optional[spack.spec.Spec] = None) -> Optional[CIJobData]:
        """Retrieve the matching job

        Args:
            name: the name of the desired job
            spec: the job spec

        Returns: the job instance or ``None`` if none match
        """
        spec_hash = spec.dag_hash() if spec else ""
        for job in self.jobs[name]:
            if not spec or job.hash == spec_hash:
                return job

        return None

    def ir(self) -> Dict[str, Any]:
        """Return the intermediate representation of the Spack CI configuration."""
        intermediate_rep = {
            "broken-specs-url": self.broken_specs_url,
            "broken-tests-packages": self.broken_tests,
            "rebuild-index": self.rebuild_index,
        }

        # Include the representation of all of the jobs
        all_jobs = {}
        for job in chain(*[self.jobs[name] for name in all_job_names]):
            if job.name == "any":
                # Not expecting 'any' jobs to be stored in memory since their
                # data should've been applied to the other types of named jobs.
                tty.debug(f"Skipping adding {job} to the intermediate representation")
                continue

            # TODO/TLD: how should these really be keyed given build and
            # TODO/TLD: test jobs will now have the same spec?
            all_jobs[job.name] = job.to_dict(self.converter)
        intermediate_rep["jobs"] = all_jobs

        return intermediate_rep

    def _named_job_name(self, section: Dict[str, Any]) -> Optional[str]:
        """Determine if there is a pipeline-gen configuration section for a
        named job.

        Args:
            section: pipeline-gen configuration section

        Returns: the base job name if the section exists; otherwise ``None``
        """
        for _name in all_job_names:
            keys = [f"{_name}-job", f"{_name}-job-remove"]
            if any([key for key in keys if key in section]):
                return _name

        return None

    def update_job_attributes(self, job_name: str, section: Dict[str, Any]):
        """Update the specified job attributes for corresponding jobs

        Args:
            job_name: the job name of jobs whose attributes are to be updated
            section: attributes to be merged or removed, depending on the job
        """
        if job_name in spec_job_names:
            # Apply the same attributes to all matching jobs that can have a spec
            for job in self.jobs[job_name]:
                tty.debug(
                    f"TLD: .. {job_name}, {job.spec}, {job.remove}: applying "
                    f"'{job_name}' section to attributes"
                )
                job.update_attributes(section)
            return

        if job_name == "any":
            # Apply section attributes to all jobs
            for name, jobs in self.jobs.items():
                for job in jobs:
                    tty.debug(
                        f"TLD: .. {name}, {job.spec}, {job.remove}: applying "
                        f"'{job_name}' section to attributes"
                    )
                    job.update_attributes(section)
            return

        # Create a signing job if there is a script and the job
        # hasn't been initialized yet
        if job_name == "signing" and len(self.jobs[job_name]) == 0:
            tty.debug("TLD: .. detected signing section and none in jobs")
            if "signing-job" in section:
                if "script" not in section["signing-job"]:
                    tty.debug("TLD: .. .. skipping signing job missing script")
                    return

                self.jobs[job_name].append(CIJobData(job_name))

        # Apply attributes to any other type of named job
        tty.debug(
            f"TLD: .. applying section {section} to ({len(self.jobs[job_name])}) {job_name} job(s)"
        )
        for job in self.jobs[job_name]:
            job.update_attributes(section)

    def update_submapping_job_attributes(self, section: Dict[str, Any]):
        """Update spec job attributes with submapping data.

        Submapping attributes can be used to customize the tags and variables
        used to ensure the runner has sufficient resources for the job.

        Args:
            section: section possibly containing relevant job attributes
        """
        if "submapping" not in section:
            return

        tty.debug(f"TLD: updating 'submapping' of section '{section}'")

        # Apply section jobs with specs to match
        for job in chain(*[self.jobs[name] for name in spec_job_names]):
            tty.debug(f"TLD: .. for job {job}")
            job.update_submapping_attributes(section)

    def process_dynamic_job_mapping(self, section: Dict[str, Any]):
        """Process cost optimization options for large scale CI."""
        if "dynamic-mapping" not in section:
            return

        # Check if this section should be skipped
        mapping = CIDynamicMap(section["dynamic-mapping"])
        if mapping.skip():
            return

        # Make sure required things are not also ignored
        assert not any([ikey in mapping.required for ikey in mapping.ignored])

        for job in chain(*[self.jobs[name] for name in spec_job_names]):
            # Create request for this spec job
            query = job.spec_query()
            if not query:
                tty.warn(f"Unable to formulate a spec query for {job}")
                continue

            clean_config = mapping.clean_config_attrs(query)
            if clean_config:
                job.merge_attributes(clean_config)

    def generate_ir(self):
        """Generate the IR from the Spack CI configurations."""

        # Merge/override the default CI job configurations
        pipeline_gen = [override_job_settings] + self.ci_config.get("pipeline-gen", [])
        tty.debug("\nTLD: generate_ir: reversed(pipeline_gen):")
        for section in reversed(pipeline_gen):
            tty.debug(f"TLD: .. {section}")
        tty.debug()

        for section in reversed(pipeline_gen):
            tty.debug(f"TLD: generate_ir: processing (reversed) section {section}")
            section = cfg.InternalConfigScope._process_dict_keyname_overrides(section)
            tty.debug(f"TLD: .. new section: {section}")

            job_name = self._named_job_name(section)
            if job_name:
                self.update_job_attributes(job_name, section)
                continue

            if "submapping" in section:
                self.update_submapping_job_attributes(section)
                continue

            if "dynamic-mapping" in section:
                self.process_dynamic_job_mapping(section)

        # Replace the job's spec with the spec's name
        for job in chain(*[self.jobs[name] for name in spec_job_names]):
            job.spec = job.spec.name

        return self.ir()


class SpackCIError(spack.error.SpackError):
    def __init__(self, msg):
        super().__init__(msg)
