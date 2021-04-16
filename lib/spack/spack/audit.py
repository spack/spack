# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Auditing for various subsystems in Spack.

- Each tag has a well defined call signature
- Only callable via kwargs
"""
import itertools
try:
    from collections.abc import Sequence  # novm
except ImportError:
    from collections import Sequence

#: Map an audit tag to a list of callables implementing checks
CALLBACKS = {}


class Error(object):
    def __init__(self, summary, details):
        self.summary = summary
        self.details = details

    def __str__(self):
        return self.summary + '\n' + '\n'.join([
            '    ' + detail for detail in self.details
        ])


class AuditClass(Sequence):
    def __init__(self, tag, description, kwargs):
        if tag in CALLBACKS:
            msg = 'audit class "{0}" already registered'
            raise ValueError(msg.format(tag))

        self.tag = tag
        self.description = description
        self.kwargs = kwargs
        self.callbacks = []

        # Init the list of hooks
        CALLBACKS[self.tag] = self

    def __call__(self, func):
        # TODO: Check function signature
        self.callbacks.append(func)

    def __getitem__(self, item):
        return self.callbacks[item]

    def __len__(self):
        return len(self.callbacks)

    def run(self, **kwargs):
        msg = 'please pass "{0}" as keyword arguments'
        msg = msg.format(', '.join(self.kwargs))
        assert set(self.kwargs) == set(kwargs), msg

        errors = []
        kwargs['error_cls'] = Error
        for fn in self.callbacks:
            errors.extend(fn(**kwargs))

        for e in errors:
            e.tag = self.tag

        return errors


audit_cfgcmp = AuditClass(
    tag='CFG-COMPILER',
    description='Sanity checks on compilers.yaml',
    kwargs=()
)


@audit_cfgcmp
def _search_duplicate_compilers(error_cls):
    import spack.config
    errors = []

    compilers = list(sorted(
        spack.config.get('compilers'), key=lambda x: x['compiler']['spec']
    ))
    for spec, group in itertools.groupby(
            compilers, key=lambda x: x['compiler']['spec']
    ):
        group = list(group)
        if len(group) == 1:
            continue

        error_msg = 'Compiler defined multiple times: {0}'
        errors.append(error_cls(
            summary=error_msg.format(spec), details=[
                str(x._start_mark).strip() for x in group
            ])
        )

    return errors
