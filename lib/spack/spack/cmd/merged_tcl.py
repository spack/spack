from __future__ import print_function

import spack
import spack.cmd
from spack.modules import MergedTclModule

import StringIO

description = "Create TCL module which loads different instances of a Spack \
package depending on the value of an environment variable"

_module_config = spack.config.get_config('modules')


def setup_parser(subparser):
    subparser.add_argument(
        'merge_spec',
        help="""All installed specs which match this query spec will be
merged into one tcl module""")


def merged_tcl(parser, args):
    specs = spack.store.db.query(args.merge_spec)

    if 'merge' not in _module_config['tcl']:
        raise ValueError("TCL section has no 'merge' subsection")
    env_vars = _module_config['tcl']['merge']
    if len(env_vars) > 1:
        raise ValueError("Spack package choice can currently only be " +
                         "conditioned on a single environment variable")
    (env_var, spec_to_val), = env_vars.items()

    query_spec = spack.spec.Spec(args.merge_spec)
    merged_module = MergedTclModule(query_spec, specs, env_var, spec_to_val)
    collect_output = StringIO.StringIO()
    merged_module.write(output=collect_output)

    print(collect_output.getvalue())

    print(merged_module.extra_path_elements)
