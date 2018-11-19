import collections
import copy
import itertools

import click
import yaml

# add support for include directive
# see : http://code.activestate.com/recipes/577613-yaml-include-support/
def yaml_include(loader, node):
    with open(node.value) as inputfile:
        return yaml.load(inputfile)

yaml.add_constructor("!include", yaml_include)


class ProductionEnvironment(object):
    def __init__(self, configuration, only=None):
        self.configuration = configuration
        self.axis = configuration['axis']

        # Check for compiler and architecture to be there
        if 'compiler' not in self.axis:
            raise RuntimeError('\'compiler\' must be set in the axis')
        if 'architecture' not in self.axis:
            raise RuntimeError('\'architecture\' must be set in the axis')

        # Create the right combinations of services
        self.combinations = collections.defaultdict(list)
        for name, specifications in configuration['combinations'].items():
            # Check that all the axis are specified
            if not all(x in specifications for x in self.axis):
                raise RuntimeError('combination \'{0}\' doesn\'t specify all axis'.format(name))
            self.combinations[name] = self._build_combination(name, specifications)

        self.packages = configuration['packages']
        self.only = only

    def _build_combination(self, name, specifications):
        # Each entry can be either a string or a list
        # All the lists MUST have the same length
        keys_that_are_list = {key: len(x) for key, x in specifications.items() if isinstance(x, list)}
        if len(keys_that_are_list) and len(set(keys_that_are_list.values())) != 1:
            raise RuntimeError('lists in combination \'{0}\' MUST have the same length'.format(name))
        # Explode all the lists in specifications if they are present
        exploded = []
        if not keys_that_are_list:
            exploded.append(specifications)
        else:
            exploded = self._explode_list_in_specification(keys_that_are_list, specifications)

        # Process each entry to have a list of unique combinations
        combinations = []

        for ii, x in enumerate(exploded):
            # Turn ':' separated values into lists
            # FIXME : python@2.6
            intermediate = dict([(key, value.split(':')) for key, value in x.items()])
            # Turn a dict of lists into a list of list of tuples
            item = []
            for key, l in intermediate.items():
                item.append([(key, value) for value in l])
            # Now itertools.product to the rescue
            for entry in itertools.product(*item):
                combinations.append(dict(entry))
        return combinations

    def _explode_list_in_specification(self, keys_that_are_list, specifications):
        exploded = []
        others = {key: value for key, value in specifications.items() if key not in keys_that_are_list}
        list_length = list(keys_that_are_list.values())[0]
        for idx in range(list_length):
            item = {}
            item.update(others)
            for key in keys_that_are_list:
                item[key] = specifications[key][idx]
            exploded.append(item)
        return exploded

    def _process(self, name, value):
        # Merge
        targets = []
        for target_name in value['target_matrix']:
            targets.extend(self.combinations[target_name])
        # Blacklist
        blacklist = value['blacklist'] if 'blacklist' in value.keys() else []
        # Filter
        for key, allowed in value.get('target_filter', {}).items():
            targets = [x for x in targets if x[key] in allowed]
        # Reduce
        requires = value['requires']
        for ii, x in enumerate(targets):
            item = targets[ii]
            targets[ii] = dict([(key, item[key]) for key in requires])
        # Make a dict hashable on the fly
        targets = [dict(y) for y in set([tuple(x.items()) for x in targets])]

        Item = collections.namedtuple('Item', ['spec', 'architecture', 'compiler'])

        # Construct the right values
        specs = value.get('specs', tuple())
        for item in targets:
            compiler = item.pop('compiler')
            architecture = item.pop('architecture')
            for base_spec in specs:
                parts = [base_spec]
                parts.extend([v for v in item.values()])
                spec = ' ^'.join(parts)
                if base_spec in blacklist or spec in blacklist:
                    continue
                yield Item(spec, architecture, compiler)

    def items(self):
        for name, value in self.packages.items():
            if self.only and name != self.only:
                continue
            for item in self._process(name, value):
                yield item


@click.group()
@click.option(
    '--input', default='paien.yaml', type=click.File('r'),
    help='YAML file containing the specification for a production environment'
)
@click.pass_context
def spackd(ctx, input):
    """This command helps with common tasks needed to deploy software stack
    with Spack in continuous integration pipeline"""
    ctx.input = input
    ctx.configuration = yaml.load(input)


@spackd.command()
@click.option(
    '--output', default='-', type=click.File('w'),
    help='Where to dump the list of targets'
)
@click.pass_context
def targets(ctx, output):
    """Dumps the list of targets that are available"""
    penv = ProductionEnvironment(ctx.parent.configuration)
    combinations = copy.copy(penv.combinations)
    core = combinations.pop('core')
    core_targets = sorted(set(x['architecture'] for x in core))

    for target in core_targets:
        output.write(target + '\n')


@spackd.command()
@click.argument('target')
@click.option(
    '--output', default='-', type=click.File('w'),
    help='Where to dump the list. Default is stdout. '
)
@click.pass_context
def compilers(ctx, target, output):
    """Dumps the list of compilers needed by a specific target"""
    penv = ProductionEnvironment(ctx.parent.configuration)
    combinations = copy.copy(penv.combinations)
    core = combinations.pop('core')

    # Get the core compiler for the given target
    core_compiler = next(iter(
        filter(lambda x: x['architecture'] == target, core)
    ))['compiler']

    # Get the compilers for the target specified as input
    valid_compilers = set()
    for items in combinations.values():
        for combination in filter(lambda x: x['architecture'] == target, items):
            compiler = combination['compiler'] + '%' + core_compiler
            valid_compilers.add(compiler + ' target=' + target)

    for item in sorted(valid_compilers):
        output.write(item + '\n')


@spackd.command()
@click.argument('target')
@click.option(
    '--output', default='-', type=click.File('w'),
    help='Where to dump the list. Default is stdout. '
)
@click.pass_context
def stack(ctx, target, output):
    """List all the providers for a given target.

    The output is made of valid Spack specs that need to be concretized.
    """
    penv = ProductionEnvironment(ctx.parent.configuration)
    combinations = copy.copy(penv.combinations)
    combinations.pop('core')

    # Get the compilers for the target specified as input
    valid_providers = set()
    for items in combinations.values():
        for combination in filter(lambda x: x['architecture'] == target, items):
            combination.pop('architecture')
            compiler = combination.pop('compiler')
            for service, provider in combination.items():
                valid_providers.add(provider + ' %' + compiler + ' target=' + target)

    for item in sorted(valid_providers):
        output.write(item + '\n')


@spackd.command()
@click.argument('target')
@click.option(
    '--output', default='-', type=click.File('w'),
    help='Where to dump the list. Default is stdout. '
)
@click.option(
    '--only', default=None,
    help='Restrict only to a named subset of the packages'
)
@click.pass_context
def packages(ctx, target, output, only):
    """List all the packages that are part of an environment.

    The packages are valid Spack specs that need to be concretized.
    """
    penv = ProductionEnvironment(ctx.parent.configuration, only=only)

    for item in filter(lambda x: x.architecture == target, penv.items()):
        # compiler spec should come before all dependencies
        if '^' in item.spec:
            spec = item.spec.replace(' ^', ' %%%s ^' % item.compiler, 1)
        else:
            spec = item.spec + ' %' + item.compiler
        output.write(spec + ' target=' + item.architecture + '\n')
