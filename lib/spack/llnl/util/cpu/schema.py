# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import json
import os.path

try:
    from collections.abc import MutableMapping
except ImportError:
    from collections import MutableMapping

compilers_schema = {
    'type': 'object',
    'properties': {
        'versions': {'type': 'string'},
        'name': {'type': 'string'},
        'flags': {'type': 'string'}
    },
    'required': ['versions', 'flags']
}

properties = {
    'microarchitectures': {
        'type': 'object',
        'patternProperties': {
            r'([\w]*)': {
                'type': 'object',
                'properties': {
                    'from': {
                        'anyOf': [
                            # More than one parent
                            {'type': 'array', 'items': {'type': 'string'}},
                            # Exactly one parent
                            {'type': 'string'},
                            # No parent
                            {'type': 'null'}
                        ]
                    },
                    'vendor': {
                        'type': 'string'
                    },
                    'features': {
                        'type': 'array',
                        'items': {'type': 'string'}
                    },
                    'compilers': {
                        'type': 'object',
                        'patternProperties': {
                            r'([\w]*)': {
                                'anyOf': [
                                    compilers_schema,
                                    {
                                        'type': 'array',
                                        'items': compilers_schema
                                    }
                                ]
                            }
                        }
                    }
                },
                'required': ['from', 'vendor', 'features']
            }
        }
    },
    'feature_aliases': {
        'type': 'object',
        'patternProperties': {
            r'([\w]*)': {
                'type': 'object',
                'properties': {},
                'additionalProperties': False
            }
        },

    }
}

schema = {
    '$schema': 'http://json-schema.org/schema#',
    'title': 'Schema for microarchitecture definitions and feature aliases',
    'type': 'object',
    'additionalProperties': False,
    'properties': properties,
}


class LazyDictionary(MutableMapping):
    """Lazy dictionary that gets constructed on first access to any object key

    Args:
        factory (callable): factory function to construct the dictionary
    """

    def __init__(self, factory, *args, **kwargs):
        self.factory = factory
        self.args = args
        self.kwargs = kwargs
        self._data = None

    @property
    def data(self):
        if self._data is None:
            self._data = self.factory(*self.args, **self.kwargs)
        return self._data

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)


def _load_targets_json():
    """Loads ``microarchitectures.json`` in memory."""
    directory_name = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(directory_name, 'microarchitectures.json')
    with open(filename, 'r') as f:
        return json.load(f)


#: In memory representation of the data in microarchitectures.json,
#: loaded on first access
targets_json = LazyDictionary(_load_targets_json)
