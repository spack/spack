import spack
import llnl.util.filesystem as fs
import spack.util.spack_json as sjson
import spack.util.spack_yaml as syaml

from spack.spec import Spec

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
        self.explicit = set()
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
            self.explicit.add(spec.dag_hash())
            install_group = set()
            for node in spec.traverse(): # deptype = (build, link)?
                self.specs_by_hash[node.dag_hash()] = node
                install_group.add(node.dag_hash())
            self.concretized_order.append(install_group)
            self.concretized_index += 1

    def install(self):
        for dag_hash, spec in self.specs_by_hash.items():
            # Existing logic in Package will avoid installing if this already
            # exists
            spec.package.do_install(explicit=dag_hash in self.explicit)

    def to_dict(self):
        concretized_order = list(list(x) for x in self.concretized_order)
        explicit = list(self.explicit)
        common_libs = syaml.syaml_dict(self.common_libs.items())
        common_bins = syaml.syaml_dict(self.common_bins.items())
        format = {
            'user_specs': self.user_specs,
            'concretized_index': self.concretized_index,
            'concretized_order': concretized_order,
            'explicit': explicit,
            'common_libs': common_libs,
            'common_bins': common_bins
        }
        return format

    @staticmethod
    def from_dict(name, d):
        c = Context(name)
        c.user_specs = list(d['user_specs'])
        c.concretized_index = int(d['concretized_index'])
        c.concretized_order = list(set(x) for x in d['concretized_order'])
        c.explicit = set(d['explicit'])
        c.common_libs = dict(d['common_libs'])
        c.common_bins = dict(d['common_bins'])
        return c

    def upgrade(self, spec, new):
        # Copy this context, replace the given spec (what if it appears multiple times?)
        pass

def write(context):
    tmp_new = fs.join_path(_db_dirname, "_" + context.name)
    final_dir = fs.join_path(_db_dirname, context.name)
    tmp_old = fs.join_path(_db_dirname, "." + context.name)

    if not os.path.exists(tmp_old):
        if os.path.exists(tmp_new):
            shutil.rmtree(tmp_new)
        fs.mkdirp(tmp_new)
        #create one file for the full specs in json format
        with open(fs.join_path(tmp_new, 'full_specs.json'), 'w') as F:
            store_specs_by_hash(context.specs_by_hash, F)
        #create one file for the rest of the data in yaml format
        with open(fs.join_path(tmp_new, 'context.yaml'), 'w') as F:
            syaml.dump(context.to_dict(), stream=F, default_flow_style=False)

    if os.path.exists(final_dir):
        shutil.move(final_dir, tmp_old)
    shutil.move(tmp_new, final_dir)
    if os.path.exists(tmp_old):
        shutil.rmtree(tmp_old) 

def store_specs_by_hash(specs_by_hash, stream):
    installs = dict((k, v.to_dict()) for k, v in specs_by_hash.items())

    try:
        sjson.dump(installs, stream)
    except YAMLError as e:
        raise syaml.SpackYAMLError(
            "Error writing context full specs:", str(e))

def read(context_name):
    context_dir = fs.join_path(_db_dirname, context_name)

    with open(fs.join_path(context_dir, 'context.yaml'), 'r') as F:
        context_dict = syaml.load(F)

    context = Context.from_dict(context_name, context_dict)

    with open(fs.join_path(context_dir, 'full_specs.json'), 'r') as F:
        install_dict = sjson.load(F)

    installs = dict((x, Spec.from_dict(y)) for x, y in install_dict.items())
    context.specs_by_hash = installs

    return context

def context_create(args):
    print args.context
    
    c = Context(args.context)
    c.add('openmpi@1.10.1')
    c.concretize()
    c.add('netlib-lapack')
    print c.to_dict()

    write(c)

    c2 = read(c.name)
    for x, y in c2.specs_by_hash.items():
        z = c.specs_by_hash[x]
        if y != z:
            print y.to_dict()
            print z.to_dict()
            break

def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar='SUBCOMMAND', dest='context_command')

    create_parser = sp.add_parser('create', help='make a context')

    create_parser.add_argument(
        'context',
        help="The context you are working with"
    )

def context(parser, args, **kwargs):
    action = {'create': context_create}
    action[args.context_command](args)
