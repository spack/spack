# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from types import ModuleType

import pickle
import pydoc
import io


patches = None


def append_patch(patch):
    global patches
    if not patches:
        patches = list()
    patches.append(patch)


def serialize(obj):
    serialized_obj = io.BytesIO()
    pickle.dump(obj, serialized_obj)
    serialized_obj.seek(0)
    return serialized_obj


class TransmitPatches(object):
    def __init__(self, module_patches, class_patches):
        self.module_patches = list(
            (x, y, serialize(z)) for (x, y, z) in module_patches)
        self.class_patches = list(
            (x, y, serialize(z)) for (x, y, z) in class_patches)

    def apply(self):
        for module_name, attr_name, value in self.module_patches:
            value = pickle.load(value)
            module = __import__(module_name)
            setattr(module, attr_name, value)
        for class_fqn, attr_name, value in self.class_patches:
            value = pickle.load(value)
            cls = pydoc.locate(class_fqn)
            setattr(cls, attr_name, value)


def store_patches():
    global patches
    module_patches = list()
    class_patches = list()
    for patch in patches:
        for target, name, _ in patch._setattr:
            if isinstance(target, ModuleType):
                new_val = getattr(target, name)
                module_name = target.__name__
                module_patches.append((module_name, name, new_val))
            elif isinstance(target, type):
                new_val = getattr(target, name)
                class_fqn = '.'.join([target.__module__, target.__name__])
                class_patches.append((class_fqn, name, new_val))

    return TransmitPatches(module_patches, class_patches)


def clear_patches():
    global patches
    patches = None
