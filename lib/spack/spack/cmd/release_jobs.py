# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import json
import os
import shutil
import tempfile

import subprocess
from jsonschema import validate, ValidationError
from six import iteritems

import llnl.util.tty as tty

from spack.architecture import sys_type
from spack.dependency import all_deptypes
from spack.spec import Spec, CompilerSpec
from spack.paths import spack_root
from spack.error import SpackError
from spack.schema.os_container_mapping import schema as mapping_schema
from spack.schema.specs_deps import schema as specs_deps_schema
from spack.spec_set import CombinatorialSpecSet
import spack.util.spack_yaml as syaml

description = "generate release build set as .gitlab-ci.yml"
section = "build"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        '-s', '--spec-set', default=None,
        help="path to release spec-set yaml file")

    subparser.add_argument(
        '-m', '--mirror-url', default=None,
        help="url of binary mirror where builds should be pushed")

    subparser.add_argument(
        '-o', '--output-file', default=".gitlab-ci.yml",
        help="path to output file to write")

    subparser.add_argument(
        '-t', '--shared-runner-tag', default=None,
        help="tag to add to jobs for shared runner selection")

    subparser.add_argument(
        '-k', '--signing-key', default=None,
        help="hash of gpg key to use for package signing")

    subparser.add_argument(
        '-c', '--cdash-url', default='https://cdash.spack.io',
        help="Base url of CDash instance jobs should communicate with")

    subparser.add_argument(
        '-p', '--print-summary', action='store_true', default=False,
        help="Print summary of staged jobs to standard output")

    subparser.add_argument(
        '--resolve-deps-locally', action='store_true', default=False,
        help="Use only the current machine to concretize specs, " +
        "instead of iterating over items in os-container-mapping.yaml " +
        "and using docker run.  Assumes the current machine architecure " +
        "is listed in the os-container-mapping.yaml config file.")

    subparser.add_argument(
        '--specs-deps-output', default='/dev/stdout',
        help="A file path to which spec deps should be written.  This " +
             "argument is generally for internal use, and should not be " +
             "provided by end-users under normal conditions.")

    subparser.add_argument(
        'specs', nargs=argparse.REMAINDER,
        help="These positional arguments are generally for internal use.  " +
             "The --spec-set argument should be used to identify a yaml " +
             "file describing the set of release specs to include in the " +
             ".gitlab-ci.yml file.")


def get_job_name(spec, osarch):
    return '{0} {1} {2} {3}'.format(spec.name, spec.version,
                                    spec.compiler, osarch)


def get_spec_string(spec):
    format_elements = [
        '${package}@${version}',
        '%${compilername}@${compilerversion}',
    ]

    if spec.architecture:
        format_elements.append(' arch=${architecture}')

    return spec.format(''.join(format_elements))


def spec_deps_key_label(s):
    return s.dag_hash(), "%s/%s" % (s.name, s.dag_hash(7))


def _add_dependency(spec_label, dep_label, deps):
    if spec_label == dep_label:
        return
    if spec_label not in deps:
        deps[spec_label] = set()
    deps[spec_label].add(dep_label)


