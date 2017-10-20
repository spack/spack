import llnl.util.tty as tty
import spack
import llnl.util.filesystem as fs
import spack.util.spack_json as sjson
import spack.util.spack_yaml as syaml
from spack.config import ConfigScope
from spack.spec import Spec, CompilerSpec, FlagMap
from spack.repository import Repo
from spack.version import VersionList

import argparse
try:
    from itertools import izip_longest as zip_longest
except ImportError:
    from itertools import zip_longest
import os
import shutil

description = "group a subset of packages"
section = "environment"
level = "long"

_db_dirname = fs.join_path(spack.var_path, 'environments')


class Environment(object):
    def __init__(self, name):
        self.name = name
        self.user_specs = list()
        self.concretized_order = list()
        self.specs_by_hash = dict()
        # Libs in this set must always appear as the dependency traced from any
        # root of link deps
        self.common_libs = dict()  # name -> hash
        # Packages in this set must always appear as the dependency traced from
        # any root of run deps
        self.common_bins = dict()  # name -> hash

    def add(self, user_spec):
        query_spec = Spec(user_spec)
        existing = set(x for x in self.user_specs
                       if Spec(x).name == query_spec.name)
        if existing:
            tty.die("Package {0} was already added to {1}"
                    .format(query_spec.name, self.name))
        self.user_specs.append(user_spec)

    def remove(self, query_spec):
        query_spec = Spec(query_spec)
        match_index = -1
        for i, spec in enumerate(self.user_specs):
            if Spec(spec).name == query_spec.name:
                match_index = i
                break

        if match_index < 0:
            tty.die("Not found: {0}".format(query_spec))

        del self.user_specs[match_index]
        if match_index < len(self.concretized_order):
            spec_hash = self.concretized_order[match_index]
            del self.concretized_order[match_index]
            del self.specs_by_hash[spec_hash]

    def concretize(self):
        num_concretized = len(self.concretized_order)
        new_specs = list()
        for user_spec in self.user_specs[num_concretized:]:
            spec = Spec(user_spec)
            spec.concretize()
            new_specs.append(spec)
            self.specs_by_hash[spec.dag_hash()] = spec
            self.concretized_order.append(spec.dag_hash())
        return new_specs

    def install(self):
        for concretized_hash in self.concretized_order:
            spec = self.specs_by_hash[concretized_hash]
            spec.package.do_install()

    def list(self, stream, include_deps=False):
        for user_spec, concretized_hash in zip_longest(
                self.user_specs, self.concretized_order):

            stream.write('{0}\n'.format(user_spec))

            if concretized_hash:
                concretized_spec = self.specs_by_hash[concretized_hash]
                if include_deps:
                    stream.write(concretized_spec.tree())
                else:
                    stream.write(concretized_spec.format() + '\n')

    def upgrade_dependency(self, dep_name, dry_run=False):
        """
        Note: if you have

        w -> x -> y

        and

        v -> x -> y

        Then if you upgrade y, you will start by re-concretizing w (and x).
        This should make sure that v uses the same x as w if this environment
        is supposed to reuse dependencies where possible. The difference
        compared to 'normal' concretization is that you want to keep things as
        similar as possible. I think the approach would be to go through all
        the common_libs and common_bins, recognize the first time they get
        re-concretized, and then replace them manually where encountered later.
        """
        new_order = list()
        new_deps = list()
        for i, spec_hash in enumerate(self.concretized_order):
            spec = self.specs_by_hash[spec_hash]
            if dep_name in spec:
                if dry_run:
                    tty.msg("Would upgrade {0} for {1}"
                            .format(spec[dep_name].format(), spec.format()))
                else:
                    new_spec = upgrade_dependency_version(spec, dep_name)
                    new_order.append(new_spec.dag_hash())
                    self.specs_by_hash[new_spec.dag_hash()] = new_spec
                    new_deps.append(new_spec[dep_name])
            else:
                new_order.append(spec_hash)

        if not dry_run:
            self.concretized_order = new_order
            return new_deps[0] if new_deps else None

    def reset_os_and_compiler(self, compiler=None):
        new_order = list()
        new_specs_by_hash = {}
        for spec_hash in self.concretized_order:
            spec = self.specs_by_hash[spec_hash]
            new_spec = reset_os_and_compiler(spec, compiler)
            new_order.append(new_spec.dag_hash())
            new_specs_by_hash[new_spec.dag_hash()] = new_spec
        self.concretized_order = new_order
        self.specs_by_hash = new_specs_by_hash

    def _get_environment_specs(self):
        # At most one instance of any package gets added to the environment
        package_to_spec = {}

        for spec_hash in self.concretized_order:
            spec = self.specs_by_hash[spec_hash]
            for dep in spec.traverse(deptype=('link', 'run')):
                if dep.name in package_to_spec:
                    tty.warn("{0} takes priority over {1}"
                             .format(package_to_spec[dep.name].format(),
                                     dep.format()))
                else:
                    package_to_spec[dep.name] = dep

        return list(package_to_spec.values())

    def get_modules(self):
        import spack.modules

        module_files = list()
        environment_specs = self._get_environment_specs()
        for spec in environment_specs:
            module = spack.modules.lmod.LmodModulefileWriter(spec)
            path = module.layout.filename
            if os.path.exists(path):
                module_files.append(path)
            else:
                tty.warn("Module file for {0} does not exist"
                         .format(spec.format()))

        return module_files

    def to_dict(self):
        concretized_order = list(self.concretized_order)
        concrete_specs = dict()
        for spec in self.specs_by_hash.values():
            for s in spec.traverse():
                if s.dag_hash() not in concrete_specs:
                    concrete_specs[s.dag_hash()] = s.to_node_dict()
        format = {
            'user_specs': self.user_specs,
            'concretized_order': concretized_order,
            'concrete_specs': concrete_specs,
        }
        return format

    @staticmethod
    def from_dict(name, d):
        c = Environment(name)
        c.user_specs = list(d['user_specs'])
        c.concretized_order = list(d['concretized_order'])
        specs_dict = d['concrete_specs']
        c.specs_by_hash = reconstitute(specs_dict, set(c.concretized_order))
        return c

    def path(self):
        return fs.join_path(_db_dirname, self.name)

    def config_path(self):
        return fs.join_path(self.path(), 'config')

    def repo_path(self):
        return fs.join_path(self.path(), 'repo')


