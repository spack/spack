import llnl.util.tty as tty
import spack
import llnl.util.filesystem as fs
import spack.util.spack_json as sjson
import spack.util.spack_yaml as syaml
from spack.spec import Spec

import argparse
import itertools
import os
import shutil

_db_dirname = fs.join_path(spack.var_path, 'contexts')

class Context(object):
    def __init__(self, name):
        self.name = name
        self.user_specs = list()
        self.concretized_index = 0
        self.concretized_order = list()
        self.specs_by_hash = dict()
        # Libs in this set must always appear as the dependency traced from any
        # root of link deps
        self.common_libs = dict() # name -> hash
        # Packages in this set must always appear as the dependency traced from
        # any root of run deps
        self.common_bins = dict() # name -> hash

    def add(self, user_spec):
        self.user_specs.append(user_spec)

    def concretize(self):
        for user_spec in self.user_specs[self.concretized_index:]:
            spec = Spec(user_spec)
            spec.concretize()
            self.specs_by_hash[spec.dag_hash()] = spec
            self.concretized_order.append(spec.dag_hash())
            self.concretized_index += 1

    def install(self):
        for dag_hash, spec in self.specs_by_hash.items():
            spec.package.do_install(explicit=True)

    def list(self, stream, include_deps=False):
        for user_spec, concretized_hash in itertools.izip_longest(
            self.user_specs, self.concretized_order):

            stream.write('{0}\n'.format(user_spec))

            if concretized_hash:
                concretized_spec = self.specs_by_hash[concretized_hash]
                if include_deps:
                    stream.write(concretized_spec.tree())
                else:
                    stream.write(concretized_spec.format())

    def reset_os_and_compiler(self):
        new_order = list()
        new_specs_by_hash = {}
        for spec_hash in self.concretized_order:
            spec = self.specs_by_hash[spec_hash]
            new_spec = reset_os_and_compiler(spec)
            new_order.append(new_spec.dag_hash())
            new_specs_by_hash[new_spec.dag_hash()] = new_spec
        self.concretized_order = new_order
        self.specs_by_hash = new_specs_by_hash

    def upgrade(self, spec, new):
        # TODO: Copy this context, replace the given spec (what if it appears
        # multiple times?)
        pass

    def to_dict(self):
        concretized_order = list(self.concretized_order)
        common_libs = syaml.syaml_dict(self.common_libs.items())
        common_bins = syaml.syaml_dict(self.common_bins.items())
        format = {
            'user_specs': self.user_specs,
            'concretized_index': self.concretized_index,
            'concretized_order': concretized_order,
            'common_libs': common_libs,
            'common_bins': common_bins
        }
        return format

    @staticmethod
    def from_dict(name, d):
        c = Context(name)
        c.user_specs = list(d['user_specs'])
        c.concretized_index = int(d['concretized_index'])
        c.concretized_order = list(d['concretized_order'])
        c.common_libs = dict(d['common_libs'])
        c.common_bins = dict(d['common_bins'])
        return c

    def path(self):
        return fs.join_path(_db_dirname, self.name)

def reset_os_and_compiler(spec):
    spec = spec.copy()
    for x in spec.traverse():
        x.compiler = None
        x.architecture = None
        x.compiler_flags = FlagMap(x)
        x._concrete = False
        x._hash = None
    spec.concretize()
    return spec

def write(context):
    tmp_new, dest, tmp_old = write_paths(context)

    if os.path.exists(tmp_new) or os.path.exists(tmp_old):
        tty.die("Partial write state, run 'spack context repair'")

    fs.mkdirp(tmp_new)
    #create one file for the full specs in json format
    with open(fs.join_path(tmp_new, 'full_specs.json'), 'w') as F:
        store_specs_by_hash(context.specs_by_hash, F)
    #create one file for the rest of the data in yaml format
    with open(fs.join_path(tmp_new, 'context.yaml'), 'w') as F:
        syaml.dump(context.to_dict(), stream=F, default_flow_style=False)

    if os.path.exists(dest):
        shutil.move(dest, tmp_old)
    shutil.move(tmp_new, dest)
    if os.path.exists(tmp_old):
        shutil.rmtree(tmp_old) 

def write_paths(context):
    tmp_new = fs.join_path(_db_dirname, "_" + context.name)
    dest = context.path()
    tmp_old = fs.join_path(_db_dirname, "." + context.name)
    return tmp_new, dest, tmp_old

def repair(context_name):
    """
    Possibilities:
        tmp_new, dest
        tmp_new, tmp_old
        tmp_old, dest
    """
    c = Context(context_name)
    tmp_new, dest, tmp_old = write_paths(context)
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

def store_specs_by_hash(specs_by_hash, stream):
    installs = dict((k, v.to_dict(all_deps=True))
                    for k, v in specs_by_hash.items())

    try:
        sjson.dump(installs, stream)
    except YAMLError as e:
        raise syaml.SpackYAMLError(
            "Error writing context full specs:", str(e))

def read(context_name):
    tmp_new, context_dir, tmp_old = write_paths(Context(context_name))

    if os.path.exists(tmp_new) or os.path.exists(tmp_old):
        tty.die("Partial write state, run 'spack context repair'")

    with open(fs.join_path(context_dir, 'context.yaml'), 'r') as F:
        context_dict = syaml.load(F)
    context = Context.from_dict(context_name, context_dict)
    with open(fs.join_path(context_dir, 'full_specs.json'), 'r') as F:
        install_dict = sjson.load(F)
    installs = dict((x, Spec.from_dict(y)) for x, y in install_dict.items())
    context.specs_by_hash = installs

    return context

def context_create(args):
    context = Context(args.context)
    if os.path.exists(context.path()):
        raise tty.die("Context already exists: " + args.context)
    write(context)

def context_add(args):
    context = read(args.context)
    for spec in spack.cmd.parse_specs(args.package):
        context.add(spec.format())
    write(context)

def context_concretize(args):
    context = read(args.context)
    context.concretize()
    write(context)

def context_list(args):
    # TODO? option to list packages w/ multiple instances?
    context = read(args.context)
    import sys
    context.list(sys.stdout, args.include_deps)

def add_common_args(parser):
    parser.add_argument(
        'context',
        help="The context you are working with"
    )

def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar='SUBCOMMAND', dest='context_command')

    create_parser = sp.add_parser('create', help='Make a context')
    add_common_args(create_parser)

    add_parser = sp.add_parser('add', help='Add a spec to a context')
    add_common_args(add_parser)
    add_parser.add_argument(
        'package',
        nargs=argparse.REMAINDER,
        help="spec of the package to install"
    )

    concretize_parser = sp.add_parser(
        'concretize', help='Concretize user specs')
    add_common_args(concretize_parser)

    list_parser = sp.add_parser('list', help='List specs in a context')
    list_parser.add_argument(
        '--include-deps', action='store_true',
        dest='include_deps', help='Show dependencies of requested packages')
    add_common_args(list_parser)

def context(parser, args, **kwargs):
    action = {
        'create': context_create,
        'add': context_add,
        'concretize': context_concretize,
        'list': context_list,
        }
    action[args.context_command](args)
