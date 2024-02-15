# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import shutil
from typing import Dict, List, Optional, TextIO

import spack
import spack.config as cfg

from ..common import PipelineDag, PipelineOptions, PruningResults, SpackCI, update_env_scopes
from . import generator


def expand_vars(s: str, vars: Dict[str, str]):
    for key, val in vars.items():
        s = s.replace(f"${{{key}}}", val)
        s = s.replace(f"${key}", val)
    return s


class SnakeRule:
    name: Optional[str]
    inputs: List[str]
    outputs: List[str]
    shell: List[str]

    def __init__(self, name: Optional[str] = None):
        self.name = name
        self.inputs = []
        self.outputs = []
        self.shell = []

    def format_list(self, title: str, items: List[str], writer: TextIO):
        if items:
            last_item = len(items) - 1
            writer.write(f"    {title}:\n")
            for idx, next_item in enumerate(items):
                comma = "" if idx == last_item else ","
                writer.write(f'        "{next_item}"{comma}\n')

    def write(self, writer: TextIO):
        writer.write("rule")
        if self.name:
            writer.write(f" {self.name}")
        writer.write(":\n")
        self.format_list("input", self.inputs, writer)
        self.format_list("output", self.outputs, writer)
        if self.shell:
            writer.write("    shell:\n")
            writer.write('        """\n')
            for next_line in self.shell:
                writer.write(f"        {next_line}\n")
            writer.write('        """\n')

        writer.write("\n")

    def expand_all(self, vars: Dict[str, str]):
        for idx, next_input in enumerate(self.inputs):
            self.inputs[idx] = expand_vars(next_input, vars)

        for idx, next_output in enumerate(self.outputs):
            self.outputs[idx] = expand_vars(next_output, vars)

        for idx, next_line in enumerate(self.shell):
            self.shell[idx] = expand_vars(next_line, vars)