def get_deps_using_container(specs, image):
    image_home_dir = '/home/spackuser'
    repo_mount_location = '{0}/spack'.format(image_home_dir)
    temp_dir = tempfile.mkdtemp(dir='/tmp')

    # The paths this module will see (from outside the container)
    temp_file = os.path.join(temp_dir, 'spec_deps.json')
    temp_err = os.path.join(temp_dir, 'std_err.log')

    # The paths the bash_command will see inside the container
    json_output = '/work/spec_deps.json'
    std_error = '/work/std_err.log'

    specs_arg = ' '.join([str(spec) for spec in specs])

    bash_command = " ".join(["source {0}/share/spack/setup-env.sh ;",
                             "spack release-jobs",
                             "--specs-deps-output {1}",
                             "{2}",
                             "2> {3}"]).format(
        repo_mount_location, json_output, specs_arg, std_error)

    docker_cmd_to_run = [
        'docker', 'run', '--rm',
        '-v', '{0}:{1}'.format(spack_root, repo_mount_location),
        '-v', '{0}:{1}'.format(temp_dir, '/work'),
        '--entrypoint', 'bash',
        '-t', str(image),
        '-c',
        bash_command,
    ]

    tty.debug('Running subprocess command:')
    tty.debug(' '.join(docker_cmd_to_run))

    # Docker is going to merge the stdout/stderr from the script and write it
    # all to the stdout of the running container.  For this reason, we won't
    # pipe any stdout/stderr from the docker command, but rather write the
    # output we care about to a file in a mounted directory.  Similarly, any
    # errors from running the spack command inside the container are redirected
    # to another file in the mounted directory.
    proc = subprocess.Popen(docker_cmd_to_run)
    proc.wait()

    # Check for errors from spack command
    if os.path.exists(temp_err) and os.path.getsize(temp_err) > 0:
        # Spack wrote something to stderr inside the container.  We will
        # print out whatever it is, but attempt to carry on with the process.
        tty.error('Encountered spack error running command in container:')
        with open(temp_err, 'r') as err:
            tty.error(err.read())

    spec_deps_obj = {}

    try:
        # Finally, try to read/parse the output we really care about: the
        # specs and dependency edges for the provided spec, as it was
        # concretized in the appropriate container.
        with open(temp_file, 'r') as fd:
            spec_deps_obj = json.loads(fd.read())

    except ValueError as val_err:
        tty.error('Failed to read json object from spec-deps output file:')
        tty.error(str(val_err))
    except IOError as io_err:
        tty.error('Problem reading from spec-deps json output file:')
        tty.error(str(io_err))
    finally:
        shutil.rmtree(temp_dir)

    return spec_deps_obj


def get_spec_dependencies(specs, deps, spec_labels, image=None):
    if image:
        spec_deps_obj = get_deps_using_container(specs, image)
    else:
        spec_deps_obj = compute_spec_deps(specs)

    try:
        validate(spec_deps_obj, specs_deps_schema)
    except ValidationError as val_err:
        tty.error('Ill-formed specs dependencies JSON object')
        tty.error(spec_deps_obj)
        tty.debug(val_err)
        return

    if spec_deps_obj:
        dependencies = spec_deps_obj['dependencies']
        specs = spec_deps_obj['specs']

        for entry in specs:
            spec_labels[entry['label']] = {
                'spec': Spec(entry['spec']),
                'rootSpec': entry['root_spec'],
            }

        for entry in dependencies:
            _add_dependency(entry['spec'], entry['depends'], deps)


def stage_spec_jobs(spec_set, containers, current_system=None):
    """Take a set of release specs along with a dictionary describing the
        available docker containers and what compilers they have, and generate
        a list of "stages", where the jobs in any stage are dependent only on
        jobs in previous stages.  This allows us to maximize build parallelism
        within the gitlab-ci framework.

    Arguments:
        spec_set (CombinatorialSpecSet): Iterable containing all the specs
            to build.
        containers (dict): Describes the docker containers available to use
            for concretizing specs (and also for the gitlab runners to use
            for building packages).  The schema can be found at
            "lib/spack/spack/schema/os_container_mapping.py"
        current_system (string): If provided, this indicates not to use the
            containers for concretizing the release specs, but rather just
            assume the current system is in the "containers" dictionary.  A
            SpackError will be raised if the current system is not in that
            dictionary.

    Returns: A tuple of information objects describing the specs, dependencies
        and stages:

        spec_labels: A dictionary mapping the spec labels which are made of
            (pkg-name/hash-prefix), to objects containing "rootSpec" and "spec"
            keys.  The root spec is the spec of which this spec is a dependency
            and the spec is the formatted spec string for this spec.

        deps: A dictionary where the keys should also have appeared as keys in
            the spec_labels dictionary, and the values are the set of
            dependencies for that spec.

        stages: An ordered list of sets, each of which contains all the jobs to
            built in that stage.  The jobs are expressed in the same format as
            the keys in the spec_labels and deps objects.

    """

    # The convenience method below, "remove_satisfied_deps()", does not modify
    # the "deps" parameter.  Instead, it returns a new dictionary where only
    # dependencies which have not yet been satisfied are included in the
    # return value.
    def remove_satisfied_deps(deps, satisfied_list):
        new_deps = {}

        for key, value in iteritems(deps):
            new_value = set([v for v in value if v not in satisfied_list])
            if new_value:
                new_deps[key] = new_value

        return new_deps

    deps = {}
    spec_labels = {}

    if current_system:
        if current_system not in containers:
            error_msg = ' '.join(['Current system ({0}) does not appear in',
                                  'os_container_mapping.yaml, ignoring',
                                  'request']).format(
                current_system)
            raise SpackError(error_msg)
        os_names = [current_system]
    else:
        os_names = [name for name in containers]

    container_specs = {}
    for name in os_names:
        container_specs[name] = {'image': None, 'specs': []}

    # Collect together all the specs that should be concretized in each
    # container so they can all be done at once, avoiding the need to
    # run the docker container for each spec separately.
    for spec in spec_set:
        for osname in os_names:
            container_info = containers[osname]
            image = None if current_system else container_info['image']
            if image:
                container_specs[osname]['image'] = image
            if 'compilers' in container_info:
                found_at_least_one = False
                for item in container_info['compilers']:
                    container_compiler_spec = CompilerSpec(item['name'])
                    if spec.compiler == container_compiler_spec:
                        container_specs[osname]['specs'].append(spec)
                        found_at_least_one = True
                if not found_at_least_one:
                    tty.warn('No compiler in {0} satisfied {1}'.format(
                        osname, spec.compiler))

    for osname in container_specs:
        if container_specs[osname]['specs']:
            image = container_specs[osname]['image']
            specs = container_specs[osname]['specs']
            get_spec_dependencies(specs, deps, spec_labels, image)

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
        dependencies = remove_satisfied_deps(dependencies, next_stage)

    if unstaged:
        stages.append(unstaged.copy())

    return spec_labels, deps, stages


