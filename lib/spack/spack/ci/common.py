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
from collections import OrderedDict, deque
from typing import Any, Callable, Dict, Generator, List, Optional, Set, Tuple
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

#: Names of all possible jobs, which include those involving specs
all_job_names = ["any", "build", "test"] + core_job_names

#: default job settings
default_job_settings = {
    "build-job": {
        "script": ["cd {env_dir}", "spack env activate --without-view .", "spack ci rebuild"]
    },
    "noop-job": {"script": ['echo "All specs already up-to-date, nothing to rebuild."']},
    "test-job": {
        "script": [
            "cd {env_dir}",
            "spack env activate --without-view .",
            "spack ci rebuild --tests",
        ]
    },
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
        raise OSError("No such file or directory: '{0}'".format(glob_or_path), errno.ENOENT)
    if len(files) > 1 and not os.path.isdir(dest):
        raise ValueError(
            "'{0}' matches multiple files but '{1}' is not a directory".format(glob_or_path, dest)
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


class CIImage:
    """CI Image."""

    def __init__(self, image_config):
        if isinstance(image_config, str):
            self.value = image_config
            self.name = None
            self.entrypoint = None
            return

        self.value = None
        self.name = image_config.get("name", None)
        self.entrypoint = image_config.get("entrypoint", [])

    def to_dict(self) -> Dict[str, Any]:
        if self.value:
            return {"image": self.value}

        base = {"image": {}}
        if self.name:
            base["name"] = self.name

        if self.entrypoint:
            base["entrypoint"] = self.entrypoint
        return base

    def to_yaml(self, stream=None):
        return syaml.dump(self.to_dict(), stream=stream)


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

    # TODO/TLD: when/how do we determine the override option is being used?
    def __init__(self, contents: List[Union[str, List[str]]], override: bool = False):
        """
        Instantiate the CI script

        Args:
            contents: the script's contents
            override: ``True`` if the contents should override all others;
                otherwise ``False``
        """
        self.contents = contents
        self.override = override

    def convert(self, converter: Optional[Callable[str], str]) -> List[str]:
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

        if converter is None:
            converter = _noop

        script = []
        for cmd in self.contents:
            if isinstance(cmd, list):
                for subcmd in cmd:
                    script.append(converter(subcmd))
            else:
                script.append(converter(cmd))

        return script


class CIJobData:
    """Job data for a given job name (and spec)."""

    def __init__(
        self, name: str, release_spec: Optional[spack.spec.Spec] = None, remove: bool = False
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

        self.image: Optional[CIImage] = None
        self.tags: List[str] = []
        self.attributes: Dict[str, Union[str, int]] = {}
        self.script: Dict[CIScriptStage, CIScript] = {}

        if self.job_name in default_job_settings:
            for key, value in default_job_settings[self.job_name].items():
                try:
                    self.script[CIScriptStage(key)] = CIScript(value)
                except KeyError:
                    setattr(self, key, value)

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

    def update_attributes(self, section: Dict[str, Any]):
        """Update the job attributes with the corresponding section data.

        Args:
            base_job_name: standard job name
        """
        if self.job_name not in section:
            return

        src = section[job_name]
        if self.remove:
            self.attributes = spack.config.remove_yaml(self.attributes, src)
        else:
            self.attributes = copy.copy(spack.schema.merge_yaml(self.attributes, src))

    # TODO/TLD: Resume here ..
    def update_submapping_attributes(self, section: Dict[str, any]):
        """Update attributes with relevant submapping data."""
        if "submapping" not in section:
            return

        matched = False
        only_first = section.get("match_behavior", "first") == "first"

        for match_attrs in reversed(section["submapping"]):
            attrs = cfg.InternalConfigScope._process_dict_keyname_overrides(match_attrs)
            for match_string in match_attrs["match"]:
                if _spec_matches(self.spec, match_string):
                    matched = True
                    # TODO/TLD: Shouldn't this only be applied if the job
                    # TODO/TLD:  has the proper job name?
                    if "build-job-remove" in match_attrs:
                        self.attributes = spack.config.remove_yaml(
                            self.attributes, attrs["build-job-remove"]
                        )
                    if "build-job" in match_attrs:
                        self.attributes = spack.schema.merge_yaml(
                            self.attributes, attrs["build-job"]
                        )
                    break
            if matched and only_first:
                break

    def converted_script(
        self, stage: CIScriptStage, converter: Optional[Callable[str], str]
    ) -> List[str]:
        """Return the converted script contents.

        Args:
            stage: the script for the provided stage
            converter:

        Returns: converted script or an empty list if there isn't one
        """
        script = self.script[stage] if stage in self.script else None
        if not script:
            return []

        return self.script[stage].convert(converter)

    def to_dict(self) -> Dict[str, Any]:
        # TODO/TLD: return the dict representation  .. only just attributes?
        data = {}


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
        through the ``SPACK_CDASH_BUILD_NAME`` variable.

        Returns: (str) given spec's CDash build name."""
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
        add_test_jobs: bool = False,
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
        self.ci_config = ci_config

        self.broken_specs_url: Optional[str] = ci_config.get("broken-specs-url", None)
        self.broken_tests: List[str] = ci_config.get("broken-tests-packages", [])
        self.rebuild_index: bool = ci_config.get("rebuild-index", True)

        self.pipeline_gen: List[Dict[str, Dict]] = ci_config.get("pipeline-gen", [])

        # TODO: Move this to GitlabConfig?
        #: Callable methods that perform variable substitutions on script lines
        self.converter: Dict[CIScriptStage, Callable] = {}

        # Prep for each possible job type
        self.jobs: Dict[str, List[CIJobData]] = {}
        for name in all_job_names:
            self.jobs[name] = []

        # Add each core job along with its defaults
        for name in core_job_names:
            print(f"TLD: SpackCIConfig: instantiating '{name}' job")
            self.jobs[name] = [CIJobData(name)]

    # Create jobs for all the pipeline specs
    def init_pipeline_jobs(self, pipeline: PipelineDag, tests: Optional[bool] = False):
        names = ["build"]
        if tests:
            names.append("test")

        for _, node in pipeline.traverse_nodes():
            for name in names:
                self.jobs[name].append(CIJobData(name, node.spec))

    # TLD/TODO: Resume here

    def register_script_converter(self, stage: CIScriptStage, op: Callable):
        """Register the function that takes and string and substitutes values.

        Args:
            stage: the stage of the scripts to be converted
            op: the method to be used to format referenced variables
        """
        self.converter[stage] = op

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

        # Include the represenation of all of the jobs
        all_jobs = {}
        for name, jobs in self.jobs.items():
            for job in jobs:
                all_jobs.update(job.to_dict())
        intermediate_rep["jobs"] = all_jobs

        return intermediate_rep

    def __is_named(self, section):
        """Check if a pipeline-gen configuration section is for a named job,
        and if so return the name otherwise return none.
        """
        for _name in all_job_names:
            keys = [f"{_name}-job", f"{_name}-job-remove"]
            if any([key for key in keys if key in section]):
                return _name

        return None

    def update_job_attributes(self, job_name: str, section: Dict[str, any]):
        """Update job attributes using the corresponding job data.

        Args:
            job_name: section job name
            section: job attribute updates
        """
        if job_name in ["build", "test"]:
            # TODO/TLD: Should we be checking for build-remove and
            # TODO/TLD:   test-remove jobs and adding them here with the
            # TODO/TLD:   attributes? OR do we assume we only update
            # TODO/TLD:   when added?
            # TODO/TLD: Is it even possible for a build or test job to NOT
            # TODO/TLD:   have a spec? IF it is, then that needs to be check
            # TODO/TLD:   here

            # Apply the same attributes to all build and test jobs
            for job in self.jobs[job_name]:
                print(
                    f"TLD: .. {job_name}, {job.spec}, {job.remove}: applying '{job_name}' section to attributes"
                )
                job.update_attributes(section)
            return

        if job_name == "any":
            # Apply section attributes too all jobs
            for name, jobs in self.jobs.items():
                for job in jobs:
                    print(
                        f"TLD: .. {name}, {job.spec}, {job.remove}: applying '{job_name}' section to attributes"
                    )
                    job.update_attributes(section)
            return

        # Create a signing job if there is a script and the job
        # hasn't been initialized yet
        if job_name == "signing" and len(self.jobs[job_name]) == 0:
            print(f"TLD: .. detected signing section and none in jobs")
            if "signing-job" in section:
                if "script" not in section["signing-job"]:
                    print(f"TLD: .. .. skipping signing job missing script")
                    continue

                self.jobs[job_name].append(CIJobData(job_name))

        # Apply attributes to any other type of named job
        print(
            f"TLD: .. applying section {section} to ({len(self.jobs[job_name])}) {job_name} job(s)"
        )
        for job in self.jobs[job_name]:
            job.update_attributes(section)

    def generate_ir(self):
        """Generate the IR from the Spack CI configurations."""

        # TODO/TLD: Resume here with determining how to process the information
        # TODO/TLD: o why reverse the configuration?
        # TODO/TLD: o Is there anything special in ir processing wrt affect
        # TODO/TLD:   on ordering of the CI jobs output in the IR?

        # TODO/TLD: defaults will be in the job instance already
        # TODO/TLD: so the goal would be to apply pipeline-gen options THEN
        # TODO/TLD: .. any overrides
        # TODO/TLD:
        # TODO/TLD: .. should overrides be in list form?
        pipeline_gen = overrides + self.ci_config.get("pipeline-gen", [])
        print(f"\nTLD: generate_ir: reversed(pipeline_gen):")
        for section in reversed(pipeline_gen):
            print(f"TLD: .. {section}")
        print()

        for section in reversed(pipeline_gen):
            print(f"TLD: generate_ir: processing (reversed) section {section}")
            section = cfg.InternalConfigScope._process_dict_keyname_overrides(section)
            print(f"TLD: .. new section: {section}")

            job_name = self.__is_named(section)
            if job_name:
                self.update_job_attributes(job_name, section)
                continue

            # TLD/TODO: Resume here .. make sure submapping is "right"
            if "submapping" in section:
                # Apply section jobs with specs to match
                for name, jobs in self.jobs.items():
                    for job in jobs:
                        if job.spec:
                            job.update_submapping_attributes(section)
                continue

            if "dynamic-mapping" in section:
                mapping = section["dynamic-mapping"]

                dynmap_name = mapping.get("name")

                # Check if this section should be skipped
                dynmap_skip = os.environ.get("SPACK_CI_SKIP_DYNAMIC_MAPPING")
                if dynmap_name and dynmap_skip:
                    if re.match(dynmap_skip, dynmap_name):
                        continue

                # Get the endpoint
                endpoint = mapping["endpoint"]
                endpoint_url = urlparse(endpoint)

                # Configure the request header
                header = {"User-Agent": web_util.SPACK_USER_AGENT}
                header.update(mapping.get("header", {}))

                # Expand header environment variables
                # ie. if tokens are passed
                for value in header.values():
                    value = os.path.expandvars(value)

                required = mapping.get("require", [])
                allowed = mapping.get("allow", [])
                ignored = mapping.get("ignore", [])

                # required keys are implicitly allowed
                allowed = sorted(set(allowed + required))
                ignored = sorted(set(ignored))
                required = sorted(set(required))

                # Make sure required things are not also ignored
                assert not any([ikey in required for ikey in ignored])

                def job_query(job):
                    job_vars = job["attributes"]["variables"]
                    query = (
                        "{SPACK_JOB_SPEC_PKG_NAME}@{SPACK_JOB_SPEC_PKG_VERSION}"
                        # The preceding spaces are required (ref. https://github.com/spack/spack-gantry/blob/develop/docs/api.md#allocation)
                        " {SPACK_JOB_SPEC_VARIANTS}"
                        " arch={SPACK_JOB_SPEC_ARCH}"
                        "%{SPACK_JOB_SPEC_COMPILER_NAME}@{SPACK_JOB_SPEC_COMPILER_VERSION}"
                    ).format_map(job_vars)
                    return f"spec={quote(query)}"

                for job in jobs.values():
                    if not job["spec"]:
                        continue

                    # Create request for this job
                    query = job_query(job)
                    request = Request(
                        endpoint_url._replace(query=query).geturl(), headers=header, method="GET"
                    )
                    try:
                        response = _urlopen(request)
                        config = json.load(response)
                    except Exception as e:
                        # For now just ignore any errors from dynamic mapping and continue
                        # This is still experimental, and failures should not stop CI
                        # from running normally
                        tty.warn(f"Failed to fetch dynamic mapping for query:\n\t{query}: {e}")
                        continue

                    # Strip ignore keys
                    if ignored:
                        for key in ignored:
                            if key in config:
                                config.pop(key)

                    # Only keep allowed keys
                    clean_config = {}
                    if allowed:
                        for key in allowed:
                            if key in config:
                                clean_config[key] = config[key]
                    else:
                        clean_config = config

                    # Verify all of the required keys are present
                    if required:
                        missing_keys = []
                        for key in required:
                            if key not in clean_config.keys():
                                missing_keys.append(key)

                        if missing_keys:
                            tty.warn(f"Response missing required keys: {missing_keys}")

                    if clean_config:
                        job["attributes"] = spack.schema.merge_yaml(
                            job.get("attributes", {}), clean_config
                        )

        for _, job in jobs.items():
            if job["spec"]:
                job["spec"] = job["spec"].name

        return self.ir


class SpackCIError(spack.error.SpackError):
    def __init__(self, msg):
        super().__init__(msg)