@generator("snakemake")
def generate_snakefile(
    pipeline: PipelineDag,
    spack_ci: SpackCI,
    options: PipelineOptions,
    pruning_results: PruningResults,
):
    """Given a pipeline graph, job attributes, and pipeline options,
    write a Snakefile that can be run by snakemake.

    Arguments:
        pipeline (spack.ci.common.PipelineDag): An already pruned graph of jobs representing all
            the specs to build
        spack_ci (spack.ci.common.SpackCI): An object containing the configured attributes of
            all jobs in the pipeline
        options (spack.ci.common.PipelineOptions): An object containing all the pipeline
            options gathered from yaml, env, etc...
        prunning_results (spack.ci.common.PruningResults): Contains filter results and
            descriptions for all specs in the environment.
    """
    artifacts_root = options.artifacts_root
    output_file = options.output_file
    if not output_file:
        output_file = os.path.abspath("Snakefile")
    else:
        output_file_path = os.path.abspath(output_file)
        gen_ci_dir = os.path.dirname(output_file_path)
        if not os.path.exists(gen_ci_dir):
            os.makedirs(gen_ci_dir)
    snakemake_context_dir = os.path.dirname(output_file)
    if artifacts_root.startswith(snakemake_context_dir):
        artifacts_root = os.path.relpath(artifacts_root, snakemake_context_dir)
    pipeline_artifacts_dir = os.path.join(snakemake_context_dir, artifacts_root)

    concrete_env_dir = os.path.join(pipeline_artifacts_dir, "concrete_environment")

    # Now that we've added the mirrors we know about, they should be properly
    # reflected in the environment manifest file, so copy that into the
    # concrete environment directory, along with the spack.lock file.
    if not os.path.exists(concrete_env_dir):
        os.makedirs(concrete_env_dir)
    shutil.copyfile(options.env.manifest_path, os.path.join(concrete_env_dir, "spack.yaml"))
    shutil.copyfile(options.env.lock_path, os.path.join(concrete_env_dir, "spack.lock"))

    update_env_scopes(
        options.env,
        [
            os.path.relpath(s.path, concrete_env_dir)
            for s in cfg.scopes().values()
            if isinstance(s, cfg.ImmutableConfigScope) and os.path.exists(s.path)
        ],
        os.path.join(concrete_env_dir, "spack.yaml"),
    )

    job_log_dir = os.path.join(pipeline_artifacts_dir, "logs")
    job_repro_dir = os.path.join(pipeline_artifacts_dir, "reproduction")
    job_test_dir = os.path.join(pipeline_artifacts_dir, "tests")

    rel_concrete_env_dir = os.path.relpath(concrete_env_dir, snakemake_context_dir)
    rel_job_log_dir = os.path.relpath(job_log_dir, snakemake_context_dir)
    rel_job_repro_dir = os.path.relpath(job_repro_dir, snakemake_context_dir)
    rel_job_test_dir = os.path.relpath(job_test_dir, snakemake_context_dir)

    spack_version = spack.main.get_version()
    version_to_clone = spack.main.get_spack_commit() or f"v{spack.spack_version}"
    rebuild_everything = not options.prune_up_to_date and not options.prune_untouched

    env_vars = {
        "SPACK_ARTIFACTS_ROOT": artifacts_root,
        "SPACK_CONCRETE_ENV_DIR": rel_concrete_env_dir,
        "SPACK_VERSION": spack_version,
        "SPACK_CHECKOUT_VERSION": version_to_clone,
        "SPACK_JOB_LOG_DIR": rel_job_log_dir,
        "SPACK_JOB_REPRO_DIR": rel_job_repro_dir,
        "SPACK_JOB_TEST_DIR": rel_job_test_dir,
        "SPACK_PIPELINE_TYPE": options.pipeline_type.name if options.pipeline_type else "None",
        "SPACK_CI_STACK_NAME": os.environ.get("SPACK_CI_STACK_NAME", "None"),
        "SPACK_REBUILD_CHECK_UP_TO_DATE": str(options.prune_up_to_date),
        "SPACK_REBUILD_EVERYTHING": str(rebuild_everything),
        "SPACK_REQUIRE_SIGNING": str(options.require_signing),
    }

    spack_ci_ir = spack_ci.generate_ir()
    rules: List[SnakeRule] = []

    for level, (spec_label, node) in pipeline.traverse():
        job_spec = node.spec
        job_spec_hash = job_spec.dag_hash()

        env_vars.update(
            {
                "SPACK_JOB_SPEC_DAG_HASH": job_spec_hash,
                "SPACK_JOB_SPEC_PKG_NAME": job_spec.name,
                "SPACK_JOB_SPEC_PKG_VERSION": job_spec.format("{version}"),
                "SPACK_JOB_SPEC_COMPILER_NAME": job_spec.format("{compiler.name}"),
                "SPACK_JOB_SPEC_COMPILER_VERSION": job_spec.format("{compiler.version}"),
                "SPACK_JOB_SPEC_ARCH": job_spec.format("{architecture}"),
                "SPACK_JOB_SPEC_VARIANTS": job_spec.format("{variants}"),
            }
        )

        rule = SnakeRule()

        job_object = spack_ci_ir["jobs"][job_spec_hash]["attributes"]

        # TODO: fix output paths (possibly with os.path.relpath)
        rule.outputs.append(
            os.path.relpath(f"{job_spec.prefix}/.spack/spec.json", snakemake_context_dir)
        )

        for dep in pipeline.get_dependencies(node):
            # TODO: fix input paths (possibly with os.path.relpath)
            rule.inputs.append(
                os.path.relpath(f"{dep.prefix}/.spack/spec.json", snakemake_context_dir)
            )

        # TODO: replace {env_dir} and {spec_hash} w/ appropriate values
        rule.shell = job_object["script"]

        rule.expand_all(env_vars)

        rules.append(rule)

    all_rule: SnakeRule = SnakeRule("all")
    concrete_env_roots = [
        concrete
        for abstract, concrete in options.env.concretized_specs()
        if abstract in options.env.spec_lists["specs"]
    ]
    for root in concrete_env_roots:
        # TODO: fix input paths (possibly with os.path.relpath)
        all_rule.inputs.append(
            os.path.relpath(f"{root.prefix}/.spack/spec.json", snakemake_context_dir)
        )

    rules.append(all_rule)

    with open(output_file, "wt") as f:
        for rule in rules:
            rule.write(f)