def print_staging_summary(spec_labels, dependencies, stages):
    if not stages:
        return

    tty.msg('Staging summary:')
    stage_index = 0
    for stage in stages:
        tty.msg('  stage {0} ({1} jobs):'.format(stage_index, len(stage)))

        for job in sorted(stage):
            s = spec_labels[job]['spec']
            tty.msg('    {0} -> {1}'.format(job, get_spec_string(s)))

        stage_index += 1


def compute_spec_deps(spec_list, stream_like=None):
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
                 "root_spec": "readline@7.0%clang@9.1.0-apple arch=darwin-...",
                 "spec": "readline@7.0%clang@9.1.0-apple arch=darwin-highs...",
                 "label": "readline/ip6aiun"
               },
               {
                 "root_spec": "readline@7.0%clang@9.1.0-apple arch=darwin-...",
                 "spec": "ncurses@6.1%clang@9.1.0-apple arch=darwin-highsi...",
                 "label": "ncurses/y43rifz"
               },
               {
                 "root_spec": "readline@7.0%clang@9.1.0-apple arch=darwin-...",
                 "spec": "pkgconf@1.5.4%clang@9.1.0-apple arch=darwin-high...",
                 "label": "pkgconf/eg355zb"
               }
           ]
       }

    The object can be optionally written out to some stream.  This is
    useful, for example, when we need to concretize and generate the
    dependencies of a spec in a specific docker container.

    """
    deptype = all_deptypes
    spec_labels = {}

    specs = []
    dependencies = []

    def append_dep(s, d):
        dependencies.append({
            'spec': s,
            'depends': d,
        })

    for spec in spec_list:
        spec.concretize()

        root_spec = get_spec_string(spec)

        rkey, rlabel = spec_deps_key_label(spec)

        for s in spec.traverse(deptype=deptype):
            skey, slabel = spec_deps_key_label(s)
            spec_labels[slabel] = {
                'spec': get_spec_string(s),
                'root': root_spec,
            }
            append_dep(rlabel, slabel)

            for d in s.dependencies(deptype=deptype):
                dkey, dlabel = spec_deps_key_label(d)
                append_dep(slabel, dlabel)

    for l, d in spec_labels.items():
        specs.append({
            'label': l,
            'spec': d['spec'],
            'root_spec': d['root'],
        })

    deps_json_obj = {
        'specs': specs,
        'dependencies': dependencies,
    }

    if stream_like:
        stream_like.write(json.dumps(deps_json_obj))

    return deps_json_obj


def release_jobs(parser, args):
    share_path = os.path.join(spack_root, 'share', 'spack', 'docker')
    os_container_mapping_path = os.path.join(
        share_path, 'os-container-mapping.yaml')

    with open(os_container_mapping_path, 'r') as fin:
        os_container_mapping = syaml.load(fin)

    try:
        validate(os_container_mapping, mapping_schema)
    except ValidationError as val_err:
        tty.error('Ill-formed os-container-mapping configuration object')
        tty.error(os_container_mapping)
        tty.debug(val_err)
        return

    containers = os_container_mapping['containers']

    if args.specs:
        # Just print out the spec labels and all dependency edges in
        # a json format.
        spec_list = [Spec(s) for s in args.specs]
        with open(args.specs_deps_output, 'w') as out:
            compute_spec_deps(spec_list, out)
        return

    current_system = sys_type() if args.resolve_deps_locally else None

    release_specs_path = args.spec_set
    if not release_specs_path:
        raise SpackError('Must provide path to release spec-set')

    release_spec_set = CombinatorialSpecSet.from_file(release_specs_path)

    mirror_url = args.mirror_url

    if not mirror_url:
        raise SpackError('Must provide url of target binary mirror')

    cdash_url = args.cdash_url

    spec_labels, dependencies, stages = stage_spec_jobs(
        release_spec_set, containers, current_system)

    if not stages:
        tty.msg('No jobs staged, exiting.')
        return

    if args.print_summary:
        print_staging_summary(spec_labels, dependencies, stages)

    output_object = {}
    job_count = 0

    stage_names = ['stage-{0}'.format(i) for i in range(len(stages))]
    stage = 0

    for stage_jobs in stages:
        stage_name = stage_names[stage]

        for spec_label in stage_jobs:
            release_spec = spec_labels[spec_label]['spec']
            root_spec = spec_labels[spec_label]['rootSpec']

            pkg_compiler = release_spec.compiler
            pkg_hash = release_spec.dag_hash()

            osname = str(release_spec.architecture)
            job_name = get_job_name(release_spec, osname)
            container_info = containers[osname]
            build_image = container_info['image']

            job_scripts = ['./bin/rebuild-package.sh']

            if 'setup_script' in container_info:
                job_scripts.insert(
                    0, container_info['setup_script'] % pkg_compiler)

            job_dependencies = []
            if spec_label in dependencies:
                job_dependencies = (
                    [get_job_name(spec_labels[dep_label]['spec'], osname)
                        for dep_label in dependencies[spec_label]])

            job_object = {
                'stage': stage_name,
                'variables': {
                    'MIRROR_URL': mirror_url,
                    'CDASH_BASE_URL': cdash_url,
                    'HASH': pkg_hash,
                    'DEPENDENCIES': ';'.join(job_dependencies),
                    'ROOT_SPEC': str(root_spec),
                },
                'script': job_scripts,
                'image': build_image,
                'artifacts': {
                    'paths': [
                        'local_mirror/build_cache',
                        'jobs_scratch_dir',
                        'cdash_report',
                    ],
                    'when': 'always',
                },
                'dependencies': job_dependencies,
            }

            # If we see 'compilers' in the container iformation, it's a
            # filter for the compilers this container can handle, else we
            # assume it can handle any compiler
            if 'compilers' in container_info:
                do_job = False
                for item in container_info['compilers']:
                    container_compiler_spec = CompilerSpec(item['name'])
                    if pkg_compiler == container_compiler_spec:
                        do_job = True
            else:
                do_job = True

            if args.shared_runner_tag:
                job_object['tags'] = [args.shared_runner_tag]

            if args.signing_key:
                job_object['variables']['SIGN_KEY_HASH'] = args.signing_key

            if do_job:
                output_object[job_name] = job_object
                job_count += 1

        stage += 1

    tty.msg('{0} build jobs generated in {1} stages'.format(
        job_count, len(stages)))

    final_stage = 'stage-rebuild-index'

    final_job = {
        'stage': final_stage,
        'variables': {
            'MIRROR_URL': mirror_url,
        },
        'image': build_image,
        'script': './bin/rebuild-index.sh',
    }

    if args.shared_runner_tag:
        final_job['tags'] = [args.shared_runner_tag]

    output_object['rebuild-index'] = final_job
    stage_names.append(final_stage)
    output_object['stages'] = stage_names

    with open(args.output_file, 'w') as outf:
        outf.write(syaml.dump(output_object))
