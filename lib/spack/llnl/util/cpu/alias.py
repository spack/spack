# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
#: Known predicates that can be used to construct feature aliases

from .schema import targets_json, LazyDictionary, properties

_feature_alias_predicate = {}


class FeatureAliasTest(object):
    """A test that must be passed for a feature alias to succeed.

    Args:
        rules (dict): dictionary of rules to be met. Each key must be a
            valid alias predicate
    """
    def __init__(self, rules):
        self.rules = rules
        self.predicates = []
        for name, args in rules.items():
            self.predicates.append(_feature_alias_predicate[name](args))

    def __call__(self, microarchitecture):
        return all(
            feature_test(microarchitecture) for feature_test in self.predicates
        )


def _feature_aliases():
    """Returns the dictionary of all defined feature aliases."""
    json_data = targets_json['feature_aliases']
    aliases = {}
    for alias, rules in json_data.items():
        aliases[alias] = FeatureAliasTest(rules)
    return aliases


feature_aliases = LazyDictionary(_feature_aliases)


def alias_predicate(predicate_schema):
    """Decorator to register a predicate that can be used to define
    feature aliases.

    Args:
        predicate_schema (dict): schema to be enforced in
            microarchitectures.json for the predicate
    """
    def decorator(func):
        name = func.__name__

        # Check we didn't register anything else with the same name
        if name in _feature_alias_predicate:
            msg = 'the alias predicate "{0}" already exists'.format(name)
            raise KeyError(msg)

        # Update the overall schema
        alias_schema = properties['feature_aliases']['patternProperties']
        alias_schema[r'([\w]*)']['properties'].update(
            {name: predicate_schema}
        )
        # Register the predicate
        _feature_alias_predicate[name] = func

        return func
    return decorator


@alias_predicate(predicate_schema={'type': 'string'})
def reason(motivation_for_the_alias):
    """This predicate returns always True and it's there to allow writing
    a documentation string in the JSON file to explain why an alias is needed.
    """
    return lambda x: True


@alias_predicate(predicate_schema={
    'type': 'array',
    'items': {'type': 'string'}
})
def any_of(list_of_features):
    """Returns a predicate that is True if any of the feature in the
    list is in the microarchitecture being tested, False otherwise.
    """
    def _impl(microarchitecture):
        return any(x in microarchitecture for x in list_of_features)
    return _impl


@alias_predicate(predicate_schema={
    'type': 'array',
    'items': {'type': 'string'}
})
def families(list_of_families):
    """Returns a predicate that is True if the architecture family of
    the microarchitecture being tested is in the list, False otherwise.
    """
    def _impl(microarchitecture):
        return str(microarchitecture.family) in list_of_families
    return _impl