def reconstitute(hash_to_node_dict, root_hashes):
    specs_by_hash = {}
    for dag_hash, node_dict in hash_to_node_dict.items():
        specs_by_hash[dag_hash] = Spec.from_node_dict(node_dict)

    for dag_hash, node_dict in hash_to_node_dict.items():
        for dep_name, dep_hash, deptypes in (
                Spec.dependencies_from_node_dict(node_dict)):
            specs_by_hash[dag_hash]._add_dependency(
                specs_by_hash[dep_hash], deptypes)

    return dict((x, y) for x, y in specs_by_hash.items() if x in root_hashes)


def reset_os_and_compiler(spec, compiler=None):
    spec = spec.copy()
    for x in spec.traverse():
        x.compiler = None
        x.architecture = None
        x.compiler_flags = FlagMap(x)
        x._concrete = False
        x._hash = None
    if compiler:
        spec.compiler = CompilerSpec(compiler)
    spec.concretize()
    return spec


def upgrade_dependency_version(spec, dep_name):
    spec = spec.copy()
    for x in spec.traverse():
        x._concrete = False
        x._hash = None
    spec[dep_name].versions = VersionList(':')
    spec.concretize()
    return spec


def write(environment, new_repo=None, config_files=None):
    """
    config_files will overwrite any existing config files in the environment.
    """
    tmp_new, dest, tmp_old = write_paths(environment)

    if os.path.exists(tmp_new) or os.path.exists(tmp_old):
        tty.die("Partial write state, run 'spack env repair'")

    fs.mkdirp(tmp_new)
    # create one file for the environment object
    with open(fs.join_path(tmp_new, 'environment.json'), 'w') as F:
        sjson.dump(environment.to_dict(), stream=F)

    dest_repo_dir = fs.join_path(tmp_new, 'repo')
    if new_repo:
        shutil.copytree(new_repo.root, dest_repo_dir)
    elif os.path.exists(environment.repo_path()):
        shutil.copytree(environment.repo_path(), dest_repo_dir)

    new_config_dir = fs.join_path(tmp_new, 'config')
    if os.path.exists(environment.config_path()):
        shutil.copytree(environment.config_path(), new_config_dir)
    else:
        fs.mkdirp(new_config_dir)

    if config_files:
        for cfg_path in config_files:
            dst_fname = os.path.basename(cfg_path)
            dst = fs.join_path(new_config_dir, dst_fname)
            shutil.copyfile(cfg_path, dst)

    if os.path.exists(dest):
        shutil.move(dest, tmp_old)
    shutil.move(tmp_new, dest)
    if os.path.exists(tmp_old):
        shutil.rmtree(tmp_old)


