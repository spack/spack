# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack
import spack.binary_distribution as bindist
import spack.ci
import spack.cmd
import spack.main
import spack.mirror
import spack.paths
import spack.repo


def generate_snakefile(env, print_summary, output_file):

    with spack.concretize.disable_compiler_existence_check():
        with env.write_transaction():
            env.concretize()
            env.write()

    phases = []
    phases.append({
        'name': 'specs',
        'strip-compilers': False,
    })

    # Speed up staging by first fetching binary indices from all mirrors
    # (including the per-PR mirror we may have just added above).
    bindist.binary_index.update()

    staged_phases = {}
    for phase in phases:
        phase_name = phase['name']
        with spack.concretize.disable_compiler_existence_check():
            staged_phases[phase_name] = spack.ci.stage_spec_jobs(
                env.spec_lists[phase_name],
                check_index_only=True)

    # There should only be one phase for now, so one snakefile
    for phase in phases:
        phase_name = phase['name']

        # We care about dependencies
        spec_labels, dependencies, stages = staged_phases[phase_name]

        # This will be the spec for the very last spec to be installed
        last_spec = [spec_labels[x] for x in stages[-1]][-1]
        last_spec['spec'].concretize()

        # The "final" output file is the last log of the last install
        snakefile = '''rule all:
    input:
        "%s"\n''' % last_spec['spec'].package.times_log_path

        seen_rules = set()

        # First generate rules for specs that don't have any deps
        for key, value in spec_labels.items():
            rule_name = key.replace("/", "_").replace('-', "_")
            if len(value['spec'].dependencies()) != 0:
                continue
            spec_labels[key]['spec'].concretize()
            output = spec_labels[key]['spec'].package.times_log_path
            snakefile += '''\nrule %s:
    output:
        "%s"
    shell:
        "spack install %s"\n''' % (rule_name, output, spec_labels[key]['spec'])
            seen_rules.add(rule_name)

        # Now for each set of package and dependencies, create a step
        for pkg, deps in dependencies.items():
            rule_name = pkg.replace("/", "_").replace('-', "_")
            if rule_name in seen_rules:
                continue
            seen_rules.add(rule_name)

            # Inputs are the dependency log files, which must exist
            inputs = []
            for dep in deps:
                spec_labels[dep]['spec'].concretize()
                inputs.append(spec_labels[dep]['spec'].package.times_log_path)
            inputs = "\n".join(['        "%s",' % ip for ip in inputs]).strip(",")

            # Outputs are the build log of the package
            spec_labels[pkg]['spec'].concretize()
            output = spec_labels[pkg]['spec'].package.times_log_path
            snakefile += '''\nrule %s:
    input:
%s
    output:
        "%s"
    shell:
        "spack install %s"\n''' % (rule_name, inputs, output, spec_labels[pkg]['spec'])

    # snakemake --cores <N>
    with open(output_file, 'w') as outf:
        outf.write(snakefile)