def write_paths(environment):
    tmp_new = fs.join_path(_db_dirname, "_" + environment.name)
    dest = environment.path()
    tmp_old = fs.join_path(_db_dirname, "." + environment.name)
    return tmp_new, dest, tmp_old


def repair(environment_name):
    """
    Possibilities:
        tmp_new, dest
        tmp_new, tmp_old
        tmp_old, dest
    """
    environment = Environment(environment_name)
    tmp_new, dest, tmp_old = write_paths(environment)
    if os.path.exists(tmp_old):
        if not os.path.exists(dest):
            shutil.move(tmp_new, dest)
        else:
            shutil.rmtree(tmp_old)
        tty.info("Previous update completed")
    elif os.path.exists(tmp_new):
        tty.info("Previous update did not complete")
    else:
        tty.info("Previous update may have completed")

    if os.path.exists(tmp_new):
        shutil.rmtree(tmp_new)


def read(environment_name):
    tmp_new, environment_dir, tmp_old = write_paths(
        Environment(environment_name))

    if os.path.exists(tmp_new) or os.path.exists(tmp_old):
        tty.die("Partial write state, run 'spack env repair'")

    with open(fs.join_path(environment_dir, 'environment.json'), 'r') as F:
        environment_dict = sjson.load(F)
    environment = Environment.from_dict(environment_name, environment_dict)

    return environment


def environment_create(args):
    environment = Environment(args.environment)
    if os.path.exists(environment.path()):
        raise tty.die("Environment already exists: " + args.environment)

    init_config = None
    if args.init_file:
        with open(args.init_file) as F:
            init_config = syaml.load(F)

    _environment_create(args.environment, init_config)


def _environment_create(name, init_config=None):
    environment = Environment(name)

    config_paths = None
    if init_config:
        user_specs = list()
        config_sections = {}
        for key, val in init_config.items():
            if key == 'user_specs':
                user_specs.extend(val)
            else:
                config_sections[key] = val

        for user_spec in user_specs:
            environment.add(user_spec)
        if config_sections:
            import tempfile
            tmp_cfg_dir = tempfile.mkdtemp()
            config_paths = []
        for key, val in config_sections.items():
            yaml_section = syaml.dump({key: val}, default_flow_style=False)
            yaml_file = '{0}.yaml'.format(key)
            yaml_path = fs.join_path(tmp_cfg_dir, yaml_file)
            config_paths.append(yaml_path)
            with open(yaml_path, 'w') as F:
                F.write(yaml_section)

    write(environment, config_files=config_paths)
    if config_paths:
        shutil.rmtree(tmp_cfg_dir)


def environment_update_config(args):
    environment = Environment(args.environment)
    write(environment, config_files=args.config_files)


def environment_add(args):
    environment = read(args.environment)
    for spec in spack.cmd.parse_specs(args.package):
        environment.add(spec.format())
    write(environment)


def environment_remove(args):
    environment = read(args.environment)
    for spec in spack.cmd.parse_specs(args.package):
        environment.remove(spec.format())
    write(environment)


def environment_concretize(args):
    environment = read(args.environment)
    _environment_concretize(environment)


def _environment_concretize(environment):
    repo = prepare_repository(environment)
    prepare_config_scope(environment)

    new_specs = environment.concretize()
    for spec in new_specs:
        for dep in spec.traverse():
            dump_to_environment_repo(dep, repo)
    write(environment, repo)


def environment_install(args):
    environment = read(args.environment)
    prepare_repository(environment)
    environment.install()


def dump_to_environment_repo(spec, repo):
    dest_pkg_dir = repo.dirname_for_package_name(spec.name)
    if not os.path.exists(dest_pkg_dir):
        spack.repo.dump_provenance(spec, dest_pkg_dir)


def prepare_repository(environment, remove=None):
    import tempfile
    repo_stage = tempfile.mkdtemp()
    new_repo_dir = fs.join_path(repo_stage, 'repo')
    if os.path.exists(environment.repo_path()):
        shutil.copytree(environment.repo_path(), new_repo_dir)
    else:
        spack.repository.create_repo(new_repo_dir, environment.name)
    if remove:
        remove_dirs = []
        repo = Repo(new_repo_dir)
        for pkg_name in remove:
            remove_dirs.append(repo.dirname_for_package_name(pkg_name))
        for d in remove_dirs:
            shutil.rmtree(d)
    repo = Repo(new_repo_dir)
    spack.repo.put_first(repo)
    return repo


def prepare_config_scope(environment):
    tty.debug("Check for config scope at " + environment.config_path())
    if os.path.exists(environment.config_path()):
        tty.msg("Using config scope at " + environment.config_path())
        ConfigScope(environment.name, environment.config_path())


def environment_relocate(args):
    environment = read(args.environment)
    prepare_repository(environment)
    environment.reset_os_and_compiler(compiler=args.compiler)
    write(environment)


def environment_list(args):
    # TODO? option to list packages w/ multiple instances?
    environment = read(args.environment)
    import sys
    environment.list(sys.stdout, args.include_deps)


def environment_stage(args):
    environment = read(args.environment)
    prepare_repository(environment)
    for spec in environment.specs_by_hash.values():
        for dep in spec.traverse():
            dep.package.do_stage()


def environment_list_modules(args):
    environment = read(args.environment)
    for module_file in environment.get_modules():
        print(module_file)


def environment_upgrade_dependency(args):
    environment = read(args.environment)
    repo = prepare_repository(environment, [args.dep_name])
    new_dep = environment.upgrade_dependency(args.dep_name, args.dry_run)
    if not args.dry_run and new_dep:
        dump_to_environment_repo(new_dep, repo)
        write(environment, repo)


def add_common_args(parser):
    parser.add_argument(
        'environment',
        help="The environment you are working with"
    )


def setup_parser(subparser):
    sp = subparser.add_subparsers(
        metavar='SUBCOMMAND', dest='environment_command')

    create_parser = sp.add_parser('create', help='Make an environment')
    add_common_args(create_parser)
    create_parser.add_argument(
        '--init-file', dest='init_file',
        help='File with user specs to add and configuration yaml to use'
    )

    add_parser = sp.add_parser('add', help='Add a spec to an environment')
    add_common_args(add_parser)
    add_parser.add_argument(
        'package',
        nargs=argparse.REMAINDER,
        help="Spec of the package to add"
    )

    remove_parser = sp.add_parser(
        'remove', help='Remove a spec from this environment')
    add_common_args(remove_parser)
    remove_parser.add_argument(
        'package',
        nargs=argparse.REMAINDER,
        help="Spec of the package to remove"
    )

    concretize_parser = sp.add_parser(
        'concretize', help='Concretize user specs')
    add_common_args(concretize_parser)

    relocate_parser = sp.add_parser(
        'relocate',
        help='Reconcretize environment with new OS and/or compiler')
    add_common_args(relocate_parser)
    relocate_parser.add_argument(
        '--compiler',
        help="Compiler spec to use"
    )

    list_parser = sp.add_parser('list', help='List specs in an environment')
    list_parser.add_argument(
        '--include-deps', action='store_true',
        dest='include_deps', help='Show dependencies of requested packages')
    add_common_args(list_parser)

    modules_parser = sp.add_parser(
        'list-modules',
        help='Show modules for for packages installed in an environment')
    add_common_args(modules_parser)

    upgrade_parser = sp.add_parser(
        'upgrade',
        help='''Upgrade a dependency package in an environment to the latest
version''')
    add_common_args(upgrade_parser)
    upgrade_parser.add_argument(
        'dep_name', help='Dependency package to upgrade')
    upgrade_parser.add_argument(
        '--dry-run', action='store_true', dest='dry_run',
        help="Just show the updates that would take place")

    stage_parser = sp.add_parser(
        'stage',
        help='Download all source files for all packages in an environment')
    add_common_args(stage_parser)

    config_update_parser = sp.add_parser(
        'update-config',
        help='Add config yaml file to environment')
    add_common_args(config_update_parser)
    config_update_parser.add_argument(
        'config_files',
        nargs=argparse.REMAINDER,
        help="Configuration files to add"
    )

    install_parser = sp.add_parser(
        'install',
        help='Install all concretized specs in an environment')
    add_common_args(install_parser)


def env(parser, args, **kwargs):
    action = {
        'create': environment_create,
        'add': environment_add,
        'concretize': environment_concretize,
        'list': environment_list,
        'list-modules': environment_list_modules,
        'remove': environment_remove,
        'relocate': environment_relocate,
        'upgrade': environment_upgrade_dependency,
        'stage': environment_stage,
        'install': environment_install,
        'update-config': environment_update_config,
    }
    action[args.environment_command](args)
